# Inside container - test latest version upgrade
python -c "
import os

print('=== TESTING LATEST CREWAI VERSIONS ===')
print()

# Test 1: Check versions
try:
    import crewai
    import crewai_tools
    print(f'✅ CrewAI: {crewai.__version__}')
    print(f'✅ CrewAI-tools: {crewai_tools.__version__}')
except Exception as e:
    print(f'❌ Version check failed: {e}')
    exit()

print()

# Test 2: Import tools
try:
    from crewai_tools import SerperDevTool, ScrapeWebsiteTool
    print('✅ Built-in tools imported successfully')
except Exception as e:
    print(f'❌ Tool import failed: {e}')
    exit()

print()

# Test 3: Create tools
try:
    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()
    print('✅ Built-in tools created successfully')
except Exception as e:
    print(f'❌ Tool creation failed: {e}')
    exit()

print()

# Test 4: LLM creation
try:
    from crewai import LLM
    import json
    
    file_path='.secrets/bro-sha-prj-logic-1-672cc2296de1.json'
    # Load the JSON file
    with open(file_path, 'r') as file:
        vertex_credentials = json.load(file)

    # Convert the credentials to a JSON string
    vertex_credentials_json = json.dumps(vertex_credentials)
    
    llm = LLM(
        model='vertex_ai/gemini-2.5-flash',
        temperature=0.0,
        project=os.getenv('GOOGLE_CLOUD_PROJECT'),
        location=os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1'),
        vertex_credentials=vertex_credentials_json,
    )
    print('✅ LLM created successfully')
except Exception as e:
    print(f'❌ LLM creation failed: {e}')
    exit()

print()

# Test 5: Agent creation
try:
    from crewai import Agent
    agent = Agent(
        role='Test Agent',
        goal='Test functionality',
        backstory='Testing agent creation',
        tools=[search_tool, scrape_tool],
        llm=llm,
        verbose=True
    )
    print('✅ Agent created successfully')
except Exception as e:
    print(f'❌ Agent creation failed: {e}')
    exit()

print()
print('🎉 ALL TESTS PASSED - Latest versions are compatible!')
print('✅ Ready to use built-in tools in your crew.py')
"
