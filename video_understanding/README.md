# FCMBench — Video Understanding Track Evaluation

This repository provides evaluation scripts for **FCMBench-Video** (Video Understanding track).
The workflow is:

1) download the video data
2) run inference with your model to produce a JSONL prediction file
3) evaluate predictions against the test groundtruth (when available)

---

## Environments

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) for environment management (recommended)

---

## Quickstart

### 1) Download video data and uncompress

The video data are hosted on both [**ModelScope**](https://modelscope.cn/datasets/QFIN/FCMBench-Data) and [**Hugging Face**](https://huggingface.co/datasets/QFIN/FCMBench-Data).

```bash
# (TBD) unzip FCMBench-Video_v1.0_Videos.zip
```

### 2) Run inference and save results (JSONL)

Use any inference framework or API to generate predictions, and save them as a **JSONL** file (one JSON object per line).

- Example API request code: *(TBD)*
- Example prediction (output) file format: *(TBD)*

> Tip: Keep the prediction file in UTF-8 and ensure each line is valid JSON.

### 3) Evaluate predictions

FCMBench-Video provides two test annotation files:
- `FCMBench-Video_testset_small.jsonl`: a subset where ground-truth annotations are provided.
  Use this file for self-testing, debugging, and diagnosis.
- `FCMBench-Video_testset_full.jsonl`: the full test set that only provides prompts (no ground-truth).
  Use this file to generate results for leaderboard submission.

Note: The subset (*_small.jsonl) is generally conservative for ranking compared with the full set, meaning relative ordering among models is often stable. However, absolute metric values may differ between the subset and the full test set.

From the repository root:

For `uv` users:

```bash
cd video_understanding # this folder
uv sync
# (TBD) uv run evaluation.py prediction_results.jsonl FCMBench-Video_testset_small.jsonl
```

For `pip` users:

```bash
cd video_understanding # this folder
# (TBD) pip3 install ...
# (TBD) python3 evaluation.py prediction_results.jsonl FCMBench-Video_testset_small.jsonl
```

---

## Leaderboard submission

To join the FCMBench-Video leaderboard:
1. Run inference on `FCMBench-Video_testset_full.jsonl`
2. Save your predictions to a JSONL file (same format as the example)
3. Email the JSONL file to [yangyehuisw@126.com] with the following information:
   - Model name / version
   - Inference framework (or API) and key settings (e.g., temperature, max tokens)
   - Any special post-processing (if applicable)

After validation, we will compute the official metrics on the hidden ground-truth and update the leaderboard.

---

## Output

The evaluator prints summary metrics to stdout.
