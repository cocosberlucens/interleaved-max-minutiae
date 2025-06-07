"""
Cycling '74 Documentation Connector

Interfaces with the official Max/MSP documentation to provide
real-time access to object references, tutorials, and guides.
"""

import asyncio
import json
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import quote, urljoin

import aiohttp
from aiofiles import open as aio_open
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Cycling74Connector:
    """
    Connector for Cycling '74 official documentation.

    Uses the legacy Max 8 documentation which is more stable
    and comprehensive than newer versions.
    """

    def __init__(self, config: Dict[str, Any]):
        self.base_url = config.get("base_url", "https://docs.cycling74.com/legacy/max8")
        self.cache_dir = Path(config.get("cache_dir", "./cache/cycling74"))
        self.cache_duration = timedelta(seconds=config.get("cache_duration", 3600))
        self.max_concurrent = config.get("max_concurrent_requests", 5)
        self.timeout = config.get("request_timeout", 30)
        self.retry_attempts = config.get("retry_attempts", 3)
        self.retry_delay = config.get("retry_delay", 1.0)

        # Create cache directory
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Session management
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(self.max_concurrent)

        # Object reference cache
        self.object_index: Dict[str, Dict[str, Any]] = {}
        self.index_loaded = False

        logger.info(f"Cycling74 Connector initialized with base URL: {self.base_url}")

    async def initialize(self):
        """Initialize the connector and load object index"""
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
        await self._load_object_index()

    async def close(self):
        """Close the connector and cleanup resources"""
        if self.session:
            await self.session.close()

    async def get_object_doc(self, object_name: str) -> Optional[Dict[str, Any]]:
        """
        Get documentation for a specific Max object.

        Args:
            object_name: Name of the Max object (e.g., "metro", "cycle~")

        Returns:
            Dictionary containing object documentation or None if not found
        """
        # Normalize object name
        object_name = object_name.lower().strip()

        # Check cache first
        cached = await self._get_cached(f"objects/{object_name}.json")
        if cached:
            return cached

        # Construct URL for object reference
        url = urljoin(self.base_url, f"/refpages/{quote(object_name)}")

        try:
            html = await self._fetch_with_retry(url)
            if not html:
                return None

            # Parse the documentation
            doc = await self._parse_object_doc(html, object_name)

            # Cache the result
            if doc:
                await self._cache_result(f"objects/{object_name}.json", doc)

            return doc

        except Exception as e:
            logger.error(f"Error fetching documentation for {object_name}: {e}")
            return None

    async def search(self, query: str) -> List[Dict[str, Any]]:
        """
        Search the documentation for relevant content.

        Args:
            query: Search query

        Returns:
            List of relevant documentation entries
        """
        results = []
        query_lower = query.lower()

        # If we have an object index, search it first
        if self.object_index:
            for obj_name, obj_info in self.object_index.items():
                relevance = 0.0

                # Check object name
                if query_lower in obj_name.lower():
                    relevance += 0.5

                # Check description
                desc = obj_info.get("description", "").lower()
                if query_lower in desc:
                    relevance += 0.3

                # Check tags/categories
                for tag in obj_info.get("tags", []):
                    if query_lower in tag.lower():
                        relevance += 0.2

                if relevance > 0:
                    # Fetch full documentation if highly relevant
                    if relevance > 0.5:
                        full_doc = await self.get_object_doc(obj_name)
                        if full_doc:
                            results.append(full_doc)
                    else:
                        # Add basic info
                        results.append(
                            {
                                "object_name": obj_name,
                                "description": obj_info.get("description", ""),
                                "category": obj_info.get("category", ""),
                                "relevance": relevance,
                            }
                        )

        # Sort by relevance
        results.sort(key=lambda x: x.get("relevance", 0), reverse=True)

        return results[:20]  # Top 20 results

    async def get_tutorial(self, tutorial_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific tutorial by name"""
        # Check cache
        cached = await self._get_cached(f"tutorials/{tutorial_name}.json")
        if cached:
            return cached

        # Construct URL
        url = urljoin(self.base_url, f"/tutorials/{quote(tutorial_name)}")

        try:
            html = await self._fetch_with_retry(url)
            if not html:
                return None

            # Parse tutorial
            tutorial = await self._parse_tutorial(html, tutorial_name)

            # Cache result
            if tutorial:
                await self._cache_result(f"tutorials/{tutorial_name}.json", tutorial)

            return tutorial

        except Exception as e:
            logger.error(f"Error fetching tutorial {tutorial_name}: {e}")
            return None

    # Private helper methods

    async def _load_object_index(self):
        """Load the object index for quick searching"""
        try:
            # Try to load from cache first
            cached = await self._get_cached("object_index.json")
            if cached:
                self.object_index = cached
                self.index_loaded = True
                logger.info(f"Loaded object index with {len(self.object_index)} objects")
                return

            # Try to load from minutiae repository's comprehensive listing
            minutiae_listing = await self._load_from_minutiae_listing()
            if minutiae_listing:
                self.object_index = minutiae_listing
            else:
                # Fall back to default objects
                self.object_index = self._get_default_object_index()

            # Cache the index
            await self._cache_result("object_index.json", self.object_index)
            self.index_loaded = True
            logger.info(f"Loaded object index with {len(self.object_index)} objects")

        except Exception as e:
            logger.error(f"Error loading object index: {e}")
            self.object_index = {}

    async def _fetch_with_retry(self, url: str) -> Optional[str]:
        """Fetch URL with retry logic"""
        async with self.semaphore:
            for attempt in range(self.retry_attempts):
                try:
                    if not self.session:
                        logger.error("Session not initialized")
                        return None

                    async with self.session.get(url) as response:
                        if response.status == 200:
                            return await response.text()
                        elif response.status == 404:
                            logger.debug(f"404 Not Found: {url}")
                            return None
                        else:
                            logger.warning(f"HTTP {response.status} for {url}")

                except asyncio.TimeoutError:
                    logger.warning(f"Timeout fetching {url} (attempt {attempt + 1})")
                except Exception as e:
                    logger.error(f"Error fetching {url}: {e}")

                if attempt < self.retry_attempts - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))

            return None

    async def _load_from_minutiae_listing(self) -> Optional[Dict[str, Dict[str, Any]]]:
        """
        Load comprehensive object index from the consolidated documentation listing.

        This is the single source of truth for all Max/MSP documentation links!
        """
        try:
            # Single source of truth - the consolidated documentation listing
            listing_paths = [
                "../docs/knowledge_sources/Max MSP Documentation Listings.md",
                "../intelligent-max-mcp/docs/knowledge_sources/Max MSP Documentation Listings.md",
                "./docs/knowledge_sources/Max MSP Documentation Listings.md",
            ]

            # Load the consolidated listing
            content = None
            loaded_path = None
            for path in listing_paths:
                try:
                    async with aio_open(path, "r", encoding="utf-8") as f:
                        content = await f.read()
                        loaded_path = path
                        logger.info(f"✅ Loaded consolidated Max/MSP documentation from: {path}")
                        break
                except FileNotFoundError:
                    continue

            if not content:
                logger.warning("❌ Could not find consolidated Max MSP Documentation Listings.md")
                return None

            # Parse the consolidated documentation
            object_index = self._parse_object_listing_content(content)

            logger.info(f"🎵 Parsed {len(object_index)} objects from consolidated documentation")
            logger.info(f"📚 Source: {loaded_path}")
            return object_index

        except Exception as e:
            logger.error(f"Error loading from consolidated documentation listing: {e}")
            return None

    def _parse_object_listing_content(self, content: str) -> Dict[str, Dict[str, Any]]:
        """
        Parse consolidated documentation content and return comprehensive object index.

        Extracts objects, tutorials, guides, and their URLs for future enhancement.
        """
        object_index = {}
        current_category = "general"

        lines = content.split("\n")
        for line in lines:
            line = line.strip()

            # Detect category headers (## Control, ## Audio, etc.)
            if line.startswith("## ") and not line.startswith("## A Functional"):
                current_category = line[3:].lower().replace(" ", "_").replace("-", "_")
                continue

            # Extract objects from lines with Max object links
            if "[" in line and "](https://docs.cycling74.com/max8/refpages/" in line:
                # Pattern to capture both object name and full URL
                pattern = r"\[([^\]]+)\]\((https://docs\.cycling74\.com/max8/refpages/[^)]+)\)"
                matches = re.findall(pattern, line)

                for obj_name, obj_url in matches:
                    # Clean up object name
                    obj_name = obj_name.strip()

                    # Skip some special cases
                    if obj_name in ["Reference page", "Technical Notes"]:
                        continue

                    # Add to index (don't overwrite existing entries)
                    if obj_name not in object_index:
                        object_index[obj_name] = {
                            "description": self._generate_description(obj_name, current_category),
                            "category": current_category,
                            "tags": self._generate_tags(obj_name, current_category),
                            "hrefs": [obj_url],  # Store the official documentation URL
                            "source": "cycling74_listing",
                        }
                    else:
                        # Add additional URL if we found the same object in multiple places
                        if obj_url not in object_index[obj_name].get("hrefs", []):
                            object_index[obj_name]["hrefs"].append(obj_url)

            # Also extract other documentation links (tutorials, guides, etc.)
            elif "[" in line and "](https://docs.cycling74.com/max8/" in line:
                # Pattern for non-object documentation
                pattern = r"\[([^\]]+)\]\((https://docs\.cycling74\.com/max8/[^)]+)\)"
                matches = re.findall(pattern, line)

                for doc_name, doc_url in matches:
                    doc_name = doc_name.strip()

                    # Create entries for tutorials, guides, etc. with special handling
                    if doc_name not in object_index:
                        # Determine if it's a tutorial, guide, or other documentation
                        doc_type = "tutorial" if "tutorial" in doc_url.lower() else "guide"

                        object_index[doc_name] = {
                            "description": f"Max/MSP {doc_type}: {doc_name}",
                            "category": f"documentation_{doc_type}",
                            "tags": [doc_type, "documentation"],
                            "hrefs": [doc_url],
                            "source": "cycling74_docs",
                        }

        return object_index

    def _generate_description(self, obj_name: str, category: str) -> str:
        """Generate a basic description for an object based on name and category"""
        # Special cases for well-known objects
        descriptions = {
            "metro": "Output bang messages at a regular interval",
            "counter": "Count and output numbers",
            "pattrhub": "Route pattr messages between patchers",
            "pattr": "Store and recall parameter values",
            "pattrstorage": "Store and recall multiple pattr states",
            "transport": "Control global timing and synchronization",
            "jsui": "Create custom user interfaces with JavaScript",
            "buffer~": "Store audio samples",
            "cycle~": "Sinusoidal oscillator",
            "groove~": "Variable-rate playback of buffer~ content",
            "delay": "Delay messages by a specified time",
            "random": "Generate random numbers",
            "expr": "Evaluate mathematical expressions",
            "scale": "Map input range to output range",
            "route": "Route messages based on first element",
            "gate": "Route input to one of several outputs",
            "select": "Output a bang when input matches stored value",
            "trigger": "Output multiple values in right-to-left order",
            "print": "Print messages to the Max console",
        }

        if obj_name in descriptions:
            return descriptions[obj_name]

        # Generate generic description based on category
        category_descriptions = {
            "control": f"Control object: {obj_name}",
            "data": f"Data manipulation object: {obj_name}",
            "timing": f"Timing and scheduling object: {obj_name}",
            "math": f"Mathematical operation object: {obj_name}",
            "midi": f"MIDI input/output object: {obj_name}",
            "user_interface": f"User interface object: {obj_name}",
            "audio": f"Audio processing object: {obj_name}",
            "patching": f"Patching and structure object: {obj_name}",
            "files": f"File handling object: {obj_name}",
            "lists": f"List processing object: {obj_name}",
            "messages": f"Message manipulation object: {obj_name}",
        }

        return category_descriptions.get(category, f"Max object: {obj_name}")

    def _generate_tags(self, obj_name: str, category: str) -> List[str]:
        """Generate tags for an object based on name and category"""
        tags = [category]

        # Add tags based on object name patterns
        if obj_name.endswith("~"):
            tags.append("audio")
        if obj_name.endswith("in"):
            tags.append("input")
        if obj_name.endswith("out"):
            tags.append("output")
        if "midi" in obj_name:
            tags.append("midi")
        if "pattr" in obj_name:
            tags.append("preset")
        if obj_name in ["metro", "delay", "timer", "transport"]:
            tags.append("timing")
        if obj_name in ["random", "drunk", "urn"]:
            tags.append("random")
        if obj_name in ["button", "dial", "slider", "toggle"]:
            tags.append("ui")

        return tags

    async def _parse_object_doc(self, html: str, object_name: str) -> Dict[str, Any]:
        """Parse object documentation from HTML"""
        soup = BeautifulSoup(html, "lxml")

        doc = {
            "object_name": object_name,
            "url": urljoin(self.base_url, f"/refpages/{object_name}"),
            "timestamp": datetime.now().isoformat(),
        }

        # Extract description
        desc_elem = soup.find("div", class_="description")
        if desc_elem:
            doc["description"] = desc_elem.get_text(strip=True)

        # Extract inlets
        inlets = []
        inlet_section = soup.find("div", class_="inlets")
        if inlet_section:
            for inlet in inlet_section.find_all("div", class_="inlet"):
                inlets.append(
                    {
                        "index": len(inlets),
                        "type": inlet.get("data-type", "signal"),
                        "description": inlet.get_text(strip=True),
                    }
                )
        doc["inlets"] = inlets

        # Extract outlets
        outlets = []
        outlet_section = soup.find("div", class_="outlets")
        if outlet_section:
            for outlet in outlet_section.find_all("div", class_="outlet"):
                outlets.append(
                    {
                        "index": len(outlets),
                        "type": outlet.get("data-type", "signal"),
                        "description": outlet.get_text(strip=True),
                    }
                )
        doc["outlets"] = outlets

        # Extract attributes
        attributes = {}
        attr_section = soup.find("div", class_="attributes")
        if attr_section:
            for attr in attr_section.find_all("div", class_="attribute"):
                name = attr.find("span", class_="name")
                if name:
                    attributes[name.get_text(strip=True)] = {
                        "type": attr.get("data-type", "float"),
                        "description": attr.get_text(strip=True),
                    }
        doc["attributes"] = attributes

        # Extract examples
        examples = []
        example_section = soup.find("div", class_="examples")
        if example_section:
            for example in example_section.find_all("div", class_="example"):
                examples.append(
                    {
                        "description": example.get_text(strip=True),
                        "code": (example.find("code").get_text() if example.find("code") else ""),
                    }
                )
        doc["examples"] = examples

        # Extract related objects
        related = []
        related_section = soup.find("div", class_="seealso")
        if related_section:
            for link in related_section.find_all("a"):
                related.append(link.get_text(strip=True))
        doc["related_objects"] = related

        return doc

    async def _parse_tutorial(self, html: str, tutorial_name: str) -> Dict[str, Any]:
        """Parse tutorial content from HTML"""
        soup = BeautifulSoup(html, "lxml")

        tutorial = {
            "name": tutorial_name,
            "url": urljoin(self.base_url, f"/tutorials/{tutorial_name}"),
            "timestamp": datetime.now().isoformat(),
        }

        # Extract title
        title = soup.find("h1")
        if title:
            tutorial["title"] = title.get_text(strip=True)

        # Extract content sections
        sections = []
        for section in soup.find_all(["h2", "h3", "p", "code"]):
            sections.append({"type": section.name, "content": section.get_text(strip=True)})
        tutorial["sections"] = sections

        return tutorial

    async def _get_cached(self, key: str) -> Optional[Dict[str, Any]]:
        """Get cached result if it exists and is fresh"""
        cache_file = self.cache_dir / key

        if not cache_file.exists():
            return None

        try:
            # Check if cache is fresh
            mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - mtime > self.cache_duration:
                return None

            # Read cached data
            async with aio_open(cache_file, "r") as f:
                content = await f.read()
                return json.loads(content)

        except Exception as e:
            logger.error(f"Error reading cache for {key}: {e}")
            return None

    async def _cache_result(self, key: str, data: Dict[str, Any]):
        """Cache a result"""
        cache_file = self.cache_dir / key
        cache_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            async with aio_open(cache_file, "w") as f:
                await f.write(json.dumps(data, indent=2))
        except Exception as e:
            logger.error(f"Error caching result for {key}: {e}")

    def _get_default_object_index(self) -> Dict[str, Dict[str, Any]]:
        """
        Get a default object index with common Max objects as fallback.

        This is only used if the consolidated documentation file is not found.
        """
        return {
            # Core objects
            "metro": {
                "description": "Output bang messages at a regular interval",
                "category": "timing",
                "tags": ["timing", "clock", "bang"],
                "hrefs": [f"{self.base_url}/refpages/metro"],
                "source": "fallback",
            },
            "counter": {
                "description": "Count and output numbers",
                "category": "math",
                "tags": ["counting", "sequence", "number"],
                "hrefs": [f"{self.base_url}/refpages/counter"],
                "source": "fallback",
            },
            "transport": {
                "description": "Control global timing and synchronization",
                "category": "timing",
                "tags": ["timing", "sync", "global", "tempo"],
                "hrefs": [f"{self.base_url}/refpages/transport"],
                "source": "fallback",
            },
            # Audio objects
            "cycle~": {
                "description": "Sinusoidal oscillator",
                "category": "audio",
                "tags": ["audio", "oscillator", "sine", "generator"],
                "hrefs": [f"{self.base_url}/refpages/cycle~"],
                "source": "fallback",
            },
            "buffer~": {
                "description": "Store audio samples",
                "category": "audio",
                "tags": ["audio", "sample", "storage", "buffer"],
                "hrefs": [f"{self.base_url}/refpages/buffer~"],
                "source": "fallback",
            },
            "groove~": {
                "description": "Variable-rate playback of buffer~ content",
                "category": "audio",
                "tags": ["audio", "playback", "sample", "variable-speed"],
                "hrefs": [f"{self.base_url}/refpages/groove~"],
                "source": "fallback",
            },
            # UI objects
            "jsui": {
                "description": "Create custom user interfaces with JavaScript",
                "category": "ui",
                "tags": ["ui", "javascript", "custom", "interface"],
                "hrefs": [f"{self.base_url}/refpages/jsui"],
                "source": "fallback",
            },
            "dial": {
                "description": "Circular dial for numeric input",
                "category": "ui",
                "tags": ["ui", "control", "input", "dial"],
                "hrefs": [f"{self.base_url}/refpages/dial"],
                "source": "fallback",
            },
            # Math objects
            "expr": {
                "description": "Evaluate mathematical expressions",
                "category": "math",
                "tags": ["math", "expression", "calculation"],
                "hrefs": [f"{self.base_url}/refpages/expr"],
                "source": "fallback",
            },
            "scale": {
                "description": "Map input range to output range",
                "category": "math",
                "tags": ["math", "mapping", "range", "scaling"],
                "hrefs": [f"{self.base_url}/refpages/scale"],
                "source": "fallback",
            },
            # Essential pattr objects (since these were specifically mentioned)
            "pattr": {
                "description": "Store and recall parameter values",
                "category": "data",
                "tags": ["data", "preset", "parameter"],
                "hrefs": [f"{self.base_url}/refpages/pattr"],
                "source": "fallback",
            },
            "pattrhub": {
                "description": "Route pattr messages between patchers",
                "category": "data",
                "tags": ["data", "preset", "routing"],
                "hrefs": [f"{self.base_url}/refpages/pattrhub"],
                "source": "fallback",
            },
        }
