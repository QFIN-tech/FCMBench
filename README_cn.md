![](assets/FCMBench_logo.jpg)


**FCMBench** 是一个面向信贷风控工作流的多模态基准测试（benchmark）。它旨在提供一个标准化的"试验场"，促进学术界与产业界的协同开发，并在多个赛道（图像、视频、语音、智能体等）上提供标准化的数据集、提示词（prompts）与评测脚本。

<p align="center">
🤗 <a href="https://huggingface.co/datasets/QFIN/FCMBench-Data"><b>Hugging Face</b></a>&nbsp;&nbsp; | &nbsp;&nbsp;🤖 <a href="https://modelscope.cn/datasets/QFIN/FCMBench-Data"><b>ModelScope</b></a>&nbsp;&nbsp; | &nbsp;&nbsp;📑 <a href="https://arxiv.org/abs/2601.00150"><b>FCMBench 论文</b></a>&nbsp;&nbsp; | &nbsp;&nbsp;📑 <a href="https://arxiv.org/abs/2604.25186"><b>FCMBench-Video 论文</b></a>&nbsp;&nbsp; | &nbsp;&nbsp;🏆 <a href="https://qfin-tech.github.io/FCMBench"><b>排行榜</b></a>
</p>

[English Version](./README.md)

## 🔥 新闻
- 【**2026. 04. 29**】🎬 我们发布了 **FCMBench-Video**，一个面向文档视频智能的基准测试。基于 495 段实拍原子视频构建，组合为 1,200 段长视频，配套 11,322 条专家标注的问答实例，覆盖 28 种文档类型（中英双语）。论文见 [arXiv 2604.25186](https://arxiv.org/abs/2604.25186)。
- 【**2026. 03. 16**】✨ 我们发布了**FCMBench-V1.1**，该版本加入了英文证件图像和相关问答对，覆盖的证件类型增加至 26 个，图像增加至 5,198 张，问答样本增加至 13,806 条。
- 【**2026. 01. 01**】我们很高兴发布**FCMBench-V1.0**，该版本覆盖 18 类核心证件类型，包含 4,043 张符合隐私合规要求的图像与 8,446 条问答样本。其任务体系涵盖 3 类感知（Perception）任务与 4 类推理（Reasoning）任务，并与 10 类健壮性推理（robustness inferences）交叉引用。所有任务与推理过程均来源于真实世界的关键业务场景。

> **状态：** 公开发布（v1.1）。
> **维护者：** [奇富科技 / Qfin Holdings](https://github.com/QFIN-tech)
> **联系方式：** [yangyehui-jk@qifu.com]

---

## 赛道概览

| 赛道入口 | 输入 | 输出 | 评测脚本 | 排行榜 | 论文 | 样例数据 |
|---|---|---|---|---|---|---|
| [Vision-Language Track](vision_language) | 文档图像 + 文本指令（JSONL，每行一个样本） | 文本响应（JSONL，每行一个样本） | [evaluation.py](vision_language/evaluation.py) | [排行榜](https://qfin-tech.github.io/FCMBench) | [arXiv 2601.00150](https://arxiv.org/abs/2601.00150) | [示例页](https://qfin-tech.github.io/FCMBench/Examples.html) |
| [Video Understanding Track](video_understanding) | 文档视频 + 文本指令（JSONL） | 文本响应（JSONL） | *(待定)* | *(待定)* | [arXiv 2604.25186](https://arxiv.org/abs/2604.25186) | *(待定)* |

---

### 1) 视觉-语言赛道（✅ 已开放）

基于图像的金融文档理解。

#### 样例数据
请访问[示例页面](https://qfin-tech.github.io/FCMBench/Examples.html)预览样例图片和问答示例。

#### 参考模型 Demo
我们也提供 Qfin-VL-Instruct 模型的交互式演示（demo）访问，该模型在 FCMBench 上表现强劲。
如果你希望试用 Gradio demo，请将以下信息发送至 [yangyehui-jk@qifu.com]：
- 姓名
- 所属单位 / 组织
- 使用目的（例如：研究探索、评测基线参考）
- 联系邮箱

我们将按具体情况逐一审批并开通访问权限。

---

### 2) 视频理解赛道（🎬 已开放）

面向文档视频智能的基准测试，覆盖真实手持拍摄条件下的文档感知、时序定位与证据推理能力。基于 495 段实拍原子视频构建，组合为 1,200 段长视频（20s/40s/60s 时长区间），配套 11,322 条专家标注的问答实例，覆盖 28 种文档类型（中英双语）。详见[论文](https://arxiv.org/abs/2604.25186)了解完整基准设计和 9 款 Video-MLLM 的评测结果。

#### 样例数据
*(待定)*

#### 参考模型 Demo
*(待定)*

---

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
