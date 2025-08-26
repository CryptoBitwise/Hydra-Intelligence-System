"""
HYDRA AI Analyzer
Uses Ollama LLMs to analyze data and provide intelligent insights
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
import json
import httpx
from datetime import datetime

from ..core.config import config

logger = logging.getLogger(__name__)

class HydraAnalyzer:
    """
    AI-powered analyzer using Ollama LLMs
    Processes data from all HYDRA heads and provides intelligent insights
    """
    
    def __init__(self):
        self.ollama_url = config.OLLAMA_BASE_URL
        self.model = config.OLLAMA_MODEL
        self.client = httpx.AsyncClient(timeout=30.0)
        
        # Analysis prompts for different heads
        self.analysis_prompts = {
            "price_watch": """
            Analyze this pricing data and provide insights:
            - Is this a significant price change?
            - What might be driving this change?
            - Is this an opportunity or threat?
            - What actions should be taken?
            
            Data: {data}
            
            Provide analysis in JSON format with:
            - summary: Brief summary
            - sentiment: -1 to 1 score
            - confidence_score: 0 to 1
            - insights: List of key insights
            - recommendations: List of actionable recommendations
            - risk_level: low/medium/high
            """,
            
            "job_spy": """
            Analyze this job posting data and provide insights:
            - What does this reveal about company strategy?
            - Are there new technology investments?
            - What market trends does this indicate?
            - Is this an opportunity or threat?
            
            Data: {data}
            
            Provide analysis in JSON format with:
            - summary: Brief summary
            - sentiment: -1 to 1 score
            - confidence_score: 0 to 1
            - insights: List of key insights
            - recommendations: List of actionable recommendations
            - strategic_implications: What this means for business
            """,
            
            "tech_radar": """
            Analyze this technology adoption data and provide insights:
            - What technology trends are emerging?
            - How does this compare to competitors?
            - What market opportunities exist?
            - What risks should be considered?
            
            Data: {data}
            
            Provide analysis in JSON format with:
            - summary: Brief summary
            - sentiment: -1 to 1 score
            - confidence_score: 0 to 1
            - insights: List of key insights
            - recommendations: List of actionable recommendations
            - market_impact: low/medium/high
            """,
            
            "social_pulse": """
            Analyze this social media sentiment data and provide insights:
            - What is the overall sentiment trend?
            - Are there emerging topics or concerns?
            - What does this reveal about brand perception?
            - What actions should be taken?
            
            Data: {data}
            
            Provide analysis in JSON format with:
            - summary: Brief summary
            - sentiment: -1 to 1 score
            - confidence_score: 0 to 1
            - insights: List of key insights
            - recommendations: List of actionable recommendations
            - urgency: low/medium/high
            """,
            
            "patent_hawk": """
            Analyze this patent data and provide insights:
            - What new technologies are being developed?
            - How does this affect competitive landscape?
            - What opportunities exist for partnerships?
            - What threats should be monitored?
            
            Data: {data}
            
            Provide analysis in JSON format with:
            - summary: Brief summary
            - sentiment: -1 to 1 score
            - confidence_score: 0 to 1
            - insights: List of key insights
            - recommendations: List of actionable recommendations
            - innovation_level: low/medium/high
            """,
            
            "ad_tracker": """
            Analyze this advertisement data and provide insights:
            - What marketing strategies are being used?
            - How does this compare to our approach?
            - What market opportunities exist?
            - What competitive threats should be monitored?
            
            Data: {data}
            
            Provide analysis in JSON format with:
            - summary: Brief summary
            - sentiment: -1 to 1 score
            - confidence_score: 0 to 1
            - insights: List of key insights
            - recommendations: List of actionable recommendations
            - competitive_intensity: low/medium/high
            """
        }
    
    async def analyze(self, head_name: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Analyze data from a specific head using AI
        
        Args:
            head_name: Name of the head that collected the data
            data: Data to analyze
            
        Returns:
            Analysis results or None if analysis fails
        """
        try:
            logger.info(f"🤖 Analyzing data from {head_name}")
            
            # Get the appropriate prompt for this head
            prompt_template = self.analysis_prompts.get(head_name, self.analysis_prompts["price_watch"])
            prompt = prompt_template.format(data=json.dumps(data, indent=2))
            
            # Get AI analysis from Ollama
            analysis_text = await self._get_ollama_analysis(prompt)
            
            if not analysis_text:
                logger.warning(f"🤖 No analysis received from Ollama for {head_name}")
                return None
            
            # Parse the analysis
            analysis_result = await self._parse_analysis(analysis_text, head_name, data)
            
            # Add metadata
            analysis_result.update({
                "head_name": head_name,
                "analyzed_at": datetime.now().isoformat(),
                "model_used": self.model,
                "raw_analysis": analysis_text
            })
            
            logger.info(f"🤖 Analysis completed for {head_name}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"🤖 Error analyzing data from {head_name}: {e}")
            return None
    
    async def _get_ollama_analysis(self, prompt: str) -> Optional[str]:
        """
        Get analysis from Ollama LLM
        
        Args:
            prompt: Analysis prompt
            
        Returns:
            Analysis text or None if failed
        """
        try:
            # Prepare the request payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Lower temperature for more consistent analysis
                    "top_p": 0.9,
                    "max_tokens": 2000
                }
            }
            
            # Make request to Ollama
            response = await self.client.post(
                f"{self.ollama_url}/api/generate",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                logger.error(f"🤖 Ollama request failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"🤖 Error calling Ollama: {e}")
            return None
    
    async def _parse_analysis(self, analysis_text: str, head_name: str, original_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse the AI analysis text into structured format
        
        Args:
            analysis_text: Raw analysis from Ollama
            head_name: Name of the head
            original_data: Original data that was analyzed
            
        Returns:
            Structured analysis result
        """
        try:
            # Try to extract JSON from the response
            json_start = analysis_text.find('{')
            json_end = analysis_text.rfind('}') + 1
            
            if json_start != -1 and json_end != 0:
                json_text = analysis_text[json_start:json_end]
                parsed = json.loads(json_text)
                
                # Validate and normalize the parsed data
                return self._normalize_analysis(parsed, head_name, original_data)
            else:
                # Fallback: create structured analysis from text
                return self._create_fallback_analysis(analysis_text, head_name, original_data)
                
        except json.JSONDecodeError as e:
            logger.warning(f"🤖 Failed to parse JSON from analysis: {e}")
            return self._create_fallback_analysis(analysis_text, head_name, original_data)
        except Exception as e:
            logger.error(f"🤖 Error parsing analysis: {e}")
            return self._create_fallback_analysis(analysis_text, head_name, original_data)
    
    def _normalize_analysis(self, parsed: Dict[str, Any], head_name: str, original_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize and validate parsed analysis
        
        Args:
            parsed: Parsed analysis data
            head_name: Name of the head
            original_data: Original data
            
        Returns:
            Normalized analysis
        """
        # Ensure required fields exist with defaults
        normalized = {
            "summary": parsed.get("summary", "AI analysis completed"),
            "sentiment": self._clamp_float(parsed.get("sentiment", 0.0), -1.0, 1.0),
            "confidence_score": self._clamp_float(parsed.get("confidence_score", 0.5), 0.0, 1.0),
            "insights": parsed.get("insights", []),
            "recommendations": parsed.get("recommendations", []),
            "risk_level": parsed.get("risk_level", "medium"),
            "urgency": parsed.get("urgency", "medium"),
            "market_impact": parsed.get("market_impact", "medium"),
            "innovation_level": parsed.get("innovation_level", "medium"),
            "competitive_intensity": parsed.get("competitive_intensity", "medium"),
            "strategic_implications": parsed.get("strategic_implications", "")
        }
        
        # Ensure lists are actually lists
        if not isinstance(normalized["insights"], list):
            normalized["insights"] = [str(normalized["insights"])]
        if not isinstance(normalized["recommendations"], list):
            normalized["recommendations"] = [str(normalized["recommendations"])]
        
        return normalized
    
    def _create_fallback_analysis(self, analysis_text: str, head_name: str, original_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create fallback analysis when JSON parsing fails
        
        Args:
            analysis_text: Raw analysis text
            head_name: Name of the head
            original_data: Original data
            
        Returns:
            Fallback analysis structure
        """
        # Simple sentiment analysis based on keywords
        sentiment = self._simple_sentiment_analysis(analysis_text)
        
        return {
            "summary": analysis_text[:200] + "..." if len(analysis_text) > 200 else analysis_text,
            "sentiment": sentiment,
            "confidence_score": 0.6,  # Lower confidence for fallback
            "insights": [f"Analysis from {head_name} head", "AI analysis completed"],
            "recommendations": ["Review raw analysis text", "Consider manual review"],
            "risk_level": "medium",
            "urgency": "medium",
            "market_impact": "medium",
            "innovation_level": "medium",
            "competitive_intensity": "medium",
            "strategic_implications": "Requires manual review"
        }
    
    def _simple_sentiment_analysis(self, text: str) -> float:
        """
        Simple sentiment analysis based on keywords
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment score from -1 to 1
        """
        text_lower = text.lower()
        
        positive_words = ["opportunity", "positive", "growth", "advantage", "benefit", "success", "improvement"]
        negative_words = ["threat", "negative", "risk", "problem", "concern", "decline", "failure"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count == 0 and negative_count == 0:
            return 0.0
        
        total = positive_count + negative_count
        sentiment = (positive_count - negative_count) / total
        
        return self._clamp_float(sentiment, -1.0, 1.0)
    
    def _clamp_float(self, value: float, min_val: float, max_val: float) -> float:
        """Clamp a float value between min and max"""
        return max(min_val, min(max_val, value))
    
    async def batch_analyze(self, data_batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze multiple data points in batch
        
        Args:
            data_batch: List of data dictionaries with 'head_name' and 'data' keys
            
        Returns:
            List of analysis results
        """
        tasks = []
        for item in data_batch:
            head_name = item.get("head_name")
            data = item.get("data", {})
            if head_name and data:
                task = self.analyze(head_name, data)
                tasks.append(task)
        
        # Run all analyses concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions and return valid results
        valid_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"🤖 Batch analysis error: {result}")
            elif result is not None:
                valid_results.append(result)
        
        return valid_results
    
    async def close(self):
        """Close the analyzer and cleanup resources"""
        await self.client.aclose()
        logger.info("🤖 HydraAnalyzer closed")
