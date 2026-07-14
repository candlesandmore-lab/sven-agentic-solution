"""Uniform ClaudeCode SDK base class shared by every coded agent in this workspace.

Mirrors the uniform base-class decision recorded in
`docs/architecture/01-technical-trader-solution.md` ("Uniform SDK Base-Class Decision"):
Anthropic-native, a LangGraph flow with entry/generate/evaluate/refine/terminal nodes, task-id
keyed state persistence across iterations and successive calls, a refine/evaluator loop capped
at five iterations, and file logging sufficient to debug the agent's activity.

This is a from-scratch implementation for the Technical Trader Solution itself -- it does not
import `agent_building_agent` (that package is this repository's development tooling, not a
runtime dependency of the delivered solution).
"""

from __future__ import annotations

import json
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from langgraph.graph import END, StateGraph

from technical_trader_solution.logging import configure_logger

MAX_ITERATIONS = 5


@dataclass
class EvaluationResult:
    """Outcome of validating one iteration's generated output."""

    passed: bool
    feedback: str


@dataclass
class CodedAgentState:
    """Working state carried across LangGraph nodes and refine iterations."""

    task_id: str
    inputs: dict[str, Any]
    answers: dict[str, Any] = field(default_factory=dict)
    iteration: int = 0
    latest_output: dict[str, Any] | None = None
    latest_evaluation: EvaluationResult | None = None
    attempts: list[dict[str, Any]] = field(default_factory=list)
    status: str = "running"


def _default_state_db_path(agent_slug: str) -> Path:
    return Path(".coded_agent_state") / f"{agent_slug}.sqlite"


class CodedAgentStateStore:
    """SQLite-backed task-id keyed state persistence, one database per coded agent."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS coded_agent_state ("
                "task_id TEXT PRIMARY KEY, state_json TEXT NOT NULL, updated_at TEXT NOT NULL)"
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def load(self, task_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT state_json FROM coded_agent_state WHERE task_id = ?", (task_id,)
            ).fetchone()
        return json.loads(row[0]) if row else None

    def save(self, task_id: str, state_dict: dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO coded_agent_state (task_id, state_json, updated_at) VALUES (?, ?, ?) "
                "ON CONFLICT(task_id) DO UPDATE SET state_json = excluded.state_json, "
                "updated_at = excluded.updated_at",
                (
                    task_id,
                    # `default=str` guards against non-JSON-serializable input values (for
                    # example an injected fetch callable used for testing); such values
                    # cannot meaningfully survive a resume across process boundaries
                    # anyway, so persisting a string placeholder is an acceptable
                    # degradation rather than a crash.
                    json.dumps(state_dict, default=str),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )


class ClaudeCodeSDKAgentBase(ABC):
    """Uniform base class: LangGraph entry/generate/evaluate/refine/terminal flow.

    Subclasses implement `run_generate` (produce one iteration's output from `state.inputs`
    and any prior refine feedback) and `evaluate` (validate that output against the coded
    agent's deterministic success criteria). The base class wires the refine/evaluator loop,
    task-id state persistence, and file logging.
    """

    agent_slug: str

    def __init__(
        self,
        *,
        state_db_path: Path | None = None,
        log_dir: str | Path | None = None,
        log_level: str = "info",
    ) -> None:
        self.state_store = CodedAgentStateStore(
            state_db_path or _default_state_db_path(self.agent_slug)
        )
        self.logger = configure_logger(
            f"technical_trader_solution.coded_agents.{self.agent_slug}",
            log_dir=log_dir,
            log_level=log_level,
        )
        self._graph = self._build_graph()

    # -- Subclass contract -------------------------------------------------------------

    @abstractmethod
    def run_generate(self, state: CodedAgentState) -> dict[str, Any]:
        """Produce this iteration's output from `state.inputs`, `state.answers`, and any
        prior `state.latest_evaluation` feedback (present on refine iterations)."""

    @abstractmethod
    def evaluate(self, state: CodedAgentState, output: dict[str, Any]) -> EvaluationResult:
        """Validate `output` against this coded agent's deterministic success criteria."""

    def build_failure_questions(self, state: CodedAgentState) -> list[str]:
        feedback = state.latest_evaluation.feedback if state.latest_evaluation else "unknown"
        return [
            f"The {self.agent_slug} coded agent could not produce a valid result after "
            f"{MAX_ITERATIONS} iterations because: {feedback}. Please clarify the input or "
            "provide the missing information so the run can be completed."
        ]

    def summarize_output(self, output: dict[str, Any]) -> str:
        return str(output)[:200]

    # -- LangGraph wiring ----------------------------------------------------------------

    def _build_graph(self):
        graph = StateGraph(dict)
        graph.add_node("generate", self._generate_node)
        graph.add_node("evaluate", self._evaluate_node)
        graph.set_entry_point("generate")
        graph.add_edge("generate", "evaluate")
        graph.add_conditional_edges(
            "evaluate",
            self._route_after_evaluate,
            {"refine": "generate", "terminal": END},
        )
        return graph.compile()

    def _generate_node(self, state_dict: dict[str, Any]) -> dict[str, Any]:
        state = _state_from_dict(state_dict)
        output = self.run_generate(state)
        state.latest_output = output
        return _state_to_dict(state)

    def _evaluate_node(self, state_dict: dict[str, Any]) -> dict[str, Any]:
        state = _state_from_dict(state_dict)
        evaluation = self.evaluate(state, state.latest_output or {})
        state.latest_evaluation = evaluation
        state.attempts.append(
            {
                "iteration": state.iteration,
                "summary": self.summarize_output(state.latest_output or {}),
                "evaluation_passed": evaluation.passed,
                "evaluation_feedback": evaluation.feedback,
            }
        )
        self.logger.info(
            "task=%s iteration=%s evaluate passed=%s feedback=%s",
            state.task_id,
            state.iteration,
            evaluation.passed,
            evaluation.feedback,
        )
        if evaluation.passed:
            state.status = "succeeded"
        elif state.iteration + 1 >= MAX_ITERATIONS:
            state.status = "failed_after_iterations"
        else:
            state.iteration += 1
            state.status = "running"
        return _state_to_dict(state)

    def _route_after_evaluate(self, state_dict: dict[str, Any]) -> str:
        return "refine" if state_dict["status"] == "running" else "terminal"

    # -- Public entry point ---------------------------------------------------------------

    def run(
        self, task_id: str, inputs: dict[str, Any], answers: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Run (or resume) this coded agent for `task_id`.

        A new `task_id` starts a run from `inputs`. Reusing a `task_id` that previously
        returned `failed_after_iterations` resumes persisted state with `answers` merged in.
        """

        persisted = self.state_store.load(task_id)
        if persisted is not None:
            state = _state_from_dict(persisted)
            state.answers = {**state.answers, **(answers or {})}
            state.status = "running"
            self.logger.info("task=%s resuming with answers=%s", task_id, answers or {})
        else:
            state = CodedAgentState(task_id=task_id, inputs=inputs, answers=answers or {})
            self.logger.info("task=%s iteration=0 entry", task_id)

        final_state_dict = self._graph.invoke(_state_to_dict(state))
        final_state = _state_from_dict(final_state_dict)
        self.state_store.save(task_id, _state_to_dict(final_state))

        if final_state.status == "succeeded":
            self.logger.info("task=%s terminal status=succeeded", task_id)
            return {
                "status": "succeeded",
                "task_id": task_id,
                "agent_slug": self.agent_slug,
                "output": final_state.latest_output,
                "iterations_used": final_state.iteration + 1,
                "attempts": final_state.attempts,
            }

        questions = self.build_failure_questions(final_state)
        self.logger.info("task=%s terminal status=failed_after_iterations", task_id)
        return {
            "status": "failed_after_iterations",
            "task_id": task_id,
            "agent_slug": self.agent_slug,
            "attempts": final_state.attempts,
            "failure_reason": final_state.latest_evaluation.feedback
            if final_state.latest_evaluation
            else "unknown",
            "questions": questions,
            "awaiting_answers": True,
        }


def _state_to_dict(state: CodedAgentState) -> dict[str, Any]:
    return {
        "task_id": state.task_id,
        "inputs": state.inputs,
        "answers": state.answers,
        "iteration": state.iteration,
        "latest_output": state.latest_output,
        "latest_evaluation": (
            {"passed": state.latest_evaluation.passed, "feedback": state.latest_evaluation.feedback}
            if state.latest_evaluation
            else None
        ),
        "attempts": state.attempts,
        "status": state.status,
    }


def _state_from_dict(state_dict: dict[str, Any]) -> CodedAgentState:
    latest_evaluation = state_dict.get("latest_evaluation")
    return CodedAgentState(
        task_id=state_dict["task_id"],
        inputs=state_dict["inputs"],
        answers=state_dict.get("answers", {}),
        iteration=state_dict.get("iteration", 0),
        latest_output=state_dict.get("latest_output"),
        latest_evaluation=(
            EvaluationResult(passed=latest_evaluation["passed"], feedback=latest_evaluation["feedback"])
            if latest_evaluation
            else None
        ),
        attempts=state_dict.get("attempts", []),
        status=state_dict.get("status", "running"),
    )
