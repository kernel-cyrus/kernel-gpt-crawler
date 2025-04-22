import os
import sys
import math

def split_markdown_file(input_file, n_parts):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_lines = len(lines)
    chunk_size = math.ceil(total_lines / n_parts)

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    parent_dir = os.path.dirname(os.path.abspath(input_file))

    for i in range(n_parts):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, total_lines)
        output_file = os.path.join(parent_dir, f"{base_name}_{i+1}.md")
        with open(output_file, 'w', encoding='utf-8') as out:
            out.writelines(lines[start:end])
        print(f"Written {output_file}: lines {start+1} to {end}")

if __name__ == "__main__":

    if len(sys.argv) >= 2:
        n_parts = int(sys.argv[1])
    else:
        n_parts = 3

    split_markdown_file('merged/lwn_merged.md', n_parts)
