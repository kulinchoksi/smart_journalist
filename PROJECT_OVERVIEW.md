# Smart and Wise Journalist App - CrewAI Implementation

## Overview
This is a comprehensive CrewAI-based news gathering and verification system that collects, processes, verifies, and organizes news across multiple regions (Global, India, Ahmedabad) and categories (Geopolitical, Economy, Technology, Science, Stock Market, Energy, Infrastructure).

## Project Structure
```
smart_journalist/
├── .env                              # Environment variables
├── pyproject.toml                    # Project dependencies
├── README.md                         # Project documentation
├── requirements.txt                  # Python dependencies
├── main.py                          # Main application entry point
├── src/
│   └── smart_journalist/
│       ├── __init__.py
│       ├── crew.py                  # Main crew orchestration
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── news_search_tool.py  # SerplyNewsSearchTool wrapper
│       │   └── web_scraper_tool.py  # FirecrawlScrapeWebsiteTool wrapper
│       ├── config/
│       │   ├── agents.yaml          # Agent configurations
│       │   └── tasks.yaml           # Task configurations
│       ├── prompts/
│       │   ├── __init__.py
│       │   └── verification_prompts.py # Quality assurance prompts
│       └── templates/
│           └── news_report.html     # HTML template for final output
└── output/                          # Generated reports directory
```

## Features
- **Multi-Region Coverage**: Global, India, and Ahmedabad local news
- **Category Specialization**: 7 key domains (Geopolitical, Economy, Technology, Science, Stock Market, Energy, Infrastructure)
- **Quality Assurance**: Dedicated fact-checking and reliability verification
- **Smart Organization**: Structured news cards with headlines, summaries, sources, and reliability indicators
- **HTML Output**: Professional, easy-to-read layout saved as HTML file
- **Vertex AI Integration**: Uses Google Gemini-2.5-pro with temperature 0.0 for maximum reliability

## Key Agents
1. **Global News Agent**: Specializes in international news across all categories
2. **India News Agent**: Focuses on Indian national news
3. **Ahmedabad News Agent**: Covers local Ahmedabad news
4. **Quality Assurance Agent**: Verifies facts and cross-checks reliability
5. **Reporting Agent**: Organizes and formats final output

## Installation & Setup

### Prerequisites
- Python 3.9+
- Google Cloud Service Account with Vertex AI access
- Serper API Key (for news search)
- Firecrawl API Key (for web scraping)

### Environment Setup
```bash
# Clone or create project directory
mkdir smart_journalist
cd smart_journalist

# Install dependencies
pip install -r requirements.txt

# Set up environment variables in .env file
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
SERPER_API_KEY=your-serper-api-key
FIRECRAWL_API_KEY=your-firecrawl-api-key
```

### Run Application
```bash
# Execute the main application
python main.py

# Or using CrewAI CLI (if using CrewAI project structure)
crewai run
```

## Configuration

### Agent Configuration (agents.yaml)
Each agent has specialized prompts for their region/category focus with emphasis on:
- Fact-checking and verification
- Source reliability assessment
- Concise, accurate reporting
- Cross-referencing multiple sources

### Task Configuration (tasks.yaml)
Sequential task execution:
1. News gathering by region-specific agents
2. Quality assurance and fact-checking
3. Final report organization and HTML generation

## Output
The application generates:
- **HTML Report**: Professional layout with news cards organized by region and category
- **Reliability Indicators**: Clear marking of verified vs unverified news
- **Source Links**: Direct links to original news sources
- **Summary Information**: Concise headlines and descriptions

## Technical Implementation
- **LLM**: Google Vertex AI Gemini-2.5-pro (temperature=0.0)
- **News Search**: SerplyNewsSearchTool for real-time news gathering
- **Web Scraping**: FirecrawlScrapeWebsiteTool for content extraction
- **Quality Assurance**: Custom verification prompts with multi-source validation
- **Output Format**: Responsive HTML with CSS styling for optimal readability

## Deployment
The application is designed for easy deployment on any hosting service supporting Python applications. All dependencies are clearly specified and the modular structure allows for easy customization and scaling.

## Daily Operation
By default, the application processes current day's news. It can be scheduled to run automatically using cron jobs or task schedulers to provide daily news reports.

## Quality Assurance Process
1. **Multi-source Verification**: Each news item is cross-checked against multiple sources
2. **Reliability Scoring**: Sources are rated based on credibility
3. **Fact Validation**: Claims are verified through authoritative sources
4. **Unverified Labeling**: Critical but unverified news is clearly marked
5. **Source Filtering**: Unreliable or spam sources are excluded