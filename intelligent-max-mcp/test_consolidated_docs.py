#!/usr/bin/env python3
"""
Test the consolidated documentation loading
"""

import asyncio
import yaml
from pathlib import Path
from src.knowledge import KnowledgeFusionEngine


async def test_consolidated_documentation():
    """Test loading from the consolidated Max MSP Documentation Listings.md"""
    print("📚 Testing Consolidated Max/MSP Documentation Loading")
    print("=" * 60)
    
    # Load configuration
    config_path = Path("config/config.development.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    # Create and initialize the knowledge engine
    print("🧠 Initializing Knowledge Fusion Engine...")
    engine = KnowledgeFusionEngine(config.get("knowledge_sources", {}))
    
    try:
        await engine.initialize()
        print("✅ Knowledge sources initialized!")
        
        # Show object index stats
        cycling74 = engine.cycling74
        total_objects = len(cycling74.object_index)
        print(f"\n📊 Consolidated Documentation Statistics:")
        print(f"   Total entries loaded: {total_objects}")
        
        # Check for source information
        sources = set()
        categories = set()
        has_hrefs = 0
        
        for obj_name, obj_info in cycling74.object_index.items():
            source = obj_info.get("source", "unknown")
            sources.add(source)
            categories.add(obj_info.get("category", "unknown"))
            if obj_info.get("hrefs"):
                has_hrefs += 1
        
        print(f"   Sources: {', '.join(sources)}")
        print(f"   Categories: {len(categories)} unique categories")
        print(f"   Entries with URLs: {has_hrefs}")
        
        # Test specific objects
        test_objects = ["metro", "pattrhub", "jsui", "buffer~", "cycle~"]
        print(f"\n🎯 Testing Specific Objects:")
        
        for obj in test_objects:
            if obj in cycling74.object_index:
                info = cycling74.object_index[obj]
                urls = info.get("hrefs", [])
                source = info.get("source", "unknown")
                print(f"   ✅ {obj}: {source} source, {len(urls)} URL(s)")
                if urls:
                    print(f"      → {urls[0]}")
            else:
                print(f"   ❌ {obj}: NOT FOUND")
        
        # Show sample of categories found
        print(f"\n📂 Sample Categories Found:")
        category_samples = {}
        for obj_name, obj_info in cycling74.object_index.items():
            category = obj_info.get("category", "unknown")
            if category not in category_samples:
                category_samples[category] = []
            if len(category_samples[category]) < 3:
                category_samples[category].append(obj_name)
        
        for category, objects in sorted(category_samples.items()):
            print(f"   {category}: {', '.join(objects)}")
        
        # Test search functionality with the consolidated data
        print(f"\n🔍 Testing Search with Consolidated Data:")
        
        search_tests = ["pattr", "audio", "timing", "ui", "tutorial"]
        for query in search_tests:
            result = await engine.query(query)
            print(f"   '{query}': {result.total_results} results")
            
            if result.entries:
                top_result = result.entries[0]
                name = top_result.object_name or top_result.pattern_name or "Unknown"
                print(f"      → Top: {name} (confidence: {top_result.confidence:.3f})")
        
        print(f"\n🎉 Consolidated documentation test completed!")
        print(f"📈 Successfully loaded {total_objects} entries from your single source of truth!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await engine.cycling74.close()


if __name__ == "__main__":
    asyncio.run(test_consolidated_documentation())