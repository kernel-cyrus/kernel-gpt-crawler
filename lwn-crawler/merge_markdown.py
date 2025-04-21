import os

def merge_markdown_files(source_dir='lwn_articles/markdown', output_file='lwn_merged.md'):
    if not os.path.isdir(source_dir):
        print(f"Directory '{source_dir}' does not exist.")
        return

    md_files = [f for f in os.listdir(source_dir) if f.endswith('.md')]
    md_files.sort()  # 可选：按文件名排序

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for fname in md_files:
            file_path = os.path.join(source_dir, fname)
            with open(file_path, 'r', encoding='utf-8') as infile:
                outfile.write(f'# {fname}\n\n')  # 可选：加文件名标题
                outfile.write(infile.read())
                outfile.write('\n\n')  # 文件间隔

    print(f"Merged {len(md_files)} files into {output_file}")

if __name__ == '__main__':
    merge_markdown_files()
