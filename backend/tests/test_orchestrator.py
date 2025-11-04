"""
Test Orchestrator Agent
"""
import asyncio
from agents.orchestrator import OrchestratorAgent
import json

async def test_orchestrator_basic():
    """Test basic orchestration"""
    print("=" * 60)
    print("TESTING ORCHESTRATOR AGENT - BASIC")
    print("=" * 60)
    
    # Create orchestrator
    orchestrator = OrchestratorAgent()
    
    # Test state
    state = {
        "repo_url": "https://github.com/octocat/Hello-World"
    }
    
    print(f"\n🎭 Starting orchestration...")
    print(f"Repository: {state['repo_url']}")
    print("=" * 60)
    
    # Execute
    result = await orchestrator.execute(state)
    
    # Display results
    print("\n" + "=" * 60)
    print("ORCHESTRATION RESULTS")
    print("=" * 60)
    
    if result.get("status") == "error":
        print(f"\n❌ ERROR: {result.get('error')}")
        return False
    
    print(f"\n✅ Status: {result.get('status')}")
    print(f"✅ Session ID: {result.get('session_id')}")
    
    # Show workflow summary
    summary = orchestrator.get_workflow_summary(result)
    
    print(f"\n📊 Workflow Summary:")
    print(f"   Total Steps: {summary['total_steps']}")
    print(f"   Total Duration: {summary['total_duration']:.2f}s")
    print(f"\n   Steps Executed:")
    for step in summary['steps']:
        print(f"      • {step['step']}: {step['duration']:.2f}s")
    
    # Show data collected
    if 'raw_data' in result:
        data = result['raw_data']
        print(f"\n📦 Data Collected:")
        print(f"   Repository: {data['repository']['full_name']}")
        print(f"   Stars: {data['repository']['stars']}")
        print(f"   Commits: {len(data['commits'])}")
        print(f"   Pull Requests: {len(data['pull_requests'])}")
        print(f"   Issues: {len(data['issues'])}")
        print(f"   Contributors: {len(data['contributors'])}")
    
    # Save full result
    with open('test_output_orchestrator.json', 'w') as f:
        # Convert to JSON-serializable format
        json_result = {
            "session_id": result.get("session_id"),
            "repo_url": result.get("repo_url"),
            "status": result.get("status"),
            "workflow_summary": summary,
            "data_summary": {
                "commits": len(result.get('raw_data', {}).get('commits', [])),
                "pull_requests": len(result.get('raw_data', {}).get('pull_requests', [])),
                "issues": len(result.get('raw_data', {}).get('issues', [])),
                "contributors": len(result.get('raw_data', {}).get('contributors', [])),
            }
        }
        json.dump(json_result, f, indent=2)
    
    print(f"\n💾 Full result saved to: test_output_orchestrator.json")
    
    return True

async def test_orchestrator_multiple_repos():
    """Test with multiple repositories"""
    print("\n\n" + "=" * 60)
    print("TESTING ORCHESTRATOR - MULTIPLE REPOS")
    print("=" * 60)
    
    repos = [
        "https://github.com/octocat/Hello-World",
        "https://github.com/microsoft/vscode",
    ]
    
    orchestrator = OrchestratorAgent()
    
    results = []
    
    for repo_url in repos:
        print(f"\n🎭 Orchestrating: {repo_url}")
        print("-" * 60)
        
        result = await orchestrator.execute({"repo_url": repo_url})
        
        if result.get("status") == "error":
            print(f"   ❌ Failed: {result.get('error')}")
        else:
            summary = orchestrator.get_workflow_summary(result)
            print(f"   ✅ Success!")
            print(f"   ⏱️  Duration: {summary['total_duration']:.2f}s")
            print(f"   📊 Steps: {summary['total_steps']}")
            
            results.append({
                "repo": repo_url,
                "status": "success",
                "duration": summary['total_duration']
            })
    
    # Summary
    print("\n" + "=" * 60)
    print("MULTI-REPO TEST SUMMARY")
    print("=" * 60)
    
    for r in results:
        print(f"✅ {r['repo']}")
        print(f"   Duration: {r['duration']:.2f}s")

async def test_orchestrator_error_handling():
    """Test error handling"""
    print("\n\n" + "=" * 60)
    print("TESTING ORCHESTRATOR - ERROR HANDLING")
    print("=" * 60)
    
    orchestrator = OrchestratorAgent()
    
    # Test 1: No repo URL
    print("\n🧪 Test 1: No repo URL")
    result = await orchestrator.execute({})
    print(f"   Expected error: {result.get('error')}")
    assert result.get("status") == "error"
    print("   ✅ Handled correctly")
    
    # Test 2: Invalid repo URL
    print("\n🧪 Test 2: Invalid repo URL")
    result = await orchestrator.execute({"repo_url": "not-a-valid-url"})
    print(f"   Expected error: {result.get('error')}")
    assert result.get("status") == "error"
    print("   ✅ Handled correctly")
    
    # Test 3: Non-existent repo
    print("\n🧪 Test 3: Non-existent repo")
    result = await orchestrator.execute({"repo_url": "https://github.com/nonexistent/repo123456"})
    print(f"   Expected error: {result.get('error')}")
    assert result.get("status") == "error"
    print("   ✅ Handled correctly")

if __name__ == "__main__":
    print("\n🚀 Starting Orchestrator Agent Tests...\n")
    
    # Run tests
    asyncio.run(test_orchestrator_basic())
    
    # Multiple repos (uncomment if you want)
    # asyncio.run(test_orchestrator_multiple_repos())
    
    # Error handling
    asyncio.run(test_orchestrator_error_handling())
    
    print("\n" + "=" * 60)
    print("✅ ALL ORCHESTRATOR TESTS COMPLETE!")
    print("=" * 60)