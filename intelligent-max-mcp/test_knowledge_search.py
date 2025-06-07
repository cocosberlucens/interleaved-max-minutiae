#!/usr/bin/env python3
"""
Test script for the Knowledge Fusion Engine

Let's see our recursive intelligence in action by searching for 'metro'!
"""

import asyncio
import json
import yaml
from pathlib import Path

from src.knowledge import KnowledgeFusionEngine


async def test_metro_search():
    """Test searching for 'metro' object across all knowledge sources"""
    print("🎵 Testing Intelligent Max MCP Knowledge Fusion Engine")
    print("=" * 60)
    
    # Load configuration
    config_path = Path("config/config.development.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Create and initialize the knowledge engine
    print("\n🧠 Initializing Knowledge Fusion Engine...")
    engine = KnowledgeFusionEngine(config.get("knowledge_sources", {}))
    
    try:
        await engine.initialize()
        print("✅ Knowledge sources initialized successfully!")
        
        # Test search for 'metro'
        print("\n🔍 Searching for 'metro' across all knowledge sources...")
        search_result = await engine.query("metro")
        
        print(f"\n📊 Search Results Summary:")
        print(f"   Query: '{search_result.query}'")
        print(f"   Total results: {search_result.total_results}")
        print(f"   Sources queried: {', '.join(search_result.sources_queried)}")
        print(f"   Query time: {search_result.query_time_ms:.2f}ms")
        
        if search_result.suggestions:
            print(f"   Related suggestions: {', '.join(search_result.suggestions)}")
        
        print("\n📚 Detailed Results:")
        print("-" * 40)
        
        for i, entry in enumerate(search_result.entries[:5], 1):  # Top 5 results
            print(f"\n{i}. {entry.object_name or entry.pattern_name or 'Unknown'}")
            print(f"   Source: {entry.source}")
            print(f"   Confidence: {entry.confidence:.3f}")
            print(f"   Description: {entry.description[:100]}...")
            
            if entry.source == "cycling74" and "inlets" in entry.content:
                inlets = entry.content.get("inlets", [])
                outlets = entry.content.get("outlets", [])
                print(f"   Inlets: {len(inlets)}, Outlets: {len(outlets)}")
                
                if inlets:
                    print(f"   Inlet 0: {inlets[0].get('description', 'N/A')}")
            
            if entry.tags:
                print(f"   Tags: {', '.join(entry.tags[:5])}")
            
            print(f"   Timestamp: {entry.timestamp}")
        
        # Test context-aware search
        print("\n\n🎯 Testing Context-Aware Search...")
        context = {
            "domain": "timing",
            "recent_objects": ["counter", "bang"]
        }
        
        contextual_result = await engine.query("metro", context)
        print(f"   With timing context: {contextual_result.total_results} results")
        
        if contextual_result.entries:
            top_result = contextual_result.entries[0]
            print(f"   Top result confidence: {top_result.confidence:.3f}")
            print(f"   (vs. {search_result.entries[0].confidence:.3f} without context)")
        
        # Test pattern analysis (if we have any metro-related patterns)
        print("\n\n🔬 Testing Pattern Analysis...")
        sample_patcher = {
            "patcher": {
                "boxes": [
                    {"class": "metro", "text": "metro 100"},
                    {"class": "counter", "text": "counter"},
                    {"class": "print", "text": "print count"}
                ]
            }
        }
        
        analysis = await engine.analyze_patcher(sample_patcher)
        print(f"   Patterns found: {len(analysis['patterns_found'])}")
        print(f"   Suggestions: {len(analysis['suggestions'])}")
        print(f"   Optimizations: {len(analysis['optimization_opportunities'])}")
        
        print("\n🎉 Knowledge Fusion Engine test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        await engine.cycling74.close()


async def test_minutiae_indexing():
    """Test the minutiae repository indexing"""
    print("\n\n📂 Testing Minutiae Repository Indexing...")
    print("-" * 50)
    
    config_path = Path("config/config.development.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    from src.knowledge import MinutiaeConnector
    
    minutiae = MinutiaeConnector(config.get("knowledge_sources", {}).get("minutiae_repo", {}))
    
    try:
        await minutiae.initialize()
        
        # Show index statistics
        total_entries = sum(len(entries) for entries in minutiae.knowledge_index.values())
        print(f"📊 Repository Index Statistics:")
        
        for category, entries in minutiae.knowledge_index.items():
            if entries:
                print(f"   {category.capitalize()}: {len(entries)} entries")
                
                # Show a sample entry
                sample = entries[0]
                print(f"      Example: {sample.get('name', sample.get('file_path', 'Unknown'))}")
        
        print(f"\n   Total indexed entries: {total_entries}")
        
        # Test search within minutiae
        results = await minutiae.search("metro")
        print(f"\n🔍 Minutiae search for 'metro': {len(results)} results")
        
        for result in results[:3]:
            print(f"   - {result.get('name', 'Unknown')} (relevance: {result.get('relevance', 0):.3f})")
        
    except Exception as e:
        print(f"❌ Error testing minutiae: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🚀 Starting Intelligent Max MCP Knowledge Engine Test")
    print("This tests the recursive beauty of our musical intelligence system!")
    
    asyncio.run(test_metro_search())
    asyncio.run(test_minutiae_indexing())