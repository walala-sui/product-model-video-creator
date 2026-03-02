# Product Model Video Creator

将模特图片转换为电商商品展示视频，为模特添加佩戴商品的动态展示效果，每个视频3-5秒。适用于首饰、眼镜、服装等商品的电商展示。

![GitHub](https://img.shields.io/github/license/walala-sui/product-model-video-creator)
![Python](https://img.shields.io/badge/Python-3.7%2B-blue)

## 功能特性

- **多种动画效果**：缩放、平移（上下左右）、淡入淡出过渡
- **高光突出**：为商品添加高光效果，增强视觉吸引力
- **批量处理**：支持多张图片批量转换为视频
- **参数可调**：视频时长、帧率、效果强度等均可自定义
- **简单易用**：提供命令行工具和交互式界面两种使用方式

## 适用场景

- 电商商品详情页展示视频
- 社交媒体商品宣传视频
- 模特佩戴首饰、眼镜、手表等展示
- 服装上身效果动态展示
- 将产品图片转换为动态内容

## 快速开始

### 安装依赖

```bash
pip install opencv-python pillow numpy
```

### 使用命令行工具

```bash
# 单张图片转换
python scripts/create_product_video.py model.jpg -e zoom -o output.mp4

# 批量处理多张图片
python scripts/create_product_video.py "images/*.jpg" -o slideshow.mp4

# 添加高光效果
python scripts/create_product_video.py model.jpg --highlight --center-x 500 --center-y 300
```

### 使用交互式界面

```bash
python scripts/quick_start.py
```

## 详细使用说明

### 命令行参数

```
usage: create_product_video.py [-h] [-o OUTPUT] [-e {zoom,pan_right,pan_left,pan_up,pan_down}]
                              [-d DURATION] [-f FPS] [--zoom-factor ZOOM_FACTOR]
                              [--highlight] [--center-x CENTER_X] [--center-y CENTER_Y]
                              [--radius RADIUS] [--intensity INTENSITY]
                              image

电商商品展示视频创建工具

positional arguments:
  image                 输入图片路径（支持通配符如 *.jpg）

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        输出视频路径
  -e {zoom,pan_right,pan_left,pan_up,pan_down}, --effect {zoom,pan_right,pan_left,pan_up,pan_down}
                        动画效果类型
  -d DURATION, --duration DURATION
                        视频时长（秒）
  -f FPS, --fps FPS     视频帧率
  --zoom-factor ZOOM_FACTOR
                        缩放效果系数
  --highlight           添加高光效果
  --center-x CENTER_X   高光中心X坐标
  --center-y CENTER_Y   高光中心Y坐标
  --radius RADIUS       高光半径
  --intensity INTENSITY
                        高光强度
```

### 效果示例

1. **缩放效果（zoom）**：镜头缓慢推进，突出商品细节
2. **向右平移（pan_right）**：模拟模特向右转身
3. **向左平移（pan_left）**：模拟模特向左转身
4. **向上平移（pan_up）**：模拟抬头动作
5. **向下平移（pan_down）**：模拟低头动作

## 项目结构

```
product-model-video-creator/
├── scripts/
│   ├── create_product_video.py    # 主脚本，命令行工具
│   └── quick_start.py             # 快速开始脚本，交互式界面
├── README.md                      # 项目说明文档
├── requirements.txt               # 依赖包列表
└── .gitignore                     # Git忽略文件
```

## 依赖说明

- **Python 3.7+**
- **OpenCV**：图像处理和视频生成
- **Pillow**：图像处理
- **NumPy**：数值计算

安装命令：
```bash
pip install -r requirements.txt
```

## 常见问题

### Q: OpenCV安装失败怎么办？
A: 尝试安装轻量级版本：
```bash
pip install opencv-python-headless
```

### Q: 生成的视频太大怎么办？
A: 调整视频分辨率或降低帧率：
```bash
python scripts/create_product_video.py image.jpg -f 24 -d 3
```

### Q: 需要更复杂的动画效果怎么办？
A: 可以结合多种效果，或使用更高级的动画库如Manim。

### Q: 如何批量处理多张图片？
A: 使用通配符或批处理脚本：
```bash
python scripts/create_product_video.py "模特图片/*.jpg" -o 商品展示.mp4
```

## 最佳实践

1. **图片质量**：使用高清图片（至少1280×720）
2. **背景简洁**：纯色或简单背景效果更好
3. **商品位置**：确保商品在图片中明显可见
4. **视频时长**：电商平台建议3-5秒
5. **文件大小**：控制视频文件大小，便于加载

## 输出示例

- 输入：模特佩戴项链的图片
- 输出：4秒视频，包含缓慢缩放效果，突出项链细节
- 文件：项链展示.mp4（约2-5MB）

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 贡献

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个Pull Request

## 支持

如果您在使用过程中遇到问题，请：
1. 查看 [常见问题](#常见问题) 部分
2. 在 [Issues](https://github.com/walala-sui/product-model-video-creator/issues) 中搜索相关问题
3. 如果没有找到相关问题，请创建新的Issue

---

**注意**：此工具提供基础的视频生成功能。对于更复杂的需求，建议使用专业的视频编辑软件。