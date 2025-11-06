#!/usr/bin/env python3
"""
Smart and Wise Journalist App - Main Entry Point

This is the main entry point for the Smart Journalist application.
It initializes and runs the CrewAI crew for news gathering and verification.
"""

import os
import sys
import signal
from datetime import datetime
from dotenv import load_dotenv
from src.smart_journalist.crew import SmartJournalistCrew

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Crew execution timeout")

def main():
    """Main entry point for the Smart Journalist application."""
    
    # Load environment variables
    load_dotenv()

    print("🚀 Starting Smart and Wise Journalist App...")
    print("=" * 60)

    # Verify environment variables
    required_env_vars = [
        "GOOGLE_CLOUD_PROJECT",
        "SERPER_API_KEY",
        "FIRECRAWL_API_KEY"
    ]

    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease check your .env file and ensure all variables are set.")
        sys.exit(1)

    try:
        # Initialize the crew
        crew_instance = SmartJournalistCrew()

        # Prepare inputs for the crew
        current_date = datetime.now().strftime("%Y-%m-%d")
        inputs = {
            "date": current_date,
            "regions": ["Global", "India", "Ahmedabad"],
            "categories": [
                "Geopolitical", "Economy", "Technology", 
                "Science", "Stock Market", "Energy", "Infrastructure"
            ]
        }

        print(f"📅 Processing news for: {current_date}")
        print(f"🌍 Regions: {', '.join(inputs['regions'])}")
        print(f"📂 Categories: {', '.join(inputs['categories'])}")
        print("=" * 60)

        # Print agent and LLM details before kickoff
        # agents = crew_instance.create_agents()
        # for name, agent in agents.items():
        #     print(f"Agent '{name}': role={agent.role}, LLM={getattr(agent.llm, 'model', None)}")

        import traceback
        try:
            # Set 25 minute timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(1500)  # 25 minutes

            # Execute the crew
            result = crew_instance.crew().kickoff(inputs=inputs)

            signal.alarm(0)  # Cancel timeout

            print("\n✅ News processing completed successfully!")
            print(f"📄 Report saved to: output/news_report_{current_date}.html")
            print("=" * 60)

            return result
        except TimeoutException:
            print("⏰ TIMEOUT: Crew took too long, stopping execution")
            print("💡 Try simplifying your task or reducing scope")
            return
        except Exception as e:
            print(f"❌ Error occurred: {str(e)}")
            traceback.print_exc()
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
