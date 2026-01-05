# FCMBench — Vision Language Track Evaluation

![](../assets/tasks_robustness_overview.png)

This repository provides evaluation scripts for **FCMBench** (Vision-Language track).  
The workflow is:

1) download the image data  
2) run inference with your model to produce a JSONL prediction file  
3) evaluate predictions against the test groundtruth (when available)

---

## Environments

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) for environment management (recommended)

---

## Quickstart

### 1) Download image data and uncompress

The image data are hosted on both [**ModelScope**](https://modelscope.cn/datasets/QFIN/FCMBench-V1.0) and [**Hugging Face**](https://huggingface.co/datasets/QFIN/FCMBench-V1.0).

```bash
unzip V1.0_TESTSET.zip # uncompress to ./data/oceanus-share/V1.0_IMAGES_TEST/
```

### 2) Run inference and save results (JSONL)

Use any inference framework or API to generate predictions, and save them as a **JSONL** file (one JSON object per line).

- Example API request code: `example_api_request.py`
- Example prediction(output) file format: `prediction_results_example.jsonl`

> Tip: Keep the prediction file in UTF-8 and ensure each line is valid JSON.

### 3) Evaluate predictions

FCMBench provides two test annotation files:
-  ```FCMBench_v1.0_testset_small.jsonl```: a subset where ground-truth annotations are provided.
Use this file for self-testing, debugging, and diagnosis.
- ```FCMBench_v1.0_testset_full.jsonl```: the full test set that only provides prompts (no ground-truth).
Use this file to generate results for leaderboard submission.

Note: The subset (*_small.jsonl) is generally conservative for ranking compared with the full set, meaning relative ordering among models is often stable. However, absolute metric values may differ between the subset and the full test set.


From the repository root:

For `uv` users:
  
```bash
cd vision_language # this folder
uv sync
uv run evaluation.py prediction_results.jsonl FCMBench_v1.0_testset_small.jsonl
```

For `pip` users:

```bash
cd vision_language # this folder
pip3 install openai>=2.14.0 pandas>=2.3.3
python3 evaluation.py prediction_results.jsonl FCMBench_v1.0_testset_small.jsonl
```

Where: 
- ```prediction_results.jsonl``` is your model output file; use ```prediction_results_example.jsonl``` if you haven't generated your own results
- ```FCMBench_v1.0_testset_small.jsonl``` is the official self-test subset annotation file (ground-truth provided). 

## Leaderboard submission

To join the FCMBench leaderboard:
1.	Run inference on ```FCMBench_v1.0_testset_full.jsonl```
2.	Save your predictions to a JSONL file (same format as the example)
3.	Email the JSONL file to [yangyehui-jk@qifu.com] with the following information:
	•	Model name / version
	•	Inference framework (or API) and key settings (e.g., temperature, max tokens)
	•	Any special post-processing (if applicable)

After validation, we will compute the official metrics on the hidden ground-truth and update the leaderboard.


## Output

The evaluator prints summary metrics to stdout.
