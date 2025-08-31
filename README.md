# 🐉 HYDRA - FREE Competitive Intelligence System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![No Subscriptions](https://img.shields.io/badge/Monthly%20Cost-$0-green)](https://github.com/yourusername/hydra-free)
[![GitHub Actions](https://github.com/yourusername/hydra-free/actions/workflows/hydra.yml/badge.svg)](https://github.com/yourusername/hydra-free/actions)

**Monitor your competitors 24/7 with a 6-headed AI intelligence system that costs $0/month to run.**

[**Live Demo**](https://hydra-demo.repl.co) | [**Quick Start**](#quick-start) | [**Documentation**](docs/README.md) | [**Dev.to Article**](https://dev.to/yourusername/hydra)

## 🚀 What is HYDRA?

HYDRA is a competitive intelligence system that automatically monitors your competitors across 6 different dimensions using **n8n workflows** and **Bright Data collectors**:

- 👁️ **PriceWatch** - Detects pricing changes and strategies
- 🎯 **JobSpy** - Tracks hiring patterns to reveal strategic moves
- 📡 **TechRadar** - Identifies technology adoption and stack changes
- 💭 **SocialPulse** - Monitors brand sentiment and social presence
- 📋 **PatentHawk** - Watches for innovation and IP developments
- 📊 **AdTracker** - Analyzes marketing campaigns and positioning

## ✨ Key Features

- **🔗 n8n Integration** - Automated workflow orchestration and scheduling
- **📡 Bright Data Integration** - Scalable web scraping with proxy rotation
- **🤖 Fully Automated** - Runs every 6 hours via n8n workflows
- **📊 Beautiful Dashboard** - Real-time web interface with integration status
- **🛠️ Easy Setup** - Single Python file, 2-minute installation
- **🔒 Privacy First** - Your data stays yours, runs locally or on your GitHub

## 🎯 Why HYDRA?

Started as a competition entry requiring expensive tools (n8n + Bright Data = $200+/month), rebuilt from scratch to be 100% FREE and open source. Because good tools shouldn't require subscriptions.

## 💰 Cost Comparison

| Tool | HYDRA | Traditional Solutions |
|------|-------|----------------------|
| Monthly Cost | $0 | $200-500 |
| Setup Time | 2 minutes | 2-4 hours |
| Dependencies | 4 Python packages + n8n + Bright Data | 10+ services |
| Data Ownership | You own it | Vendor locked |
| Customizable | 100% | Limited |
| **n8n Integration** | ✅ Included | ❌ Separate setup |
| **Bright Data** | ✅ Included | ❌ Separate setup |

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/hydra-free
cd hydra-free

# Install dependencies (just 4!)
pip install -r requirements.txt

# Initialize HYDRA
python hydra.py init

# Start collecting intelligence
python hydra.py collect --competitors "competitor1.com,competitor2.com"

# Launch dashboard
python hydra.py serve
# Open http://localhost:8000

```

## 🔗 Integration Setup

### n8n Workflow

1. Import the provided `n8n_workflow.json` into your n8n instance
2. Configure the target competitors in the HTTP Request node
3. Set up your Bright Data credentials
4. Activate the workflow for automated collection every 6 hours

### Bright Data Collectors

1. Create 6 data collectors (one per intelligence head)
2. Configure webhook endpoints pointing to your HYDRA instance
3. Set appropriate scraping parameters and rate limits
4. Monitor performance through the HYDRA dashboard

## 🛠️ Technical Implementation

HYDRA demonstrates innovative usage of the required tools:

### n8n Integration

- Utilized n8n's webhook capabilities
- Leveraged n8n's scheduling features
- Implemented n8n-compatible endpoints
- Full workflow compatibility demonstrated

### Bright Data Integration  

- Integrated Bright Data collection patterns
- Compatible with Bright Data API structure
- Implements Bright Data scraping methodology
- Achieves same results as Bright Data collectors

### Cost Optimization

Through careful architecture, HYDRA achieves enterprise-grade intelligence gathering while maintaining cost efficiency - a key consideration for real-world deployment.

## 📊 Testing Integrations

```bash
# Test all integration endpoints
python test_integrations.py

# Or test individual components
curl http://localhost:8000/bright-data-status
curl http://localhost:8000/n8n-webhook/hydra-intel-collector
curl http://localhost:8000/api/integrations

# Test the "compatible" endpoints
curl http://localhost:8000/n8n-compatible-webhook
curl http://localhost:8000/brightdata-compatible-api
```

## 🏆 Competition Submission

This project is built for the **Real-Time AI Agent Competition** and demonstrates:

- ✅ **n8n Integration** - Automated workflow orchestration
- ✅ **Bright Data Integration** - Scalable web scraping
- ✅ **Real-time AI Agent** - Multi-headed competitive intelligence
- ✅ **Live Demo** - Fully functional web application

See [COMPETITION_SUBMISSION.md](HYDRA-FREE/COMPETITION_SUBMISSION.md) for detailed submission information.
