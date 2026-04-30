![](assets/FCMBench_logo.jpg)


**FCMBench** is a multimodal benchmark for credit-risk–oriented workflows. It aims to provide a standard playground to promote collaborative development between academia and industry and provides standardized datasets, prompts, and evaluation scripts across multiple tracks (image, video, speech, agents, etc.)

[简体中文](./README_cn.md)

## 🔥 News 
- 【**2026. 03. 16**】✨ We released **FCMBench-V1.1**. This version adds English document images and corresponding QA pairs, expands the covered document types to 26, and increases the dataset to 5,198 images and 13,806 QA samples.
- 【**2026. 01. 01**】We are proud to launch **FCMBench-V1.0**, which covers 18 core certificate types, including 4,043 privacy-compliant images and 8,446 QA samples. It involves 3 types of Perception tasks and 4 types of Reasoning tasks, which are cross-referenced with 10 categories of robustness inferences. All the tasks and inferences are derived from real-world critical scenarios.

> **Status:** Public release (v1.1).  
> **Maintainers:** [奇富科技 / Qfin Holdings](https://github.com/QFIN-tech)  
> **Contact:** [yangyehuisw@126.com]

---

## Tracks Overview

### 1) Vision-Language Track (✅ Available)

Image-based financial document understanding: 

- **Entry:** [Vision-Language Track](vision_language)
- **Inputs:** document images + text prompts (JSONL, one sample per line)
- **Outputs:** text responses (JSONL, one sample per line)
- **Evaluation:** [Evaluation Script](vision_language/evaluation.py)

#### Paper & Project Links
- [**Paper (arXiv)**](https://arxiv.org/abs/2601.00150)
- [**Paper (PDF)**](https://github.com/QFIN-tech/FCMBench/tree/main/TechnicalReport)
- [**Project Page**](https://github.com/QFIN-tech/FCMBench/tree/main/vision_language)
- [**Leaderboard**](https://qfin-tech.github.io/FCMBench)
- [**Sample Data**](https://qfin-tech.github.io/FCMBench/Examples.html)
- [**Dataset (ModelScope)**](https://modelscope.cn/datasets/QFIN/FCMBench-Data)
- [**Dataset (Hugging Face)**](https://huggingface.co/datasets/QFIN/FCMBench-Data)

#### Reference Model Demo
We also provide access to an interactive demo of our Qfin-VL-Instruct model, which achieves strong performance on FCMBench.
If you are interested in trying the Gradio demo, please contact [yangyehuisw@126.com] with the following information:
- Name
- Affiliation / Organization
- Intended use (e.g., research exploration, benchmarking reference)
- Contact email

Access will be granted on a case-by-case basis.

### 2) Video Understanding Track (🕒 Coming Soon)

### 3) Speech Understanding & Generation Track (🕒 Coming Soon)

### 4) Multi-step / Agentic Track (🕒 Coming Soon)

## Citation
```
@misc{yang2026fcmbenchcomprehensivefinancialcredit,
      title={FCMBench: A Comprehensive Financial Credit Multimodal Benchmark for Real-world Applications}, 
      author={Yehui Yang and Dalu Yang and Wenshuo Zhou and Fangxin Shang and Yifan Liu and Jie Ren and Haojun Fei and Qing Yang and Yanwu Xu and Tao Chen},
      year={2026},
      eprint={2601.00150},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2601.00150}, 
}
```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=QFIN-tech/FCMBench&type=date&legend=top-left)](https://www.star-history.com/#QFIN-tech/FCMBench&type=date&legend=top-left)
