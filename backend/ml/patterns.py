"""
HYDRA Pattern Recognition
Identifies patterns and correlations across different HYDRA heads
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import json
import numpy as np
from collections import defaultdict, Counter
import re

from ..core.config import config
from ..core.database import get_db

logger = logging.getLogger(__name__)

class PatternRecognizer:
    """
    Pattern recognition system for cross-head analysis
    Identifies correlations, trends, and anomalies across different data sources
    """
    
    def __init__(self):
        self.pattern_cache = {}
        self.correlation_matrix = {}
        self.trend_indicators = {}
        self.anomaly_thresholds = {
            "price_change": 0.15,  # 15% price change
            "sentiment_shift": 0.3,  # 30% sentiment change
            "volume_spike": 2.0,    # 2x normal volume
            "frequency_change": 1.5  # 1.5x normal frequency
        }
        
        # Pattern types to look for
        self.pattern_types = {
            "correlation": "Data correlation between heads",
            "trend": "Emerging trends across heads",
            "anomaly": "Unusual patterns or outliers",
            "sequence": "Temporal sequence of events",
            "cluster": "Geographic or thematic clustering",
            "cyclical": "Recurring patterns over time"
        }
    
    async def find_cross_head_patterns(self, head_name: str, new_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find patterns across different HYDRA heads
        
        Args:
            head_name: Name of the head that collected new data
            new_data: New data to analyze for patterns
            
        Returns:
            List of pattern insights
        """
        try:
            logger.info(f"🔍 Looking for cross-head patterns involving {head_name}")
            
            patterns = []
            
            # Get recent data from all heads
            recent_data = await self._get_recent_data_from_all_heads()
            
            # Look for different types of patterns
            correlation_patterns = await self._find_correlations(head_name, new_data, recent_data)
            trend_patterns = await self._find_trends(head_name, new_data, recent_data)
            anomaly_patterns = await self._find_anomalies(head_name, new_data, recent_data)
            sequence_patterns = await self._find_sequences(head_name, new_data, recent_data)
            
            # Combine all patterns
            patterns.extend(correlation_patterns)
            patterns.extend(trend_patterns)
            patterns.extend(anomaly_patterns)
            patterns.extend(sequence_patterns)
            
            # Filter and rank patterns by significance
            significant_patterns = self._rank_patterns_by_significance(patterns)
            
            logger.info(f"🔍 Found {len(significant_patterns)} significant cross-head patterns")
            return significant_patterns
            
        except Exception as e:
            logger.error(f"🔍 Error finding cross-head patterns: {e}")
            return []
    
    async def _get_recent_data_from_all_heads(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get recent data from all heads for pattern analysis
        
        Returns:
            Dictionary mapping head names to recent data
        """
        # This would query the database for recent data
        # For now, return mock data structure
        return {
            "price_watch": [],
            "job_spy": [],
            "tech_radar": [],
            "social_pulse": [],
            "patent_hawk": [],
            "ad_tracker": []
        }
    
    async def _find_correlations(self, head_name: str, new_data: Dict[str, Any], 
                                recent_data: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Find correlations between data from different heads
        
        Args:
            head_name: Name of the head with new data
            new_data: New data to analyze
            recent_data: Recent data from all heads
            
        Returns:
            List of correlation patterns
        """
        correlations = []
        
        try:
            # Extract key metrics from new data
            new_metrics = self._extract_metrics(new_data, head_name)
            
            # Compare with metrics from other heads
            for other_head, other_data in recent_data.items():
                if other_head == head_name:
                    continue
                
                for data_point in other_data:
                    other_metrics = self._extract_metrics(data_point, other_head)
                    
                    # Calculate correlation
                    correlation_score = self._calculate_correlation(new_metrics, other_metrics)
                    
                    if abs(correlation_score) > 0.7:  # Strong correlation threshold
                        correlation = {
                            "pattern_type": "correlation",
                            "head_name": head_name,
                            "correlated_head": other_head,
                            "correlation_score": correlation_score,
                            "description": f"Strong correlation ({correlation_score:.2f}) between {head_name} and {other_head}",
                            "significance": abs(correlation_score),
                            "data_points": [new_data, data_point],
                            "detected_at": datetime.now().isoformat()
                        }
                        correlations.append(correlation)
        
        except Exception as e:
            logger.error(f"🔍 Error finding correlations: {e}")
        
        return correlations
    
    async def _find_trends(self, head_name: str, new_data: Dict[str, Any], 
                           recent_data: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Find emerging trends across heads
        
        Args:
            head_name: Name of the head with new data
            new_data: New data to analyze
            recent_data: Recent data from all heads
            
        Returns:
            List of trend patterns
        """
        trends = []
        
        try:
            # Look for trending topics, companies, or technologies
            trending_entities = self._identify_trending_entities(new_data, head_name)
            
            for entity, trend_data in trending_entities.items():
                # Check if this entity appears in other heads
                cross_head_mentions = self._count_cross_head_mentions(entity, recent_data)
                
                if cross_head_mentions > 1:  # Entity mentioned in multiple heads
                    trend = {
                        "pattern_type": "trend",
                        "entity": entity,
                        "head_name": head_name,
                        "trend_strength": trend_data.get("strength", 0.5),
                        "cross_head_mentions": cross_head_mentions,
                        "description": f"Trending entity '{entity}' detected across {cross_head_mentions} heads",
                        "significance": min(1.0, cross_head_mentions * 0.3),
                        "trend_data": trend_data,
                        "detected_at": datetime.now().isoformat()
                    }
                    trends.append(trend)
        
        except Exception as e:
            logger.error(f"🔍 Error finding trends: {e}")
        
        return trends
    
    async def _find_anomalies(self, head_name: str, new_data: Dict[str, Any], 
                              recent_data: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Find anomalies or unusual patterns
        
        Args:
            head_name: Name of the head with new data
            new_data: New data to analyze
            recent_data: Recent data from all heads
            
        Returns:
            List of anomaly patterns
        """
        anomalies = []
        
        try:
            # Check for statistical anomalies
            metrics = self._extract_metrics(new_data, head_name)
            
            for metric_name, metric_value in metrics.items():
                if metric_name in self.anomaly_thresholds:
                    threshold = self.anomaly_thresholds[metric_name]
                    
                    # Check if value exceeds threshold
                    if abs(metric_value) > threshold:
                        anomaly = {
                            "pattern_type": "anomaly",
                            "head_name": head_name,
                            "metric": metric_name,
                            "value": metric_value,
                            "threshold": threshold,
                            "description": f"Anomaly detected: {metric_name} = {metric_value} (threshold: {threshold})",
                            "significance": min(1.0, abs(metric_value) / threshold),
                            "anomaly_type": "threshold_exceeded",
                            "detected_at": datetime.now().isoformat()
                        }
                        anomalies.append(anomaly)
            
            # Check for unusual patterns in text data
            text_anomalies = self._find_text_anomalies(new_data, head_name)
            anomalies.extend(text_anomalies)
        
        except Exception as e:
            logger.error(f"🔍 Error finding anomalies: {e}")
        
        return anomalies
    
    async def _find_sequences(self, head_name: str, new_data: Dict[str, Any], 
                              recent_data: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """
        Find temporal sequences of events across heads
        
        Args:
            head_name: Name of the head with new data
            new_data: New data to analyze
            recent_data: Recent data from all heads
            
        Returns:
            List of sequence patterns
        """
        sequences = []
        
        try:
            # Look for events that might be related in time
            current_time = datetime.now()
            
            # Check for recent events in other heads that might be related
            for other_head, other_data in recent_data.items():
                if other_head == head_name:
                    continue
                
                for data_point in other_data:
                    # Check if events are close in time (within 24 hours)
                    if "created_at" in data_point:
                        try:
                            event_time = datetime.fromisoformat(data_point["created_at"])
                            time_diff = abs((current_time - event_time).total_seconds())
                            
                            if time_diff < 86400:  # 24 hours
                                # Check if events might be related
                                if self._events_might_be_related(new_data, data_point):
                                    sequence = {
                                        "pattern_type": "sequence",
                                        "head_name": head_name,
                                        "related_head": other_head,
                                        "time_gap_hours": time_diff / 3600,
                                        "description": f"Temporal sequence detected between {head_name} and {other_head}",
                                        "significance": max(0.5, 1.0 - (time_diff / 86400)),
                                        "events": [new_data, data_point],
                                        "detected_at": current_time.isoformat()
                                    }
                                    sequences.append(sequence)
                        except (ValueError, TypeError):
                            continue
        
        except Exception as e:
            logger.error(f"🔍 Error finding sequences: {e}")
        
        return sequences
    
    def _extract_metrics(self, data: Dict[str, Any], head_name: str) -> Dict[str, float]:
        """
        Extract numerical metrics from data for analysis
        
        Args:
            data: Data to extract metrics from
            head_name: Name of the head
            
        Returns:
            Dictionary of metric names and values
        """
        metrics = {}
        
        try:
            if head_name == "price_watch":
                if "price_change_percent" in data:
                    metrics["price_change"] = float(data["price_change_percent"])
                if "price_change" in data:
                    metrics["price_change_absolute"] = float(data["price_change"])
            
            elif head_name == "social_pulse":
                if "sentiment_score" in data:
                    metrics["sentiment"] = float(data["sentiment_score"])
                if "engagement_count" in data:
                    metrics["engagement"] = float(data["engagement_count"])
            
            elif head_name == "job_spy":
                if "salary_min" in data and "salary_max" in data:
                    avg_salary = (float(data["salary_min"]) + float(data["salary_max"])) / 2
                    metrics["salary"] = avg_salary
            
            elif head_name == "tech_radar":
                if "investment_amount" in data:
                    metrics["investment"] = float(data["investment_amount"])
            
            # Add generic metrics
            if "confidence_score" in data:
                metrics["confidence"] = float(data["confidence_score"])
            
        except (ValueError, TypeError) as e:
            logger.debug(f"Could not extract metric: {e}")
        
        return metrics
    
    def _calculate_correlation(self, metrics1: Dict[str, float], metrics2: Dict[str, float]) -> float:
        """
        Calculate correlation between two sets of metrics
        
        Args:
            metrics1: First set of metrics
            metrics2: Second set of metrics
            
        Returns:
            Correlation coefficient (-1 to 1)
        """
        try:
            # Find common metrics
            common_keys = set(metrics1.keys()) & set(metrics2.keys())
            
            if len(common_keys) < 2:
                return 0.0
            
            # Extract values for common metrics
            values1 = [metrics1[key] for key in common_keys]
            values2 = [metrics2[key] for key in common_keys]
            
            # Calculate Pearson correlation
            correlation = np.corrcoef(values1, values2)[0, 1]
            
            return correlation if not np.isnan(correlation) else 0.0
            
        except Exception as e:
            logger.debug(f"Error calculating correlation: {e}")
            return 0.0
    
    def _identify_trending_entities(self, data: Dict[str, Any], head_name: str) -> Dict[str, Dict[str, Any]]:
        """
        Identify trending entities in the data
        
        Args:
            data: Data to analyze
            head_name: Name of the head
            
        Returns:
            Dictionary of trending entities and their trend data
        """
        trending = {}
        
        try:
            # Extract company names, technologies, or other entities
            entities = []
            
            if "company" in data:
                entities.append(data["company"])
            if "product_name" in data:
                entities.append(data["product_name"])
            if "technology_name" in data:
                entities.append(data["technology_name"])
            if "patent_number" in data:
                entities.append(data["patent_number"])
            
            # Calculate trend strength based on data characteristics
            for entity in entities:
                if entity:
                    trend_strength = 0.5  # Base strength
                    
                    # Adjust based on data characteristics
                    if "confidence_score" in data:
                        trend_strength += float(data["confidence_score"]) * 0.3
                    
                    if "sentiment_score" in data:
                        sentiment = abs(float(data["sentiment_score"]))
                        trend_strength += sentiment * 0.2
                    
                    trending[entity] = {
                        "strength": min(1.0, trend_strength),
                        "type": "company" if "company" in data else "product",
                        "detected_in": head_name
                    }
        
        except Exception as e:
            logger.debug(f"Error identifying trending entities: {e}")
        
        return trending
    
    def _count_cross_head_mentions(self, entity: str, recent_data: Dict[str, List[Dict[str, Any]]]) -> int:
        """
        Count how many heads mention a specific entity
        
        Args:
            entity: Entity to search for
            recent_data: Recent data from all heads
            
        Returns:
            Number of heads mentioning the entity
        """
        mention_count = 0
        
        try:
            for head_name, data_list in recent_data.items():
                for data_point in data_list:
                    # Check if entity appears in the data
                    if self._entity_in_data(entity, data_point):
                        mention_count += 1
                        break  # Count each head only once
        
        except Exception as e:
            logger.debug(f"Error counting cross-head mentions: {e}")
        
        return mention_count
    
    def _entity_in_data(self, entity: str, data: Dict[str, Any]) -> bool:
        """
        Check if an entity appears in data
        
        Args:
            entity: Entity to search for
            data: Data to search in
            
        Returns:
            True if entity found, False otherwise
        """
        try:
            # Convert data to string and search
            data_str = json.dumps(data).lower()
            entity_lower = entity.lower()
            
            return entity_lower in data_str
        
        except Exception:
            return False
    
    def _find_text_anomalies(self, data: Dict[str, Any], head_name: str) -> List[Dict[str, Any]]:
        """
        Find anomalies in text data
        
        Args:
            data: Data to analyze
            head_name: Name of the head
            
        Returns:
            List of text anomalies
        """
        anomalies = []
        
        try:
            # Look for unusual text patterns
            text_fields = ["title", "message", "ad_copy", "summary"]
            
            for field in text_fields:
                if field in data and data[field]:
                    text = str(data[field])
                    
                    # Check for unusual length
                    if len(text) > 1000:  # Very long text
                        anomaly = {
                            "pattern_type": "anomaly",
                            "head_name": head_name,
                            "metric": f"{field}_length",
                            "value": len(text),
                            "threshold": 1000,
                            "description": f"Unusually long {field} detected",
                            "significance": 0.7,
                            "anomaly_type": "text_length",
                            "detected_at": datetime.now().isoformat()
                        }
                        anomalies.append(anomaly)
                    
                    # Check for unusual characters or patterns
                    if re.search(r'[A-Z]{5,}', text):  # Multiple consecutive caps
                        anomaly = {
                            "pattern_type": "anomaly",
                            "head_name": head_name,
                            "metric": f"{field}_caps",
                            "value": "multiple_caps",
                            "threshold": "normal",
                            "description": f"Unusual capitalization pattern in {field}",
                            "significance": 0.6,
                            "anomaly_type": "text_pattern",
                            "detected_at": datetime.now().isoformat()
                        }
                        anomalies.append(anomaly)
        
        except Exception as e:
            logger.debug(f"Error finding text anomalies: {e}")
        
        return anomalies
    
    def _events_might_be_related(self, event1: Dict[str, Any], event2: Dict[str, Any]) -> bool:
        """
        Check if two events might be related
        
        Args:
            event1: First event
            event2: Second event
            
        Returns:
            True if events might be related, False otherwise
        """
        try:
            # Check for common entities
            entities1 = set()
            entities2 = set()
            
            # Extract entities from both events
            for event, entities in [(event1, entities1), (event2, entities2)]:
                for key in ["company", "product_name", "technology_name", "patent_number"]:
                    if key in event and event[key]:
                        entities.add(str(event[key]).lower())
            
            # Check for common entities
            common_entities = entities1 & entities2
            
            # Check for similar topics or keywords
            text1 = json.dumps(event1).lower()
            text2 = json.dumps(event2).lower()
            
            # Simple keyword matching
            keywords1 = set(re.findall(r'\b\w{4,}\b', text1))
            keywords2 = set(re.findall(r'\b\w{4,}\b', text2))
            
            common_keywords = keywords1 & keywords2
            
            # Events are related if they share entities or many keywords
            return len(common_entities) > 0 or len(common_keywords) > 3
        
        except Exception as e:
            logger.debug(f"Error checking event relationship: {e}")
            return False
    
    def _rank_patterns_by_significance(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank patterns by their significance score
        
        Args:
            patterns: List of patterns to rank
            
        Returns:
            Ranked list of patterns
        """
        try:
            # Sort by significance (descending)
            ranked = sorted(patterns, key=lambda x: x.get("significance", 0), reverse=True)
            
            # Filter out low-significance patterns
            significant = [p for p in ranked if p.get("significance", 0) > 0.3]
            
            return significant
        
        except Exception as e:
            logger.error(f"Error ranking patterns: {e}")
            return patterns
    
    async def get_pattern_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all detected patterns
        
        Returns:
            Pattern summary statistics
        """
        try:
            # This would aggregate pattern data from the database
            # For now, return mock summary
            return {
                "total_patterns": 0,
                "patterns_by_type": {},
                "most_significant_patterns": [],
                "trending_entities": [],
                "last_updated": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error getting pattern summary: {e}")
            return {}
    
    async def clear_cache(self):
        """Clear the pattern cache"""
        self.pattern_cache.clear()
        self.correlation_matrix.clear()
        self.trend_indicators.clear()
        logger.info("🔍 Pattern cache cleared")
