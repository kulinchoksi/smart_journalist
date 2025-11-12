# Implementation Guide: Pydantic Structured Output + Jinja2 Templates

## 📋 Overview

This implementation provides **100% consistent HTML output** by separating data generation from presentation using:
- **Pydantic Models** for structured data validation
- **Jinja2 Templates** for consistent HTML rendering

## 🗂️ File Structure

```
src/smart_journalist/
├── models.py                      # ← NEW: Pydantic data models
├── renderer.py                    # ← NEW: HTML renderer with Jinja2
├── crew.py                        # ← UPDATE: Add structured output
├── config/
│   ├── agents.yaml               # ← NO CHANGE
│   └── tasks.yaml                # ← UPDATE: final_news_report task
├── templates/
│   └── news_report_template.html # ← NEW: Jinja2 HTML template
└── output/
    ├── final_news_report.json    # ← NEW: Structured JSON output
    └── final_news_report.html    # ← Generated HTML
```

## 🚀 Implementation Steps

### Step 1: Add New Files

**1.1 Create `src/smart_journalist/models.py`**
- Copy content from [33] models.py
- Defines Pydantic schemas for NewsReport, NewsStory, etc.

**1.2 Create `src/smart_journalist/renderer.py`**
- Copy content from [35] renderer.py
- Handles Jinja2 template rendering

**1.3 Create `src/smart_journalist/templates/news_report_template.html`**
- Copy content from [34] news_report_template.html
- Professional HTML template based on your existing design
- Includes: Source links, metadata footer, regional tabs

### Step 2: Update Configuration

**2.1 Update `src/smart_journalist/config/tasks.yaml`**

Replace the `final_news_report` task section with:

```yaml
final_news_report:
  description: >
    Organize all verified news into a STRUCTURED JSON format.
    
    CRITICAL: Output data in Pydantic schema format. Do NOT generate HTML directly.
    
    DATA REQUIREMENTS:
    1. Executive Summary (3-5 paragraphs)
    2. Featured Stories (5-10 top stories with full details including source URLs)
    3. Regional Organization (World/India/Ahmedabad)
       - Each region has categories with stories
       - Each story needs: headline, summary, source, source_url, category, region, 
         verification_status, confidence_score, timestamp
    4. Metadata (statistics, models used, execution time)
    
    Extract source URLs from verification reports and search results.
    
  expected_output: >
    Complete NewsReport JSON object with all required fields.
    See updated_tasks_config.yaml for detailed structure.
    
  agent: news_reporting_specialist
  context: [
    political_news_verification, 
    economy_news_verification, 
    technology_news_verification, 
    science_news_verification, 
    stock_market_news_verification, 
    energy_news_verification, 
    infrastructure_news_verification
  ]
  output_pydantic: NewsReport
  output_file: "output/final_news_report.json"
```

**Full task definition available in [36] updated_tasks_config.yaml**

### Step 3: Update crew.py

**3.1 Add imports at the top:**
```python
import time
from models import NewsReport
from renderer import NewsReportRenderer
```

**3.2 Update `__init__` method:**
```python
def __init__(self):
    # ... existing code ...
    
    # Add renderer initialization
    self.renderer = NewsReportRenderer(template_dir="src/smart_journalist/templates")
    self.start_time = None
```

**3.3 Update `final_news_report` task:**
```python
@task
def final_news_report(self) -> Task:
    """Creates the final news report task with structured output."""
    return Task(
        config=self.tasks_config['final_news_report'],
        agent=self.news_reporting_specialist(),
        output_pydantic=NewsReport,  # ← Add this line
        output_file="output/final_news_report.json"
    )
```

**3.4 Update `crew` method:**
```python
@crew
def crew(self) -> Crew:
    """Create and return the configured crew."""
    self.start_time = time.time()  # ← Add this line
    
    # ... rest of existing code ...
```

**3.5 Add new method `kickoff_and_render`:**
```python
def kickoff_and_render(self) -> tuple[Any, str]:
    """Execute crew and render HTML report."""
    print("🚀 Starting Smart Journalist Crew execution...")
    
    try:
        # Execute crew
        crew_instance = self.crew()
        result = crew_instance.kickoff()
        
        # Calculate execution time
        execution_time = int(time.time() - self.start_time) if self.start_time else None
        
        # Extract structured output
        if hasattr(result, 'pydantic'):
            report_data = result.pydantic
        elif isinstance(result, NewsReport):
            report_data = result
        else:
            report_data = NewsReport.model_validate_json(result)
        
        # Update metadata
        if execution_time:
            report_data.metadata.execution_time_seconds = execution_time
        
        print(f"✅ Collected {report_data.metadata.total_stories_collected} stories")
        
        # Render to HTML
        output_path = f"output/final_news_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        self.renderer.render(report_data, output_file=output_path)
        
        print(f"✅ HTML report: {output_path}")
        return result, output_path
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
```

**3.6 Update `main()` function:**
```python
def main():
    # ... existing setup ...
    
    try:
        crew_instance = SmartJournalistCrew()
        result, html_path = crew_instance.kickoff_and_render()  # ← Changed
        
        print(f"📄 JSON: output/final_news_report.json")
        print(f"🌐 HTML: {html_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
```

**Complete updated crew.py available in [37] crew_updated.py**

### Step 4: Update Dependencies

**Add to `requirements.txt`:**
```txt
# Existing dependencies
crewai>=1.3.0
crewai-tools>=1.3.0
# ... other existing dependencies ...

# NEW: Add these
pydantic>=2.5.0
jinja2>=3.1.2
```

### Step 5: Test Implementation

**5.1 Test with sample data:**
```bash
# Run the sample in renderer.py
cd src/smart_journalist
python renderer.py
```

**5.2 Run full application:**
```bash
python main.py
```

## ✅ Expected Results

### Before (Current):
- ❌ Different HTML layout each execution
- ❌ Inconsistent styling
- ❌ Missing source links
- ❌ No metadata footer

### After (With This Implementation):
- ✅ **100% Consistent HTML layout** every time
- ✅ Professional styling with tabs and cards
- ✅ **Clickable source links** on headlines and source names
- ✅ **Comprehensive metadata footer** with statistics
- ✅ Color-coded verification badges
- ✅ Confidence score indicators
- ✅ Responsive design
- ✅ Regional navigation tabs

## 📊 Output Files

**JSON Output (`output/final_news_report.json`):**
```json
{
  "title": "Daily News Report",
  "generation_date": "2025-11-10",
  "executive_summary": "...",
  "featured_stories": [...],
  "world_news": {...},
  "india_news": {...},
  "ahmedabad_news": {...},
  "metadata": {
    "generation_date": "2025-11-10 21:30:00",
    "total_stories_collected": 42,
    "total_stories_verified": 38,
    "llm_model_used": "vertex_ai/gemini-1.5-flash",
    "verification_model_used": "vertex_ai/gemini-2.5-pro"
  }
}
```

**HTML Output (`output/final_news_report_YYYYMMDD_HHMMSS.html`):**
- Professional news report with consistent layout
- Regional tabs (World, India, Ahmedabad)
- Category sections within each region
- Clickable source links
- Verification badges
- Metadata footer

## 🔧 Customization

### Modify HTML Template
Edit `src/smart_journalist/templates/news_report_template.html`:
- Change colors, fonts, layout
- Add new sections
- Modify styling

### Modify Data Schema
Edit `src/smart_journalist/models.py`:
- Add new fields to NewsStory
- Add new categories
- Modify metadata structure

### Modify Rendering Logic
Edit `src/smart_journalist/renderer.py`:
- Add custom Jinja2 filters
- Add data preprocessing
- Add multiple template support

## ⚠️ Important Notes

1. **LLM Must Follow Schema**: The reporting agent must output data matching the Pydantic schema
2. **Source URLs Required**: Verification tasks must preserve source URLs
3. **Template Location**: Template must be in `src/smart_journalist/templates/`
4. **Output Directory**: Ensure `output/` and `templates/` directories exist

## 🐛 Troubleshooting

**Problem**: "Template not found"
- **Solution**: Check `template_dir` path in renderer initialization

**Problem**: Pydantic validation error
- **Solution**: Check that LLM output matches NewsReport schema exactly

**Problem**: Missing source URLs
- **Solution**: Update verification tasks to extract and preserve URLs

**Problem**: JSON parsing error
- **Solution**: Check `output_pydantic=NewsReport` is set in task

## 📚 Benefits Summary

1. ✅ **100% Consistent** - Same HTML structure every execution
2. ✅ **Maintainable** - Separate data from presentation
3. ✅ **Validated** - Pydantic ensures data quality
4. ✅ **Flexible** - Easy to add new formats (PDF, email, etc.)
5. ✅ **Professional** - Clean, modern HTML design
6. ✅ **Source Attribution** - All links properly included
7. ✅ **Metadata Tracking** - Comprehensive execution statistics

## 🎉 Result

Every execution produces **identical HTML layout** with only the content changing - exactly what you wanted!