# 重建教程图解

SVG是本教程原创的确定性矢量图。发布图位于`assets/diagrams/`，正文另有图注与阅读步骤。

```bash
python tools/generate_diagrams.py
```

生成只依赖Python标准库。`diagram_lib.py`提供统一的文字、卡片、箭头和角色图例；`diagrams_advanced.py`绘制协作与案例图。

## 可选：手机尺寸视觉检查

安装Inkscape及Pillow后运行：

```bash
python tools/render_diagrams.py /tmp/tutorial-diagram-review
```

检查程序将每张图渲染为375像素宽PNG，并生成每页四图的检查拼图。PNG不必提交到仓库。

设计约束：640像素画布、中文字体回退、主要文字28–32像素、辅助文字24像素、角色标签22像素；颜色总有文字标签配合。SVG带`title`及`desc`，无脚本、外部资源或`foreignObject`。渲染结果受本地安装字体影响，推荐Noto Sans CJK SC。
