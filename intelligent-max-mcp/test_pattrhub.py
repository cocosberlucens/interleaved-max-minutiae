#!/usr/bin/env python3
"""
Test the enhanced object loading to find pattrhub
"""

import asyncio
from pathlib import Path

import yaml

from src.knowledge import KnowledgeFusionEngine


async def test_pattrhub_search():
    """Test searching for pattrhub with our enhanced object index"""
    print("🔍 Testing Enhanced Object Index for 'pattrhub'")
    print("=" * 55)

    # Load configuration
    config_path = Path("config/config.development.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Create and initialize the knowledge engine
    print("🧠 Initializing Knowledge Fusion Engine...")
    engine = KnowledgeFusionEngine(config.get("knowledge_sources", {}))

    try:
        await engine.initialize()
        print("✅ Knowledge sources initialized successfully!")

        # Show object index stats
        cycling74 = engine.cycling74
        total_objects = len(cycling74.object_index)
        print(f"\n📊 Object Index Statistics:")
        print(f"   Total objects loaded: {total_objects}")

        # Test search for 'pattrhub'
        print(f"\n🎯 Searching for 'pattrhub'...")
        search_result = await engine.query("pattrhub")

        print(f"\n📊 Search Results:")
        print(f"   Query: '{search_result.query}'")
        print(f"   Total results: {search_result.total_results}")
        print(f"   Query time: {search_result.query_time_ms:.2f}ms")

        if search_result.entries:
            print(f"\n📚 Results:")
            for i, entry in enumerate(search_result.entries, 1):
                name = entry.object_name or entry.pattern_name or "Unknown"
                print(f"  {i}. {name} (confidence: {entry.confidence:.3f})")
                print(f"     Source: {entry.source}")
                print(f"     Description: {entry.description}")
                print(f"     Tags: {', '.join(entry.tags)}")
                print()
        else:
            print("❌ No results found for 'pattrhub'")

        # Test some other pattr objects
        print("\n🔍 Testing other pattr objects...")
        for obj in ["pattr", "pattrstorage", "pattrforward"]:
            result = await engine.query(obj)
            found = "✅" if result.entries else "❌"
            print(f"   {found} {obj}: {result.total_results} results")

        # Show a sampling of all objects to verify comprehensive loading
        print(f"\n📋 Sample of loaded objects:")
        sample_objects = list(cycling74.object_index.keys())[:20]
        for obj in sample_objects:
            info = cycling74.object_index[obj]
            print(f"   - {obj} ({info['category']})")

        if total_objects > 20:
            print(f"   ... and {total_objects - 20} more objects!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()

    finally:
        await engine.cycling74.close()


if __name__ == "__main__":
    asyncio.run(test_pattrhub_search())
