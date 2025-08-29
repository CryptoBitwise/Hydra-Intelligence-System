# hydra_web.py - Full Web UI for HYDRA
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import asyncio
from hydra import HydraFree
from datetime import datetime
from pathlib import Path

app = FastAPI(title="HYDRA Intelligence System")

# Store hydra instance
hydra = HydraFree()

# HTML for web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🐉 HYDRA Control Panel</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
        }
        h1 {
            text-align: center;
            font-size: 3em;
            margin-bottom: 30px;
        }
        .controls {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .control-card {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 1.1em;
            cursor: pointer;
            width: 100%;
            margin: 10px 0;
            transition: transform 0.3s;
        }
        button:hover {
            transform: scale(1.05);
        }
        input, select {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border: none;
            background: rgba(255,255,255,0.2);
            color: white;
            font-size: 1em;
        }
        input::placeholder {
            color: rgba(255,255,255,0.7);
        }
        .results {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            border-radius: 10px;
            max-height: 500px;
            overflow-y: auto;
        }
        .intel-item {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #00ff00;
        }
        .loading {
            text-align: center;
            padding: 20px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .stat {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
        }
    </style>
    <script>
        // CSRF protection not needed for demo; add for production
    </script>
</head>
<body>
    <div class="container">
        <h1>🐉 HYDRA Control Panel</h1>
        
        <div class="controls">
            <div class="control-card">
                <h3>🎯 Collect Intelligence</h3>
                <input type="text" id="competitors" placeholder="competitor1.com, competitor2.com">
                <button onclick="collectIntelligence()">Start Collection</button>
            </div>
            
            <div class="control-card">
                <h3>📊 Quick Actions</h3>
                <button onclick="viewReport()">View Report</button>
                <button onclick="viewDashboard()">Open Dashboard</button>
                <button onclick="getStats()">Refresh Stats</button>
            </div>
            
            <div class="control-card">
                <h3>⚙️ Settings</h3>
                <select id="heads">
                    <option value="all">All Heads</option>
                    <option value="PriceWatch">PriceWatch Only</option>
                    <option value="JobSpy">JobSpy Only</option>
                    <option value="TechRadar">TechRadar Only</option>
                </select>
                <button onclick="configure()">Save Settings</button>
            </div>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat">
                <div class="stat-number" id="total">0</div>
                <div>Total Discoveries</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="critical">0</div>
                <div>Critical Threats</div>
            </div>
            <div class="stat">
                <div class="stat-number" id="competitors-count">0</div>
                <div>Competitors</div>
            </div>
            <div class="stat">
                <div class="stat-number">6</div>
                <div>Active Heads</div>
            </div>
        </div>
        
        <div class="results" id="results">
            <h3>Intelligence Feed</h3>
            <div id="intelligence-feed">
                Click "Start Collection" to begin gathering intelligence...
            </div>
        </div>
    </div>
    
    <script>
        async function collectIntelligence() {
            const competitors = document.getElementById('competitors').value || 'example.com';
            const feed = document.getElementById('intelligence-feed');
            
            feed.innerHTML = '<div class="loading">🔍 Collecting intelligence...</div>';
            
            try {
                const response = await fetch('/api/collect', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({competitors: competitors.split(',').map(c => c.trim())})
                });
                
                const data = await response.json();
                
                if (data.success) {
                    feed.innerHTML = `<div style="color: #00ff00;">✅ Collected ${data.count} pieces of intelligence!</div>`;
                    setTimeout(loadIntelligence, 1000);
                }
            } catch (error) {
                feed.innerHTML = `<div style="color: #ff0000;">❌ Error: ${error}</div>`;
            }
        }
        
        async function loadIntelligence() {
            try {
                const response = await fetch('/api/intelligence');
                const data = await response.json();
                
                const feed = document.getElementById('intelligence-feed');
                
                if (data.length === 0) {
                    feed.innerHTML = 'No intelligence collected yet.';
                } else {
                    feed.innerHTML = data.slice(0, 20).map(intel => `
                        <div class="intel-item">
                            <strong>[${'${intel.head}'}]</strong> ${'${intel.competitor}'}<br>
                            <p>${'${intel.discovery}'}</p>
                            <small>Threat: ${'${intel.threat_level}'} | ${'${new Date(intel.timestamp).toLocaleString()}'} </small>
                        </div>
                    `).join('');
                }
            } catch (error) {
                console.error('Error loading intelligence:', error);
            }
        }
        
        async function getStats() {
            try {
                const response = await fetch('/api/stats');
                const stats = await response.json();
                
                document.getElementById('total').textContent = stats.total_discoveries;
                document.getElementById('critical').textContent = stats.critical_threats;
                document.getElementById('competitors-count').textContent = stats.competitors.length;
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        function viewReport() {
            window.open('/report', '_blank');
        }
        
        function viewDashboard() {
            window.open('/dashboard', '_blank');
        }
        
        function configure() {
            alert('Settings saved!');
        }
        
        // Load initial data
        loadIntelligence();
        getStats();
        
        // Auto-refresh every 30 seconds
        setInterval(() => {
            loadIntelligence();
            getStats();
        }, 30000);
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    """Main web interface"""
    return HTML_TEMPLATE

@app.get("/favicon.ico")
async def favicon():
    """Silence favicon 404s; serve file if present"""
    fav_path = Path("dashboard/favicon.ico")
    if fav_path.exists():
        return HTMLResponse(fav_path.read_text(), media_type="image/x-icon")
    return JSONResponse({"status": "no favicon"})

@app.get("/api/intelligence")
async def get_intelligence():
    """Get recent intelligence"""
    return JSONResponse(hydra.get_recent_intelligence(24))

@app.get("/api/stats")
async def get_stats():
    """Get statistics"""
    stats = hydra.export_dashboard()
    return JSONResponse(stats)

@app.post("/api/collect")
async def collect_intelligence(background_tasks: BackgroundTasks, competitors: list = None):
    """Start intelligence collection"""
    
    async def run_collection():
        await hydra.collect_intelligence(competitors)
    
    background_tasks.add_task(run_collection)
    
    return {"success": True, "message": "Collection started", "count": len(competitors or [])}

@app.get("/dashboard")
async def dashboard():
    """Serve dashboard"""
    dashboard_path = Path("dashboard/index.html")
    if dashboard_path.exists():
        return HTMLResponse(dashboard_path.read_text())
    return HTMLResponse("<h1>Dashboard not found. Run: python hydra.py init</h1>")

@app.get("/report")
async def report():
    """Generate HTML report"""
    recent = hydra.get_recent_intelligence(24)
    
    html = """
    <html>
    <head>
        <title>HYDRA Report</title>
        <style>
            body { font-family: sans-serif; margin: 40px; }
            .intel { padding: 20px; margin: 20px 0; border-left: 4px solid #0066cc; background: #f5f5f5; }
        </style>
    </head>
    <body>
        <h1>🐉 HYDRA Intelligence Report</h1>
    """
    
    for intel in recent:
        html += f"""
        <div class=\"intel\">
            <h3>[{intel['head']}] {intel['competitor']}</h3>
            <p>{intel['discovery']}</p>
            <small>Threat: {intel['threat_level']} | {intel['timestamp']}</small>
        </div>
        """
    
    html += "</body></html>"
    return HTMLResponse(html)

if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════╗
    ║         🐉 HYDRA WEB INTERFACE                 ║
    ║                                                ║
    ║  Opening in browser: http://localhost:8000    ║
    ║                                                ║
    ║  Press Ctrl+C to stop                         ║
    ╚════════════════════════════════════════════════╝
    """)
    
    import webbrowser
    webbrowser.open("http://localhost:8000")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)


