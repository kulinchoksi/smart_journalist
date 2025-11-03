# Smart and Wise Journalist App

A comprehensive CrewAI-based news gathering and verification system that automatically collects, processes, verifies, and organizes news across multiple regions and categories.

## 🚀 Features

- **Multi-Region Coverage**: Global, India, and Ahmedabad local news
- **Category Specialization**: 7 key domains (Geopolitical, Economy, Technology, Science, Stock Market, Energy, Infrastructure)
- **Quality Assurance**: Dedicated fact-checking and reliability verification
- **Smart Organization**: Structured news cards with headlines, summaries, sources, and reliability indicators
- **Professional Output**: Clean HTML reports with responsive design
- **Vertex AI Integration**: Powered by Google Gemini-2.5-pro for maximum accuracy

## 🏗️ Architecture

### Agents
1. **Global News Agent**: International news specialist
2. **India News Agent**: India-focused news expert
3. **Ahmedabad News Agent**: Local Gujarat/Ahmedabad specialist
4. **Quality Assurance Agent**: Fact-checking and verification expert
5. **Reporting Agent**: Professional report compiler

### Tools
- **SerperDev API**: Real-time news search
- **Firecrawl API**: Clean web content extraction
- **Google Vertex AI**: Advanced language processing

## 📋 Prerequisites

- Python 3.9+
- Google Cloud Service Account with Vertex AI access
- Serper API Key ([get here](https://serper.dev))
- Firecrawl API Key ([get here](https://firecrawl.dev))

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd smart_journalist
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file with:
```
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
GOOGLE_CLOUD_LOCATION=us-central1
SERPER_API_KEY=your-serper-api-key
FIRECRAWL_API_KEY=your-firecrawl-api-key
TEMPERATURE=0.0
MODEL_NAME=gemini-2.5-pro
```

## 🚀 Usage

**Run the application:**
```
podman-compose up -d --build
podman exec -it smart-journalist bash
python main.py
```

The application will:
1. Gather news from multiple sources
2. Verify and fact-check information
3. Organize by region and category
4. Generate a professional HTML report in `output/`

## 📊 Output

The system generates:
- **HTML Report**: `output/news_report_YYYY-MM-DD.html`
- **Professional Layout**: Responsive design with news cards
- **Quality Indicators**: Verified/Developing/Unverified badges
- **Source Attribution**: Direct links to original articles
- **Statistics**: Coverage summary and reliability metrics

## 🔧 Configuration

### Agents Configuration
Each agent has specialized prompts in `src/smart_journalist/crew.py`:
- **Role-based expertise** for different regions/categories
- **Fact-checking emphasis** for accuracy
- **Source verification** protocols

### Categories Covered
- **Geopolitical**: International relations, conflicts, diplomacy
- **Economy**: Markets, policy, business developments
- **Technology**: Innovation, AI, digital transformation
- **Science**: Research, discoveries, health
- **Stock Market**: Trading, IPOs, market analysis
- **Energy**: Oil, renewables, power sector
- **Infrastructure**: Transportation, urban development

## 🎯 Quality Assurance

The system implements:
1. **Multi-source Verification**: Cross-referencing information
2. **Reliability Scoring**: Source credibility assessment
3. **Fact Validation**: Claims verification through authoritative sources
4. **Clear Labeling**: Unverified content clearly marked
5. **Source Filtering**: Exclusion of unreliable sources

## 🌐 Deployment

The application is designed for easy deployment on any hosting service:
- **Containerized**: Docker-ready structure
- **Cloud-Native**: Google Cloud integration
- **Scalable**: Modular architecture
- **Configurable**: Environment-based settings

## 📅 Scheduling

For daily operation, set up automated execution:

**Linux/Mac (cron):**
```bash
# Run daily at 8 AM
0 8 * * * cd /path/to/smart_journalist && python main.py
```

**Windows (Task Scheduler):**
Create a scheduled task to run `main.py` daily

## 🔍 Monitoring

The application provides:
- **Execution logs** with detailed progress
- **Error handling** with clear messages
- **Quality metrics** in the final report
- **Source verification** statistics

## 📝 Customization

### Adding New Categories
1. Update the `categories` list in `main.py`
2. Modify agent prompts in `crew.py`
3. Update HTML template if needed

### Adding New Regions
1. Create new specialized agents in `crew.py`
2. Add corresponding tasks
3. Update the reporting structure

### Modifying Quality Standards
1. Update verification prompts in the Quality Assurance agent
2. Modify reliability scoring criteria
3. Adjust filtering thresholds

## 🚨 Error Handling

The system handles:
- **API failures** with fallback mechanisms
- **Rate limiting** with appropriate delays
- **Content parsing** errors gracefully
- **Missing data** with clear indicators

## 📊 Performance

Typical execution:
- **Processing time**: 5-15 minutes
- **Articles processed**: 40-80 per run
- **Verification rate**: 85-95% successful
- **Source coverage**: 15-25 unique sources

## 🔒 Security

- **API keys** stored in environment variables
- **No sensitive data** in logs or outputs
- **Secure communication** with all external APIs
- **Input validation** for all user inputs

## 🆘 Troubleshooting

### Common Issues:

**"Missing API Key" Error:**
- Check `.env` file has all required keys
- Verify key format and validity

**"Vertex AI Authentication Failed":**
- Ensure service account JSON path is correct
- Verify project permissions

**"No News Found":**
- Check API rate limits
- Verify internet connectivity
- Review search parameters

### Getting Help:

1. Check the logs for detailed error messages
2. Verify all environment variables are set
3. Test individual API connections
4. Review the troubleshooting section in logs

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📧 Support

For support and questions:
- Open an issue in the repository
- Check the documentation
- Review the troubleshooting guide

---

**Built with CrewAI** | **Powered by Google Vertex AI** | **Professional News Intelligence**
