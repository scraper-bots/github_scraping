# 🔍 GitHub Repository Scraper

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub API](https://img.shields.io/badge/GitHub%20API-v3-green.svg)](https://docs.github.com/en/rest)

A comprehensive Python tool for scraping and analyzing GitHub repositories. This scraper extracts detailed information about all repositories for a given user, including README content, programming languages, repository statistics, and automatically categorizes projects.

## 🌟 Features

### 📊 **Comprehensive Data Extraction**
- **Repository Metadata**: Stars, forks, watchers, size, creation dates
- **Content Analysis**: README content extraction and cleaning
- **Language Detection**: Primary and all programming languages used
- **Repository Settings**: Privacy, fork status, issues, wiki, pages
- **Topics & Categories**: Automatic categorization and topic extraction

### 🤖 **Intelligent Categorization**
Automatically categorizes repositories into:
- **Web Development** (JavaScript, TypeScript, HTML, CSS)
- **Mobile Development** (Swift, Kotlin, Dart)
- **Data Science/ML** (Python, R, Jupyter notebooks)
- **API/Backend** (Server-side applications, databases)
- **Tools/Utilities** (Scripts, automation, CLI tools)
- **Learning/Tutorial** (Educational content, examples)

### 🚀 **Advanced Features**
- **Rate Limiting**: Respectful API usage with built-in delays
- **Error Handling**: Robust error handling for API failures
- **README Processing**: Smart content extraction and cleaning
- **CSV Export**: Clean, structured data export
- **Token Support**: Optional GitHub token for higher rate limits

## 📋 Requirements

- Python 3.7+
- GitHub account
- Personal Access Token (recommended for better rate limits)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Ismat-Samadov/github_scraping.git
cd github_scraping
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root:
```env
GITHUB_USERNAME=your_github_username
GITHUB_TOKEN=your_personal_access_token
```

## 🔑 GitHub Token Setup

### Why Use a Token?
- **Higher Rate Limits**: 5,000 requests/hour vs 60 requests/hour
- **Private Repositories**: Access to your private repos
- **Better Reliability**: Reduced chance of hitting rate limits

### How to Create a Token:
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes:
   - `public_repo` (for public repositories)
   - `repo` (for private repositories access)
4. Copy the token and add it to your `.env` file

## 🚀 Usage

### Basic Usage
```python
from github_scraper import GitHubRepoScraper

# Initialize scraper
scraper = GitHubRepoScraper('your_username', 'your_token')

# Scrape all repositories and save to CSV
scraper.scrape_to_csv('my_repositories.csv')
```

### Command Line Usage
```bash
python github_scraper.py
```

### Advanced Usage
```python
# Custom output file
scraper.scrape_to_csv('custom_output.csv')

# Get specific data
repos = scraper.get_all_repositories()
readme = scraper.get_readme_content('repository_name')
languages = scraper.get_languages('repository_name')
```

## 📊 Output Format

The scraper generates a CSV file with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `name` | Repository name | `github_scraping` |
| `description` | Repository description | `GitHub repositories scraping` |
| `readme_content` | First 500 chars of README | `This project implements...` |
| `url` | Repository URL | `https://github.com/user/repo` |
| `clone_url` | HTTPS clone URL | `https://github.com/user/repo.git` |
| `ssh_url` | SSH clone URL | `git@github.com:user/repo.git` |
| `homepage` | Project homepage | `https://example.com` |
| `language` | Primary language | `Python` |
| `languages_used` | All languages | `Python, JavaScript, HTML` |
| `stars` | Star count | `42` |
| `forks` | Fork count | `5` |
| `watchers` | Watcher count | `42` |
| `size_kb` | Repository size in KB | `1024` |
| `created_at` | Creation date | `2023-01-01T12:00:00Z` |
| `updated_at` | Last update | `2023-12-01T12:00:00Z` |
| `pushed_at` | Last push | `2023-12-01T12:00:00Z` |
| `is_private` | Private repository | `False` |
| `is_fork` | Is a fork | `False` |
| `is_archived` | Archived status | `False` |
| `has_issues` | Has issues enabled | `True` |
| `has_wiki` | Has wiki enabled | `True` |
| `has_pages` | Has GitHub Pages | `False` |
| `open_issues_count` | Open issues count | `3` |
| `default_branch` | Default branch | `main` |
| `category` | Auto-generated category | `Data Science/ML` |
| `topics` | Repository topics | `python, scraping, api` |

## 🏗️ Project Structure

```
github_scraping/
├── github_scraper.py          # Main scraper class
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables (create this)
├── .gitignore               # Git ignore file
├── LICENSE                  # MIT License
├── README.md               # This file
├── index.md               # Project portfolio index
└── my_github_repositories.csv # Example output
```

## ⚙️ Configuration

### Environment Variables
- `GITHUB_USERNAME`: Your GitHub username (required)
- `GITHUB_TOKEN`: Personal access token (optional but recommended)

### Customization Options
- **Rate Limiting**: Adjust `time.sleep()` values in the code
- **README Length**: Modify the 500-character limit
- **Categories**: Customize categorization logic in `categorize_repo()`
- **Output Fields**: Add/remove CSV columns as needed

## 🔧 API Rate Limits

### Without Token
- **60 requests per hour** per IP address
- **Public repositories only**

### With Token
- **5,000 requests per hour** per token
- **Access to private repositories**
- **Higher success rate**

### Rate Limiting Strategy
The scraper implements several strategies to respect GitHub's API limits:
- Built-in delays between requests (0.1-0.2 seconds)
- Progressive backoff on rate limit errors
- Efficient API usage patterns

## 🎯 Use Cases

### 📈 **Portfolio Analysis**
- Analyze your coding journey over time
- Identify your most popular projects
- Track repository growth and engagement

### 🔍 **Project Discovery**
- Find repositories by category or language
- Discover forgotten or underutilized projects
- Identify candidates for archival or cleanup

### 📊 **Analytics & Reporting**
- Generate repository statistics
- Create development timelines
- Analyze programming language usage

### 🏢 **Organization Management**
- Audit team repositories
- Track project compliance
- Monitor repository standards

## 🚨 Error Handling

The scraper includes comprehensive error handling:
- **API Rate Limits**: Automatic detection and graceful handling
- **Network Issues**: Retry logic with exponential backoff
- **Missing Content**: Fallback values for missing README files
- **Invalid Responses**: Proper error logging and continuation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Include error handling for external API calls
- Write descriptive commit messages

## 🐛 Troubleshooting

### Common Issues

**Rate Limit Exceeded**
```
Solution: Add a GitHub token or wait for the rate limit to reset
```

**Empty README Content**
```
Cause: Repository doesn't have a README file
Result: "No README found" will be recorded
```

**Authentication Failed**
```
Solution: Check your GitHub token permissions and validity
```

**Network Timeouts**
```
Solution: Check internet connection and GitHub API status
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- GitHub API for providing comprehensive repository data
- Python `requests` library for HTTP functionality
- The open-source community for inspiration and feedback

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review GitHub API documentation

---

**Happy Scraping! 🚀**

*Last updated: December 2024*
