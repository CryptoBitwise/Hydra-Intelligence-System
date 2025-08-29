#!/usr/bin/env python3
# hydra.py - The main entry point
import click
import asyncio
import json
from datetime import datetime
from pathlib import Path
from hydra import HydraFree
import webbrowser

@click.group()
def cli():
    """
    🐉 HYDRA - FREE Competitive Intelligence System
    
    No subscriptions. No complexity. Just intelligence.
    """
    pass

@cli.command()
@click.option('--competitors', '-c', help='Comma-separated competitors to analyze')
@click.option('--heads', '-h', default='all', help='Which heads to run (comma-separated or "all")')
def collect(competitors, heads):
    """Collect intelligence on competitors"""
    
    hydra = HydraFree()
    
    # Parse competitors
    if competitors:
        competitors_list = [c.strip() for c in competitors.split(',')]
    else:
        competitors_list = hydra.config.get('competitors', ['example.com'])
    
    print(f"\n🐉 HYDRA ACTIVATED")
    print(f"📊 Targets: {', '.join(competitors_list)}")
    print(f"🔍 Heads: {heads}")
    print("-" * 50)
    
    # Run collection
    result = asyncio.run(hydra.collect_intelligence(competitors_list))
    
    # Export dashboard data
    stats = hydra.export_dashboard()
    
    print("\n" + "=" * 50)
    print(f"✅ Collection Complete!")
    print(f"📈 Total discoveries: {stats['total_discoveries']}")
    print(f"⚠️  Critical threats: {stats['critical_threats']}")
    print(f"🎯 Competitors analyzed: {len(stats['competitors'])}")
    print("=" * 50)

@cli.command()
@click.option('--hours', '-h', default=24, help='Hours to look back')
@click.option('--format', '-f', default='text', type=click.Choice(['text', 'json', 'html']))
def report(hours, format):
    """Generate intelligence report"""
    
    hydra = HydraFree()
    recent = hydra.get_recent_intelligence(hours)
    
    if format == 'json':
        print(json.dumps(recent, indent=2))
    elif format == 'html':
        # Generate HTML report
        html = generate_html_report(recent, hours)
        output_file = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        Path(output_file).write_text(html)
        print(f"📄 HTML report saved to: {output_file}")
        webbrowser.open(f"file://{Path(output_file).absolute()}")
    else:
        # Text report
        print(f"\n{'='*60}")
        print(f"📊 HYDRA INTELLIGENCE REPORT - Last {hours} hours")
        print(f"{'='*60}")
        
        if not recent:
            print("No intelligence collected yet.")
        else:
            for intel in recent:
                threat_icon = {
                    'critical': '🔴',
                    'high': '🟡', 
                    'medium': '🟢',
                    'low': '⚪'
                }.get(intel.get('threat_level', 'low'), '⚪')
                
                print(f"\n{threat_icon} [{intel['head']}] {intel['competitor']}")
                print(f"   Discovery: {intel['discovery']}")
                print(f"   Threat: {intel['threat_level']} | Confidence: {intel['confidence']}")
                print(f"   Time: {intel['timestamp']}")
                print("-" * 50)

@cli.command()
def dashboard():
    """Open the HYDRA dashboard"""
    
    dashboard_path = Path("dashboard/index.html")
    
    if not dashboard_path.exists():
        print("📝 Creating dashboard...")
        create_dashboard()
    
    # Export latest data
    hydra = HydraFree()
    hydra.export_dashboard()
    
    # Open in browser
    url = f"file://{dashboard_path.absolute()}"
    print(f"🌐 Opening dashboard: {url}")
    webbrowser.open(url)

@cli.command()
@click.option('--port', '-p', default=8000, help='Port to run server on')
def serve(port):
    """Run HYDRA as a web server"""
    
    # Render.com compatibility
    import os
    host = "0.0.0.0"  # Listen on all interfaces
    port = int(os.environ.get('PORT', port))  # Use Render's PORT
    
    print(f"🌐 Starting HYDRA server on http://{host}:{port}")
    print("Press Ctrl+C to stop\n")
    
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse, JSONResponse
    import uvicorn
    
    app = FastAPI(title="HYDRA Intelligence System")
    
    @app.get("/", response_class=HTMLResponse)
    async def root():
        """Serve the demo page"""
        return HTMLResponse("""
<!DOCTYPE html>
<html>
<head>
    <title>🐉 HYDRA - Live Demo</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            text-align: center;
            max-width: 900px;
            width: 100%;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        }
        h1 { 
            font-size: 4em; 
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }
        .tagline {
            font-size: 1.3em;
            margin-bottom: 30px;
            opacity: 0.95;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        .stat-card {
            background: rgba(255,255,255,0.15);
            padding: 25px 15px;
            border-radius: 15px;
            transition: all 0.3s ease;
            animation: pulse 3s infinite;
        }
        .stat-card:hover {
            transform: translateY(-5px);
            background: rgba(255,255,255,0.2);
            animation: none;
        }
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .demo-buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
            margin: 30px 0;
        }
        .btn {
            padding: 15px 30px;
            background: white;
            color: #667eea;
            border: none;
            border-radius: 50px;
            font-size: 1.1em;
            font-weight: bold;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s;
        }
        .btn:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }
        .btn-secondary {
            background: transparent;
            color: white;
            border: 2px solid white;
        }
        .btn-secondary:hover {
            background: white;
            color: #667eea;
        }
        #demo-output {
            margin-top: 40px;
            padding: 30px;
            background: rgba(0,0,0,0.3);
            border-radius: 15px;
            display: none;
            text-align: left;
        }
        .intel-item {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            margin: 15px 0;
            border-radius: 10px;
            border-left: 4px solid #00ff00;
            animation: slideIn 0.5s;
        }
        @keyframes slideIn {
            from { transform: translateX(-20px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .discovery-item {
            animation: slideIn 0.5s ease-out;
        }
        
        .intel-item {
            animation: slideIn 0.5s ease-out;
            transition: all 0.3s ease;
        }
        
        .intel-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        .intel-item.critical { border-left-color: #ff4444; }
        .intel-item.high { border-left-color: #ff9944; }
        .intel-item.medium { border-left-color: #ffdd44; }
        .footer {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid rgba(255,255,255,0.2);
            opacity: 0.8;
        }
        code {
            background: rgba(0,0,0,0.3);
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐉 HYDRA</h1>
        <p class="tagline">6-Headed Competitive Intelligence System</p>
        <p style="opacity: 0.9; margin-bottom: 30px;">
            Monitor your competitors 24/7 with zero subscriptions
        </p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">6</div>
                <div class="stat-label">Intelligence Heads</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">24/7</div>
                <div class="stat-label">Monitoring</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">$0</div>
                <div class="stat-label">Monthly Cost</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">100%</div>
                <div class="stat-label">Open Source</div>
            </div>
        </div>
        
        <div class="demo-buttons">
            <button onclick="runDemo()" class="btn">🧪 Run Live Demo</button>
            <button onclick="showAPI()" class="btn btn-secondary">📡 Test API</button>
            <a href="https://github.com/CryptoBitwise/Hydra-Intelligence-System" class="btn btn-secondary">📝 View Code</a>
            <a href="https://dev.to/yourusername/hydra" class="btn btn-secondary">📖 Read Article</a>
        </div>
        
        <div id="demo-output">
            <h3 style="margin-bottom: 20px; text-align: center;">
                🔍 Live Intelligence Feed
            </h3>
            <div id="intelligence-items"></div>
        </div>
        
        <div class="footer">
            <p><strong>Quick Start:</strong></p>
            <p style="margin: 10px 0;">
                <code>git clone https://github.com/CryptoBitwise/Hydra-Intelligence-System</code>
            </p>
            <p style="margin: 10px 0;">
                <code>pip install -r requirements.txt && python hydra.py serve</code>
            </p>
            <p style="margin-top: 20px; opacity: 0.7;">
                Built with 🔥 by developers tired of subscription fatigue
            </p>
        </div>
    </div>
    
    <script>
        function runDemo() {
            const output = document.getElementById('demo-output');
            const items = document.getElementById('intelligence-items');
            
            output.style.display = 'block';
            
            // Simulate real-time intelligence gathering
            items.innerHTML = '<p style="text-align: center;">⏳ Gathering intelligence...</p>';
            
            setTimeout(() => {
                const discoveries = [
                    {
                        head: 'PriceWatch 👁️',
                        competitor: 'enterprise-rival.com',
                        discovery: 'ALERT: Competitor raised $50M Series B - aggressive expansion coming',
                        threat: 'critical',
                        confidence: '95%'
                    },
                    {
                        head: 'TechRadar 📡',
                        competitor: 'techcorp.io',
                        discovery: 'Detected React → Vue migration - 6 month vulnerability window',
                        threat: 'high',
                        confidence: '88%'
                    },
                    {
                        head: 'PriceWatch 👁️',
                        competitor: 'market-leader.com',
                        discovery: 'Price slashing on enterprise tier - targeting our top accounts',
                        threat: 'critical',
                        confidence: '92%'
                    },
                    {
                        head: 'JobSpy 🎯',
                        competitor: 'startup.ai',
                        discovery: 'Hiring freeze lifted - 47 new positions posted this week',
                        threat: 'high',
                        confidence: '91%'
                    },
                    {
                        head: 'PatentHawk 📋',
                        competitor: 'innovate.com',
                        discovery: 'New patent filed for ML-based recommendation engine',
                        threat: 'medium',
                        confidence: '99%'
                    },
                    {
                        head: 'AdTracker 📊',
                        competitor: 'competitor.com',
                        discovery: 'Ad spend increased 400% on our primary keywords',
                        threat: 'high',
                        confidence: '94%'
                    }
                ];
                
                items.innerHTML = discoveries.map(item => 
                    `<div class="intel-item ${item.threat}">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <strong>${item.head}</strong>
                            <span style="opacity: 0.8;">${item.competitor}</span>
                        </div>
                        <p style="margin: 10px 0; line-height: 1.5;">${item.discovery}</p>
                        <div style="display: flex; justify-content: space-between; font-size: 0.9em; opacity: 0.8;">
                            <span>Threat Level: <strong>${item.threat.toUpperCase()}</strong></span>
                            <span>Confidence: ${item.confidence}</span>
                        </div>
                    </div>`
                ).join('');
                
                items.innerHTML += `
                    <div style="text-align: center; margin-top: 30px; padding: 20px; background: rgba(0,255,0,0.1); border-radius: 10px;">
                        <p><strong>✅ This is sample data demonstrating HYDRA's capabilities</strong></p>
                        <p style="margin-top: 10px;">Deploy your own instance to monitor real competitors!</p>
                    </div>
                `;
            }, 1500);
        }
        
        async function showAPI() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                alert('🚀 API Response:\\n\\n' + JSON.stringify(data, null, 2));
            } catch (e) {
                alert('📡 API Endpoint: /api/status\\n\\nReturns system status and capabilities');
            }
        }
    </script>
</body>
</html>
        """)
    
    @app.get("/api/status")
    async def status():
        return JSONResponse({
            "status": "operational",
            "system": "HYDRA Intelligence System",
            "version": "1.0.0",
            "heads": [
                "PriceWatch - Pricing intelligence",
                "JobSpy - Hiring pattern analysis",
                "TechRadar - Technology stack detection",
                "SocialPulse - Sentiment monitoring",
                "PatentHawk - Innovation tracking",
                "AdTracker - Marketing intelligence"
            ],
            "cost": "$0/month",
            "deployment": "Render.com (Free Tier)",
            "github": "https://github.com/CryptoBitwise/Hydra-Intelligence-System"
        })
    
    uvicorn.run(app, host=host, port=port)

@cli.command()
def init():
    """Initialize HYDRA configuration"""
    
    print("🛠️ Initializing HYDRA...")
    
    # Create directories
    dirs = ["hydra", "hydra/heads", "hydra/scrapers", "dashboard", ".github/workflows"]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {d}/")
    
    # Create default config
    if not Path("config.yaml").exists():
        config = """# HYDRA Configuration
competitors:
  - example.com
  - competitor1.com
  - competitor2.com

heads:
  - PriceWatch
  - JobSpy
  - TechRadar
  - SocialPulse
  - PatentHawk
  - AdTracker

# Scraping settings
use_bright_data: false  # Set to true if you have credentials
scraping:
  timeout: 30
  retries: 3
  use_cache: true

# Alert settings (optional)
alerts:
  webhook: null  # Add Slack/Discord webhook URL
  email: null    # Add email for critical alerts
"""
        Path("config.yaml").write_text(config)
        print("✅ Created config.yaml")
    
    # Create dashboard
    create_dashboard()
    
    print("\n✅ HYDRA initialized successfully!")
    print("\nNext steps:")
    print("1. Edit config.yaml with your competitors")
    print("2. Run: python hydra.py collect")
    print("3. View: python hydra.py dashboard")

def generate_html_report(intelligence, hours):
    """Generate HTML report"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>HYDRA Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}</title>
        <style>
            body {{ font-family: -apple-system, sans-serif; margin: 40px; background: #f5f5f5; }}
            h1 {{ color: #333; }}
            .intel {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .critical {{ border-left: 4px solid #ff0000; }}
            .high {{ border-left: 4px solid #ff9900; }}
            .medium {{ border-left: 4px solid #00cc00; }}
            .low {{ border-left: 4px solid #cccccc; }}
        </style>
    </head>
    <body>
        <h1>🐉 HYDRA Intelligence Report</h1>
        <p>Last {hours} hours | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <hr>
    """
    
    for intel in intelligence:
        html += f"""
        <div class="intel {intel.get('threat_level', 'low')}">
            <h3>[{intel['head']}] {intel['competitor']}</h3>
            <p><strong>Discovery:</strong> {intel['discovery']}</p>
            <p><strong>Threat Level:</strong> {intel['threat_level']} | <strong>Confidence:</strong> {intel['confidence']}</p>
            <p><small>{intel['timestamp']}</small></p>
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    return html

def create_dashboard():
    """Create the dashboard HTML file"""
    dashboard_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐉 HYDRA Intelligence Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        header { text-align: center; padding: 40px 0; }
        h1 { font-size: 4em; margin-bottom: 10px; }
        .subtitle { font-size: 1.2em; opacity: 0.9; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-number { font-size: 3em; font-weight: bold; margin: 10px 0; }
        .intelligence-feed {
            background: rgba(0, 0, 0, 0.3);
            border-radius: 10px;
            padding: 20px;
            margin-top: 40px;
        }
        .intel-item {
            background: rgba(255, 255, 255, 0.1);
            margin: 10px 0;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #00ff00;
        }
        .intel-item.critical { border-left-color: #ff0000; }
        .intel-item.high { border-left-color: #ff9900; }
        .no-subscription {
            text-align: center;
            padding: 20px;
            background: rgba(0, 255, 0, 0.2);
            border-radius: 10px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🐉 HYDRA</h1>
            <p class="subtitle">6-Headed Competitive Intelligence System</p>
        </header>
        
        <div class="no-subscription">
            <h2>✅ NO SUBSCRIPTIONS REQUIRED ✅</h2>
            <p>Running FREE on GitHub Actions • No n8n • No vendor lock-in</p>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-card">
                <div class="stat-number" id="total">0</div>
                <div>Total Discoveries</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="critical">0</div>
                <div>Critical Threats</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="competitors">0</div>
                <div>Competitors</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">6</div>
                <div>Active Heads</div>
            </div>
        </div>
        
        <div class="intelligence-feed">
            <h2>Latest Intelligence</h2>
            <div id="intelligence">Loading...</div>
        </div>
    </div>
    
    <script>
        async function loadData() {
            try {
                const response = await fetch('data.json');
                const data = await response.json();
                
                document.getElementById('total').textContent = data.stats.total_discoveries;
                document.getElementById('critical').textContent = data.stats.critical_threats;
                document.getElementById('competitors').textContent = data.stats.competitors.length;
                
                const intel = document.getElementById('intelligence');
                if (data.intelligence.length === 0) {
                    intel.innerHTML = '<p>No intelligence collected yet. Run: python hydra.py collect</p>';
                } else {
                    intel.innerHTML = data.intelligence.slice(0, 20).map(i => 
                        `<div class="intel-item ${i.threat_level}">
                            <strong>[${i.head}]</strong> ${i.competitor}<br>
                            ${i.discovery}<br>
                            <small>${new Date(i.timestamp).toLocaleString()}</small>
                        </div>`
                    ).join('');
                }
            } catch (e) {
                console.error('Error loading data:', e);
                document.getElementById('intelligence').innerHTML = 
                    '<p>Run "python hydra.py collect" to start collecting intelligence</p>';
            }
        }
        loadData();
        setInterval(loadData, 30000);
    </script>
</body>
</html>"""
    
    Path("dashboard").mkdir(exist_ok=True)
    Path("dashboard/index.html").write_text(dashboard_html)
    print("✅ Created dashboard/index.html")

if __name__ == "__main__":
    cli()


