"""
LangGraph Workflow - The Agentic Orchestration Layer

This is where the magic happens! LangGraph coordinates all agents
and manages the flow of data between them.
"""
from langgraph.graph import StateGraph, END
from .state_schema import AnalysisState
from agents.data_fetcher import DataFetcherAgent
from datetime import datetime
import uuid

class AnalysisWorkflow:
    """
    LangGraph-powered agentic workflow for repository analysis.
    
    This class creates and manages the agent coordination graph.
    """
    
    def __init__(self):
        """Initialize workflow with all agents"""
        
        # Initialize agents
        self.data_fetcher = DataFetcherAgent()
        
        # Future agents (we'll add these later):
        # self.code_analyst = CodeAnalystAgent()
        # self.metrics_calculator = MetricsCalculatorAgent()
        # self.issue_scanner = IssueScannerAgent()
        # self.contributor_analyst = ContributorAnalystAgent()
        # self.report_generator = ReportGeneratorAgent()
        
        # Build the graph
        self.app = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow graph.
        
        This defines:
        1. What agents exist (nodes)
        2. How they connect (edges)
        3. What order they execute
        
        Returns:
            Compiled LangGraph application
        """
        
        # Create the graph with our state schema
        workflow = StateGraph(AnalysisState)
        
        # Add nodes (each node is an agent or processing step)
        workflow.add_node("start", self._start_node)
        workflow.add_node("fetch_data", self._fetch_data_node)
        workflow.add_node("finalize", self._finalize_node)
        
        # Future nodes (we'll add these later):
        # workflow.add_node("analyze_code", self._analyze_code_node)
        # workflow.add_node("calculate_metrics", self._calculate_metrics_node)
        # workflow.add_node("scan_issues", self._scan_issues_node)
        # workflow.add_node("analyze_contributors", self._analyze_contributors_node)
        # workflow.add_node("generate_report", self._generate_report_node)
        
        # Define the flow (edges connect nodes)
        workflow.set_entry_point("start")
        workflow.add_edge("start", "fetch_data")
        workflow.add_edge("fetch_data", "finalize")
        
        # Future flow (when we add more agents):
        # workflow.add_edge("fetch_data", "analyze_code")
        # workflow.add_edge("analyze_code", "calculate_metrics")
        # workflow.add_edge("calculate_metrics", "scan_issues")
        # workflow.add_edge("scan_issues", "analyze_contributors")
        # workflow.add_edge("analyze_contributors", "generate_report")
        # workflow.add_edge("generate_report", "finalize")
        
        workflow.set_finish_point("finalize")
        
        # Compile the graph into an executable app
        return workflow.compile()
    
    # ===== NODE FUNCTIONS =====
    # Each function represents one step in the workflow
    
    async def _start_node(self, state: AnalysisState) -> AnalysisState:
        """
        Starting node - initializes the workflow.
        
        This is where we set up the session and prepare for analysis.
        """
        # Generate session ID if not present
        if "session_id" not in state or not state["session_id"]:
            state["session_id"] = str(uuid.uuid4())
        
        # Initialize state fields
        state["status"] = "running"
        state["started_at"] = datetime.now().isoformat()
        state["current_agent"] = "Workflow Manager"
        
        # Add starting message
        if "messages" not in state:
            state["messages"] = []
        state["messages"].append(f"Workflow started for {state['repo_url']}")
        
        print(f"\n{'='*60}")
        print(f"🚀 LANGGRAPH WORKFLOW STARTED")
        print(f"{'='*60}")
        print(f"Repository: {state['repo_url']}")
        print(f"Session ID: {state['session_id']}")
        print(f"{'='*60}\n")
        
        return state
    
    async def _fetch_data_node(self, state: AnalysisState) -> AnalysisState:
        """
        Data fetching node - collects all GitHub data.
        
        Calls the Data Fetcher Agent and updates state with results.
        """
        print(f"📥 Executing: Data Fetcher Agent")
        
        state["current_agent"] = "Data Fetcher"
        state["messages"].append("Fetching repository data from GitHub")
        
        # Execute Data Fetcher Agent
        result = await self.data_fetcher.execute(state)
        
        # Update state with results
        state.update(result)
        state["messages"].append("Data fetching completed")
        
        return state
    
    async def _finalize_node(self, state: AnalysisState) -> AnalysisState:
        """
        Finalization node - completes the workflow.
        
        This is where we wrap up and prepare the final output.
        """
        print(f"\n{'='*60}")
        print(f"✅ LANGGRAPH WORKFLOW COMPLETED")
        print(f"{'='*60}")
        
        # Set completion status
        if state.get("status") != "error":
            state["status"] = "completed"
        
        state["completed_at"] = datetime.now().isoformat()
        state["current_agent"] = "Workflow Manager"
        state["messages"].append("Workflow completed successfully")
        
        # Calculate total duration
        if state.get("started_at") and state.get("completed_at"):
            start = datetime.fromisoformat(state["started_at"])
            end = datetime.fromisoformat(state["completed_at"])
            duration = (end - start).total_seconds()
            
            print(f"Total Duration: {duration:.2f}s")
            print(f"Status: {state['status']}")
            print(f"{'='*60}\n")
        
        return state
    
    # ===== PUBLIC METHODS =====
    
    async def run(self, repo_url: str, session_id: str = None) -> AnalysisState:
        """
        Run the complete workflow for a repository.
        
        This is the main entry point for analysis.
        
        Args:
            repo_url: GitHub repository URL
            session_id: Optional session ID (generated if not provided)
            
        Returns:
            Final state with all analysis results
        """
        # Create initial state
        initial_state: AnalysisState = {
            "repo_url": repo_url,
            "session_id": session_id or str(uuid.uuid4()),
            "status": "initialized",
            "messages": [],
            "current_agent": None,
            "raw_data": None,
            "code_analysis": None,
            "metrics": None,
            "issue_insights": None,
            "contributor_report": None,
            "final_report": None,
            "error": None,
            "failed_agent": None,
            "workflow_steps": None,
            "started_at": None,
            "completed_at": None,
        }
        
        # Run the workflow
        final_state = await self.app.ainvoke(initial_state)
        
        return final_state
    
    def get_graph_visualization(self) -> str:
        """
        Get a text visualization of the workflow graph.
        
        Useful for debugging and documentation.
        """
        return """
        LangGraph Workflow Visualization:
        
        START
          ↓
        [Start Node]
          ↓
        [Fetch Data] ← Data Fetcher Agent
          ↓
        [Finalize]
          ↓
        END
        
        Future expansion (when we add more agents):
        
        START
          ↓
        [Start Node]
          ↓
        [Fetch Data] ← Data Fetcher Agent
          ↓
        [Analyze Code] ← Code Analyst Agent
          ↓
        [Calculate Metrics] ← Metrics Calculator Agent
          ↓
        [Scan Issues] ← Issue Scanner Agent
          ↓
        [Analyze Contributors] ← Contributor Analyst Agent
          ↓
        [Generate Report] ← Report Generator Agent
          ↓
        [Finalize]
          ↓
        END
        """


# ===== CONVENIENCE FUNCTION =====

async def analyze_repository(repo_url: str) -> AnalysisState:
    """
    Convenience function to analyze a repository.
    
    This is the simplest way to run an analysis.
    
    Example:
        result = await analyze_repository("https://github.com/facebook/react")
        print(result["raw_data"])
    
    Args:
        repo_url: GitHub repository URL
        
    Returns:
        Complete analysis state
    """
    workflow = AnalysisWorkflow()
    return await workflow.run(repo_url)