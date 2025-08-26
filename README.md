# 🐉 HYDRA: The Competitive Intelligence Monster

> **HYDRA - A multi-headed AI beast that never sleeps. Each head watches a different aspect of your competitive landscape. When one head spots opportunity or threat, all heads turn to analyze. Your unfair advantage in business intelligence.**

## 🏗️ System Architecture

HYDRA is a production-ready competitive intelligence system with a modular, multi-headed architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                        HYDRA CORE                              │
├─────────────────────────────────────────────────────────────────┤
│  🧠 Brain Controller  │  🗄️ PostgreSQL  │  🚀 FastAPI Backend │
│  (Orchestrates all    │  (Data storage) │  (REST API + WS)    │
│   heads & analysis)   │                 │                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                          6 HEADS                               │
├─────────────────────────────────────────────────────────────────┤
│  👁️ PriceWatch    │  🎯 JobSpy      │  📡 TechRadar          │
│  (Price monitoring)│  (Job tracking) │  (Tech adoption)       │
├─────────────────────────────────────────────────────────────────┤
│  💭 SocialPulse   │  📋 PatentHawk  │  📊 AdTracker          │
│  (Sentiment)       │  (Patents)      │  (Ad intelligence)     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA SOURCES                              │
├─────────────────────────────────────────────────────────────────┤
│  🌐 Bright Data   │  🕷️ Web Scraping │  🔌 Public APIs       │
│  (Proxy network)  │  (Custom bots)   │  (External services)   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PROCESSING                                │
├─────────────────────────────────────────────────────────────────┤
│  🎮 4090 Analysis │  🤖 Ollama LLMs  │  🔍 Pattern Recognition│
│  (GPU acceleration)│  (AI analysis)   │  (Cross-head patterns) │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        OUTPUT                                  │
├─────────────────────────────────────────────────────────────────┤
│  📊 React Dashboard│  🚨 Alert System │  📋 Reports            │
│  (Real-time UI)   │  (Notifications) │  (Analytics)           │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Features

### **Multi-Head Intelligence**
- **👁️ PriceWatch**: Real-time price monitoring and competitive pricing analysis
- **🎯 JobSpy**: Job posting tracking and talent acquisition intelligence
- **📡 TechRadar**: Technology adoption monitoring and trend analysis
- **💭 SocialPulse**: Social media sentiment and brand perception tracking
- **📋 PatentHawk**: Patent monitoring and innovation intelligence
- **📊 AdTracker**: Advertisement tracking and marketing strategy analysis

### **AI-Powered Analysis**
- **Ollama Integration**: Local LLM analysis for data insights
- **Pattern Recognition**: Cross-head correlation detection
- **Anomaly Detection**: Automatic identification of unusual patterns
- **Predictive Analytics**: Trend forecasting and opportunity identification

### **Real-Time Monitoring**
- **WebSocket Updates**: Live dashboard updates
- **Alert System**: Configurable notifications for critical events
- **Automated Scanning**: Continuous monitoring with configurable intervals
- **Bright Data Integration**: Professional web scraping infrastructure

### **Production Ready**
- **FastAPI Backend**: High-performance async API
- **PostgreSQL Database**: Robust data storage
- **Docker Support**: Easy deployment and scaling
- **Health Monitoring**: System health and performance tracking

## 📁 Project Structure

```
HYDRA/
├── backend/                    # Python backend
│   ├── core/                  # Core system components
│   │   ├── brain.py          # Central controller
│   │   ├── database.py       # Database models
│   │   └── config.py         # Configuration
│   ├── heads/                # Intelligence heads
│   │   ├── price_watch.py    # Price monitoring
│   │   ├── job_spy.py        # Job tracking
│   │   ├── tech_radar.py     # Tech adoption
│   │   ├── social_pulse.py   # Sentiment analysis
│   │   ├── patent_hawk.py    # Patent monitoring
│   │   └── ad_tracker.py     # Ad intelligence
│   ├── api/                  # API layer
│   │   ├── main.py          # FastAPI application
│   │   └── websocket.py     # WebSocket manager
│   └── ml/                  # Machine learning
│       ├── analyzer.py       # AI analysis engine
│       └── patterns.py       # Pattern recognition
├── frontend/                 # React dashboard (coming soon)
├── docker/                   # Docker configuration
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+**
- **PostgreSQL 12+**
- **Ollama** (for local LLM analysis)
- **Bright Data** account (optional, for web scraping)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd HYDRA

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://hydra:hydra@localhost:5432/hydra_db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=True

# Bright Data (optional)
BRIGHT_DATA_USERNAME=your_username
BRIGHT_DATA_PASSWORD=your_password
BRIGHT_DATA_HOST=brd.superproxy.io
BRIGHT_DATA_PORT=22225

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Head Configuration
PRICE_WATCH_ENABLED=True
JOB_SPY_ENABLED=True
TECH_RADAR_ENABLED=True
SOCIAL_PULSE_ENABLED=True
PATENT_HAWK_ENABLED=True
AD_TRACKER_ENABLED=True
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb hydra_db

# Initialize database tables
python -c "from backend.core.database import init_db; init_db()"
```

### 4. Start HYDRA

```bash
# Start the API server
cd backend
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Access the System

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **System Status**: http://localhost:8000/status

## 🔧 Configuration

### Head Configuration

Each HYDRA head can be configured independently:

```env
# PriceWatch Configuration
PRICE_WATCH_ENABLED=True
PRICE_WATCH_INTERVAL=300          # 5 minutes
PRICE_WATCH_TARGETS=amazon,netflix,spotify

# JobSpy Configuration
JOB_SPY_ENABLED=True
JOB_SPY_INTERVAL=600              # 10 minutes
JOB_SPY_COMPANIES=google,microsoft,apple

# TechRadar Configuration
TECH_RADAR_ENABLED=True
TECH_RADAR_INTERVAL=1800          # 30 minutes
TECH_RADAR_KEYWORDS=ai,blockchain,cloud
```

### Custom Targets

Add custom monitoring targets through the API:

```bash
# Add price monitoring target
curl -X POST "http://localhost:8000/heads/price_watch/targets" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Custom Product",
    "url": "https://example.com/product",
    "company": "Example Corp",
    "selectors": {
      "price": ".price-selector",
      "currency": ".currency-selector"
    }
  }'
```

## 📊 API Endpoints

### Core Endpoints

- `GET /` - System information
- `GET /health` - Health check
- `GET /status` - System status
- `GET /config` - Configuration (safe)

### Head Management

- `GET /heads` - All heads status
- `GET /heads/{head_name}` - Specific head status
- `POST /heads/{head_name}/scan` - Manual scan trigger

### Data Access

- `GET /data/{head_name}` - Data from specific head
- `GET /data/{head_name}/latest` - Latest data
- `GET /analysis/{head_name}` - AI analysis results
- `GET /analysis/cross-head` - Cross-head patterns

### Real-Time Updates

- `WS /ws` - WebSocket for live updates

## 🤖 AI Analysis

HYDRA uses Ollama for intelligent data analysis:

### Analysis Types

- **Sentiment Analysis**: Positive/negative sentiment scoring
- **Trend Detection**: Emerging patterns and opportunities
- **Anomaly Detection**: Unusual events and outliers
- **Cross-Head Correlation**: Patterns across different data sources

### Example Analysis

```python
# Data automatically analyzed by HYDRA
{
  "summary": "Major price increase detected in streaming services",
  "sentiment": -0.8,
  "confidence_score": 0.95,
  "insights": [
    "Netflix price increased by 20%",
    "Competitors may follow suit",
    "Market consolidation trend emerging"
  ],
  "recommendations": [
    "Monitor competitor pricing strategies",
    "Prepare for potential market shifts",
    "Review pricing strategy"
  ]
}
```

## 🚨 Alert System

HYDRA automatically generates alerts for significant events:

### Alert Types

- **Price Changes**: Significant pricing movements
- **Job Market Shifts**: New hiring trends
- **Technology Adoption**: Emerging tech trends
- **Social Sentiment**: Brand perception changes
- **Patent Activity**: Innovation developments
- **Marketing Changes**: New advertising strategies

### Alert Configuration

```env
# Alert thresholds
ALERT_WEBHOOK_URL=https://hooks.slack.com/...
ALERT_EMAIL=alerts@company.com

# Custom thresholds per head
PRICE_WATCH_ALERT_THRESHOLD=10    # 10% price change
SOCIAL_PULSE_ALERT_THRESHOLD=0.5  # Sentiment threshold
```

## 🔍 Monitoring and Health

### System Health

- **Database Connectivity**: PostgreSQL health checks
- **Head Status**: Individual head monitoring
- **Performance Metrics**: Response times and throughput
- **Error Tracking**: Comprehensive error logging

### Health Endpoints

```bash
# Check system health
curl http://localhost:8000/health

# Get detailed status
curl http://localhost:8000/status

# Monitor specific head
curl http://localhost:8000/heads/price_watch
```

## 🐳 Docker Deployment

### Docker Compose

```yaml
version: '3.8'
services:
  hydra-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://hydra:hydra@postgres:5432/hydra_db
    depends_on:
      - postgres
      - ollama

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: hydra_db
      POSTGRES_USER: hydra
      POSTGRES_PASSWORD: hydra
    volumes:
      - postgres_data:/var/lib/postgresql/data

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama

volumes:
  postgres_data:
  ollama_data:
```

### Build and Run

```bash
# Build the image
docker build -t hydra .

# Run with docker-compose
docker-compose up -d
```

## 🔒 Security Considerations

### Production Security

- **Environment Variables**: Never commit sensitive data
- **API Keys**: Secure storage of external service credentials
- **Rate Limiting**: Implement API rate limiting
- **Authentication**: Add JWT or OAuth2 authentication
- **HTTPS**: Use SSL/TLS in production

### Access Control

```env
# Enable authentication
AUTH_ENABLED=True
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600
```

## 🧪 Testing

### Run Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest backend/tests/

# Run with coverage
pytest --cov=backend backend/tests/
```

### Test Structure

```
backend/tests/
├── test_core/          # Core system tests
├── test_heads/         # Head functionality tests
├── test_api/           # API endpoint tests
└── test_ml/            # ML component tests
```

## 📈 Performance Optimization

### Scaling Strategies

- **Async Processing**: Non-blocking I/O operations
- **Connection Pooling**: Database connection optimization
- **Caching**: Redis integration for data caching
- **Load Balancing**: Multiple API instances
- **Background Workers**: Celery for heavy tasks

### Performance Monitoring

```python
# Monitor performance metrics
from backend.core.brain import brain

status = brain.get_system_status()
print(f"Total data collected: {status['total_data_collected']}")
print(f"System performance: {status['performance_score']}")
```

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Code Style

- **Python**: Black formatting, flake8 linting
- **Type Hints**: Use type annotations
- **Documentation**: Docstrings for all functions
- **Testing**: Maintain test coverage >80%

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help

- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Documentation**: Check the `/docs` endpoint
- **Community**: Join our Discord/Telegram

### Common Issues

1. **Database Connection**: Check PostgreSQL is running
2. **Ollama Issues**: Ensure Ollama service is accessible
3. **Bright Data**: Verify proxy credentials
4. **Port Conflicts**: Check if ports 8000/8001 are available

## 🚀 Roadmap

### Phase 2: Enhanced Intelligence
- [ ] Advanced ML models integration
- [ ] Predictive analytics
- [ ] Natural language querying
- [ ] Automated report generation

### Phase 3: Enterprise Features
- [ ] Multi-tenant architecture
- [ ] Advanced security features
- [ ] API rate limiting
- [ ] Enterprise SSO integration

### Phase 4: AI Agents
- [ ] Autonomous decision making
- [ ] Proactive opportunity detection
- [ ] Automated competitive responses
- [ ] Market prediction models

---

**🐉 HYDRA: When one head sees, all heads know. Your competitive advantage is now automated.**

*Built with ❤️ for competitive intelligence professionals*
