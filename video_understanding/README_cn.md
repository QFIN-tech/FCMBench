# FCMBench — 视频理解赛道评测

[🌐 English](README.md)

本仓库提供 **FCMBench-Video**（视频理解赛道）的评测脚本。
整体流程为：

1) 准备视频数据和指令文件
2) 使用你的模型进行推理，生成 JSONL 预测文件
3) 依据提供的真值标注进行评估（或提交结果参与排行榜排名）

---

## 测试数据组成

FCMBench-Video v1.0 包含 **11,322** 组视频-问题对，覆盖 7 个任务和 2 个语言设置。

每个视频为信用审核文档的手持拍摄片段（每段 2-4 份文件），设置 20s / 40s / 60s 三种时长，每种时长拍摄 3 次。共 `1,200` 个视频（约 135 个人物场景），目录结构如下：

```
FCMBench-Video_v1.0_Videos/
└── video/
    ├── Construction/          # 中文原始视频（15 人 × 9 = 135 个片段）
    ├── Construction-en-US/    # 英文原始视频（30 人 × 9 = 265 个片段）
    ├── VPI-cn/                # 中文视觉提示注入视频（135 个片段）
    ├── VPI-cot-cn/            # 中文 VPI + 思维链视频（135 个片段）
    ├── VPI-en-US/             # 英文 VPI 视频（265 个片段）
    └── VPI-cot-en-US/         # 英文 VPI + 思维链视频（265 个片段）
```

### 指令文件说明

| 文件 | 说明 | 含真值 | 用途 |
|------|------|:------:|------|
| `FCMBench-Video_v1.0_full.jsonl` | 全量 11,322 条（中英文合并） | ✗ | 公开发布，用于推理 |
| `FCMBench-Video_v1.0_small.jsonl` | 分层 10% 采样（~1,135 条） | ✓ | 快速自测 / 调试诊断 |
| `FCMBench-Video_v1.0_full-gt.jsonl` | 全量 11,322 条 | ✓ | 内部参考（不分发） |

**任务分布**（7 类，覆盖感知与推理）：

| 类别 | 任务 | 中文 (zh_zh / zh_en) | 英文 (en_en) |
|------|------|---------------------|-------------|
| 感知 | classification（文档分类） | 1,350 | 1,325 |
| 感知 | counting（文档计数） | 1,350 | 1,325 |
| 感知 | temporal_grounding（时序定位） | 1,350 | 1,325 |
| 推理 | VPI（视觉提示注入） | 540 | 530 |
| 推理 | VPI-CoT（VPI + 思维链） | 540 | 530 |
| 推理 | CDV（跨文档验证） | 270 | — |
| 推理 | EGS（证据支撑度评分） | 560 | 327 |
| **合计** | | **5,960** | **5,362** |

---

## 环境要求

- Python 3.10+
- 推荐使用 `uv` 进行依赖管理
- 也可以使用 `pip` 创建传统虚拟环境

```bash
# uv
uv sync

# pip
pip install openai tqdm json-repair
```

---

## 快速开始

### 1) 准备视频数据

```bash
unzip FCMBench-Video_v1.0_Videos.zip
```

解压后目录结构如下：

```
FCMBench-Video_v1.0_Videos/
└── video/
    ├── Construction/
    ├── Construction-en-US/
    ├── VPI-cn/
    ├── VPI-cot-cn/
    ├── VPI-en-US/
    └── VPI-cot-en-US/
```

指令文件的每条记录使用 `video_prefix` + `video_path` 来定位视频（例如：
`"video_prefix": "Construction", "video_path": "yangyimiao/yangyimiao_20s_1.mp4"`），
因此将 `--video_root` 指向 `FCMBench-Video_v1.0_Videos/` 目录即可。

### 2) 运行推理

使用**单一的**指令文件 `FCMBench-Video_v1.0_full.jsonl`（不含真值）。
Python 脚本和 Shell 管道脚本均接受 `--input_file` 参数。

```bash
bash benchmark_pipeline.sh \
  --input_file FCMBench-Video_v1.0_full.jsonl \
  --output_dir ./results \
  --video_root ./FCMBench-Video_v1.0_Videos \
  --model <模型名称> \
  --base_url <API地址>
```

也可以直接调用 `benchmark_infer.py`：

```bash
python benchmark_infer.py \
  --input_file FCMBench-Video_v1.0_full.jsonl \
  --output_dir ./results \
  --video_root ./FCMBench-Video_v1.0_Videos \
  --model <模型名称> \
  --base_url <API地址>
```

> **断点续传：** 添加 `--resume` 可跳过已有输出的 `task_id`。

推理脚本会生成一个结果文件：
```
results/FCMBench-Video_v1.0_full_<模型名>_<run_id>.jsonl
```

输出的每一行由原始指令行加上一个 `"response"` 字段组成，该字段为模型的原始回复文本。

### 3) 评估预测结果

```bash
python benchmark_eval.py --result_dir ./results
```

评估器要求 `--result_dir` 目录中**有且仅有一个** `.jsonl` 文件。它会在终端打印各任务维度的指标（按中/英文子集和视频时长拆分），同时写入：

- `results/eval_reports/FCMBench-Video_v1.0_full_<模型名>_<run_id>.txt` — 各任务详细指标
- `results/eval_reports/benchmark_overall.txt` — 基准总得分

### 使用 small.jsonl 自测

如需快速验证，可使用 `FCMBench-Video_v1.0_small.jsonl`（约 1,135 条分层采样，含真值标注）。
按照上述相同流程运行推理，再进行评估——指标将直接根据内置的真值计算。

---

## 排行榜

### 自测（small.jsonl）

研究人员可以使用 `FCMBench-Video_v1.0_small.jsonl` 进行推理，并利用
`benchmark_eval.py` 在本地计算评测指标，从而得到模型在全部 7 个任务和两种语言子集上的可靠近似性能表现。

### 官方排行榜提交

如需将你的模型纳入 **FCMBench-Video 排行榜**排名：

1. 使用你的模型对 **`FCMBench-Video_v1.0_full.jsonl`** 进行推理。
2. 将预测结果保存为单个 JSONL 文件（`benchmark_infer.py` 输出格式即为预期格式——每行一个 JSON 对象，包含 `task_id` 和 `response` 字段）。
3. 将结果文件发送至 **yangyehuisw@126.com**，并附上以下信息：
   - 模型名称 / 版本
   - 推理框架（或 API）及关键参数设置（如 temperature、max tokens 等）
   - 是否使用了特殊的后处理（如适用）

我们验证通过后，会在隐藏的真值文件（`FCMBench-Video_v1.0_full-gt.jsonl`）上计算官方指标并更新排行榜。
