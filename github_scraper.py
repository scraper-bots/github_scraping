import requests
import csv
import base64
import time
import os
from datetime import datetime
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class GitHubRepoScraper:
    def __init__(self, username, token=None):
        """
        Initialize the scraper with GitHub username and optional personal access token
        
        Args:
            username (str): Your GitHub username
            token (str, optional): Personal access token for higher rate limits and private repos
        """
        self.username = username
        self.token = token
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Repo-Scraper'
        }
        
        if token:
            self.headers['Authorization'] = f'token {token}'
    
    def get_all_repositories(self):
        """Fetch all repositories for the user"""
        repos = []
        page = 1
        per_page = 100
        
        while True:
            url = f'https://api.github.com/users/{self.username}/repos'
            params = {
                'page': page,
                'per_page': per_page,
                'sort': 'updated',
                'direction': 'desc'
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                print(f"Error fetching repositories: {response.status_code}")
                print(response.text)
                break
            
            page_repos = response.json()
            
            if not page_repos:
                break
                
            repos.extend(page_repos)
            page += 1
            
            # Rate limiting - be nice to GitHub's API
            time.sleep(0.1)
        
        return repos
    
    def get_readme_content(self, repo_name):
        """Fetch README content for a repository"""
        readme_files = ['README.md', 'README.rst', 'README.txt', 'README']
        
        for readme_file in readme_files:
            url = f'https://api.github.com/repos/{self.username}/{repo_name}/contents/{readme_file}'
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                content_data = response.json()
                if content_data.get('encoding') == 'base64':
                    try:
                        readme_content = base64.b64decode(content_data['content']).decode('utf-8')
                        # Clean up the README content - remove excessive newlines and markdown
                        readme_clean = re.sub(r'\n+', ' ', readme_content)
                        readme_clean = re.sub(r'[#*`]', '', readme_clean)
                        return readme_clean.strip()[:500]  # Limit to 500 chars for CSV
                    except:
                        continue
            
            time.sleep(0.1)  # Rate limiting
        
        return "No README found"
    
    def get_languages(self, repo_name):
        """Get programming languages used in the repository"""
        url = f'https://api.github.com/repos/{self.username}/{repo_name}/languages'
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            languages = response.json()
            return ', '.join(languages.keys()) if languages else 'Not specified'
        
        return 'Not specified'
    
    def categorize_repo(self, repo_data, readme_content, languages):
        """Categorize repository based on various factors"""
        name = repo_data['name'].lower()
        description = (repo_data.get('description') or '').lower()
        readme_lower = readme_content.lower()
        
        # Define categories based on common patterns
        categories = []
        
        # Web development
        if any(lang in languages.lower() for lang in ['javascript', 'typescript', 'html', 'css']):
            categories.append('Web Development')
        
        # Mobile development
        if any(lang in languages.lower() for lang in ['swift', 'kotlin', 'dart']):
            categories.append('Mobile Development')
        
        # Data Science/ML
        if any(keyword in f"{name} {description} {readme_lower}" for keyword in 
               ['data', 'machine learning', 'ml', 'ai', 'analysis', 'visualization', 'pandas', 'numpy']):
            categories.append('Data Science/ML')
        
        # API/Backend
        if any(keyword in f"{name} {description} {readme_lower}" for keyword in 
               ['api', 'backend', 'server', 'database', 'microservice']):
            categories.append('API/Backend')
        
        # Tools/Utilities
        if any(keyword in f"{name} {description} {readme_lower}" for keyword in 
               ['tool', 'utility', 'script', 'automation', 'cli']):
            categories.append('Tools/Utilities')
        
        # Learning/Tutorial
        if any(keyword in f"{name} {description} {readme_lower}" for keyword in 
               ['tutorial', 'learning', 'practice', 'example', 'demo', 'course']):
            categories.append('Learning/Tutorial')
        
        return '; '.join(categories) if categories else 'Other'
    
    def scrape_to_csv(self, output_file='github_repositories.csv'):
        """Main method to scrape repositories and save to CSV"""
        print(f"Fetching repositories for user: {self.username}")
        repos = self.get_all_repositories()
        
        if not repos:
            print("No repositories found or error occurred")
            return
        
        print(f"Found {len(repos)} repositories. Processing...")
        
        # CSV headers
        fieldnames = [
            'name', 'description', 'readme_content', 'url', 'clone_url', 'ssh_url',
            'homepage', 'language', 'languages_used', 'stars', 'forks', 'watchers',
            'size_kb', 'created_at', 'updated_at', 'pushed_at', 'is_private', 
            'is_fork', 'is_archived', 'has_issues', 'has_wiki', 'has_pages',
            'open_issues_count', 'default_branch', 'category', 'topics'
        ]
        
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for i, repo in enumerate(repos, 1):
                print(f"Processing {i}/{len(repos)}: {repo['name']}")
                
                # Get additional data
                readme_content = self.get_readme_content(repo['name'])
                languages_used = self.get_languages(repo['name'])
                
                # Categorize repository
                category = self.categorize_repo(repo, readme_content, languages_used)
                
                # Prepare row data
                row_data = {
                    'name': repo['name'],
                    'description': repo.get('description') or '',
                    'readme_content': readme_content,
                    'url': repo['html_url'],
                    'clone_url': repo['clone_url'],
                    'ssh_url': repo['ssh_url'],
                    'homepage': repo.get('homepage') or '',
                    'language': repo.get('language') or '',
                    'languages_used': languages_used,
                    'stars': repo['stargazers_count'],
                    'forks': repo['forks_count'],
                    'watchers': repo['watchers_count'],
                    'size_kb': repo['size'],
                    'created_at': repo['created_at'],
                    'updated_at': repo['updated_at'],
                    'pushed_at': repo.get('pushed_at') or '',
                    'is_private': repo['private'],
                    'is_fork': repo['fork'],
                    'is_archived': repo['archived'],
                    'has_issues': repo['has_issues'],
                    'has_wiki': repo['has_wiki'],
                    'has_pages': repo['has_pages'],
                    'open_issues_count': repo['open_issues_count'],
                    'default_branch': repo['default_branch'],
                    'category': category,
                    'topics': ', '.join(repo.get('topics', []))
                }
                
                writer.writerow(row_data)
                
                # Be respectful to GitHub's API
                time.sleep(0.2)
        
        print(f"\nScraping completed! Data saved to {output_file}")
        print(f"Total repositories processed: {len(repos)}")

# Usage example
if __name__ == "__main__":
    # Read configuration from environment variables
    USERNAME = os.getenv('GITHUB_USERNAME')
    TOKEN = os.getenv('GITHUB_TOKEN')
    
    if not USERNAME:
        print("Error: GITHUB_USERNAME not found in environment variables.")
        print("Please create a .env file with your GitHub username.")
        exit(1)
    
    if not TOKEN:
        print("Warning: GITHUB_TOKEN not found. You'll have lower rate limits and can't access private repos.")
        print("Consider adding your personal access token to the .env file.")
    
    print(f"Starting scrape for user: {USERNAME}")
    
    # Create scraper instance
    scraper = GitHubRepoScraper(USERNAME, TOKEN)
    
    # Scrape repositories and save to CSV
    scraper.scrape_to_csv('my_github_repositories.csv')