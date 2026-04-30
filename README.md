# FCMBench

[![arXiv](https://img.shields.io/badge/arXiv-2601.00150-b31b1b.svg)](https://arxiv.org/abs/2601.00150)
[![Dataset: Hugging Face](https://img.shields.io/badge/dataset-Hugging%20Face-yellow)](https://huggingface.co/datasets/QFIN/FCMBench-Data)
[![Dataset: ModelScope](https://img.shields.io/badge/dataset-ModelScope-blue)](https://modelscope.cn/datasets/QFIN/FCMBench-Data)
[![License](https://img.shields.io/github/license/QFIN-tech/FCMBench)](LICENSE)

![](assets/FCMBench_logo.jpg)

FCMBench is a multimodal benchmark for credit-risk and financial document workflows. It provides standardized datasets, prompts, evaluation scripts, and leaderboard-ready task definitions so research and industry teams can compare models on realistic credit scenarios.

[简体中文](./README_cn.md)

## Table of Contents
- [Highlights](#highlights)
- [News](#news)
- [Tracks](#tracks)
- [Quick Start](#quick-start)
- [Leaderboard Submission](#leaderboard-submission)
- [Resources](#resources)
- [Citation](#citation)
- [Contact](#contact)

## Highlights
- **Real-world focus** for financial credit and document intelligence workflows.
- **Multimodal evaluation** across image, video, speech, and agentic task directions.
- **Public benchmark assets** including datasets, prompts, example predictions, and evaluation scripts.
- **Leaderboard path** for submitting full-set results.

## News
- **2026-03-16**: Released **FCMBench v1.1**, adding English document images, more document types, and an expanded dataset with 5,198 images and 13,806 QA samples.
- **2026-01-01**: Released **FCMBench v1.0**, covering 18 certificate types, 4,043 privacy-compliant images, 8,446 QA samples, 3 perception tasks, 4 reasoning tasks, and 10 robustness inference categories.

## Tracks
### 1. Vision-Language Track (available)
Image-based financial document understanding.

- Entry: [vision_language](vision_language)
- Inputs: document images plus text prompts in JSONL
- Outputs: JSONL predictions, one sample per line
- Evaluation: [vision_language/evaluation.py](vision_language/evaluation.py)

### 2. Video Understanding Track (coming soon)
### 3. Speech Understanding and Generation Track (coming soon)
### 4. Multi-step / Agentic Track (coming soon)

## Quick Start
### Prerequisites
- Python 3.10+
- `uv` recommended, or `pip`
- Downloaded image assets from ModelScope or Hugging Face

### 1. Download the dataset
- [ModelScope dataset](https://modelscope.cn/datasets/QFIN/FCMBench-Data)
- [Hugging Face dataset](https://huggingface.co/datasets/QFIN/FCMBench-Data)

Unpack the image archive locally:

```bash
unzip FCMBench_v1.1_Images.zip
```

### 2. Review the track assets
Useful files in `vision_language/`:
- `README.md`, task-specific instructions
- `example_api_request.py`, sample inference request
- `prediction_results_example.jsonl`, output format example
- `FCMBench_v1.1_testset_small.jsonl`, self-test subset with ground truth
- `FCMBench_v1.1_testset_full.jsonl`, full evaluation file for submission

### 3. Install dependencies
Using `uv`:

```bash
cd vision_language
uv sync
```

Using `pip`:

```bash
cd vision_language
pip install "openai>=2.14.0" "pandas>=2.3.3"
```

### 4. Run evaluation
```bash
python evaluation.py prediction_results_example.jsonl FCMBench_v1.1_testset_small.jsonl
```

The small test set is best for debugging and sanity checks before you generate full-set predictions.

## Leaderboard Submission
To join the official leaderboard:
1. Run inference on `FCMBench_v1.1_testset_full.jsonl`.
2. Save predictions as JSONL in the same format as the provided example.
3. Email the result file with model details, inference settings, and post-processing notes.

## Resources
- [Paper on arXiv](https://arxiv.org/abs/2601.00150)
- [Technical report PDFs](https://github.com/QFIN-tech/FCMBench/tree/main/TechnicalReport)
- [Project page](https://github.com/QFIN-tech/FCMBench/tree/main/vision_language)
- [Leaderboard](https://qfin-tech.github.io/FCMBench)
- [Sample data](https://qfin-tech.github.io/FCMBench/Examples.html)

## Citation
```bibtex
@misc{yang2026fcmbenchlargescalefinancialcredit,
  title={FCMBench: The First Large-scale Financial Credit Multimodal Benchmark for Real-world Applications},
  author={Yehui Yang and Dalu Yang and Fangxin Shang and Wenshuo Zhou and Jie Ren and Yifan Liu and Haojun Fei and Qing Yang and Yanwu Xu and Tao Chen},
  year={2026},
  eprint={2601.00150},
  archivePrefix={arXiv},
  primaryClass={cs.CV},
  url={https://arxiv.org/abs/2601.00150}
}
```

## Contact
Maintainer: [Qfin Holdings / 奇富科技](https://github.com/QFIN-tech)  
Contact: `yangyehuisw@126.com`

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=QFIN-tech/FCMBench&type=date&legend=top-left)](https://www.star-history.com/#QFIN-tech/FCMBench&type=date&legend=top-left)
