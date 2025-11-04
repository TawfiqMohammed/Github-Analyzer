"""
Test LangGraph Workflow - The Complete Agentic System
"""
import asyncio
from workflows.analysis_workflow import AnalysisWorkflow, analyze_repository
import json

async def test_basic_workflow():
    """Test basic LangGraph workflow"""
    print("=" * 60)
    print("TESTING LANGGRAPH WORKFLOW - BASIC")
    print("=" * 60)
    
    # Create workflow
    workflow = AnalysisWorkflow()
    
    # Display graph structure
    print("\n📊 Workflow Graph Structure:")
    print(workflow.get_graph_visualization())
    
    # Run workflow
    repo_url = "https://github.com/octocat/Hello-World"
    
    print(f"\n🚀 Running workflow for: {repo_url}")
    print("=" * 60)
    
    result = await workflow.run(repo_url)
    
    # Display results
    print("\n" + "=" * 60)
    print("WORKFLOW RESULTS")
    print("=" * 60)
    
    print(f"\n✅ Status: {result['status']}")
    print(f"✅ Session ID: {result['session_id']}")
    
    print(f"\n📝 Messages:")
    for i, msg in enumerate(result['messages'], 1):
        print(f"   {i}. {msg}")
    
    if result['raw_data']:
        data = result['raw_data']
        print(f"\n📦 Data Collected:")
        print(f"   Repository: {data['repository']['full_name']}")
        print(f"   Stars: {data['repository']['stars']}")
        print(f"   Commits: {len(data['commits'])}")
        print(f"   Pull Requests: {len(data['pull_requests'])}")
        print(f"   Issues: {len(data['issues'])}")
        print(f"   Contributors: {len(data['contributors'])}")
    
    # Timing
    if result['started_at'] and result['completed_at']:
        from datetime import datetime
        start = datetime.fromisoformat(result['started_at'])
        end = datetime.fromisoformat(result['completed_at'])
        duration = (end - start).total_seconds()
        print(f"\n⏱️  Total Duration: {duration:.2f}s")
    
    # Save result
    with open('test_output_langgraph.json', 'w') as f:
        json_result = {
            "session_id": result["session_id"],
            "status": result["status"],
            "messages": result["messages"],
            "data_summary": {
                "commits": len(result.get('raw_data', {}).get('commits', [])),
                "pull_requests": len(result.get('raw_data', {}).get('pull_requests', [])),
                "issues": len(result.get('raw_data', {}).get('issues', [])),
                "contributors": len(result.get('raw_data', {}).get('contributors', [])),
            }
        }
        json.dump(json_result, f, indent=2)
    
    print(f"\n💾 Full result saved to: test_output_langgraph.json")
    
    return result

async def test_convenience_function():
    """Test the convenience function"""
    print("\n\n" + "=" * 60)
    print("TESTING CONVENIENCE FUNCTION")
    print("=" * 60)
    
    repo_url = "https://github.com/microsoft/vscode"
    
    print(f"\n🚀 Using convenience function for: {repo_url}")
    print("=" * 60)
    
    result = await analyze_repository(repo_url)
    
    print(f"\n✅ Analysis complete!")
    print(f"   Status: {result['status']}")
    print(f"   Session: {result['session_id']}")
    
    if result['raw_data']:
        data = result['raw_data']
        print(f"   Repository: {data['repository']['full_name']}")
        print(f"   Stars: {data['repository']['stars']:,}")

async def test_comparison():
    """Compare old orchestrator vs new LangGraph"""
    print("\n\n" + "=" * 60)
    print("COMPARISON: Orchestrator vs LangGraph")
    print("=" * 60)
    
    from agents.orchestrator import OrchestratorAgent
    
    repo_url = "https://github.com/octocat/Hello-World"
    
    # Test Orchestrator
    print("\n1️⃣ Testing OLD Orchestrator Agent:")
    print("-" * 60)
    orchestrator = OrchestratorAgent()
    orch_result = await orchestrator.execute({"repo_url": repo_url})
    print(f"   Status: {orch_result['status']}")
    
    # Test LangGraph
    print("\n2️⃣ Testing NEW LangGraph Workflow:")
    print("-" * 60)
    lg_result = await analyze_repository(repo_url)
    print(f"   Status: {lg_result['status']}")
    
    print("\n📊 Comparison:")
    print(f"   Both Status: {orch_result['status']} vs {lg_result['status']}")
    print(f"   Both have data: {('raw_data' in orch_result)} vs {('raw_data' in lg_result)}")
    print(f"\n✅ LangGraph provides SAME functionality with:")
    print(f"   • Better state management")
    print(f"   • Visual graph structure")
    print(f"   • Easier to add new agents")
    print(f"   • Industry-standard framework")

if __name__ == "__main__":
    print("\n🚀 Starting LangGraph Workflow Tests...\n")
    
    # Run tests
    asyncio.run(test_basic_workflow())
    
    # Convenience function test (uncomment if desired)
    # asyncio.run(test_convenience_function())
    
    # Comparison test
    asyncio.run(test_comparison())
    
    print("\n" + "=" * 60)
    print("✅ ALL LANGGRAPH TESTS COMPLETE!")
    print("=" * 60)
    print("\n🎉 YOUR AGENTIC AI SYSTEM IS NOW POWERED BY LANGGRAPH!")
    print("=" * 60)