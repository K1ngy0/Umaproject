import os
import json
import argparse
import time

def find_video_files(root_dir, server_root, exclude_folders=None, show_progress=True, min_size_mb=3):
    """
    server_root: 服务器根目录（网页所在文件夹路径，如"D:\\VideoServer"）
    """
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv',
                        '.mpeg', '.mpg', '.m4v', '.webm', '.3gp', '.ogv',
                        '.rmvb', '.rm', '.asf', '.ts', '.mts', '.vob'}
    min_size_bytes = min_size_mb * 1024 * 1024
    
    # 标准化排除目录
    default_exclude = {os.path.normpath(p).strip() for p in [
        "C:\\Windows", "C:\\Program Files", "C:\\Program Files (x86)",
        "C:\\ProgramData", "C:\\Recovery", "C:\\System Volume Information"
    ]}
    exclude_folders_norm = set()
    if exclude_folders:
        exclude_folders_norm = {os.path.normpath(f).strip() for f in exclude_folders if os.path.isdir(f)}
    exclude_folders_norm.update(default_exclude)
    
    video_files = []
    scanned_dirs = 0
    start_time = time.time()
    small_files_count = 0

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        dirpath_norm = os.path.normpath(dirpath).strip()
        scanned_dirs += 1
        
        # 显示进度
        if show_progress and scanned_dirs % 50 == 0:
            elapsed = time.time() - start_time
            print(f"已扫描 {scanned_dirs} 目录 | 有效视频：{len(video_files)} | 排除小文件：{small_files_count} | 耗时 {elapsed:.1f}s", end='\r')
        
        # 跳过排除目录
        if dirpath_norm in exclude_folders_norm:
            continue
        dirnames[:] = [d.strip() for d in dirnames if os.path.normpath(os.path.join(dirpath_norm, d)).strip() not in exclude_folders_norm]
        
        for filename in filenames:
            # 过滤非法字符
            if any(c in filename for c in {'*', '?', '"', '<', '>', '|', ':'}):
                continue
            
            ext = os.path.splitext(filename)[1].lower()
            if ext not in video_extensions:
                continue
            
            # 关键：生成服务器相对路径（而非本地绝对路径）
            full_abs_path = os.path.join(dirpath_norm, filename)  # 本地绝对路径
            try:
                # 计算相对于服务器根目录的路径，并用/分隔（服务器标准）
                full_rel_path = os.path.relpath(full_abs_path, server_root).replace("\\", "/")
            except ValueError:
                # 视频不在服务器根目录范围内，跳过（或提示）
                print(f"\n警告：视频{full_abs_path}不在服务器范围内，已跳过", end='\r')
                continue
            
            # 检查文件大小
            try:
                file_size = os.path.getsize(full_abs_path)
            except (PermissionError, OSError):
                file_size = -1
            
            if file_size != -1 and file_size < min_size_bytes:
                small_files_count += 1
                continue
            
            video_files.append({
                "filename": filename,
                "server_path": full_rel_path,  # 仅输出服务器相对路径（如"UmaProject/movie.mp4"）
                "local_abs_path": full_abs_path,  # 可选：保留本地路径供参考
                "extension": ext,
                "size_bytes": file_size,
                "size_human": _format_size(file_size)
            })
    
    if show_progress:
        elapsed = time.time() - start_time
        print(f"\n遍历完成 | 总目录：{scanned_dirs} | 有效视频：{len(video_files)} | 排除小文件：{small_files_count} | 耗时 {elapsed:.1f}s")
    
    return video_files

def _format_size(size_bytes):
    if size_bytes < 0:
        return "无法访问"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(units)-1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.1f} {units[i]}"

def save_to_json(data, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"\nJSON已保存到：{os.path.abspath(output_file)}")
    except IOError as e:
        print(f"\n保存失败：{e}")

def main():
    parser = argparse.ArgumentParser(description="生成服务器相对路径的视频JSON")
    parser.add_argument("-r", "--root", default="C:\\Users\\Administrator\\Documents", help="视频扫描起始目录")
    parser.add_argument("-s", "--server-root", required=True, help="服务器根目录（网页所在文件夹，如 -s D:\\VideoServer）")
    parser.add_argument("-o", "--output", default="windows_videos.json", help="输出JSON文件名")
    parser.add_argument("-min", "--min-size", type=float, default=3, help="最小视频大小(MB)")
    args = parser.parse_args()
    
    # 验证服务器根目录存在（必须是网页所在文件夹）
    server_root = os.path.normpath(args.server_root).strip()
    if not os.path.isdir(server_root):
        print(f"错误：服务器根目录不存在 - {server_root}")
        return
    
    # 验证扫描目录存在
    root_dir = os.path.normpath(args.root).strip()
    if not os.path.isdir(root_dir):
        print(f"错误：扫描目录不存在 - {root_dir}")
        return
    
    print(f"扫描目录：{root_dir}")
    print(f"服务器根目录：{server_root}")
    print(f"最小视频大小：{args.min_size}MB")
    
    try:
        videos = find_video_files(
            root_dir=root_dir,
            server_root=server_root,  # 传入服务器根目录，用于计算相对路径
            min_size_mb=args.min_size
        )
        save_to_json(videos, args.output)
    except PermissionError:
        print("权限错误：以管理员身份运行CMD")
    except Exception as e:
        print(f"错误：{str(e)}")

if __name__ == "__main__":
    main()