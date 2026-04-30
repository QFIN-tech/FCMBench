# FCMBench — Video Understanding Track Evaluation

[🌐 简体中文](README_cn.md)

This repository provides evaluation scripts for **FCMBench-Video** (Video Understanding track).
The workflow is:

1) prepare the video data and instruction file
2) run inference with your model to produce a JSONL prediction file
3) evaluate predictions against the provided ground-truth (or submit results for leaderboard ranking)

---

## Test Data Composition

FCMBench-Video v1.0 contains **11,322** video–question pairs across 7 tasks and 2 language settings.

Each video is a handheld recording of credit-review documents (2—4 per clip) at 20s / 40s / 60s, with 3 takes per duration. The `1,200` videos (≈135 person-scenarios) are organized as:

```
FCMBench-Video_v1.0_Videos/
└── video/
    ├── Construction/          # CN original videos (15 persons × 9 = 135 clips)
    ├── Construction-en-US/    # EN original videos (30 persons × 9 = 265 clips)
    ├── VPI-cn/                # CN videos with visual prompt injection (135 clips)
    ├── VPI-cot-cn/            # CN VPI + Chain-of-Thought (135 clips)
    ├── VPI-en-US/             # EN VPI (265 clips)
    └── VPI-cot-en-US/         # EN VPI + CoT (265 clips)
```

### Instruction files

| File | Description | Has GT | Use case |
|------|-------------|--------|----------|
| `FCMBench-Video_v1.0_full.jsonl` | Full 11,322 samples (CN + EN merged) | ✗ | Public release; run inference |
| `FCMBench-Video_v1.0_small.jsonl` | Stratified 10% sample (~1,135) | ✓ | Quick self-evaluation / sanity check |
| `FCMBench-Video_v1.0_full-gt.jsonl` | Full 11,322 samples | ✓ | Internal reference (not distributed) |

**Tasks** (7 types across perception & reasoning):

| Category | Task | CN (zh_zh / zh_en) | EN (en_en) |
|----------|------|---------------------|------------|
| perception | classification | 1,350 | 1,325 |
| perception | counting | 1,350 | 1,325 |
| perception | temporal_grounding | 1,350 | 1,325 |
| reasoning | VPI | 540 | 530 |
| reasoning | VPI-CoT | 540 | 530 |
| reasoning | CDV | 270 | — |
| reasoning | EGS | 560 | 327 |
| **Total** | | **5,960** | **5,362** |

---

## Environments

- Python 3.10+
- `uv` is recommended for dependency management
- Or use `pip` if you prefer a traditional virtual environment

```bash
# uv
uv sync

# pip
pip install openai tqdm json-repair
```

---

## Quickstart

### 1) Prepare video data

```bash
unzip FCMBench-Video_v1.0_Videos.zip
```

The unzipped tree will look like:

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

The instruction JSONL files use `video_prefix` + `video_path` fields (e.g.
`"video_prefix": "Construction", "video_path": "yangyimiao/yangyimiao_20s_1.mp4"`),
so point `--video_root` to the `FCMBench-Video_v1.0_Videos/` directory.

### 2) Run inference

Use the **single** instruction file `FCMBench-Video_v1.0_full.jsonl` (no ground-truth).
Both the Python script and the shell pipeline accept a `--input_file` argument.

```bash
bash benchmark_pipeline.sh \
  --input_file FCMBench-Video_v1.0_full.jsonl \
  --output_dir ./results \
  --video_root ./FCMBench-Video_v1.0_Videos \
  --model <model_name> \
  --base_url <base_url>
```

Or call `benchmark_infer.py` directly:

```bash
python benchmark_infer.py \
  --input_file FCMBench-Video_v1.0_full.jsonl \
  --output_dir ./results \
  --video_root ./FCMBench-Video_v1.0_Videos \
  --model <model_name> \
  --base_url <base_url>
```

> **Resume support:** add `--resume` to skip task IDs already present in the output file.

The inference script writes one result file:
```
results/FCMBench-Video_v1.0_full_<model>_<run_id>.jsonl
```

Each output line is the original instruction line plus a `"response"` field
containing the model's raw reply.

### 3) Evaluate predictions

```bash
python benchmark_eval.py --result_dir ./results
```

The evaluator expects **exactly one** `.jsonl` file in `--result_dir`. It prints
per-task metrics (by zh/en subset and by video duration) to stdout and also writes:

- `results/eval_reports/FCMBench-Video_v1.0_full_<model>_<run_id>.txt` — per-task breakdown
- `results/eval_reports/benchmark_overall.txt` —  benchmark-level overall score

### Self-evaluation with small.jsonl

For a quick sanity check, use `FCMBench-Video_v1.0_small.jsonl` (~1,135 stratified
samples with ground-truth). Run inference on it (same workflow as above), then
evaluate — metrics are computed against the included GT.

---

## Leaderboard

### Self-assessment (small.jsonl)

Researchers can run inference on `FCMBench-Video_v1.0_small.jsonl` and compute
evaluation metrics locally using `benchmark_eval.py`. This gives a reliable
approximation of model performance across all 7 tasks and both language subsets.

### Official leaderboard submission

To have your model ranked on the **FCMBench-Video leaderboard**:

1. Run inference on **`FCMBench-Video_v1.0_full.jsonl`** with your model.
2. Save predictions to a single JSONL file (the `benchmark_infer.py` output format
   is the expected format — one JSON object per line with `task_id` and `response`).
3. Email the result file to **yangyehuisw@126.com** with the following information:
   - Model name / version
   - Inference framework (or API) and key settings (e.g., temperature, max tokens)
   - Any special post-processing applied (if applicable)

After validation, we will compute the official metrics on the hidden ground-truth
(`FCMBench-Video_v1.0_full-gt.jsonl`) and update the leaderboard.