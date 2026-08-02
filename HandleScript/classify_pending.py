import os
import shutil
import unicodedata
from pathlib import Path

def stabilize_path(path_str):
    abs_path = os.path.abspath(path_str)
    if abs_path.startswith("\\\\"):
        return "\\\\?\\UNC\\" + abs_path[2:]
    return "\\\\?\\" + abs_path

def clean_filename(filename):
    # 移除 Z-Library 等元数据
    filename = filename.split(" (Z-Library")[0]
    filename = filename.split(" (z-library")[0]
    filename = filename.split(" (1lib.sk")[0]
    filename = filename.split(" (z-lib.sk")[0]
    filename = filename.split(" (1)")[0]
    filename = filename.split(" (2)")[0]
    
    # 清洗非法字符
    illegal_chars = {'/': '／', ':': '：', '*': '＊', '?': '？', '"': '＂', '<': '＜', '>': '＞', '|': '｜', '\\': '＼'}
    for char, replacement in illegal_chars.items():
        filename = filename.replace(char, replacement)
    
    # 去除首尾空格
    filename = filename.strip()
    return filename

def safe_move(src, dst_dir, final_name=None):
    if not final_name:
        final_name = clean_filename(os.path.basename(src))
    
    # 补充后缀（如果清理过程中丢失了）
    ext = os.path.splitext(src)[1]
    if not final_name.endswith(ext):
        final_name += ext
        
    dst_path = os.path.join(dst_dir, final_name)
    
    s_src = stabilize_path(src)
    s_dst = stabilize_path(dst_path)
    s_dst_dir = stabilize_path(dst_dir)
    
    os.makedirs(s_dst_dir, exist_ok=True)
    
    # 处理同名冲突
    counter = 1
    base_name, extension = os.path.splitext(dst_path)
    while os.path.exists(s_dst):
        new_name = f"{base_name}_{counter}{extension}"
        s_dst = stabilize_path(new_name)
        counter += 1
    
    shutil.move(s_src, s_dst)
    return os.path.basename(s_dst)

# 映射逻辑（AI语义识别结果）
# 基准目录统一为 已分类文件
tasks = [
    {
        "src": "待分类/保卫历史 马克思主义与后现代主义 (【美】埃伦.梅克辛斯.伍德 主编) (Z-Library).pdf",
        "dst": "已分类文件/社会意识/马克思主义哲学/"
    },
    {
        "src": "待分类/布伦纳《繁荣与泡沫 全球视角中的美国经济》.pdf",
        "dst": "已分类文件/社会意识/经济学/"
    },
    {
        "src": "待分类/布伦纳《全球动荡的经济学》([马克思主义研究译丛·典藏版]).pdf",
        "dst": "已分类文件/社会意识/经济学/"
    },
    {
        "src": "待分类/回到马克思 第2卷：社会场境论中的市民社会与劳动异化批判(上) (张一兵) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
        "dst": "已分类文件/社会意识/马克思主义哲学/"
    },
    {
        "src": "待分类/回到马克思 第2卷：社会场境论中的市民社会与劳动异化批判（下）_(张一兵)_(z-library.sk,_1lib.sk,_z-lib.sk).pdf",
        "dst": "已分类文件/社会意识/马克思主义哲学/"
    },
    {
        "src": "待分类/回到马克思：经济学语境中的哲学话语（第四版）_(张一兵)_(z-library.sk,_1lib.sk,_z-lib.sk).pdf",
        "dst": "已分类文件/社会意识/马克思主义哲学/"
    },
    {
        "src": "待分类/历史唯物主义原理 第3版 肖前 经典教科书系列 (萧前，李秀林，汪永祥) (z-library.sk, 1lib.sk, z-lib.sk)(1).pdf",
        "dst": "已分类文件/社会意识/马克思主义哲学/"
    },
    {
        "src": "待分类/社交媒体批判导言 (（英）克里斯蒂安·福克斯著；赵文丹译；李珮主编) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
        "dst": "已分类文件/社会意识/马克思主义哲学/"
    },
    {
        "src": "待分类/书评：列斐伏尔《马克思的社会学》.docx",
        "dst": "已分类文件/其它作品及论文/"
    },
    {
        "src": "待分类/数字劳动与卡尔·马克思 ([英] 克里斯蒂安·福克斯 译者 周延云) (z-library.sk, 1lib.sk, z-lib.sk).pdf",
        "dst": "已分类文件/社会意识/马克思主义哲学/"
    },
    {
        "src": "待分类/伍德《从阶级退却》.pdf",
        "dst": "已分类文件/社会意识/马克思主义哲学/"
    },
    {
        "src": "待分类/伍德《民主反对资本主义：重建历史唯物主义》 (1).pdf",
        "dst": "已分类文件/社会意识/马克思主义哲学/"
    },
    {
        "src": "待分类/伍德《为何阶级斗争是中心？》.pdf",
        "dst": "已分类文件/社会意识/马克思主义哲学/"
    },
    {
        "src": "待分类/伍德《资本的帝国》.pdf",
        "dst": "已分类文件/社会意识/马克思主义哲学/"
    },
    {
        "src": "待分类/伍德《资本主义的起源，一个更加长远的视角》.pdf",
        "dst": "已分类文件/社会意识/马克思主义哲学/"
    },
    {
        "src": "待分类/西方政治思想的社会史：公民到领主by艾伦·伍德.pdf",
        "dst": "已分类文件/历史与社会研究/西欧北美分区/"
    },
    {
        "src": "待分类/新的增长机制的诞生——对罗伯特·布伦纳危机理论的反驳_米歇尔·阿格利埃塔.pdf",
        "dst": "已分类文件/社会意识/经济学/"
    },
    {
        "src": "待分类/新社会主义by【加】艾伦·伍德.pdf",
        "dst": "已分类文件/社会意识/马克思主义哲学/"
    },
    {
        "src": "待分类/星火手册2022_马列毛主义入门_(mlm)_(z-library.sk,_1lib.sk,_z-lib.sk).pdf",
        "dst": "已分类文件/社科当代论/"
    }
]

log_entries = []
date_str = "2026/6/28"

for task in tasks:
    if os.path.exists(task["src"]):
        final_name = safe_move(task["src"], task["dst"])
        log_entries.append(f"  - `{os.path.basename(task['src'])}` -> `{task['dst']}{final_name}`")
    else:
        # 尝试搜索文件夹内是否存在类似文件（处理可能的空格或字符差异）
        found = False
        if os.path.exists("待分类"):
            for f in os.listdir("待分类"):
                # 这里使用简单的包含匹配，如果文件名非常相似则匹配
                # 为简单起见，在正式脚本中建议保持精确映射，此处作为鲁棒性备份
                src_basename = os.path.basename(task["src"])
                if src_basename[:10] in f: 
                    src = os.path.join("待分类", f)
                    final_name = safe_move(src, task["dst"])
                    log_entries.append(f"  - `{f}` -> `{task['dst']}{final_name}`")
                    found = True
                    break
        if not found:
            print(f"错误: 文件不存在 {task['src']}")

if log_entries:
    with open("classification_log.md", "a", encoding="utf-8") as log:
        log.write(f"\n# 分类操作日志 - {date_str}\n")
        log.write("操作内容：处理“待分类/”目录下的文件\n")
        log.write("处理逻辑：基于“AI 语义识别操作准则”进行全文件名整体语义分析，并严格映射至《分类标准.md》定义的路径。\n")
        log.write("操作结果：\n")
        log.write("- 成功将以下文件归入指定分区：\n")
        log.write("\n".join(log_entries) + "\n")
    print("处理完成，日志已更新。")
else:
    print("未发现待处理文件。")