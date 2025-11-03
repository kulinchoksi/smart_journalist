#!/bin/bash

# Smart Journalist Setup Script

echo "🚀 Setting up Smart and Wise Journalist App..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📈 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create output directory
mkdir -p output

# Copy example .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Please configure your .env file with the required API keys:"
    echo "   - GOOGLE_CLOUD_PROJECT"
    echo "   - GOOGLE_APPLICATION_CREDENTIALS" 
    echo "   - SERPER_API_KEY"
    echo "   - FIRECRAWL_API_KEY"
    echo ""
    echo "Example .env file has been created. Please edit it with your actual values."
fi

echo "✅ Setup complete!"
echo ""
echo "🚀 To run the application:"
echo "   1. Configure your .env file with API keys"
echo "   2. Activate the virtual environment: source venv/bin/activate"
echo "   3. Run the application: python main.py"
