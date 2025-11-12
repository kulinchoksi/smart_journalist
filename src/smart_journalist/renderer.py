"""
HTML Report Renderer using Jinja2 Template
Converts structured Pydantic data to consistent HTML reports
"""

import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path
from typing import Union

from .models import NewsReport


class NewsReportRenderer:
    """Renders structured news data to HTML using Jinja2 templates."""
    
    def __init__(self, template_dir: str = "templates"):
        """
        Initialize the renderer with template directory.
        
        Args:
            template_dir: Directory containing Jinja2 templates
        """
        self.template_dir = Path(template_dir)
        
        # Create template directory if it doesn't exist
        self.template_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=True,  # Auto-escape HTML for security
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['format_date'] = self._format_date
        self.env.filters['format_confidence'] = self._format_confidence
        
    def _format_date(self, date_string: str) -> str:
        """Format date string for display."""
        try:
            date_obj = datetime.fromisoformat(date_string)
            return date_obj.strftime("%B %d, %Y %I:%M %p")
        except:
            return date_string
    
    def _format_confidence(self, score: int) -> str:
        """Format confidence score with visual indicator."""
        if score >= 8:
            return f"High ({score}/10)"
        elif score >= 5:
            return f"Medium ({score}/10)"
        else:
            return f"Low ({score}/10)"
    
    def render(
        self, 
        report_data: Union[NewsReport, dict],
        template_name: str = "news_report_template.html",
        output_file: str = None
    ) -> str:
        """
        Render news report to HTML.
        
        Args:
            report_data: NewsReport Pydantic model or dict
            template_name: Name of the Jinja2 template file
            output_file: Optional path to save rendered HTML
            
        Returns:
            Rendered HTML string
        """
        # Convert Pydantic model to dict if necessary
        if isinstance(report_data, NewsReport):
            data = report_data.model_dump()
        else:
            data = report_data
        
        # Load template
        try:
            template = self.env.get_template(template_name)
        except Exception as e:
            raise ValueError(f"Failed to load template '{template_name}': {e}")
        
        # Render template with data
        html_output = template.render(report=data)
        
        # Save to file if output path specified
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_output)
            
            print(f"✅ HTML report saved to: {output_path}")
        
        return html_output
    
    def render_from_json(
        self,
        json_file: str,
        template_name: str = "news_report_template.html",
        output_file: str = None
    ) -> str:
        """
        Render news report from JSON file.
        
        Args:
            json_file: Path to JSON file containing report data
            template_name: Name of the Jinja2 template file
            output_file: Optional path to save rendered HTML
            
        Returns:
            Rendered HTML string
        """
        import json
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Validate and parse with Pydantic model
        report = NewsReport(**data)
        
        return self.render(report, template_name, output_file)


# Convenience function for direct usage
def render_news_report(
    report: Union[NewsReport, dict, str],
    output_file: str = None,
    template_dir: str = "templates"
) -> str:
    """
    Convenience function to render news report.
    
    Args:
        report: NewsReport model, dict, or path to JSON file
        output_file: Optional path to save rendered HTML
        template_dir: Directory containing templates
        
    Returns:
        Rendered HTML string
    """
    renderer = NewsReportRenderer(template_dir)
    
    # Handle different input types
    if isinstance(report, str):
        # Assume it's a JSON file path
        return renderer.render_from_json(report, output_file=output_file)
    else:
        return renderer.render(report, output_file=output_file)


if __name__ == "__main__":
    # Example usage
    from models import NewsReport, NewsStory, CategoryNews, RegionalNews, ReportMetadata
    
    # Create sample data
    sample_story = NewsStory(
        headline="Major Technology Breakthrough Announced",
        summary="Scientists have developed a revolutionary new approach to quantum computing...",
        source="Tech News Daily",
        source_url="https://example.com/article",
        category="Technology",
        region="World",
        verification_status="Verified",
        confidence_score=9,
        timestamp="2025-11-10 14:30:00"
    )
    
    sample_category = CategoryNews(
        category="Technology",
        stories=[sample_story],
        total_stories=1,
        verified_count=1,
        developing_count=0
    )
    
    sample_regional = RegionalNews(
        region="World",
        categories=[sample_category],
        total_stories=1
    )
    
    sample_metadata = ReportMetadata(
        generation_date="2025-11-10 21:00:00",
        total_stories_collected=42,
        total_stories_verified=38,
        total_sources_consulted=25,
        categories_covered=["Political", "Economy", "Technology"],
        regions_covered=["World", "India", "Ahmedabad"],
        llm_model_used="gemini-1.5-flash",
        verification_model_used="gemini-2.5-pro"
    )
    
    sample_report = NewsReport(
        title="Daily News Report",
        generation_date="2025-11-10",
        executive_summary="Today's top developments include breakthrough in quantum computing...",
        featured_stories=[sample_story],
        world_news=sample_regional,
        india_news=RegionalNews(region="India", categories=[], total_stories=0),
        ahmedabad_news=RegionalNews(region="Ahmedabad", categories=[], total_stories=0),
        metadata=sample_metadata
    )
    
    # Render report
    html_output = render_news_report(
        sample_report,
        output_file="output/sample_report.html",
        template_dir="templates"
    )
    
    print("Sample report rendered successfully!")