"""
Smart Journalist Crew - CrewAI Implementation

This module defines the main crew orchestration for the Smart Journalist application.
It includes all agents, tasks, and the crew configuration.
"""

import os
import json
# from datetime import datetime
from typing import Dict, Any
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

class SmartJournalistCrew:
    """Smart Journalist CrewAI implementation."""

    def __init__(self):
        """Initialize the SmartJournalistCrew with LLM configuration."""

        file_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        # Load the JSON file
        with open(file_path, 'r') as file:
            vertex_credentials = json.load(file)

        # Convert the credentials to a JSON string
        vertex_credentials_json = json.dumps(vertex_credentials)

        # Configure Google Vertex AI Gemini LLM
        self.llm = LLM(
            model=os.getenv("MODEL_NAME", "vertex_ai/gemini-2.5-flash"),
            temperature=os.getenv("TEMPERATURE", 0.0),
            project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
            vertex_credentials=vertex_credentials_json,
        )
        
        # Use CrewAI built-in tools
        self.news_search_tool = SerperDevTool()
        self.web_scraper_tool = ScrapeWebsiteTool()

    def create_agents(self):
        """Create all specialized agents for the crew."""

        # Global News Agent
        global_news_agent = Agent(
            role='Global News Specialist',
            goal='Gather accurate, verified, and comprehensive global news across all specified categories with rigorous fact-checking',
            backstory="""You are an elite international news correspondent with 15 years of experience covering 
            global affairs. Your expertise spans geopolitics, international economics, global technology trends, 
            scientific breakthroughs, worldwide stock markets, energy sector developments, and infrastructure 
            projects. You have an exceptional ability to identify reliable sources, cross-verify information, 
            and present complex global events in clear, concise summaries. Your reputation is built on accuracy, 
            speed, and the ability to distinguish between verified facts and unconfirmed reports.
            
            TOOL USAGE RULES:
            - Use ONE tool at a time
            - Search for ONE category at a time. DO NOT search for multiple categories in one go.
            - Search for news using: {"search_query": "your search terms"}  
            - Read websites using: {"website_url": "https://example.com"}
            - NEVER use arrays or multiple inputs in Search/Read tool call
            - Complete one action, get result, then decide next action
            - NEVER repeat the same search query
            - If a search fails, try different keywords
            ERROR HANDLING:
            - If scraping returns "Please enable JS", "ad blocker", or similar errors, immediately stop scraping that URL
            - Use the search result snippet and title instead
            - Move on to next story quickly
            - Don't retry failed scrapes
            FALLBACK RULES:
            - If search says "reusing same input", change your search terms completely
            - Try: "tech news 3 Nov 2025", "technology updates today", "latest tech developments"
            - If 3 different searches fail, STOP and provide final answer
            - Never get stuck - always have an exit strategy
            COMPLETION CRITERIA:
            - Find 3 most important stories from ALL categories
            - Maximum 10 tool uses total before giving final answer
            """,
            verbose=True,
            allow_delegation=False,
            tools=[self.news_search_tool, self.web_scraper_tool],
            llm=self.llm,
            max_iter=10,  # ← Limit iterations
            max_execution_time=300  # ← 5 minute timeout
        )

        # India News Agent
        india_news_agent = Agent(
            role='India News Specialist',
            goal='Collect precise, fact-checked news specifically about India across all categories with emphasis on national significance',
            backstory="""You are a senior Indian news analyst with deep knowledge of India's political landscape, 
            economic policies, technological advancement, scientific research institutions, stock markets (NSE/BSE), 
            energy sector, and infrastructure development. You understand the nuances of Indian governance, 
            regulatory environment, and market dynamics. Your strength lies in identifying news that impacts 
            India nationally, verifying information through multiple Indian and international sources, and 
            presenting news with proper context about India's domestic and international implications.
            
            TOOL USAGE RULES:
            - Use ONE tool at a time
            - Search for ONE category at a time. DO NOT search for multiple categories in one go.
            - Search for news using: {"search_query": "your search terms"}  
            - Read websites using: {"website_url": "https://example.com"}
            - NEVER use arrays or multiple inputs in Search/Read tool call
            - Complete one action, get result, then decide next action
            - NEVER repeat the same search query
            - If a search fails, try different keywords
            ERROR HANDLING:
            - If scraping returns "Please enable JS", "ad blocker", or similar errors, immediately stop scraping that URL
            - Use the search result snippet and title instead
            - Move on to next story quickly
            - Don't retry failed scrapes
            FALLBACK RULES:
            - If search says "reusing same input", change your search terms completely
            - Try: "tech news 3 Nov 2025", "technology updates today", "latest tech developments"
            - If 3 different searches fail, STOP and provide final answer
            - Never get stuck - always have an exit strategy
            COMPLETION CRITERIA:
            - Find 3 most important stories from ALL categories
            - Maximum 10 tool uses total before giving final answer
            """,
            verbose=True,
            allow_delegation=False,
            tools=[self.news_search_tool, self.web_scraper_tool],
            llm=self.llm,
            max_iter=10,  # ← Limit iterations
            max_execution_time=300  # ← 5 minute timeout
        )

        # Ahmedabad News Agent
        ahmedabad_news_agent = Agent(
            role='Ahmedabad Local News Specialist',
            goal='Gather accurate local news about Ahmedabad city and Gujarat state with focus on regional impact and verification',
            backstory="""You are a local Ahmedabad journalist with intimate knowledge of Gujarat's business 
            ecosystem, political dynamics, infrastructure projects, and local governance. You specialize in 
            covering Ahmedabad's role as a major commercial hub, its textile and chemical industries, 
            infrastructure developments, local stock exchange activities, energy projects in Gujarat, 
            and technological initiatives. You have strong connections with local sources and the ability 
            to verify local news through multiple channels including government sources, business associations, 
            and community networks.
            
            TOOL USAGE RULES:
            - Use ONE tool at a time
            - Search for ONE category at a time. DO NOT search for multiple categories in one go.
            - Search for news using: {"search_query": "your search terms"}  
            - Read websites using: {"website_url": "https://example.com"}
            - NEVER use arrays or multiple inputs in Search/Read tool call
            - Complete one action, get result, then decide next action
            - NEVER repeat the same search query
            - If a search fails, try different keywords
            ERROR HANDLING:
            - If scraping returns "Please enable JS", "ad blocker", or similar errors, immediately stop scraping that URL
            - Use the search result snippet and title instead
            - Move on to next story quickly
            - Don't retry failed scrapes
            FALLBACK RULES:
            - If search says "reusing same input", change your search terms completely
            - Try: "tech news 3 Nov 2025", "technology updates today", "latest tech developments"
            - If 3 different searches fail, STOP and provide final answer
            - Never get stuck - always have an exit strategy
            COMPLETION CRITERIA:
            - Find 3 most important stories from ALL categories
            - Maximum 10 tool uses total before giving final answer
            """,
            verbose=True,
            allow_delegation=False,
            tools=[self.news_search_tool, self.web_scraper_tool],
            llm=self.llm,
            max_iter=10,  # ← Limit iterations
            max_execution_time=300  # ← 5 minute timeout
        )

        # Quality Assurance Agent
        quality_assurance_agent = Agent(
            role='News Verification and Quality Assurance Specialist',
            goal='Rigorously verify all collected news for accuracy, reliability, and credibility while filtering out misinformation',
            backstory="""You are a fact-checking expert with advanced training in information verification, 
            source credibility assessment, and misinformation detection. You have worked with leading 
            fact-checking organizations and have expertise in cross-referencing information across multiple 
            sources, evaluating source reliability, detecting potential bias, and identifying unverified claims. 
            Your systematic approach includes checking publication credibility, author expertise, corroborating 
            evidence, and temporal accuracy. You maintain high standards for factual accuracy and are skilled 
            at distinguishing between verified facts, probable information, and unconfirmed reports.
            
            TOOL USAGE RULES:
            - Use ONE tool at a time
            - Search for ONE category at a time. DO NOT search for multiple categories in one go.
            - Search for news using: {"search_query": "your search terms"}  
            - Read websites using: {"website_url": "https://example.com"}
            - NEVER use arrays or multiple inputs in Search/Read tool call
            - Complete one action, get result, then decide next action
            - NEVER repeat the same search query
            - If a search fails, try different keywords
            ERROR HANDLING:
            - If scraping returns "Please enable JS", "ad blocker", or similar errors, immediately stop scraping that URL
            - Use the search result snippet and title instead
            - Move on to next story quickly
            - Don't retry failed scrapes
            FALLBACK RULES:
            - If 3 different searches fail, STOP and provide final answer
            - Never get stuck - always have an exit strategy
            COMPLETION CRITERIA:
            - Find 3 most important stories from ALL categories
            - Maximum 10 tool uses total before giving final answer
            """,
            verbose=True,
            allow_delegation=False,
            tools=[self.news_search_tool, self.web_scraper_tool],
            llm=self.llm,
            max_iter=10,  # ← Limit iterations
            max_execution_time=300  # ← 5 minute timeout
        )

        # Reporting Agent
        reporting_agent = Agent(
            role='Executive News Reporting Specialist',
            goal='Organize verified news into a structured, professional HTML report with clear categorization and reliability indicators',
            backstory="""You are a senior news editor and report compiler with expertise in digital publishing 
            and information architecture. You specialize in creating clear, well-organized news presentations 
            that serve busy executives and decision-makers. Your strength lies in structuring information 
            hierarchically, creating intuitive navigation, highlighting key insights, and presenting complex 
            information in digestible formats. You understand the importance of source attribution, reliability 
            indicators, and professional presentation standards. Your reports are known for their clarity, 
            completeness, and actionable insights.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=10,  # ← Limit iterations
            max_execution_time=300  # ← 5 minute timeout
        )

        return {
            'global_news': global_news_agent,
            'india_news': india_news_agent,
            'ahmedabad_news': ahmedabad_news_agent,
            'quality_assurance': quality_assurance_agent,
            'reporting': reporting_agent
        }

    def create_tasks(self, agents: Dict[str, Agent]):
        """Create all tasks for the crew."""

        # Global News Collection Task
        global_news_task = Task(
            description="""Collect comprehensive global news for today ({date}) across these categories:
            {categories}

            REQUIREMENTS:
            1. Search for the latest global news in each category
            2. Focus on significant international developments
            3. Prioritize news from reputable international sources (Reuters, BBC, AP, Bloomberg, etc.)
            4. For each news item, gather:
               - Headline
               - Key details and summary
               - Source publication and URL
               - Publication timestamp
               - Geographic relevance
            5. Ensure coverage spans different regions (US, Europe, Asia, etc.)
            6. Verify information through multiple sources where possible
            7. Flag any breaking or developing stories

            CRITICAL: Only include news that can be verified through credible sources.
            Exclude opinion pieces, rumors, or unconfirmed reports unless marked as "developing" or "unverified".""",
            expected_output="""A comprehensive collection of global news organized by category:

            Format for each news item:
            - Category: {categories}
            - Headline: [Clear, factual headline]
            - Summary: [2-3 sentence summary with key facts]
            - Source: [Publication name and credibility level]
            - URL: [Direct link to article]
            - Timestamp: [Publication time]
            - Verification Status: [Verified/Developing/Unverified]
            - Geographic Focus: [Primary regions/countries affected]

            Aim for 3-5 significant news items per category, totaling 20-35 items.""",
            agent=agents['global_news'],
            output_file="output/global_news_raw.md"
        )

        # India News Collection Task
        india_news_task = Task(
            description="""Collect comprehensive India-specific news for today ({date}) across these categories:
            {categories}

            REQUIREMENTS:
            1. Search for news specifically related to India in each category
            2. Include domestic developments and India's international relations
            3. Focus on sources like Economic Times, Hindu, Times of India, Mint, Business Standard, etc.
            4. For each news item, gather:
               - Headline with India context
               - Detailed summary with national implications
               - Source publication and URL
               - Publication timestamp
               - Regional/state relevance within India
            5. Prioritize news affecting India's economy, policy, or international standing
            6. Include relevant stock market news (NSE/BSE)
            7. Cross-verify through multiple Indian news sources

            CRITICAL: Focus on news with direct relevance to India. 
            Verify all information and mark confidence levels.""",
            expected_output="""A comprehensive collection of India-specific news organized by category:

            Format for each news item:
            - Category: {categories}
            - Headline: [Clear headline emphasizing India relevance]
            - Summary: [2-3 sentences highlighting impact on India]
            - Source: [Indian publication name and credibility]
            - URL: [Direct link to article]
            - Timestamp: [Publication time]
            - Verification Status: [Verified/Developing/Unverified]
            - India Impact: [National/Regional/International implications]
            - Related States/Sectors: [If applicable]

            Target 2-4 significant news items per category, totaling 15-25 items.""",
            agent=agents['india_news'],
            output_file="output/india_news_raw.md",
            context=[global_news_task]
        )

        # Ahmedabad News Collection Task
        ahmedabad_news_task = Task(
            description="""Collect local news for Ahmedabad and Gujarat for today ({date}) across relevant categories:
            {categories}

            REQUIREMENTS:
            1. Search for news specifically about Ahmedabad city and Gujarat state
            2. Include business developments, infrastructure projects, local governance
            3. Focus on local sources: Times of India Ahmedabad, Gujarat Samachar, Divya Bhaskar, etc.
            4. For each news item, gather:
               - Headline with local context
               - Summary with local implications
               - Source publication and URL
               - Publication timestamp
               - Specific area/district relevance
            5. Include relevant local business and infrastructure news
            6. Cover developments in textile, chemical, pharmaceutical industries
            7. Verify through local sources and government releases

            FOCUS AREAS:
            - Ahmedabad Municipal Corporation developments
            - Gujarat state government initiatives
            - Local business and industry news
            - Infrastructure and urban development
            - Educational and research institution updates""",
            expected_output="""A collection of Ahmedabad/Gujarat news organized by relevant categories:

            Format for each news item:
            - Category: {categories}
            - Headline: [Clear headline with local context]
            - Summary: [2-3 sentences highlighting local impact]
            - Source: [Local publication name]
            - URL: [Direct link to article]
            - Timestamp: [Publication time]
            - Verification Status: [Verified/Developing/Unverified]
            - Local Relevance: [Ahmedabad/Gujarat/Regional impact]
            - Area/District: [Specific location if applicable]

            Target 1-2 news items per relevant category, totaling 8-15 items.""",
            agent=agents['ahmedabad_news'],
            output_file="output/ahmedabad_news_raw.md",
            context=[global_news_task, india_news_task]
        )

        # Quality Assurance Task
        quality_assurance_task = Task(
            description="""Perform comprehensive fact-checking and quality assurance on all collected news items.

            VERIFICATION PROCESS:
            1. Review all news items from Global, India, and Ahmedabad agents
            2. For each news item, assess:
               - Source credibility and track record
               - Information accuracy through cross-referencing
               - Potential bias or misleading information
               - Completeness and clarity of reporting
               - Temporal accuracy (ensure news is current)

            QUALITY STANDARDS:
            - Verify claims through at least 2 independent sources
            - Check source publication's reputation and reliability
            - Identify any potential conflicts of interest
            - Flag unverified or developing stories appropriately
            - Remove or mark questionable or unreliable information
            - Ensure geographical and temporal accuracy

            RELIABILITY CLASSIFICATION:
            - HIGH: Verified by multiple credible sources
            - MEDIUM: Single credible source, corroborating evidence
            - LOW: Unverified but from credible source
            - UNVERIFIED: Developing story or single unconfirmed source
            - EXCLUDE: Unreliable, biased, or false information""",
            expected_output="""Quality-assured news collection with reliability assessments:

            For each verified news item:
            - Original Information: [All original details]
            - Reliability Score: [HIGH/MEDIUM/LOW/UNVERIFIED]
            - Verification Notes: [Sources checked, corroboration found]
            - Source Credibility: [Assessment of original source]
            - Recommendation: [INCLUDE/INCLUDE_WITH_WARNING/EXCLUDE]
            - Quality Notes: [Any concerns or additional context]

            EXCLUDED ITEMS:
            - List of excluded items with reasons
            - Source credibility issues identified
            - Misinformation or bias detected

            SUMMARY STATISTICS:
            - Total items reviewed: [number]
            - Items verified and included: [number]
            - Items flagged as unverified: [number]
            - Items excluded: [number]""",
            agent=agents['quality_assurance'],
            context=[global_news_task, india_news_task, ahmedabad_news_task],
            output_file="output/quality_assurance_report.md"
        )

        # Final Reporting Task
        reporting_task = Task(
            description="""Create a comprehensive, professional HTML news report organizing all verified news.

            ORGANIZATION STRUCTURE:
            1. Create three main regional sections: Global, India, Ahmedabad
            2. Within each region, organize by categories: 
               {categories}
            3. For each news item, create a professional news card showing:
               - Clear headline
               - Concise summary (2-3 sentences)
               - Source with credibility indicator
               - Publication timestamp
               - Reliability badge (Verified/Unverified/Developing)
               - Direct source link

            DESIGN REQUIREMENTS:
            - Clean, professional layout with responsive design
            - Color-coded reliability indicators (Green=Verified, Yellow=Developing, Orange=Unverified)
            - Easy navigation between regions and categories
            - Professional typography and spacing
            - Clear visual hierarchy
            - Source attribution for all items

            HTML STRUCTURE:
            - Header with title and generation timestamp
            - Navigation menu for regions
            - Tabbed or sectioned category organization
            - News cards with hover effects
            - Footer with methodology and disclaimer""",
            expected_output="""A complete, professional HTML report saved as 'output/news_report_{date}.html' containing:

            1. DOCUMENT STRUCTURE:
               - Professional header with app title and date
               - Executive summary of news coverage
               - Navigation between regions and categories
               - Responsive news card layout
               - Professional footer

            2. CONTENT ORGANIZATION:
               - Global News Section (with category subsections)
               - India News Section (with category subsections)
               - Ahmedabad News Section (with category subsections)
               - Each news item as a styled card with all required information

            3. QUALITY INDICATORS:
               - Visual reliability badges
               - Source credibility markers
               - Clear distinction between verified and unverified news
               - Timestamp and freshness indicators

            4. METADATA:
               - Total news items processed
               - Coverage statistics by region and category
               - Quality assurance summary
               - Generation methodology

            The report should be immediately readable and suitable for executive review.""",
            agent=agents['reporting'],
            context=[quality_assurance_task],
            output_file="output/final_news_report.html"
        )

        return [global_news_task, india_news_task, ahmedabad_news_task, 
                quality_assurance_task, reporting_task]

    def crew(self) -> Crew:
        """Create and return the configured crew."""

        agents = self.create_agents()
        tasks = self.create_tasks(agents)
        
        # for agent in agents.values():
        #     if not getattr(agent.llm, 'model', '').startswith('vertex_ai'):
        #         raise RuntimeError(f"Agent {agent.role} is not using Vertex AI LLM!")

        return Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
            # memory=True,
            # planning=True,
            # embedder={
                # "provider": "huggingface",
                # "config": {
                    # "model": "sentence-transformers/all-MiniLM-L6-v2"
                # }
                
                # "provider": "google-vertex",
                # "config": {
                #     "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
                #     "region": os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
                #     "model_name": "textembedding-gecko"
                # }
            # },
            max_rpm=60,  # ← Request Rate limiting to LLM per minute
        )
