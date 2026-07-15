Training Curriculum Ideas - Sven

PART 1 - Creating your own Agent-Build-Agents Framework 
"Students will learn how to plan, design and build an agent-builds-agents framework to create, extend and maintain their own (agentic) software solutions. 
This part of the training will end with a fully-functional, working agent-builds-agents framework that can be used to build and extend their own software solutions. 
Students that are mainly concerned with the application side of the frame work can skip this session"
    - what you will have built at the end of this part => teaser
    - Prerequisites (tech knowledge and experience to follow this Part 1)
    - Purpose of an agent-builds-agents framework
    - Specific Goals
    - Components
    - Architecture (structure, workflow, skills, agents, tools, instructed vs. coded agents, data structures, etc.)
    - Implementation of existing framework
    - Adding additional special purpose agents
    - ... all main parts a student needs to know when they want to create a similar solution on their own 

PART 2 - Applying the Agent-Build-Agents Framework to create a sophisticated Stock Trader Research Cockpit
"Students will learn how to use the agent-builds-agents framework to create a sophisticated stock trader research cockpit which will allow them to quickly focus on only those tickers with presumed institutional buying or selling for their individual trading strategies and executions.
"
    - what you will have built at the end of this part => teaser
        - market themes reasearch (early detecting of institutional trends)
            - Tickers resemblence screening and persistent storage
                - detect confluent price and volume action accross multiple tickers
                - detect chart pattern resemblence between tickers based on a trained model
                - tickers resemblence strength graph (sync rank)
            - regular narrative mining across earnings transcripts, SEC filings, and news reporting 
            - market themes hub and research dashboard (strength cycle, tickers, aggregated performance, etc.)
            - financial ticker scorecard based on 
        - pattern hunting across tickers universe based on chart pattern examples
        - synthetical themes and industries charts
        - themes and industries relative ranking
        - stock screener based on individual price and volume data and derived data
            - defined your own derived price and volume indicators (e.g. number of up/down days, volume density, ...)
        - combining price/volume screener results with market themes resaerch data to narrow the watched universe
        - data feeds connector hub with persistent storage
        - integrating the cockpit into your propriatory systems and data hubs
        - all principles applicable to equivalent non-US market APIs     
    - Bonus 1: TradingView Sync Chrome extension
        - show your own data side-by-side with your TradingView charts
        - bidirectional sync with selected ticker in TV 
        - display theme performance chart of selected ticker
        - display selected ticker's relative performance vs. other tickers in thema/sector/industry
    - Bonus 2: Train you own chart resemblence model
        - Training/Validation framework
        - Labelling App
        - Integration in your own solutions

    - training content:
        - Training Curriculum
        - environments (OS, IDE, plug-ins)
            - Installation of agent-builds-agents framework
            - repo introdcution (where to find what in it as overview)
        - API provide and model consideration 
            - capabilities vs costs
            - what we used for the training solutions and what the approx. costs were 
        - Prerequisites (data feeds, APIs, etc.)
            - estimated cost estimates for agent api's
        - Structuring and Authoring of Trader Input data (optional)
            - this chapter may be skipped as training is based on example input data
            - structuring your existing input using authoring and validation skills
            - structuring your own view on relevent market behavior and applied strategies into coherent input data
            - authoring of user stories
            - glossary
        - (Prompt) Communictaion between trader and agent-builds-agents framework across project phases
            - understanding the trader requirements
            - solution refinement (option, Pros/Cons, alternatives)
            - design
            - architecture
            - implementation
            - testing / debugging
            - maintenance
        - Step-by-Step Trader Reasearch Cockpit Creation
            - chapters for each step 
            - sequence to be aligned between functional and technical constraints
                roughly:
                - install agent-builds-agents framework
                - create a new project
                - establish required APIs to agent-builds-agents models
                - establish required market data feeds
                - EOD data load and storage in mongodb
                - define your own derived price and volume indicators (e.g. number of up/down days, volume density, ...)
                - Ticker Screener creation with results vizualization and export for Tradingview
                - Creating industry synthetic performance data incl. chart vizualization and rel ranking
                - Detecting Tickers resemblence by price and volume action accross multiple tickers
                - Detecting Tickers resemblence by visual chart pattern comparison
                    - setting up ResNet model inference (training in Bonus 2)
                - Creating Bonding Graph based on Tickers resemblence strength
                - creating market narrative mining data
                    - NLP, clustering, trend data
                - Connections Research for resembling tickers (3-stage agent pipeline)
                    - 3-staged agent pipeline
                - Themes Creation based on accepted connections
                - calculating and vizualizing themes performance data
                - calculating and vizualizing themes internals (breadth, coheasion, leaders, laggards)
                - combining price/volume screener results with market themes data to surface tickers for individual strategies
                    - including what filters to apply to the screener results
                    - what filters applied to themes data
                    - viszualization of the combined results and watchlist generation / export for Tradingview
                - integration aspects into existing systems and data hubs
                    - linked to trader input data (tech constraints)
                    - how to tell the agent-framework what is existing and should be re-used
                        - interfaces
                        - data (files, DB)
                        - existing AI data hubs (RAG, etc.)
                        - functions (as Tools?)
                - Bonus 1
                - Bonus 2


