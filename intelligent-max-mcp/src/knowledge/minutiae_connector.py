"""
Minutiae Repository Connector

Interfaces with the interleaved-max-minutiae repository to access
our accumulated knowledge, patterns, and discoveries.
"""

import asyncio
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import aiofiles
from git import Repo

logger = logging.getLogger(__name__)


class MinutiaeConnector:
    """
    Connector for the interleaved-max-minutiae knowledge repository.

    This connector indexes and searches through our accumulated
    Max/MSP knowledge, including temporal scaffolding patterns,
    JSON format insights, and discovered techniques.
    """

    def __init__(self, config: Dict[str, Any]):
        self.repo_path = Path(config.get("local_path", "../")).resolve()
        self.auto_update = config.get("auto_update", True)
        self.update_interval = config.get("update_interval", 300)
        self.watch_for_changes = config.get("watch_for_changes", True)

        # Knowledge index
        self.knowledge_index: Dict[str, List[Dict[str, Any]]] = {
            "patterns": [],
            "objects": [],
            "techniques": [],
            "jsui": [],
            "temporal": [],
        }

        # File patterns to index
        self.index_patterns = {
            "*.md": self._index_markdown,
            "*.maxpat": self._index_maxpat,
            "*.js": self._index_javascript,
            "*.json": self._index_json,
        }

        # Important directories in the repository
        self.key_directories = {
            "meta-programming/json-format": "JSON format patterns",
            "jsui-temporal-scaffolding": "Temporal scaffolding systems",
            "max-reference-findings": "Object discoveries",
            "sample-playback": "Audio manipulation techniques",
            "presets": "Preset patterns and templates",
        }

        # Git repository handle
        self.repo: Optional[Repo] = None
        self.last_commit_hash: Optional[str] = None

        logger.info(f"Minutiae Connector initialized with repo path: {self.repo_path}")

    async def initialize(self):
        """Initialize the connector and build initial index"""
        try:
            # Initialize git repository
            self.repo = Repo(self.repo_path)
            self.last_commit_hash = self.repo.head.commit.hexsha

            # Build initial index
            await self._build_index()

            # Start watching for changes if enabled
            if self.watch_for_changes:
                asyncio.create_task(self._watch_repository())

            logger.info(f"Minutiae repository indexed: {len(self.knowledge_index['patterns'])} patterns found")

        except Exception as e:
            logger.error(f"Error initializing Minutiae connector: {e}")
            raise

    async def search(self, query: str, context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search the minutiae repository for relevant content.

        Args:
            query: Search query
            context: Optional context for relevance boosting

        Returns:
            List of relevant knowledge entries
        """
        results = []
        query_lower = query.lower()
        query_tokens = set(query_lower.split())

        # Search all knowledge categories
        for category, entries in self.knowledge_index.items():
            for entry in entries:
                relevance = self._calculate_relevance(entry, query_lower, query_tokens)

                # Apply context-based boosting
                if context:
                    relevance = self._apply_context_boost(entry, relevance, context)

                if relevance > 0.1:  # Threshold
                    result = entry.copy()
                    result["relevance"] = relevance
                    result["category"] = category
                    results.append(result)

        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)

        return results[:50]  # Top 50 results

    async def get_pattern(self, pattern_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific pattern by name"""
        for pattern in self.knowledge_index["patterns"]:
            if pattern.get("name") == pattern_name:
                return pattern
        return None

    async def add_pattern(self, pattern: Any) -> bool:
        """
        Add a new pattern to the repository.

        This creates a new markdown file in the appropriate section
        and commits it to the repository.
        """
        try:
            # Determine appropriate location
            category = pattern.metadata.get("category", "discoveries")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{pattern.name.replace(' ', '_')}_{timestamp}.md"

            # Create appropriate directory
            target_dir = self.repo_path / "discoveries" / category
            target_dir.mkdir(parents=True, exist_ok=True)

            # Generate markdown content
            content = self._generate_pattern_markdown(pattern)

            # Write file
            file_path = target_dir / filename
            async with aiofiles.open(file_path, "w") as f:
                await f.write(content)

            # Git operations
            if self.repo:
                self.repo.index.add([str(file_path.relative_to(self.repo_path))])
                self.repo.index.commit(
                    f"Add discovered pattern: {pattern.name}\n\n"
                    f"Confidence: {pattern.confidence}\n"
                    f"Category: {category}\n"
                    f"Generated by Intelligent Max MCP Server"
                )
                logger.info(f"Pattern '{pattern.name}' committed to repository")

            # Update index
            await self._index_file(file_path)

            return True

        except Exception as e:
            logger.error(f"Error adding pattern to repository: {e}")
            return False

    async def get_temporal_scaffolding_examples(self) -> List[Dict[str, Any]]:
        """Get all temporal scaffolding examples"""
        return [entry for entry in self.knowledge_index["temporal"] if "scaffolding" in entry.get("tags", [])]

    async def get_jsui_templates(self) -> List[Dict[str, Any]]:
        """Get all JSUI templates and examples"""
        return self.knowledge_index["jsui"]

    # Private methods

    async def _build_index(self):
        """Build the knowledge index from repository files"""
        logger.info("Building knowledge index...")

        # Index key directories
        for dir_path, description in self.key_directories.items():
            full_path = self.repo_path / dir_path
            if full_path.exists():
                await self._index_directory(full_path, description)

        # Also index root-level important files
        await self._index_root_files()

        logger.info(f"Index built: {sum(len(v) for v in self.knowledge_index.values())} total entries")

    async def _index_directory(self, directory: Path, description: str):
        """Index all relevant files in a directory"""
        for pattern, indexer in self.index_patterns.items():
            for file_path in directory.rglob(pattern):
                try:
                    await self._index_file(file_path)
                except Exception as e:
                    logger.error(f"Error indexing {file_path}: {e}")

    async def _index_file(self, file_path: Path):
        """Index a single file based on its type"""
        suffix = file_path.suffix.lower()

        if suffix == ".md":
            await self._index_markdown(file_path)
        elif suffix == ".maxpat":
            await self._index_maxpat(file_path)
        elif suffix == ".js":
            await self._index_javascript(file_path)
        elif suffix == ".json":
            await self._index_json(file_path)

    async def _index_markdown(self, file_path: Path):
        """Index a markdown file"""
        try:
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                content = await f.read()

            # Extract metadata
            entry = {
                "file_path": str(file_path.relative_to(self.repo_path)),
                "type": "markdown",
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            }

            # Extract title
            title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            if title_match:
                entry["title"] = title_match.group(1)
                entry["name"] = title_match.group(1)

            # Extract description (first paragraph after title)
            desc_match = re.search(r"^#\s+.+\n\n(.+?)(?:\n\n|$)", content, re.MULTILINE | re.DOTALL)
            if desc_match:
                entry["description"] = desc_match.group(1).strip()

            # Extract code blocks
            code_blocks = re.findall(r"```(\w+)?\n(.*?)\n```", content, re.DOTALL)
            entry["code_examples"] = [{"language": lang or "text", "code": code} for lang, code in code_blocks]

            # Extract tags from content
            tags = set()

            # Common Max objects mentioned
            max_objects = re.findall(r"\b([a-z]+~?)\b(?:\s+object|\s+is|\s+the)", content.lower())
            tags.update(obj for obj in max_objects if self._is_likely_max_object(obj))

            # Key concepts
            if "temporal" in content.lower():
                tags.add("temporal")
            if "scaffolding" in content.lower():
                tags.add("scaffolding")
            if "jsui" in content.lower():
                tags.add("jsui")
            if "buffer" in content.lower():
                tags.add("buffer")
            if "sample" in content.lower():
                tags.add("sample")

            entry["tags"] = list(tags)
            entry["content_preview"] = content[:500]

            # Categorize
            category = self._categorize_entry(file_path, entry)
            self.knowledge_index[category].append(entry)

        except Exception as e:
            logger.error(f"Error indexing markdown {file_path}: {e}")

    async def _index_maxpat(self, file_path: Path):
        """Index a Max patcher file"""
        try:
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                content = await f.read()
                patcher_data = json.loads(content)

            entry = {
                "file_path": str(file_path.relative_to(self.repo_path)),
                "type": "maxpat",
                "name": file_path.stem,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            }

            # Extract patcher info
            patcher = patcher_data.get("patcher", {})

            # Count objects by type
            object_counts = {}
            for box in patcher.get("boxes", []):
                obj_class = box.get("class", "unknown")
                object_counts[obj_class] = object_counts.get(obj_class, 0) + 1

            entry["object_counts"] = object_counts
            entry["total_objects"] = sum(object_counts.values())
            entry["unique_objects"] = list(object_counts.keys())

            # Detect patterns
            patterns = []
            if "metro" in object_counts and "counter" in object_counts:
                patterns.append("timing-counter")
            if "buffer~" in object_counts and "groove~" in object_counts:
                patterns.append("sample-playback")
            if "jsui" in object_counts:
                patterns.append("custom-ui")

            entry["patterns"] = patterns
            entry["tags"] = list(set(patterns + list(object_counts.keys())[:5]))

            # Add description based on content
            if patterns:
                entry["description"] = f"Max patcher demonstrating: {', '.join(patterns)}"
            else:
                entry["description"] = f"Max patcher with {entry['total_objects']} objects"

            # Categorize
            if "jsui" in object_counts:
                self.knowledge_index["jsui"].append(entry)
            elif any(p in patterns for p in ["timing-counter", "tempo"]):
                self.knowledge_index["temporal"].append(entry)
            else:
                self.knowledge_index["patterns"].append(entry)

        except Exception as e:
            logger.error(f"Error indexing maxpat {file_path}: {e}")

    async def _index_javascript(self, file_path: Path):
        """Index a JavaScript file (likely for jsui)"""
        try:
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                content = await f.read()

            entry = {
                "file_path": str(file_path.relative_to(self.repo_path)),
                "type": "javascript",
                "name": file_path.stem,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            }

            # Extract function definitions
            functions = re.findall(r"function\s+(\w+)\s*\([^)]*\)", content)
            entry["functions"] = functions

            # Look for Max-specific patterns
            if "mgraphics" in content:
                entry["tags"] = ["jsui", "graphics"]
                entry["description"] = "JSUI graphics script"
                self.knowledge_index["jsui"].append(entry)
            elif "outlet" in content or "inlet" in content:
                entry["tags"] = ["js", "max-integration"]
                entry["description"] = "Max JavaScript integration"
                self.knowledge_index["objects"].append(entry)

        except Exception as e:
            logger.error(f"Error indexing JavaScript {file_path}: {e}")

    async def _index_json(self, file_path: Path):
        """Index a JSON file"""
        try:
            async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
                content = await f.read()
                json.loads(content)  # Validate JSON format

            entry = {
                "file_path": str(file_path.relative_to(self.repo_path)),
                "type": "json",
                "name": file_path.stem,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            }

            # Check if it's a preset or configuration
            if "preset" in file_path.stem.lower():
                entry["tags"] = ["preset", "configuration"]
                entry["description"] = f"Preset configuration: {file_path.stem}"
                self.knowledge_index["patterns"].append(entry)

        except Exception as e:
            logger.error(f"Error indexing JSON {file_path}: {e}")

    async def _index_root_files(self):
        """Index important root-level files"""
        important_files = ["README.md", "DISCOVERIES.md", "PATTERNS.md"]

        for filename in important_files:
            file_path = self.repo_path / filename
            if file_path.exists():
                await self._index_file(file_path)

    def _categorize_entry(self, file_path: Path, entry: Dict[str, Any]) -> str:
        """Categorize an entry based on its path and content"""
        path_str = str(file_path).lower()

        if "temporal" in path_str or "scaffolding" in path_str:
            return "temporal"
        elif "jsui" in path_str:
            return "jsui"
        elif "sample" in path_str or "buffer" in path_str:
            return "techniques"
        elif "meta-programming" in path_str:
            return "patterns"
        else:
            # Default based on tags
            tags = entry.get("tags", [])
            if "temporal" in tags:
                return "temporal"
            elif "jsui" in tags:
                return "jsui"
            else:
                return "patterns"

    def _calculate_relevance(self, entry: Dict[str, Any], query_lower: str, query_tokens: Set[str]) -> float:
        """Calculate relevance score for a search result"""
        relevance = 0.0

        # Title/name match
        name = entry.get("name", "").lower()
        if query_lower in name:
            relevance += 0.5
        elif any(token in name for token in query_tokens):
            relevance += 0.3

        # Description match
        desc = entry.get("description", "").lower()
        if query_lower in desc:
            relevance += 0.3
        elif any(token in desc for token in query_tokens):
            relevance += 0.2

        # Tag match
        tags = [t.lower() for t in entry.get("tags", [])]
        matching_tags = sum(1 for token in query_tokens if any(token in tag for tag in tags))
        relevance += matching_tags * 0.1

        # File path match
        file_path = entry.get("file_path", "").lower()
        if any(token in file_path for token in query_tokens):
            relevance += 0.1

        # Boost recent entries slightly
        if "modified" in entry:
            try:
                modified = datetime.fromisoformat(entry["modified"])
                days_old = (datetime.now() - modified).days
                if days_old < 30:
                    relevance *= 1.1
                elif days_old < 90:
                    relevance *= 1.05
            except:
                pass

        return min(relevance, 1.0)  # Cap at 1.0

    def _apply_context_boost(self, entry: Dict[str, Any], relevance: float, context: Dict[str, Any]) -> float:
        """Apply context-based relevance boosting"""
        # Boost based on current domain
        domain = context.get("domain")
        if domain:
            tags = entry.get("tags", [])
            if domain in tags:
                relevance *= 1.3

        # Boost based on recent objects used
        recent_objects = context.get("recent_objects", [])
        if recent_objects:
            entry_objects = entry.get("unique_objects", [])
            if any(obj in entry_objects for obj in recent_objects):
                relevance *= 1.2

        return min(relevance, 1.0)

    def _is_likely_max_object(self, name: str) -> bool:
        """Check if a string is likely a Max object name"""
        # Common Max object patterns
        if name.endswith("~"):  # Audio objects
            return True
        if name in [
            "metro",
            "counter",
            "bang",
            "toggle",
            "message",
            "route",
            "gate",
            "sel",
            "prepend",
            "append",
            "pack",
            "unpack",
        ]:
            return True
        return False

    def _generate_pattern_markdown(self, pattern: Any) -> str:
        """Generate markdown content for a pattern"""
        content = f"""# {pattern.name}

## Description
{pattern.description}

## Discovery Details
- **Discovered**: {pattern.discovered_at.isoformat()}
- **Confidence**: {pattern.confidence}
- **Usage Count**: {pattern.usage_count}
- **Validated**: {pattern.validated}

## Examples
"""

        for i, example in enumerate(pattern.examples, 1):
            content += f"\n### Example {i}\n"
            content += f"```json\n{json.dumps(example, indent=2)}\n```\n"

        if pattern.metadata.get("tags"):
            content += f"\n## Tags\n{', '.join(pattern.metadata['tags'])}\n"

        content += "\n---\n*Generated by Intelligent Max MCP Server*\n"

        return content

    async def _watch_repository(self):
        """Watch repository for changes and update index"""
        while self.watch_for_changes:
            try:
                await asyncio.sleep(self.update_interval)

                if self.repo and self.auto_update:
                    # Check for new commits
                    self.repo.remotes.origin.fetch()
                    current_hash = self.repo.head.commit.hexsha

                    if current_hash != self.last_commit_hash:
                        logger.info("Repository updated, rebuilding index...")
                        self.last_commit_hash = current_hash
                        await self._build_index()

            except Exception as e:
                logger.error(f"Error watching repository: {e}")
                await asyncio.sleep(60)  # Wait longer on error
