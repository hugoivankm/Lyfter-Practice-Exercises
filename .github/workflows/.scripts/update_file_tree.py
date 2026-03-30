import os
import sys

def update_readme():
    new_tree = os.environ.get('FILE_TREE', '').strip()

    if not new_tree:
        print("Error: No FILE_TREE data found.")
        sys.exit(1)
    
    start_marker = "<!-- START -->"
    end_marker = "<!-- END -->"

    if not os.path.exists('README.md'):
        print("README.md not found!")
        sys.exit(1)
    
    with open('README.md', 'r') as f:
        content = f.read()

    if start_marker not in content or end_marker not in content:
        print(f"Markers {start_marker} or {end_marker} not found.")
        sys.exit(1)

    before_part = content.split(start_marker)[0]
    after_part = content.split(end_marker)[1]

    updated_content = (
        before_part +
        start_marker +
        "\n\n" +
        new_tree.strip() +
        "\n\n" +
        end_marker +
        after_part
    )

    with open('README.md', 'w') as f:
        f.write(updated_content)
    
    print("Successfully updated README.md")

if __name__ == "__main__":
    update_readme()
