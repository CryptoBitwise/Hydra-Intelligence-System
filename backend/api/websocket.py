"""
HYDRA WebSocket Manager
Manages real-time WebSocket connections for live updates
"""

import asyncio
import logging
from typing import List, Dict, Any
from fastapi import WebSocket, WebSocketDisconnect
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class ConnectionManager:
    """
    Manages WebSocket connections for real-time HYDRA updates
    """
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
        self.broadcast_queue = asyncio.Queue()
        
        # Start background broadcast task
        asyncio.create_task(self._broadcast_worker())
    
    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection"""
        try:
            await websocket.accept()
            self.active_connections.append(websocket)
            
            # Store connection metadata
            self.connection_metadata[websocket] = {
                "connected_at": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat(),
                "message_count": 0
            }
            
            logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")
            
            # Send welcome message
            welcome_message = {
                "type": "connection_established",
                "message": "Connected to HYDRA real-time feed",
                "timestamp": datetime.now().isoformat(),
                "connection_id": id(websocket)
            }
            
            await websocket.send_text(json.dumps(welcome_message))
            
        except Exception as e:
            logger.error(f"Error accepting WebSocket connection: {e}")
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
            if websocket in self.connection_metadata:
                del self.connection_metadata[websocket]
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        try:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
            
            if websocket in self.connection_metadata:
                del self.connection_metadata[websocket]
            
            logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
            
        except Exception as e:
            logger.error(f"Error disconnecting WebSocket: {e}")
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """Send a message to a specific WebSocket connection"""
        try:
            if websocket in self.active_connections:
                message_text = json.dumps(message)
                await websocket.send_text(message_text)
                
                # Update connection metadata
                if websocket in self.connection_metadata:
                    self.connection_metadata[websocket]["message_count"] += 1
                    self.connection_metadata[websocket]["last_activity"] = datetime.now().isoformat()
                
                logger.debug(f"Personal message sent to connection {id(websocket)}")
            
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            # Remove broken connection
            self.disconnect(websocket)
    
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast a message to all connected WebSockets"""
        try:
            # Add to broadcast queue
            await self.broadcast_queue.put(message)
            
        except Exception as e:
            logger.error(f"Error queuing broadcast message: {e}")
    
    async def _broadcast_worker(self):
        """Background worker that processes broadcast messages"""
        while True:
            try:
                # Wait for messages in the queue
                message = await self.broadcast_queue.get()
                
                # Send to all active connections
                disconnected_websockets = []
                
                for websocket in self.active_connections:
                    try:
                        message_text = json.dumps(message)
                        await websocket.send_text(message_text)
                        
                        # Update connection metadata
                        if websocket in self.connection_metadata:
                            self.connection_metadata[websocket]["message_count"] += 1
                            self.connection_metadata[websocket]["last_activity"] = datetime.now().isoformat()
                    
                    except Exception as e:
                        logger.warning(f"Failed to send broadcast to connection {id(websocket)}: {e}")
                        disconnected_websockets.append(websocket)
                
                # Remove disconnected websockets
                for websocket in disconnected_websockets:
                    self.disconnect(websocket)
                
                # Log broadcast stats
                if self.active_connections:
                    logger.debug(f"Broadcast sent to {len(self.active_connections)} connections")
                
            except Exception as e:
                logger.error(f"Error in broadcast worker: {e}")
                await asyncio.sleep(1)
    
    async def broadcast_head_update(self, head_name: str, status: Dict[str, Any]):
        """Broadcast a head status update"""
        message = {
            "type": "head_update",
            "head_name": head_name,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    async def broadcast_data_update(self, head_name: str, data: Dict[str, Any]):
        """Broadcast new data from a head"""
        message = {
            "type": "data_update",
            "head_name": head_name,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    async def broadcast_analysis_update(self, head_name: str, analysis: Dict[str, Any]):
        """Broadcast new analysis results"""
        message = {
            "type": "analysis_update",
            "head_name": head_name,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    async def broadcast_alert(self, alert: Dict[str, Any]):
        """Broadcast a new alert"""
        message = {
            "type": "alert",
            "alert": alert,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    async def broadcast_pattern_update(self, pattern: Dict[str, Any]):
        """Broadcast a new cross-head pattern"""
        message = {
            "type": "pattern_update",
            "pattern": pattern,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    async def broadcast_system_status(self, status: Dict[str, Any]):
        """Broadcast system status update"""
        message = {
            "type": "system_status",
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get statistics about active connections"""
        try:
            total_connections = len(self.active_connections)
            total_messages = sum(
                meta.get("message_count", 0) 
                for meta in self.connection_metadata.values()
            )
            
            # Calculate average messages per connection
            avg_messages = total_messages / total_connections if total_connections > 0 else 0
            
            # Get connection age distribution
            connection_ages = []
            for meta in self.connection_metadata.values():
                if "connected_at" in meta:
                    try:
                        connected_time = datetime.fromisoformat(meta["connected_at"])
                        age_seconds = (datetime.now() - connected_time).total_seconds()
                        connection_ages.append(age_seconds)
                    except (ValueError, TypeError):
                        continue
            
            avg_age = sum(connection_ages) / len(connection_ages) if connection_ages else 0
            
            return {
                "total_connections": total_connections,
                "total_messages_sent": total_messages,
                "average_messages_per_connection": round(avg_messages, 2),
                "average_connection_age_seconds": round(avg_age, 2),
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error getting connection stats: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def ping_connections(self):
        """Send ping to all connections to check health"""
        try:
            ping_message = {
                "type": "ping",
                "timestamp": datetime.now().isoformat()
            }
            
            await self.broadcast(ping_message)
            logger.debug("Ping sent to all connections")
            
        except Exception as e:
            logger.error(f"Error sending ping: {e}")
    
    async def cleanup_stale_connections(self, max_age_seconds: int = 3600):
        """Remove connections that have been inactive for too long"""
        try:
            current_time = datetime.now()
            stale_websockets = []
            
            for websocket, metadata in self.connection_metadata.items():
                if "last_activity" in metadata:
                    try:
                        last_activity = datetime.fromisoformat(metadata["last_activity"])
                        age_seconds = (current_time - last_activity).total_seconds()
                        
                        if age_seconds > max_age_seconds:
                            stale_websockets.append(websocket)
                    
                    except (ValueError, TypeError):
                        # Invalid timestamp, mark as stale
                        stale_websockets.append(websocket)
            
            # Remove stale connections
            for websocket in stale_websockets:
                logger.info(f"Removing stale connection {id(websocket)}")
                self.disconnect(websocket)
            
            if stale_websockets:
                logger.info(f"Cleaned up {len(stale_websockets)} stale connections")
        
        except Exception as e:
            logger.error(f"Error cleaning up stale connections: {e}")
    
    async def get_connection_info(self) -> List[Dict[str, Any]]:
        """Get detailed information about all connections"""
        try:
            connection_info = []
            
            for websocket, metadata in self.connection_metadata.items():
                info = {
                    "connection_id": id(websocket),
                    "connected_at": metadata.get("connected_at"),
                    "last_activity": metadata.get("last_activity"),
                    "message_count": metadata.get("message_count", 0),
                    "status": "active"
                }
                
                # Calculate connection age
                if "connected_at" in metadata:
                    try:
                        connected_time = datetime.fromisoformat(metadata["connected_at"])
                        age_seconds = (datetime.now() - connected_time).total_seconds()
                        info["age_seconds"] = round(age_seconds, 2)
                    except (ValueError, TypeError):
                        info["age_seconds"] = "unknown"
                
                connection_info.append(info)
            
            return connection_info
        
        except Exception as e:
            logger.error(f"Error getting connection info: {e}")
            return []
