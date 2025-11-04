"""
State Schema for the Agentic Workflow

This defines the shared state that flows through all agents.
Think of it as the "memory" that all agents can read and write to.
"""
from typing import TypedDict, Optional, List, Dict, Any
from typing_extensions import Annotated
import operator

class AnalysisState(TypedDict):
    """
    The complete state for repository analysis workflow.
    
    This state is passed through all agents and accumulates data
    as each agent completes its work.
    
    Flow:
    User Input → State Created → Agent 1 → State Updated → Agent 2 → ... → Final State
    """
    
    # ===== INPUT (from user) =====
    repo_url: str
    """GitHub repository URL to analyze"""
    
    # ===== METADATA =====
    session_id: str
    """Unique session identifier"""
    
    current_agent: Optional[str]
    """Name of currently executing agent"""
    
    status: str
    """Current workflow status: running, completed, error"""
    
    # ===== MESSAGES (for tracking) =====
    messages: Annotated[List[str], operator.add]
    """
    List of messages tracking workflow progress.
    Using operator.add means each agent APPENDS to this list
    instead of replacing it.
    """
    
    # ===== AGENT OUTPUTS =====
    raw_data: Optional[Dict[str, Any]]
    """
    Raw data from GitHub (Data Fetcher Agent output)
    Contains: commits, PRs, issues, contributors, etc.
    """
    
    code_analysis: Optional[Dict[str, Any]]
    """
    Code quality analysis (Code Analyst Agent output)
    Future: Will contain quality scores, complexity, etc.
    """
    
    metrics: Optional[Dict[str, Any]]
    """
    Repository metrics (Metrics Calculator Agent output)
    Future: Will contain commit frequency, PR stats, etc.
    """
    
    issue_insights: Optional[Dict[str, Any]]
    """
    Issue pattern analysis (Issue Scanner Agent output)
    Future: Will contain categorized issues, patterns, etc.
    """
    
    contributor_report: Optional[Dict[str, Any]]
    """
    Contributor analysis (Contributor Analyst Agent output)
    Future: Will contain top contributors, bus factor, etc.
    """
    
    final_report: Optional[Dict[str, Any]]
    """
    Final synthesized report (Report Generator Agent output)
    Future: Will contain executive summary, recommendations, etc.
    """
    
    # ===== ERROR HANDLING =====
    error: Optional[str]
    """Error message if something goes wrong"""
    
    failed_agent: Optional[str]
    """Name of agent that failed (if any)"""
    
    # ===== TIMING =====
    workflow_steps: Optional[List[Dict[str, Any]]]
    """List of completed workflow steps with timing info"""
    
    started_at: Optional[str]
    """ISO timestamp when workflow started"""
    
    completed_at: Optional[str]
    """ISO timestamp when workflow completed"""

# Type hint for cleaner code
State = AnalysisState