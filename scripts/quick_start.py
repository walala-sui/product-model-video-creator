#!/usr/bin/env python3
"""
快速开始脚本 - 电商商品展示视频创建
最简单的使用方式，适合新手
"""

import os
import sys

# 添加当前目录到路径，以便导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from create_product_video import ProductVideoCreator
except ImportError:
    print("错误：无法导入 create_product_video 模块")
    print("请确保脚本在同一目录下")
    sys.exit(1)

def check_dependencies():
    """检查依赖是否已安装"""
    try:
        import cv2
        import numpy as np
        print("✅ 依赖检查通过")
        return True
    except ImportError as e:
        print(f"❌ 依赖缺失：{e}")
        print("\n请安装所需依赖：")
        print("pip install opencv-python pillow numpy")
        return False

def create_sample_video():
    """创建示例视频"""
    print("=" * 50)
    print("电商商品展示视频创建工具 - 快速开始")
    print("=" * 50)

    # 检查依赖
    if not check_dependencies():
        return

    # 获取用户输入
    print("\n📁 请提供模特图片路径：")
    image_path = input("图片路径（如：model.jpg）: ").strip()

    if not os.path.exists(image_path):
        print(f"❌ 文件不存在：{image_path}")
        return

    print("\n🎬 选择动画效果：")
    print("1. 缩放效果（镜头推进，突出商品细节）")
    print("2. 向右平移（模拟模特向右转身）")
    print("3. 向左平移（模拟模特向左转身）")
    print("4. 向上平移（模拟抬头）")
    print("5. 向下平移（模拟低头）")

    effect_choice = input("请选择效果（1-5，默认1）: ").strip() or "1"

    effect_map = {
        "1": "zoom",
        "2": "pan_right",
        "3": "pan_left",
        "4": "pan_up",
        "5": "pan_down"
    }

    effect = effect_map.get(effect_choice, "zoom")

    print("\n⏱️ 设置视频参数：")
    duration = input("视频时长（秒，默认4）: ").strip()
    duration = float(duration) if duration else 4.0

    fps = input("视频帧率（默认30）: ").strip()
    fps = int(fps) if fps else 30

    # 生成输出文件名
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_file = f"{base_name}_商品展示.mp4"

    print(f"\n📹 输出文件：{output_file}")

    # 创建视频
    print("\n🚀 正在创建视频...")
    creator = ProductVideoCreator(output_fps=fps, video_duration=duration)

    success = creator.process_single_image(image_path, effect, output_file)

    if success:
        print("\n🎉 视频创建成功！")
        print(f"文件位置：{os.path.abspath(output_file)}")

        # 建议
        print("\n💡 建议：")
        print("1. 使用高清图片（至少1280×720像素）效果更好")
        print("2. 纯色背景能让商品更突出")
        print("3. 视频时长3-5秒最适合电商平台")
        print("4. 可尝试不同效果找到最佳展示方式")
    else:
        print("\n😞 视频创建失败，请检查错误信息")

def batch_process():
    """批量处理多张图片"""
    print("\n🔄 批量处理模式")
    print("将处理指定文件夹中的所有图片")

    folder_path = input("图片文件夹路径: ").strip()

    if not os.path.isdir(folder_path):
        print(f"❌ 文件夹不存在：{folder_path}")
        return

    # 查找图片文件
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    image_files = []

    for ext in image_extensions:
        image_files.extend([
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.lower().endswith(ext)
        ])

    if not image_files:
        print("❌ 文件夹中没有找到图片文件")
        return

    print(f"✅ 找到 {len(image_files)} 张图片")

    output_folder = input("输出文件夹（默认: videos）: ").strip() or "videos"
    os.makedirs(output_folder, exist_ok=True)

    fps = 30
    duration = 4.0

    creator = ProductVideoCreator(output_fps=fps, video_duration=duration)

    success_count = 0
    for i, image_file in enumerate(image_files, 1):
        print(f"\n处理第 {i}/{len(image_files)} 张：{os.path.basename(image_file)}")

        base_name = os.path.splitext(os.path.basename(image_file))[0]
        output_file = os.path.join(output_folder, f"{base_name}_展示视频.mp4")

        # 交替使用不同效果
        effect = "zoom" if i % 2 == 0 else "pan_right"

        try:
            if creator.process_single_image(image_file, effect, output_file):
                success_count += 1
        except Exception as e:
            print(f"  处理失败：{e}")

    print(f"\n✅ 批量处理完成！成功：{success_count}/{len(image_files)}")

def main_menu():
    """主菜单"""
    while True:
        print("\n" + "=" * 50)
        print("电商商品展示视频创建工具")
        print("=" * 50)
        print("1. 创建单个商品展示视频")
        print("2. 批量处理多张图片")
        print("3. 查看使用说明")
        print("4. 退出")

        choice = input("\n请选择操作（1-4）: ").strip()

        if choice == "1":
            create_sample_video()
        elif choice == "2":
            batch_process()
        elif choice == "3":
            show_instructions()
        elif choice == "4":
            print("感谢使用！")
            break
        else:
            print("无效选择，请重新输入")

def show_instructions():
    """显示使用说明"""
    print("\n" + "=" * 50)
    print("使用说明")
    print("=" * 50)
    print("""
📌 准备工作：
1. 准备模特图片（建议1280×720以上分辨率）
2. 图片格式：JPG、PNG等常见格式
3. 确保商品在图片中清晰可见

🎬 效果说明：
• 缩放效果：镜头缓慢推进，突出商品细节
• 平移效果：模拟模特转身，展示不同角度
• 可添加高光效果，让商品更亮眼

⚙️ 命令行使用：
python create_product_video.py 图片路径 -e zoom -o 输出.mp4

🔧 高级选项：
• 调整视频时长：-d 参数
• 调整帧率：-f 参数
• 添加高光效果：--highlight 参数

📁 批量处理：
可将多张图片放在同一文件夹，使用批量处理功能

📞 技术支持：
如遇到问题，请检查：
1. Python版本（需要3.7+）
2. 依赖是否安装（opencv-python, pillow, numpy）
3. 图片路径是否正确
""")

    input("\n按Enter键返回主菜单...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n程序已退出")
    except Exception as e:
        print(f"\n❌ 发生错误：{e}")
        print("请检查输入和依赖安装")