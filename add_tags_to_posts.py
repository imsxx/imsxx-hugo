import os
import re
from pathlib import Path

import jieba


def add_tags_to_posts(content_dir):
    posts_dir = Path(content_dir) / "posts"
    print(f"Searching for markdown files in: {posts_dir.resolve()}")

    markdown_files = list(posts_dir.glob("*.md"))
    if not markdown_files:
        print("No markdown files found.")
        return

    print(f"Found {len(markdown_files)} markdown files.")

    for filepath in markdown_files:
        print(f"\nProcessing file: {filepath.name}")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Find front matter
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            print(f"Skipping {filepath.name}: No front matter found.")
            continue

        front_matter_str = match.group(1)
        print("Found front matter.")

        # Check if tags already exist
        if "tags:" in front_matter_str or "tags =" in front_matter_str:
            print(f"Skipping {filepath.name}: Tags already exist.")
            continue

        # Generate tags from filename
        filename_stem = filepath.stem
        # Remove date prefix like 2024-01-01-
        filename_no_date = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", filename_stem)
        print(f"Generating tags from: {filename_no_date}")
        tags = list(jieba.cut(filename_no_date.replace("-", " ")))
        tags = [tag for tag in tags if tag.strip() and len(tag.strip()) > 1] # Filter out single characters and empty strings

        if not tags:
            print(f"Skipping {filepath.name}: Could not generate tags from filename.")
            continue
        
        print(f"Generated tags: {tags}")

        # Add tags to front matter
        new_front_matter_str = front_matter_str.strip()
        new_front_matter_str += f"\ntags: {tags}"

        new_content = content.replace(match.group(1), new_front_matter_str)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"Successfully added tags to {filepath.name}")

if __name__ == "__main__":
    # The script is in the root of the hugo project, so content is in a subdirectory
    content_directory = "content"
    add_tags_to_posts(content_directory)