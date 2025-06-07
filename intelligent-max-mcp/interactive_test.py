#!/usr/bin/env python3
"""
Interactive test of the Knowledge Fusion Engine

Try searching for any Max object or concept!
"""

import asyncio
from pathlib import Path

import yaml

from src.knowledge import KnowledgeFusionEngine


async def interactive_search():
    """Interactive search interface"""
    print("🎵 Interactive Intelligent Max MCP Knowledge Search")
    print("=" * 55)
    print("Search across Cycling74 docs AND your minutiae repository!")
    print("Try searching for: metro, counter, jsui, temporal, buffer, etc.")
    print("Type 'quit' to exit")
    print()

    # Load configuration
    config_path = Path("config/config.development.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Initialize engine
    engine = KnowledgeFusionEngine(config.get("knowledge_sources", {}))
    await engine.initialize()

    try:
        while True:
            # Get user input
            query = input("🔍 Search> ").strip()

            if query.lower() in ["quit", "exit", "q"]:
                print("👋 Goodbye!")
                break

            if not query:
                continue

            # Perform search
            print(f"\n🧠 Searching for '{query}'...")
            start_time = asyncio.get_event_loop().time()

            result = await engine.query(query)

            end_time = asyncio.get_event_loop().time()
            search_time = (end_time - start_time) * 1000

            # Display results
            print(f"📊 Found {result.total_results} results in {search_time:.1f}ms")

            if result.suggestions:
                print(f"💡 Related: {', '.join(result.suggestions)}")

            if result.entries:
                print("\n📚 Top Results:")
                for i, entry in enumerate(result.entries[:3], 1):
                    name = entry.object_name or entry.pattern_name or "Unknown"
                    source_emoji = {
                        "cycling74": "🌐",
                        "minutiae": "📂",
                        "discovery": "💡",
                    }.get(entry.source, "❓")

                    print(f"  {i}. {source_emoji} {name} (confidence: {entry.confidence:.3f})")
                    print(f"     {entry.description[:80]}...")

                    if entry.tags:
                        print(f"     Tags: {', '.join(entry.tags[:4])}")
                    print()
            else:
                print("❌ No results found")

            print("-" * 50)

    finally:
        await engine.cycling74.close()


if __name__ == "__main__":
    asyncio.run(interactive_search())
