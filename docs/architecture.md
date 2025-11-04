# Agentic GitHub Analyzer - Architecture

## System Overview
Multi-agent system using LangGraph for orchestrating specialized AI agents
that analyze GitHub repositories.

## Agent Architecture

### 1. Orchestrator Agent 🎭
**Role:** Main coordinator
**Input:** User query + repo URL
**Output:** Coordinated analysis results
**Decisions:** Which agents to call, in what order

### 2. Data Fetcher Agent 📥
**Role:** GitHub data collection
**Tools:** 
- PyGithub API
- Caching layer
**Fetches:**
- Commits
- Pull Requests
- Issues
- Contributors
- Code structure
**Output:** Structured data dict

### 3. Code Analyst Agent 💻
**Role:** Code quality analysis
**Tools:**
- AST parser
- LLM for insights
**Analyzes:**
- Code structure
- Complexity
- Documentation
**Output:** Code quality report

### 4. Metrics Calculator Agent 📊
**Role:** Performance metrics
**Calculates:**
- Commit frequency
- PR merge time
- Issue resolution time
- Repository health score
**Output:** Metrics dict

### 5. Issue Scanner Agent 🔍
**Role:** Issue pattern detection
**Uses LLM to:**
- Categorize issues
- Find common patterns
- Identify pain points
**Output:** Issue insights

### 6. Contributor Analyst Agent 👥
**Role:** Contributor analysis
**Analyzes:**
- Top contributors
- Contribution patterns
- Bus factor
**Output:** Contributor report

### 7. Report Generator Agent 📝
**Role:** Synthesize everything
**Uses LLM to:**
- Combine all agent outputs
- Generate natural language report
- Create actionable recommendations
**Output:** Final report

## State Schema
```python
class AnalysisState(TypedDict):
    repo_url: str
    session_id: str
    current_agent: str
    
    # Data from agents
    raw_data: dict
    code_analysis: dict
    metrics: dict
    issue_insights: dict
    contributor_report: dict
    
    # Final output
    final_report: dict
    status: str
    errors: list
```

## Workflow Graph
```
User Input (repo_url)
    ↓
Orchestrator (decide what to do)
    ↓
Data Fetcher (collect all GitHub data)
    ↓
┌───────────────┴───────────────┐
│               │               │
Code Analyst  Metrics Calc  Issue Scanner
│               │               │
└───────────────┬───────────────┘
    ↓
Contributor Analyst
    ↓
Report Generator
    ↓
Final Output
```

## Technology Stack
- **LangGraph:** Agent orchestration
- **LangChain:** LLM integration
- **Ollama/LM Studio:** Local LLM
- **PyGithub:** GitHub API
- **FastAPI:** Backend API
- **WebSocket:** Real-time updates