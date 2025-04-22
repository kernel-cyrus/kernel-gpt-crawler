import os
import subprocess

# Merge to seprate files.
def convert_rst_to_md(rst_path, md_path):
    try:
        subprocess.run(['pandoc', '-f', 'rst', '-t', 'markdown', rst_path, '-o', md_path],
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"❌ 转换失败：{rst_path} -> {md_path}，错误信息：{e.stderr.decode()}")

def merge_md_by_top_level_dirs(src_dir, output_dir, encoding='utf-8'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    top_dirs = [d for d in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, d))]

    for top_dir in top_dirs:
        top_path = os.path.join(src_dir, top_dir)
        md_contents = []
        temp_md_files = []

        for root, _, files in os.walk(top_path):
            for file in files:
                if file.endswith('.rst'):
                    rst_path = os.path.join(root, file)
                    rel_path = os.path.relpath(rst_path, top_path)
                    temp_md_path = rst_path + '.tmp.md'
                    convert_rst_to_md(rst_path, temp_md_path)
                    temp_md_files.append(temp_md_path)

                    try:
                        with open(temp_md_path, 'r', encoding=encoding) as f:
                            content = f.read()
                            md_contents.append(f"\n\n<!-- START OF: {rel_path} -->\n\n{content}\n\n<!-- END OF: {rel_path} -->\n\n")
                    except Exception as e:
                        print(f"⚠️ 读取失败: {temp_md_path}，错误: {e}")
                        continue

        # 写入最终合并文件
        output_file = os.path.join(output_dir, f"{top_dir}.md")
        with open(output_file, 'w', encoding=encoding) as outfile:
            outfile.writelines(md_contents)

        print(f"✅ 合并完成: {output_file}")

        # 删除中间文件
        for tmp_file in temp_md_files:
            try:
                os.remove(tmp_file)
            except:
                pass

# Merge to one file
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


merge_md_by_top_level_dirs('docs/Documentation', 'merged')
merge_rst_files('docs/Documentation', 'merged/KERNEL-DOC-MERGED.rst')