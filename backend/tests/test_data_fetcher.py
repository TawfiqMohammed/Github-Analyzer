"""
Test Data Fetcher Agent
"""
import asyncio
from agents.data_fetcher import DataFetcherAgent
import json

async def test_data_fetcher():
    print("=" * 60)
    print("TESTING DATA FETCHER AGENT")
    print("=" * 60)
    
    # Create agent
    agent = DataFetcherAgent()
    
    # Test with a real repo (use a small one for testing)
    state = {
        "repo_url": "https://github.com/octocat/Hello-World",
        "session_id": "test-001"
    }
    
    print(f"\n📥 Testing with: {state['repo_url']}")
    print("=" * 60)
    
    # Execute agent
    result = await agent.execute(state)
    
    # Check result
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    if result.get("status") == "error":
        print(f"❌ ERROR: {result.get('error')}")
        return False
    
    if "raw_data" in result:
        data = result["raw_data"]
        
        print(f"\n✅ SUCCESS! Data fetched in {result.get('data_fetch_duration', 0):.2f}s\n")
        
        # Repository info
        repo = data["repository"]
        print(f"📦 Repository: {repo['full_name']}")
        print(f"   ⭐ Stars: {repo['stars']}")
        print(f"   🍴 Forks: {repo['forks']}")
        print(f"   📝 Language: {repo['language']}")
        print(f"   📅 Created: {repo['created_at'][:10]}")
        
        # Data counts
        print(f"\n📊 Data Collected:")
        print(f"   📝 Commits: {len(data['commits'])}")
        print(f"   🔀 Pull Requests: {len(data['pull_requests'])}")
        print(f"   🐛 Issues: {len(data['issues'])}")
        print(f"   👥 Contributors: {len(data['contributors'])}")
        
        # Show sample data
        if data['commits']:
            print(f"\n📝 Latest Commit:")
            commit = data['commits'][0]
            print(f"   SHA: {commit['sha']}")
            print(f"   Author: {commit['author']}")
            print(f"   Message: {commit['message'][:50]}...")
        
        if data['contributors']:
            print(f"\n👥 Top Contributor:")
            top = data['contributors'][0]
            print(f"   User: {top['login']}")
            print(f"   Contributions: {top['contributions']}")
        
        # Save to file for inspection
        with open('test_output_data_fetcher.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n💾 Full data saved to: test_output_data_fetcher.json")
        
        return True
    else:
        print("❌ No data returned!")
        return False

async def test_multiple_repos():
    """Test with multiple repositories"""
    print("\n\n" + "=" * 60)
    print("TESTING MULTIPLE REPOSITORIES")
    print("=" * 60)
    
    repos = [
        "https://github.com/octocat/Hello-World",
        "https://github.com/microsoft/vscode",
        "https://github.com/facebook/react",
    ]
    
    agent = DataFetcherAgent()
    
    for repo_url in repos:
        print(f"\n📥 Testing: {repo_url}")
        
        result = await agent.execute({"repo_url": repo_url})
        
        if result.get("status") == "error":
            print(f"   ❌ Failed: {result.get('error')}")
        else:
            data = result["raw_data"]
            print(f"   ✅ Success! Fetched {len(data['commits'])} commits in {result['data_fetch_duration']:.2f}s")

if __name__ == "__main__":
    print("\n🚀 Starting Data Fetcher Agent Tests...\n")
    
    # Run tests
    asyncio.run(test_data_fetcher())
    
    # Test multiple repos (comment out if API rate limited)
    # asyncio.run(test_multiple_repos())
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETE!")
    print("=" * 60)