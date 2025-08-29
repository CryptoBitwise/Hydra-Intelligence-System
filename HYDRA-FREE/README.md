# 🐉 HYDRA - FREE Competitive Intelligence System

[![HYDRA](https://github.com/YOUR_USERNAME/hydra-free/actions/workflows/hydra.yml/badge.svg)](https://github.com/YOUR_USERNAME/hydra-free/actions)

**No subscriptions. No vendor lock-in. Just intelligence.**

Started as a competition entry that required expensive tools (n8n + Bright Data), rebuilt to be **actually FREE**.

## Features

🐉 **6 Specialized Heads:**

- 👁️ PriceWatch - Monitor pricing changes
- 🎯 JobSpy - Track hiring patterns
- 📡 TechRadar - Detect tech adoption
- 💭 SocialPulse - Sentiment analysis
- 📋 PatentHawk - Innovation tracking
- 📊 AdTracker - Marketing intelligence

✅ **Actually FREE:**

- Runs on GitHub Actions (free)
- No n8n subscription needed
- No Bright Data required
- SQLite database (no setup)
- Single Python script

## Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/hydra-free
cd hydra-free

# Install
pip install -r requirements.txt

# Initialize
python hydra.py init

# Collect intelligence
python hydra.py collect --competitors "competitor1.com,competitor2.com"

# View dashboard
python hydra.py dashboard
```
