#!/usr/bin/env python3
"""
Git Hook Knowledge Index Generator for Max/MSP Interleaved Minutiae

Generates an iOS-accessible knowledge base index with raw.githubusercontent.com URLs
for all markdown files in the repository, organized by folder structure.

Usage: python3 generate_knowledge_index.py <output_file_path>
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Repository configuration
REPO_OWNER = "cocosberlucens"
REPO_NAME = "interleaved-max-minutiae" 
BASE_URL = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/main"

# Folder structure mapping for human-readable names
FOLDER_NAMES = {
    "max-reference-findings": "Max Reference Findings (Our Discoveries)",
    "meta-programming": "Meta-Programming & Automation", 
    "jsui-temporal-scaffolding": "JavaScript & Temporal Scaffolding System",
    "sample-playback": "Sample Playback & Manipulation",
    "shared-resources": "Shared Resources & Utilities"
}

def get_git_files() -> List[str]:
    """Get all tracked files from git repository."""
    try:
        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except subprocess.CalledProcessError as e:
        print(f"Error getting git files: {e}")
        return []

def extract_title_from_markdown(file_path: str) -> Optional[str]:
    """Extract the first # heading from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
                # Stop at first content to avoid reading entire large files
                if line and not line.startswith('#'):
                    break
    except (IOError, UnicodeDecodeError):
        pass
    return None

def organize_files_by_structure(files: List[str]) -> Dict[str, List[Tuple[str, str, str]]]:
    """
    Organize files by directory structure.
    Returns: {folder_name: [(filename, title, url), ...]}
    """
    organized = {}
    
    for file_path in files:
        # Only process markdown files
        if not file_path.endswith('.md'):
            continue
            
        # Skip root level files except README
        path_parts = file_path.split('/')
        if len(path_parts) == 1 and file_path != 'README.md':
            continue
            
        # Determine the main folder
        if len(path_parts) == 1:
            folder = "root"
        else:
            folder = path_parts[0]
            
        # Extract title
        title = extract_title_from_markdown(file_path)
        if not title:
            # Fallback to filename without extension
            title = Path(file_path).stem.replace('-', ' ').replace('_', ' ').title()
            
        # Generate raw GitHub URL
        url = f"{BASE_URL}/{file_path}"
        
        # Add to organized structure
        if folder not in organized:
            organized[folder] = []
            
        # Create a nice display name for the file
        filename = Path(file_path).name
        subpath = '/'.join(path_parts[1:]) if len(path_parts) > 1 else filename
        
        organized[folder].append((subpath, title, url))
    
    return organized

def generate_markdown_index(organized_files: Dict[str, List[Tuple[str, str, str]]]) -> str:
    """Generate the formatted markdown index."""
    
    markdown = [
        "# Interleaved Max Minutiae - Knowledge Base",
        "",
        "Auto-generated index of Max/MSP knowledge with iOS-accessible URLs.",
        "",
        f"**Repository**: [`{REPO_OWNER}/{REPO_NAME}`](https://github.com/{REPO_OWNER}/{REPO_NAME})",
        "",
        "---",
        ""
    ]
    
    # Add table of contents
    markdown.extend([
        "## Table of Contents",
        ""
    ])
    
    for folder in sorted(organized_files.keys()):
        if folder == "root":
            continue
        folder_name = FOLDER_NAMES.get(folder, folder.replace('-', ' ').title())
        markdown.append(f"- [{folder_name}](#{folder.lower().replace('-', '-').replace('_', '')})")
    
    markdown.extend(["", "---", ""])
    
    # Add each section
    for folder in sorted(organized_files.keys()):
        if folder == "root":
            continue
            
        folder_name = FOLDER_NAMES.get(folder, folder.replace('-', ' ').title())
        files = organized_files[folder]
        
        if not files:
            continue
            
        markdown.extend([
            f"## {folder_name}",
            ""
        ])
        
        # Sort files: README first, then alphabetically
        files_sorted = sorted(files, key=lambda x: (
            0 if x[0].lower().startswith('readme') else 1,
            x[1].lower()
        ))
        
        for subpath, title, url in files_sorted:
            # Special formatting for README files
            if subpath.lower().startswith('readme'):
                markdown.append(f"**📁 {title}** - *Section Overview*")
            else:
                markdown.append(f"- [{title}]({url})")
                
        markdown.extend(["", ""])
    
    # Add root files if any
    if "root" in organized_files and organized_files["root"]:
        markdown.extend([
            "## Repository Root",
            ""
        ])
        
        for subpath, title, url in organized_files["root"]:
            markdown.append(f"- [{title}]({url})")
            
        markdown.append("")
    
    # Add footer
    markdown.extend([
        "---",
        "",
        "*This index is automatically generated by git hook after each commit.*",
        "",
        f"*Last updated: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}*"
    ])
    
    return '\n'.join(markdown)

def main():
    """Main function to generate the knowledge index."""
    
    if len(sys.argv) != 2:
        print("Usage: python3 generate_knowledge_index.py <output_file_path>")
        sys.exit(1)
    
    output_path = sys.argv[1]
    
    # Ensure we're in a git repository
    if not os.path.exists('.git'):
        print("Error: Not in a git repository")
        sys.exit(1)
    
    print("🔍 Scanning repository for markdown files...")
    files = get_git_files()
    
    if not files:
        print("No files found in repository")
        sys.exit(1)
    
    print(f"📁 Found {len(files)} total files")
    
    print("🗂️  Organizing files by structure...")
    organized = organize_files_by_structure(files)
    
    markdown_count = sum(len(file_list) for file_list in organized.values())
    print(f"📝 Processing {markdown_count} markdown files")
    
    print("📋 Generating knowledge index...")
    index_content = generate_markdown_index(organized)
    
    print(f"💾 Saving to {output_path}...")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the index file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print("✅ Knowledge index generated successfully!")
    print(f"📱 Ready for Claude iOS app via Project Knowledge")
    print(f"🔗 Contains raw.githubusercontent.com URLs for all content")

if __name__ == "__main__":
    main()
