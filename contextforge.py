#!/usr/bin/env python3
import os
import sys
import fnmatch
from pathlib import Path

def load_gitignore(repo_path):
    """Loads local .gitignore rules and layers in standard developer exclusions."""
    ignored_patterns = {
        '.git', '.github', 'node_modules', '__pycache__', 
        '.venv', 'venv', 'env', '.DS_Store', '.pytest_cache',
        '*.pyc', '*.o', '*.exe', 'dist', 'build', '.idea', '.vscode'
    }
    gitignore_file = Path(repo_path) / '.gitignore'
    if gitignore_file.exists():
        try:
            with open(gitignore_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        ignored_patterns.add(line.rstrip('/'))
        except Exception:
            pass
    return list(ignored_patterns)

def is_ignored(path, base_path, ignored_patterns):
    """Checks if a file/folder matches gitignore, default patterns, or is a symlink."""
    # Safety Check: Skip symbolic links to prevent circular infinite loops
    if os.path.islink(path):
        return True
        
    try:
        relative_path = os.path.relpath(path, base_path)
        parts = Path(relative_path).parts
        for part in parts:
            for pattern in ignored_patterns:
                if fnmatch.fnmatch(part, pattern) or fnmatch.fnmatch(relative_path, pattern):
                    return True
    except Exception:
        return True
    return False

def is_binary(file_path):
    """Check if a file is binary to avoid ripping raw bytes from images, zip files, etc."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:  # Null byte indicates a binary payload
                return True
    except Exception:
        return True
    return False

def estimate_tokens(text):
    """Approximates standard LLM tokens based on a 4-characters-per-token average."""
    return len(text) // 4

def generate_tree(dir_path, base_path, ignored_patterns, prefix=""):
    """Generates a text-based visual map of the directory layout structure safely."""
    tree_str = ""
    try:
        entries = sorted([e for e in os.scandir(dir_path) if not is_ignored(e.path, base_path, ignored_patterns)], key=lambda e: e.name)
    except (PermissionError, OSError):
        return ""
    
    pointers = [r"├── "] * (len(entries) - 1) + [r"└── "] if entries else []
    for pointer, entry in zip(pointers, entries):
        tree_str += f"{prefix}{pointer}{entry.name}\n"
        if entry.is_dir():
            extension = "│   " if pointer == r"├── " else "    "
            tree_str += generate_tree(entry.path, base_path, ignored_patterns, prefix + extension)
    return tree_str

def pack_repository(repo_path, output_file):
    """Traverses the codebase safely, extracts text files, and binds them into markdown."""
    repo_path = os.path.abspath(repo_path)
    ignored_patterns = load_gitignore(repo_path)
    
    print(f"📦 ContextForge: Processing repository '{os.path.basename(repo_path)}'...")
    print("🔍 Filtering structural files and respecting exclusions...")
    
    markdown_content = f"# Repository Context: {os.path.basename(repo_path)}\n\n"
    markdown_content += "## Directory Tree\n```text\n"
    markdown_content += generate_tree(repo_path, repo_path, ignored_patterns)
    markdown_content += "```\n\n## File Contents\n\n"

    total_characters = 0
    file_count = 0

    # Walk files to add contents, using error handling to safely skip protected folders
    for root, dirs, files in os.walk(repo_path, onerror=lambda err: None):
        # Prevent tracking symlinks or accessing forbidden directory scopes
        try:
            dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), repo_path, ignored_patterns)]
        except (PermissionError, OSError):
            dirs[:] = []
            continue
        
        for file in sorted(files):
            file_path = os.path.join(root, file)
            
            # Check if ignored or if it's the script's own output file
            if is_ignored(file_path, repo_path, ignored_patterns):
                continue
            if os.path.abspath(file_path) == os.path.abspath(output_file):
                continue
            
            # Skip non-text data structures completely
            if is_binary(file_path):
                continue
                
            rel_path = os.path.relpath(file_path, repo_path)
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                total_characters += len(content)
                file_count += 1
                ext = os.path.splitext(file)[1].lstrip('.')
                
                markdown_content += f"### File: `{rel_path}`\n"
                markdown_content += f"```{ext}\n"
                markdown_content += content
                markdown_content += "\n```\n\n"
            except (PermissionError, OSError, IOError):
                markdown_content += f"### File: `{rel_path}`\n*Access Denied: System permissions restricted context extraction*\n\n"
            except Exception as e:
                markdown_content += f"### File: `{rel_path}`\n*Error reading file: {str(e)}*\n\n"

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
    except Exception as e:
        print(f"❌ Critical Error: Could not write output file. {str(e)}")
        sys.exit(1)
        
    estimated_tokens = estimate_tokens(total_characters)
    print(f"\n🎉 Success! Consolidated {file_count} files into '{output_file}'")
    print(f"📊 Content Telemetry:")
    print(f"   - Total Character Payload: {total_characters:,}")
    print(f"   - Estimated Prompt Volume: ~{estimated_tokens:,} tokens")
    print(f"💡 Copy-paste or drag '{output_file}' directly into your AI dashboard!")

if __name__ == '__main__':
    target_repo = sys.argv[1] if len(sys.argv) > 1 else "."
    output_md = sys.argv[2] if len(sys.argv) > 2 else "context_bundle.md"
    pack_repository(target_repo, output_md)
