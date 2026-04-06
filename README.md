# Academic-Gantt：学术时间线甘特图工具

Academic-Gantt 是一个面向论文、课题和课程项目汇报的甘特图生成工具。
它的核心目标是：使用标准化数据模板，一条命令自动生成可用于论文/汇报的图表。

## 项目特性

- A4 竖版输出
- 统一学术配色（无标题、无图例）
- 图像字体适配：英文默认 Arial，中文默认宋体（SimSun）
- 支持英文与中文数据模板
- 支持里程碑（`Type=Milestone` 或 `类型=里程碑`）
- 支持输出 `pdf/png/svg`
- PNG 默认 `600 DPI`，并强制不低于 `300 DPI`

## 预览（中英并排）

<div align="center">
  <img src="assets/readme_preview_en.png" alt="English Preview" width="48%" />
  <img src="assets/readme_preview_zh.png" alt="中文预览" width="48%" />
</div>

### 中文预览（放大）

<div align="center">
  <img src="assets/readme_preview_zh.png" alt="中文预览放大" width="72%" />
</div>

## 示例模板（中英并排）

| 英文模板 | 中文模板 |
|---|---|
| [data_template.md](data_template.md) | [data_template_zh.md](data_template_zh.md) |

## 环境准备（Conda）

```bash
# 1) 创建环境
conda create -n gantt python=3.11 -y

# 2) 激活环境
conda activate gantt

# 3) 安装依赖
pip install -r requirements.txt
```

## 一键运行

```bash
python main.py
```

默认行为：

- 输入：`data_template.md`
- 输出：`output/academic_gantt.pdf`

## 常用命令

```bash
# 英文模板 -> PDF
python main.py --input data_template.md --output output/plan_en --format pdf

# 中文模板 -> PNG（默认 600 DPI）
python main.py --input data_template_zh.md --output output/plan_zh --format png

# 指定 PNG 分辨率（必须 >=300）
python main.py --input data_template_zh.md --output output/plan_zh --format png --dpi 600
```

## DPI 规则

- `--dpi` 只对 `png` 生效，默认值为 `600`
- 当 `--format png` 时，`--dpi` 必须 `>=300`
- 对 `pdf/svg` 输出，`--dpi` 会被忽略

## 字体安装说明（不通过 pip）

字体属于系统资源，不是 Python 包，因此**不通过 `pip install` 安装**。

当前策略：

- 英文文本优先：`Arial`
- 中文文本优先：`SimSun`（宋体）
- 若缺失会自动回退到系统可用字体

### Windows（推荐）

1. 打开 `C:\Windows\Fonts`
2. 确认存在 `Arial` 和 `SimSun`（宋体）
3. 若缺失，安装对应字体文件（通常 `.ttf/.ttc`），右键“安装”
4. 重启终端后重新运行 `python main.py`

### macOS

1. 用“字体册”安装字体
2. 中文可选 `Songti SC`，英文可选 `Arial`

### Linux

1. 英文可安装 Liberation/Arial 兼容字体
2. 中文建议安装 `Noto Sans CJK`
3. 常见命令（Ubuntu/Debian）：

```bash
sudo apt update
sudo apt install -y fonts-noto-cjk
```

## 数据模板规范

| 字段（英文） | 字段（中文） | 说明 |
|---|---|---|
| Task | 任务/任务名称 | 任务名称 |
| Start | 开始/开始日期 | 开始日期（YYYY-MM-DD） |
| End | 结束/结束日期 | 结束日期（YYYY-MM-DD） |
| Resource | 资源/任务类别 | 分类字段（当前用于数据管理） |
| Type | 类型/节点类型 | Task/任务 或 Milestone/里程碑 |

## 项目结构

```text
.
├── assets/
│   ├── readme_preview_en.png
│   └── readme_preview_zh.png
├── src/
│   ├── parser.py
│   ├── plotter.py
│   └── styles.py
├── data_template.md
├── data_template_zh.md
├── data_template.csv
├── main.py
├── requirements.txt
└── README.md
```

## 更新日志

### 2026-04-06

- 增加中文数据模板支持（中文列名、中文类型值）
- 增加 PNG 分辨率接口 `--dpi`（默认 600，PNG 最低 300）
- 中英文模板与预览图并排展示，并增加中文放大预览
- 图像字体策略更新为：英文 Arial、中文 SimSun（宋体）优先
- 图表纵向布局进一步收窄，视觉更贴近课程模板
- 明确字体安装为系统级操作，不通过 pip
