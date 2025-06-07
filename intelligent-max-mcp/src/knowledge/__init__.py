"""
Knowledge module - The brain of the Intelligent Max MCP Server

This module provides the fusion of multiple knowledge sources:
- Official Cycling '74 documentation
- Our interleaved-max-minutiae repository
- Discovered patterns and learned insights
"""

from .engine import KnowledgeFusionEngine, KnowledgeEntry, SearchResult, Pattern
from .cycling74_connector import Cycling74Connector
from .minutiae_connector import MinutiaeConnector

__all__ = [
    "KnowledgeFusionEngine",
    "KnowledgeEntry", 
    "SearchResult",
    "Pattern",
    "Cycling74Connector",
    "MinutiaeConnector"
]