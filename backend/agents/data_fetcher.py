"""
Data Fetcher Agent - Collects all data from GitHub
"""
from .base_agent import BaseAgent
from github import Github
from typing import Dict, Any
from dotenv import load_dotenv
import os
from datetime import datetime

class DataFetcherAgent(BaseAgent):
    """
    Agent responsible for fetching all data from GitHub repository.
    
    Uses PyGithub to interact with GitHub API.
    Collects: repo info, commits, PRs, issues, contributors
    """
    
    load_dotenv() 

    def __init__(self):
        super().__init__("Data Fetcher")
        
        # Get GitHub token from environment (optional)
        self.github_token = os.getenv("GITHUB_TOKEN", "")
        
        # Initialize GitHub client
        if self.github_token:
            self.github = Github(self.github_token)
            self.log("Authenticated with GitHub token")
        else:
            self.github = Github()
            self.log("Using GitHub without authentication (rate limited)")
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch all repository data from GitHub.
        
        Args:
            state: Must contain 'repo_url'
            
        Returns:
            state with 'raw_data' added
        """
        self.start_timer()
        
        # Get repo URL from state
        repo_url = state.get("repo_url")
        if not repo_url:
            return self.create_error_state(state, "No repository URL provided")
        
        self.log(f"Fetching data for: {repo_url}")
        
        # Extract owner/repo from URL
        try:
            repo_full_name = self._extract_repo_name(repo_url)
            self.log(f"Repository: {repo_full_name}")
        except Exception as e:
            return self.create_error_state(state, f"Invalid GitHub URL: {str(e)}")
        
        # Fetch all data
        try:
            repo = self.github.get_repo(repo_full_name)
            
            # Fetch each data type
            repo_info = self._fetch_repo_info(repo)
            commits = self._fetch_commits(repo)
            pull_requests = self._fetch_pull_requests(repo)
            issues = self._fetch_issues(repo)
            contributors = self._fetch_contributors(repo)
            
            # Combine all data
            raw_data = {
                "repository": repo_info,
                "commits": commits,
                "pull_requests": pull_requests,
                "issues": issues,
                "contributors": contributors,
                "fetched_at": datetime.now().isoformat()
            }
            
            duration = self.end_timer()
            
            self.log(f"✓ Successfully fetched:")
            self.log(f"  - {len(commits)} commits")
            self.log(f"  - {len(pull_requests)} pull requests")
            self.log(f"  - {len(issues)} issues")
            self.log(f"  - {len(contributors)} contributors")
            
            return {
                **state,
                "raw_data": raw_data,
                "status": "data_fetched",
                "data_fetch_duration": duration
            }
            
        except Exception as e:
            return self.create_error_state(state, f"Failed to fetch data: {str(e)}")
    
    def _extract_repo_name(self, repo_url: str) -> str:
        """
        Extract owner/repo from GitHub URL.
        
        Examples:
            https://github.com/facebook/react -> facebook/react
            github.com/microsoft/vscode -> microsoft/vscode
        """
        # Remove https:// or http://
        url = repo_url.replace("https://", "").replace("http://", "")
        
        # Remove github.com/
        url = url.replace("github.com/", "")
        
        # Split and get first two parts
        parts = url.split("/")
        if len(parts) < 2:
            raise ValueError("Invalid GitHub URL format")
        
        return f"{parts[0]}/{parts[1]}"
    
    def _fetch_repo_info(self, repo) -> Dict[str, Any]:
        """Fetch basic repository information"""
        self.log("Fetching repository info...")
        
        return {
            "name": repo.name,
            "full_name": repo.full_name,
            "description": repo.description,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "watchers": repo.watchers_count,
            "language": repo.language,
            "size": repo.size,
            "open_issues": repo.open_issues_count,
            "created_at": repo.created_at.isoformat(),
            "updated_at": repo.updated_at.isoformat(),
            "pushed_at": repo.pushed_at.isoformat() if repo.pushed_at else None,
            "default_branch": repo.default_branch,
            "has_wiki": repo.has_wiki,
            "has_pages": repo.has_pages,
            "archived": repo.archived,
        }
    
    def _fetch_commits(self, repo, max_commits: int = 100) -> list:
        """Fetch recent commits"""
        self.log(f"Fetching last {max_commits} commits...")
        
        commits = []
        try:
            for commit in repo.get_commits()[:max_commits]:
                commits.append({
                    "sha": commit.sha[:7],  # Short SHA
                    "author": commit.author.login if commit.author else "Unknown",
                    "date": commit.commit.author.date.isoformat(),
                    "message": commit.commit.message.split('\n')[0],  # First line only
                    "additions": commit.stats.additions if commit.stats else 0,
                    "deletions": commit.stats.deletions if commit.stats else 0,
                })
        except Exception as e:
            self.log(f"Warning: Could not fetch all commits: {str(e)}", level="warning")
        
        return commits
    
    def _fetch_pull_requests(self, repo, max_prs: int = 50) -> list:
        """Fetch pull requests"""
        self.log(f"Fetching last {max_prs} pull requests...")
        
        prs = []
        try:
            for pr in repo.get_pulls(state='all')[:max_prs]:
                prs.append({
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "user": pr.user.login if pr.user else "Unknown",
                    "created_at": pr.created_at.isoformat(),
                    "merged_at": pr.merged_at.isoformat() if pr.merged_at else None,
                    "closed_at": pr.closed_at.isoformat() if pr.closed_at else None,
                })
        except Exception as e:
            self.log(f"Warning: Could not fetch all PRs: {str(e)}", level="warning")
        
        return prs
    
    def _fetch_issues(self, repo, max_issues: int = 50) -> list:
        """Fetch issues (excluding PRs)"""
        self.log(f"Fetching last {max_issues} issues...")
        
        issues = []
        try:
            for issue in repo.get_issues(state='all')[:max_issues]:
                # Skip pull requests (they show up as issues)
                if issue.pull_request:
                    continue
                
                issues.append({
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "user": issue.user.login if issue.user else "Unknown",
                    "created_at": issue.created_at.isoformat(),
                    "closed_at": issue.closed_at.isoformat() if issue.closed_at else None,
                    "labels": [label.name for label in issue.labels],
                    "comments": issue.comments,
                })
        except Exception as e:
            self.log(f"Warning: Could not fetch all issues: {str(e)}", level="warning")
        
        return issues
    
    def _fetch_contributors(self, repo, max_contributors: int = 20) -> list:
        """Fetch top contributors"""
        self.log(f"Fetching top {max_contributors} contributors...")
        
        contributors = []
        try:
            for contributor in repo.get_contributors()[:max_contributors]:
                contributors.append({
                    "login": contributor.login,
                    "contributions": contributor.contributions,
                    "type": contributor.type,
                })
        except Exception as e:
            self.log(f"Warning: Could not fetch all contributors: {str(e)}", level="warning")
        
        return contributors