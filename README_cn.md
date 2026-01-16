![](assets/FCMBench_logo.jpg)


**FCMBench** 是一个面向信贷风控工作流的多模态基准测试（benchmark）。它旨在提供一个标准化的“试验场”，促进学术界与产业界的协同开发，并在多个赛道（图像、视频、语音、智能体等）上提供标准化的数据集、提示词（prompts）与评测脚本。

[English Version](./README.md)

## 🔥 新闻
- 【**2026. 01. 01**】✨ 我们很高兴发布 [**FCMBench-V1.0**](https://github.com/QFIN-tech/FCMBench/tree/main/vision_language)，该版本覆盖 18 类核心证件类型，包含 4,043 张符合隐私合规要求的图像与 8,446 条问答样本。其任务体系涵盖 3 类感知（Perception）任务与 4 类推理（Reasoning）任务，并与 10 类健壮性推理（robustness inferences）交叉引用。所有任务与推理过程均来源于真实世界的关键业务场景。

> **状态：** 公开发布（v1.0）。  
> **维护者：** [奇富科技 / Qfin Holdings](https://github.com/QFIN-tech)  
> **联系方式：** [yangyehui-jk@qifu.com]

---

## 赛道概览

### 1) 视觉-语言赛道（✅ 已开放，**FCMBench-V1.0**）

基于图像的金融文档理解：

- **入口：** [视觉-语言赛道](vision_language)
- **输入：** 文档图像 + 文本提示词（JSONL，每行一个样本）
- **输出：** 文本响应（JSONL，每行一个样本）
- **评测：** [评测脚本](vision_language/evaluation.py)

#### 论文与项目链接
- [**技术报告（arXiv）**](https://arxiv.org/abs/2601.00150)
- [**技术报告（PDF）**](https://arxiv.org/pdf/2601.00150)
- [**项目主页**](https://github.com/QFIN-tech/FCMBench/tree/main/vision_language)
- [**排行榜**](vision_language/LEADERBOARD.md)
- [**数据集（ModelScope）**](https://modelscope.cn/datasets/QFIN/FCMBench-V1.0)
- [**数据集（Hugging Face）**](https://huggingface.co/datasets/QFIN/FCMBench-V1.0)

#### 参考模型 Demo
我们也提供 Qfin-VL-Instruct 模型的交互式演示（demo）访问，该模型在 FCMBench-V1.0 上表现强劲。  
如果你希望试用 Gradio demo，请将以下信息发送至 [yangyehui-jk@qifu.com]：
- 姓名
- 所属单位 / 组织
- 使用目的（例如：研究探索、评测基线参考）
- 联系邮箱

我们将按具体情况逐一审批并开通访问权限。

### 2) 视频理解赛道（🕒 即将推出）

### 3) 语音理解与生成赛道（🕒 即将推出）

### 4) 多步推理 / 智能体赛道（🕒 即将推出）

## 引用
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
