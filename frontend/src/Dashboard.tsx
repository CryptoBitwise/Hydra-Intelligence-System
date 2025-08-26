// frontend/src/Dashboard.tsx
import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

interface Intelligence {
    head: string;
    competitor: string;
    discovery: string;
    threatLevel: string;
    confidence: number;
    timestamp: string;
    recommendedAction: string;
}

const Dashboard: React.FC = () => {
    const [intelligence, setIntelligence] = useState<Intelligence[]>([]);
    const [ws, setWs] = useState<WebSocket | null>(null);
    const [activeHeads, setActiveHeads] = useState({
        PriceWatch: true,
        JobSpy: true,
        TechRadar: true,
        SocialPulse: true,
        PatentHawk: true,
        AdTracker: true
    });

    useEffect(() => {
        // Connect to WebSocket for real-time updates
        const websocket = new WebSocket('ws://localhost:8000/ws');

        websocket.onmessage = (event) => {
            const intel: Intelligence = JSON.parse(event.data);
            setIntelligence(prev => [intel, ...prev].slice(0, 100));

            // Show notification for critical threats
            if (intel.threatLevel === 'critical') {
                showCriticalAlert(intel);
            }
        };

        setWs(websocket);

        return () => websocket.close();
    }, []);

    const showCriticalAlert = (intel: Intelligence) => {
        // Browser notification
        if (Notification.permission === 'granted') {
            new Notification('🚨 HYDRA CRITICAL ALERT', {
                body: `${intel.competitor}: ${intel.discovery}`,
                icon: '/hydra-icon.png'
            });
        }
    };

    return (
        <div className="hydra-dashboard">
            <header className="dashboard-header">
                <h1>🐉 HYDRA INTELLIGENCE DASHBOARD</h1>
                <div className="status-bar">
                    {Object.entries(activeHeads).map(([head, active]) => (
                        <div key={head} className={`head-status ${active ? 'active' : 'inactive'}`}>
                            <span className="head-icon">{getHeadIcon(head)}</span>
                            <span>{head}</span>
                        </div>
                    ))}
                </div>
            </header>

            <div className="dashboard-grid">
                <div className="intel-feed">
                    <h2>Live Intelligence Feed</h2>
                    {intelligence.map((intel, i) => (
                        <div key={i} className={`intel-card threat-${intel.threatLevel}`}>
                            <div className="intel-header">
                                <span className="head-badge">{intel.head}</span>
                                <span className="threat-badge">{intel.threatLevel.toUpperCase()}</span>
                                <span className="confidence">{(intel.confidence * 100).toFixed(0)}% confident</span>
                            </div>
                            <h3>{intel.competitor}</h3>
                            <p>{intel.discovery}</p>
                            <div className="recommended-action">
                                <strong>Recommended Action:</strong> {intel.recommendedAction}
                            </div>
                            <time>{new Date(intel.timestamp).toLocaleTimeString()}</time>
                        </div>
                    ))}
                </div>

                <div className="metrics-panel">
                    <h2>Competitive Metrics</h2>
                    {/* Add charts here */}
                </div>
            </div>
        </div>
    );
};

const getHeadIcon = (head: string) => {
    const icons: Record<string, string> = {
        PriceWatch: '👁️',
        JobSpy: '🎯',
        TechRadar: '📡',
        SocialPulse: '💭',
        PatentHawk: '📋',
        AdTracker: '📊'
    };
    return icons[head] || '🐉';
};

export default Dashboard;
