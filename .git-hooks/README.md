# Git Hooks for Knowledge Base Generation

This folder contains scripts for automatically generating iOS-accessible knowledge base indices.

## What This Does

After each commit, the git hook will:
1. 🔍 Scan the repository for all markdown files
2. 📁 Organize them by folder structure  
3. 🔗 Generate raw.githubusercontent.com URLs for each file
4. 📝 Create a formatted markdown index
5. 💾 Save it to your Obsidian vault
6. 📱 Make it ready for Claude iOS Project Knowledge

## Installation

### Step 1: Set Up Your Obsidian Path

Edit the `post-commit-template` file and replace:
```bash
OBSIDIAN_VAULT_PATH="/Users/corrado/YOUR_OBSIDIAN_VAULT_PATH_HERE"
```

With your actual Obsidian vault path, for example:
```bash
OBSIDIAN_VAULT_PATH="/Users/corrado/Documents/Obsidian Vault"
```

### Step 2: Copy and Activate the Hook

```bash
# Navigate to the repository
cd /Users/corrado/miei-repo/interleaved-max-minutiae

# Copy the template to the actual git hook location
cp .git-hooks/post-commit-template .git/hooks/post-commit

# Make it executable
chmod +x .git/hooks/post-commit
```

### Step 3: Test the Hook

```bash
# Make a test commit to trigger the hook
echo "Test" >> README.md
git add README.md
git commit -m "Test knowledge base generation"

# Check if the file was created in your Obsidian vault
ls -la "/path/to/your/obsidian/vault/Max-MSP Project/"
```

## Files Generated

The hook will create:
```
/Your/Obsidian/Vault/Max-MSP Project/Interleaved Max Minutiae Knowledge Base.md
```

This file contains:
- 📋 Table of contents organized by folder
- 🔗 Raw GitHub URLs for all markdown files  
- 📱 iOS-accessible links for Claude app
- 🕒 Auto-update timestamp

## Folder Organization

The generated index organizes content by:

- **Max Reference Findings**: Our discoveries about Max objects
- **Meta-Programming**: JSON format and automation tools
- **JavaScript & Temporal Scaffolding**: Mathematical rhythm systems
- **Sample Playback**: Breaks manipulation and drum machines  
- **Shared Resources**: Common utilities and patterns

## Troubleshooting

### Hook Not Running
- Check if `.git/hooks/post-commit` exists and is executable
- Verify the Obsidian path is correct
- Look for error messages in the terminal

### Python Script Errors
- Ensure Python 3 is installed and in PATH
- Check that git commands are available
- Verify repository structure

### File Not Created
- Check if the Obsidian vault path exists
- Ensure write permissions to the target directory
- Look for path typos in the configuration

## Manual Generation

You can also generate the index manually:

```bash
cd /Users/corrado/miei-repo/interleaved-max-minutiae
python3 .git-hooks/generate_knowledge_index.py "/path/to/output/file.md"
```

## Customization

### Adding New File Types

Edit `generate_knowledge_index.py` and modify:
```python
# Only process markdown files
if not file_path.endswith('.md'):
    continue
```

Add other extensions like `.txt`, `.json`, etc.

### Changing Folder Names

Update the `FOLDER_NAMES` dictionary in the Python script:
```python
FOLDER_NAMES = {
    "your-folder": "Your Friendly Folder Name",
    # ... etc
}
```

### Output Format

Modify the `generate_markdown_index()` function to change the generated markdown structure.

---

*This system bridges the gap between our growing Max/MSP knowledge and iOS accessibility!* 🚀
# Git Hook Test
