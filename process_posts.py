import os
import re
from pathlib import Path
import yaml

def process_markdown_files(directory):
    posts_dir = Path(directory)
    if not posts_dir.is_dir():
        print(f"Error: Directory not found at {posts_dir.resolve()}")
        return

    print(f"Processing files in: {posts_dir.resolve()}")
    file_count = 0
    processed_count = 0

    for filepath in posts_dir.glob("*.md"):
        file_count += 1
        try:
            with open(filepath, "r", encoding="utf-8-sig") as f:
                content = f.read()

            # Use a simple regex to find the front matter block
            match = re.match(r'\A---\s*\r?\n(.*?)\r?\n---\s*\r?\n', content, re.DOTALL)

            if not match:
                print(f"- Skipping {filepath.name}: No front matter found.")
                continue

            front_matter_str = match.group(1)
            post_content = content[match.end():]
            
            # The YAML parser is more robust for handling duplicates.
            # We load it and it will automatically keep the last defined key.
            try:
                front_matter_data = yaml.safe_load(front_matter_str)
                if not isinstance(front_matter_data, dict):
                    print(f"- Skipping {filepath.name}: Front matter is not a valid dictionary.")
                    continue
            except yaml.YAMLError as e:
                print(f"- Skipping {filepath.name}: Could not parse YAML front matter. Error: {e}")
                continue

            made_changes = False

            # 1. Add tags if they don't exist
            if 'tags' not in front_matter_data or not front_matter_data['tags']:
                filename_stem = filepath.stem
                filename_no_date = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', filename_stem)
                tags = [tag for tag in filename_no_date.split('-') if tag]
                if tags:
                    front_matter_data['tags'] = tags
                    print(f"  - Added tags {tags} to {filepath.name}")
                    made_changes = True

            # 2. Re-dumping the YAML will automatically handle duplicate slugs
            # We can check if the original string had duplicates to be sure
            if len(re.findall(r'^slug:', front_matter_str, re.MULTILINE)) > 1:
                print(f"  - Merged duplicate 'slug' entries in {filepath.name}")
                made_changes = True

            if made_changes:
                # Convert dict back to YAML string
                new_front_matter_str = yaml.dump(front_matter_data, allow_unicode=True, default_flow_style=False, sort_keys=False)
                
                # Reconstruct the file content
                new_content = "---\n" + new_front_matter_str + "---\n" + post_content

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                processed_count += 1
                print(f"- Successfully processed {filepath.name}")

        except Exception as e:
            print(f"- ERROR processing {filepath.name}: {e}")

    print(f"\nFinished processing. Looked at {file_count} files, updated {processed_count} files.")

if __name__ == "__main__":
    # The script is in the root of the hugo project, so content is in a subdirectory
    process_markdown_files("content/posts")