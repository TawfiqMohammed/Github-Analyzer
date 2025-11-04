"""
Orchestrator Agent - The Brain of the System
Coordinates all other agents and manages the analysis workflow
"""
from .base_agent import BaseAgent
from .data_fetcher import DataFetcherAgent
from typing import Dict, Any
import uuid
from datetime import datetime

class OrchestratorAgent(BaseAgent):
    """
    Main coordinator agent that orchestrates the entire analysis workflow.
    
    Responsibilities:
    1. Receives user request (repo URL)
    2. Decides which agents to call
    3. Manages the workflow sequence
    4. Collects all results
    5. Returns comprehensive analysis
    """
    
    def __init__(self):
        super().__init__("Orchestrator")
        
        # Initialize all sub-agents
        self.data_fetcher = DataFetcherAgent()
        
        # Track workflow state
        self.workflow_steps = []
        
        self.log("Orchestrator initialized with agents:")
        self.log("  ✓ Data Fetcher Agent")
        # We'll add more agents later:
        # self.log("  ✓ Code Analyst Agent")
        # self.log("  ✓ Metrics Calculator Agent")
        # etc.
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main orchestration logic.
        
        Workflow:
        1. Validate input
        2. Generate session ID
        3. Plan workflow
        4. Execute agents in sequence
        5. Collect results
        6. Return final state
        
        Args:
            state: Must contain 'repo_url'
            
        Returns:
            Complete state with all agent results
        """
        self.start_timer()
        self.workflow_steps = []
        
        # Step 1: Validate input
        self.log("=" * 60)
        self.log("STARTING ORCHESTRATION")
        self.log("=" * 60)
        
        if "repo_url" not in state:
            return self.create_error_state(state, "No repository URL provided")
        
        repo_url = state["repo_url"]
        self.log(f"Repository: {repo_url}")
        
        # Step 2: Generate session ID if not present
        if "session_id" not in state:
            state["session_id"] = str(uuid.uuid4())
        
        session_id = state["session_id"]
        self.log(f"Session ID: {session_id}")
        
        # Step 3: Plan workflow
        workflow = self._plan_workflow(state)
        self.log(f"\nWorkflow planned: {len(workflow)} steps")
        for i, step in enumerate(workflow, 1):
            self.log(f"  {i}. {step}")
        
        # Step 4: Execute workflow
        self.log("\n" + "=" * 60)
        self.log("EXECUTING WORKFLOW")
        self.log("=" * 60)
        
        state = await self._execute_workflow(state, workflow)
        
        # Step 5: Check for errors
        if state.get("status") == "error":
            self.log(f"✗ Workflow failed: {state.get('error')}", level="error")
            duration = self.end_timer()
            return state
        
        # Step 6: Finalize
        state["status"] = "completed"
        state["completed_at"] = datetime.now().isoformat()
        state["workflow_steps"] = self.workflow_steps
        
        duration = self.end_timer()
        
        self.log("\n" + "=" * 60)
        self.log("ORCHESTRATION COMPLETE")
        self.log("=" * 60)
        self.log(f"✓ Total time: {duration:.2f}s")
        self.log(f"✓ Steps executed: {len(self.workflow_steps)}")
        
        return state
    
    def _plan_workflow(self, state: Dict[str, Any]) -> list:
        """
        Plan which agents to call and in what order.
        
        This is where the orchestrator makes DECISIONS!
        
        For now, simple sequence:
        1. Data Fetcher (always first)
        2. Code Analyst (later)
        3. Metrics Calculator (later)
        4. Issue Scanner (later)
        5. Contributor Analyst (later)
        6. Report Generator (later)
        
        Args:
            state: Current state
            
        Returns:
            List of agent names to execute
        """
        workflow = []
        
        # Always fetch data first
        workflow.append("Data Fetcher")
        
        # Later, we'll add conditional logic:
        # if state.get("analyze_code"):
        #     workflow.append("Code Analyst")
        # if state.get("calculate_metrics"):
        #     workflow.append("Metrics Calculator")
        
        # For now, just data fetcher
        # We'll add more agents in next sessions
        
        return workflow
    
    async def _execute_workflow(self, state: Dict[str, Any], workflow: list) -> Dict[str, Any]:
        """
        Execute the planned workflow step by step.
        
        Args:
            state: Current state
            workflow: List of agent names to execute
            
        Returns:
            Updated state after all agents
        """
        for step_name in workflow:
            self.log(f"\n► Executing: {step_name}")
            
            step_start = datetime.now()
            
            # Execute the agent
            if step_name == "Data Fetcher":
                state = await self.data_fetcher.execute(state)
            
            # elif step_name == "Code Analyst":
            #     state = await self.code_analyst.execute(state)
            
            # etc. - we'll add more agents later
            
            step_end = datetime.now()
            step_duration = (step_end - step_start).total_seconds()
            
            # Track step
            self.workflow_steps.append({
                "step": step_name,
                "duration": step_duration,
                "status": state.get("status", "unknown"),
                "timestamp": step_end.isoformat()
            })
            
            # Check for errors
            if state.get("status") == "error":
                self.log(f"✗ {step_name} failed: {state.get('error')}", level="error")
                return state
            
            self.log(f"✓ {step_name} completed in {step_duration:.2f}s")
        
        return state
    
    def get_workflow_summary(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of the workflow execution.
        
        Useful for debugging and monitoring.
        
        Args:
            state: Final state after workflow
            
        Returns:
            Summary dict
        """
        if "workflow_steps" not in state:
            return {"error": "No workflow steps found"}
        
        total_duration = sum(step["duration"] for step in state["workflow_steps"])
        
        return {
            "session_id": state.get("session_id"),
            "repo_url": state.get("repo_url"),
            "status": state.get("status"),
            "total_steps": len(state["workflow_steps"]),
            "total_duration": total_duration,
            "steps": state["workflow_steps"],
            "completed_at": state.get("completed_at"),
        }