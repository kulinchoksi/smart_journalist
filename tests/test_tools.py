"""
Test cases for Smart Journalist tools
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from smart_journalist.tools.news_search_tool import NewsSearchTool
from smart_journalist.tools.web_scraper_tool import WebScraperTool


class TestNewsSearchTool(unittest.TestCase):
    """Test cases for NewsSearchTool"""

    def setUp(self):
        """Set up test environment"""
        os.environ['SERPER_API_KEY'] = 'test-api-key'
        self.tool = NewsSearchTool()

    @patch('requests.post')
    def test_news_search_success(self, mock_post):
        """Test successful news search"""
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'news': [
                {
                    'title': 'Test News Title',
                    'snippet': 'Test news summary',
                    'source': 'Test Source',
                    'date': '2024-01-01',
                    'link': 'https://example.com/news1',
                    'position': 1
                }
            ]
        }
        mock_post.return_value = mock_response

        # Test the tool
        result = self.tool._run("test query")

        # Assertions
        self.assertIn("Test News Title", result)
        self.assertIn("Test Source", result)
        self.assertIn("https://example.com/news1", result)

    @patch('requests.post')
    def test_news_search_api_error(self, mock_post):
        """Test API error handling"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        result = self.tool._run("test query")

        self.assertIn("Error: API request failed", result)

    def test_category_news_search(self):
        """Test category-specific news search"""
        with patch.object(self.tool, '_run') as mock_run:
            mock_run.return_value = "Test result"

            result = self.tool.search_category_news("technology", "india")

            # Check that the query was constructed with India context
            mock_run.assert_called_once()
            call_args = mock_run.call_args[1]
            self.assertIn("India", call_args['query'])


class TestWebScraperTool(unittest.TestCase):
    """Test cases for WebScraperTool"""

    def setUp(self):
        """Set up test environment"""
        os.environ['FIRECRAWL_API_KEY'] = 'test-api-key'

        # Mock FirecrawlApp to avoid import issues in testing
        with patch('smart_journalist.tools.web_scraper_tool.FirecrawlApp'):
            self.tool = WebScraperTool()

    def test_scrape_success(self):
        """Test successful web scraping"""
        # Mock successful response
        mock_result = {
            'success': True,
            'data': {
                'title': 'Test Article Title',
                'markdown': 'Test article content in markdown format',
                'metadata': {
                    'description': 'Test description',
                    'author': 'Test Author'
                }
            }
        }

        self.tool.app.scrape_url.return_value = mock_result

        result = self.tool._run("https://example.com/article")

        # Assertions
        self.assertIn("Test Article Title", result)
        self.assertIn("Test article content", result)
        self.assertIn("Test Author", result)

    def test_scrape_failure(self):
        """Test scraping failure handling"""
        mock_result = {
            'success': False,
            'error': 'Page not found'
        }

        self.tool.app.scrape_url.return_value = mock_result

        result = self.tool._run("https://example.com/nonexistent")

        self.assertIn("Error scraping", result)
        self.assertIn("Page not found", result)

    def test_scrape_multiple_urls(self):
        """Test scraping multiple URLs"""
        with patch.object(self.tool, '_run') as mock_run:
            mock_run.return_value = "Test content"

            urls = ["https://example1.com", "https://example2.com"]
            result = self.tool.scrape_multiple_urls(urls)

            # Should call _run for each URL
            self.assertEqual(mock_run.call_count, 2)
            self.assertIn("ARTICLE 1", result)
            self.assertIn("ARTICLE 2", result)


if __name__ == '__main__':
    unittest.main()
