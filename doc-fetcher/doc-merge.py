import os

def merge_rst_files(src_dir, output_file):
    rst_files = []

    # 递归查找所有 .rst 文件
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith('.rst'):
                full_path = os.path.join(root, file)
                rst_files.append(full_path)

    # 排序（可按路径或名称排序）
    rst_files.sort()

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file_path in rst_files:
            rel_path = os.path.relpath(file_path, src_dir)
            outfile.write(f"\n\n.. START OF: {rel_path}\n{'='*60}\n\n")
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                outfile.write(infile.read())
            outfile.write(f"\n\n.. END OF: {rel_path}\n{'='*60}\n\n")

    print(f"✅ 合并完成，输出文件: {output_file}")

# 示例使用
merge_rst_files('docs/Documentation', 'merged.rst')
