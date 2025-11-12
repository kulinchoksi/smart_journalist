"""
Pydantic Models for Structured News Output
Defines the data schema for consistent news report generation
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Literal
from datetime import datetime


class NewsStory(BaseModel):
    """Individual news story with all required fields."""
    
    headline: str = Field(..., description="Clear, factual headline")
    summary: str = Field(..., description="2-3 sentence summary with key facts")
    source: str = Field(..., description="Publication name")
    source_url: Optional[HttpUrl] = Field(None, description="Direct link to original article")
    category: Literal[
        "Political", "Economy", "Technology", "Science", 
        "Stock Market", "Energy", "Infrastructure"
    ] = Field(..., description="News category")
    region: Literal["World", "India", "Ahmedabad"] = Field(
        ..., description="Geographic relevance"
    )
    verification_status: Literal[
        "Verified", "Partially Verified", "Developing", "Unverified"
    ] = Field(..., description="Verification level")
    confidence_score: int = Field(
        ..., ge=1, le=10, description="Confidence rating (1-10)"
    )
    timestamp: Optional[str] = Field(None, description="Publication timestamp")
    impact_score: Optional[int] = Field(
        None, ge=1, le=10, description="Impact significance (1-10)"
    )
    key_points: Optional[List[str]] = Field(
        None, description="Bullet points of key information"
    )


class CategoryNews(BaseModel):
    """News collection for a specific category."""
    
    category: str
    stories: List[NewsStory]
    total_stories: int
    verified_count: int
    developing_count: int


class RegionalNews(BaseModel):
    """News collection for a specific region."""
    
    region: str
    categories: List[CategoryNews]
    total_stories: int


class ReportMetadata(BaseModel):
    """Metadata about the report generation."""
    
    generation_date: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    total_stories_collected: int
    total_stories_verified: int
    total_sources_consulted: int
    categories_covered: List[str]
    regions_covered: List[str]
    llm_model_used: str
    verification_model_used: str
    execution_time_seconds: Optional[int] = None
    success_rate: Optional[float] = Field(
        None, description="Percentage of successfully collected stories"
    )


class NewsReport(BaseModel):
    """Complete structured news report."""
    
    # Report Header
    title: str = Field(default="Daily News Report")
    generation_date: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d")
    )
    
    # Executive Summary
    executive_summary: str = Field(
        ..., 
        description="3-5 paragraph summary highlighting top stories across all categories"
    )
    
    # Top Stories (Featured)
    featured_stories: List[NewsStory] = Field(
        ..., 
        description="Top 5-10 most significant stories across all categories and regions",
        max_items=10
    )
    
    # Regional Organization
    world_news: RegionalNews
    india_news: RegionalNews
    ahmedabad_news: RegionalNews
    
    # Category Summaries (Optional - for quick reference)
    category_highlights: Optional[dict[str, str]] = Field(
        None,
        description="Brief highlights for each category"
    )
    
    # Report Metadata
    metadata: ReportMetadata
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Daily News Report",
                "generation_date": "2025-11-10",
                "executive_summary": "Today's top developments include...",
                "featured_stories": [
                    {
                        "headline": "Major Policy Announcement",
                        "summary": "Government announces new policy...",
                        "source": "Reuters",
                        "source_url": "https://reuters.com/article",
                        "category": "Political",
                        "region": "World",
                        "verification_status": "Verified",
                        "confidence_score": 9
                    }
                ],
                "world_news": {
                    "region": "World",
                    "categories": [],
                    "total_stories": 15
                },
                "metadata": {
                    "generation_date": "2025-11-10 21:30:00",
                    "total_stories_collected": 45,
                    "total_stories_verified": 38,
                    "llm_model_used": "gemini-1.5-flash"
                }
            }
        }