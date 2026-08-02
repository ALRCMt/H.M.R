import os
import shutil

def stabilize_path(path_str):
    abs_path = os.path.abspath(path_str)
    if abs_path.startswith("\\\\"):
        return "\\\\?\\UNC\\" + abs_path[2:]
    return "\\\\?\\" + abs_path

src_root = "已分类文件26.6.5"
dst_root = "已分类文件"

if os.path.exists(src_root):
    for root, dirs, files in os.walk(src_root):
        for file in files:
            src_file = os.path.join(root, file)
            # 计算相对路径
            rel_path = os.path.relpath(src_file, src_root)
            dst_file = os.path.join(dst_root, rel_path)
            dst_dir = os.path.dirname(dst_file)
            
            s_src = stabilize_path(src_file)
            s_dst = stabilize_path(dst_file)
            s_dst_dir = stabilize_path(dst_dir)
            
            os.makedirs(s_dst_dir, exist_ok=True)
            
            # 移动文件，如果目标已存在则覆盖（因为是纠偏操作）
            if os.path.exists(s_dst):
                os.remove(s_dst)
            shutil.move(s_src, s_dst)
            print(f"Moved: {rel_path}")

    # 清理空目录
    shutil.rmtree(stabilize_path(src_root))
    print(f"Cleaned up {src_root}")
else:
    print(f"Source {src_root} not found.")
