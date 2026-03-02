#!/usr/bin/env python3
"""
电商商品展示视频创建工具
将模特图片转换为动态展示视频，支持缩放、平移等效果
"""

import cv2
import numpy as np
import os
import sys
import argparse

class ProductVideoCreator:
    def __init__(self, output_fps=30, video_duration=4):
        """初始化视频创建器
        Args:
            output_fps: 输出视频帧率（默认30fps）
            video_duration: 视频时长（秒，默认4秒）
        """
        self.output_fps = output_fps
        self.video_duration = video_duration
        self.total_frames = output_fps * video_duration

    def read_image(self, image_path):
        """读取图片并转换为RGB格式"""
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"无法读取图片：{image_path}")
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    def create_zoom_effect(self, image, zoom_factor=1.2):
        """创建缩放效果（模拟镜头推进）
        Args:
            image: 输入图像（RGB格式）
            zoom_factor: 缩放系数（>1为放大，<1为缩小）
        """
        height, width = image.shape[:2]
        frames = []

        for i in range(self.total_frames):
            # 计算当前缩放比例
            progress = i / (self.total_frames - 1)
            current_zoom = 1.0 + (zoom_factor - 1.0) * progress

            # 计算新的尺寸
            new_width = int(width / current_zoom)
            new_height = int(height / current_zoom)

            # 计算裁剪区域（居中）
            x1 = (width - new_width) // 2
            y1 = (height - new_height) // 2
            x2 = x1 + new_width
            y2 = y1 + new_height

            # 裁剪并调整大小
            cropped = image[y1:y2, x1:x2]
            resized = cv2.resize(cropped, (width, height))
            frames.append(resized)

        return frames

    def create_pan_effect(self, image, pan_direction='right'):
        """创建平移效果（模拟模特转身）
        Args:
            image: 输入图像（RGB格式）
            pan_direction: 平移方向（'left', 'right', 'up', 'down'）
        """
        height, width = image.shape[:2]
        frames = []

        # 扩展图像以允许平移
        expand_factor = 1.5
        expanded_width = int(width * expand_factor)
        expanded_height = int(height * expand_factor)

        # 创建扩展画布
        if len(image.shape) == 3:
            expanded = np.zeros((expanded_height, expanded_width, 3), dtype=np.uint8)
        else:
            expanded = np.zeros((expanded_height, expanded_width), dtype=np.uint8)

        # 将原图放在扩展画布中央
        x_offset = (expanded_width - width) // 2
        y_offset = (expanded_height - height) // 2
        expanded[y_offset:y_offset+height, x_offset:x_offset+width] = image

        # 计算平移范围
        if pan_direction == 'right':
            start_x = 0
            end_x = expanded_width - width
            y = y_offset
        elif pan_direction == 'left':
            start_x = expanded_width - width
            end_x = 0
            y = y_offset
        elif pan_direction == 'down':
            x = x_offset
            start_y = 0
            end_y = expanded_height - height
        elif pan_direction == 'up':
            x = x_offset
            start_y = expanded_height - height
            end_y = 0
        else:
            raise ValueError(f"不支持的平移方向：{pan_direction}")

        for i in range(self.total_frames):
            progress = i / (self.total_frames - 1)

            if pan_direction in ['right', 'left']:
                current_x = int(start_x + (end_x - start_x) * progress)
                frame = expanded[y:y+height, current_x:current_x+width]
            else:  # up or down
                current_y = int(start_y + (end_y - start_y) * progress)
                frame = expanded[current_y:current_y+height, x:x+width]

            frames.append(frame)

        return frames

    def create_fade_transition(self, image1, image2):
        """创建淡入淡出过渡效果（用于多张图片）
        Args:
            image1: 第一张图片
            image2: 第二张图片
        """
        # 确保两张图片尺寸相同
        if image1.shape != image2.shape:
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

        frames = []
        half_frames = self.total_frames // 2

        # 第一张图片淡出，第二张图片淡入
        for i in range(half_frames):
            alpha = 1.0 - (i / (half_frames - 1))
            frame = cv2.addWeighted(image1, alpha, image2, 1-alpha, 0)
            frames.append(frame)

        # 第二张图片保持
        for i in range(half_frames, self.total_frames):
            frames.append(image2)

        return frames

    def add_highlight_effect(self, image, center_x, center_y, radius=50, intensity=0.3):
        """为商品添加高光效果
        Args:
            image: 输入图像
            center_x: 高光中心X坐标
            center_y: 高光中心Y坐标
            radius: 高光半径
            intensity: 高光强度（0-1）
        """
        height, width = image.shape[:2]

        # 创建高光遮罩
        y, x = np.ogrid[:height, :width]
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        mask = np.clip(1 - distance/radius, 0, 1)

        # 将遮罩应用到所有通道
        if len(image.shape) == 3:
            mask = np.stack([mask]*3, axis=2)

        # 增强亮度
        highlighted = image.astype(np.float32)
        highlighted += highlighted * mask * intensity
        highlighted = np.clip(highlighted, 0, 255).astype(np.uint8)

        return highlighted

    def create_video(self, frames, output_path, quality=23):
        """将帧序列保存为视频
        Args:
            frames: 帧列表
            output_path: 输出视频路径
            quality: 视频质量（0-51，越小质量越高）
        """
        if not frames:
            print("错误：没有帧可保存")
            return False

        height, width = frames[0].shape[:2]

        # 创建视频写入器（使用H.264编码）
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.output_fps, (width, height))

        if not out.isOpened():
            print(f"无法创建视频文件：{output_path}")
            return False

        for frame in frames:
            # 转换为BGR格式（OpenCV使用BGR）
            if len(frame.shape) == 3:
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            else:
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            out.write(frame_bgr)

        out.release()
        print(f"✓ 视频已保存至：{output_path}")
        print(f"  分辨率：{width}×{height}")
        print(f"  时长：{self.video_duration}秒")
        print(f"  帧数：{len(frames)}帧")
        print(f"  帧率：{self.output_fps}fps")

        # 获取文件大小
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / (1024*1024)  # MB
            print(f"  文件大小：{file_size:.2f} MB")

        return True

    def process_single_image(self, image_path, effect='zoom', output_path=None, **kwargs):
        """处理单张图片
        Args:
            image_path: 输入图片路径
            effect: 效果类型 ('zoom', 'pan_right', 'pan_left', 'pan_up', 'pan_down')
            output_path: 输出视频路径（默认为图片名+_video.mp4）
            **kwargs: 其他参数（如zoom_factor, pan_direction等）
        """
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = f"{base_name}_展示视频.mp4"

        print(f"正在处理：{image_path}")
        print(f"效果类型：{effect}")
        print(f"输出文件：{output_path}")

        # 读取图片
        try:
            image = self.read_image(image_path)
        except ValueError as e:
            print(f"错误：{e}")
            return False

        # 应用选定效果
        if effect == 'zoom':
            zoom_factor = kwargs.get('zoom_factor', 1.2)
            frames = self.create_zoom_effect(image, zoom_factor)
        elif effect.startswith('pan_'):
            direction = effect.split('_')[1]
            frames = self.create_pan_effect(image, direction)
        else:
            print(f"警告：不支持的效果 '{effect}'，使用默认缩放效果")
            frames = self.create_zoom_effect(image)

        # 如果需要高光效果
        if kwargs.get('highlight'):
            center_x = kwargs.get('center_x', image.shape[1] // 2)
            center_y = kwargs.get('center_y', image.shape[0] // 2)
            radius = kwargs.get('radius', 50)
            intensity = kwargs.get('intensity', 0.3)

            highlighted_frames = []
            for frame in frames:
                highlighted = self.add_highlight_effect(frame, center_x, center_y, radius, intensity)
                highlighted_frames.append(highlighted)
            frames = highlighted_frames

        # 保存视频
        success = self.create_video(frames, output_path)
        return success

    def process_multiple_images(self, image_paths, output_path='product_slideshow.mp4'):
        """处理多张图片（创建幻灯片）
        Args:
            image_paths: 图片路径列表
            output_path: 输出视频路径
        """
        if not image_paths:
            print("错误：没有提供图片路径")
            return False

        print(f"正在处理 {len(image_paths)} 张图片...")

        all_frames = []
        frames_per_image = self.total_frames // len(image_paths)

        # 临时修改设置
        original_duration = self.video_duration
        self.video_duration = original_duration // len(image_paths)
        self.total_frames = self.output_fps * self.video_duration

        for i, image_path in enumerate(image_paths):
            print(f"  处理第 {i+1}/{len(image_paths)} 张：{os.path.basename(image_path)}")

            try:
                image = self.read_image(image_path)
            except ValueError as e:
                print(f"  跳过：{e}")
                continue

            # 交替使用不同的效果
            if i % 2 == 0:
                frames = self.create_zoom_effect(image, zoom_factor=1.1)
            else:
                direction = 'right' if i % 2 == 0 else 'left'
                frames = self.create_pan_effect(image, direction)

            all_frames.extend(frames)

        # 恢复原始设置
        self.video_duration = original_duration
        self.total_frames = self.output_fps * self.video_duration

        # 保存视频
        success = self.create_video(all_frames, output_path)
        return success


def main():
    """命令行入口函数"""
    parser = argparse.ArgumentParser(description='电商商品展示视频创建工具')
    parser.add_argument('image', help='输入图片路径（支持通配符如 *.jpg）')
    parser.add_argument('-o', '--output', help='输出视频路径')
    parser.add_argument('-e', '--effect', default='zoom',
                       choices=['zoom', 'pan_right', 'pan_left', 'pan_up', 'pan_down'],
                       help='动画效果类型')
    parser.add_argument('-d', '--duration', type=float, default=4.0,
                       help='视频时长（秒）')
    parser.add_argument('-f', '--fps', type=int, default=30,
                       help='视频帧率')
    parser.add_argument('--zoom-factor', type=float, default=1.2,
                       help='缩放效果系数')
    parser.add_argument('--highlight', action='store_true',
                       help='添加高光效果')
    parser.add_argument('--center-x', type=int, help='高光中心X坐标')
    parser.add_argument('--center-y', type=int, help='高光中心Y坐标')
    parser.add_argument('--radius', type=int, default=50, help='高光半径')
    parser.add_argument('--intensity', type=float, default=0.3, help='高光强度')

    args = parser.parse_args()

    # 处理通配符
    import glob
    image_paths = glob.glob(args.image)

    if not image_paths:
        print(f"错误：找不到匹配的图片：{args.image}")
        return

    # 创建视频生成器
    creator = ProductVideoCreator(output_fps=args.fps, video_duration=args.duration)

    if len(image_paths) == 1:
        # 单张图片
        kwargs = {
            'zoom_factor': args.zoom_factor,
            'highlight': args.highlight,
            'center_x': args.center_x,
            'center_y': args.center_y,
            'radius': args.radius,
            'intensity': args.intensity
        }
        success = creator.process_single_image(
            image_paths[0],
            args.effect,
            args.output,
            **kwargs
        )
    else:
        # 多张图片
        print(f"找到 {len(image_paths)} 张图片，创建幻灯片...")
        success = creator.process_multiple_images(image_paths, args.output)

    if success:
        print("\n✅ 视频创建完成！")
    else:
        print("\n❌ 视频创建失败")
        sys.exit(1)


if __name__ == "__main__":
    main()