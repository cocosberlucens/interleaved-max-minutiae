#!/usr/bin/env python3
"""
Direct test of Cycling74 connector to fetch metro documentation
"""

import asyncio
from pathlib import Path

import yaml

from src.knowledge import Cycling74Connector


async def test_metro_docs():
    """Test fetching metro documentation directly"""
    print("🌐 Testing Direct Cycling74 Documentation Fetch")
    print("=" * 55)

    # Load configuration
    config_path = Path("config/config.development.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Create connector
    cycling74 = Cycling74Connector(config.get("knowledge_sources", {}).get("cycling74_docs", {}))

    try:
        await cycling74.initialize()
        print("✅ Cycling74 connector initialized")

        # Test getting metro documentation
        print("\n📖 Fetching 'metro' object documentation...")
        metro_doc = await cycling74.get_object_doc("metro")

        if metro_doc:
            print("✅ Metro documentation retrieved!")
            print(f"\n📋 Metro Object Details:")
            print(f"   Name: {metro_doc.get('object_name')}")
            print(f"   URL: {metro_doc.get('url')}")
            print(f"   Description: {metro_doc.get('description', 'N/A')}")

            inlets = metro_doc.get("inlets", [])
            outlets = metro_doc.get("outlets", [])
            print(f"   Inlets: {len(inlets)}")
            print(f"   Outlets: {len(outlets)}")

            if inlets:
                print(f"\n   📥 Inlets:")
                for i, inlet in enumerate(inlets):
                    print(f"      {i}: {inlet.get('type', 'unknown')} - {inlet.get('description', 'N/A')}")

            if outlets:
                print(f"\n   📤 Outlets:")
                for i, outlet in enumerate(outlets):
                    print(f"      {i}: {outlet.get('type', 'unknown')} - {outlet.get('description', 'N/A')}")

            attributes = metro_doc.get("attributes", {})
            if attributes:
                print(f"\n   ⚙️  Attributes:")
                for name, attr in attributes.items():
                    print(f"      {name}: {attr.get('type', 'unknown')} - {attr.get('description', 'N/A')}")

            examples = metro_doc.get("examples", [])
            if examples:
                print(f"\n   💡 Examples: {len(examples)} found")
                for i, example in enumerate(examples[:2], 1):
                    print(f"      Example {i}: {example.get('description', 'N/A')[:80]}...")

            related = metro_doc.get("related_objects", [])
            if related:
                print(f"\n   🔗 Related Objects: {', '.join(related[:5])}")
        else:
            print("❌ No documentation found for 'metro'")

        # Test search functionality
        print("\n\n🔍 Testing search functionality...")
        search_results = await cycling74.search("timing")
        print(f"Search for 'timing': {len(search_results)} results")

        for result in search_results[:3]:
            print(f"   - {result.get('object_name', 'Unknown')}: {result.get('description', 'N/A')[:60]}...")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()

    finally:
        await cycling74.close()


if __name__ == "__main__":
    asyncio.run(test_metro_docs())
