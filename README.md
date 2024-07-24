# 🦀 CRAB: Cross-platform Agent Benchmark for Multimodal Embodied Language Model Agents

[![arXiv][arxiv-image]][arxiv-url]
[![Slack][slack-image]][slack-url]
[![Discord][discord-image]][discord-url]
[![Wechat][wechat-image]][wechat-url]
[![Twitter][twitter-image]][twitter-url]

## Overview

CRAB is a framework for building LLM agent benchmark environments in a Python-centric way.

#### Key Features

🌐 Cross-platform and Multi-environment
* Create build agent environments that support various deployment options including in-memory, Docker-hosted, virtual machines, or distributed physical machines, provided they are accessible via Python functions.
* Let the agent access all the environments in the same time through a unified interface.

⚙ ️Easy-to-use Configuration
* Add a new action by simply adding a `@action` decorator on a Python function.
* Deine the environment by integrating several actions together.

📐 Novel Benchmarking Suite
* Define tasks and the corresponding evlauators in an intuitive Python-native way.
* Introduce a novel graph evaluator method providing fine-grained metrics.

## Installation

#### Prerequisites

- Python 3.10 or newer

```bash
pip install crab-framework[visual-prompt]
```

## Experiment on CRAB-Benchmark-v0

All datasets and experiment code are in [crab-benchmark-v0](./crab-benchmark-v0/) directory. Please carefully read the [experiment instructions](./crab-benchmark-v0/README.md) before using our benchmark.

## Examples

#### Run template environment with openai agent

```bash
export OPENAI_API_KEY=<your api key>
python examples/single_env.py
python examples/multi_env.py
```

#### Run desktop environment with openai agent

```bash
export OPENAI_API_KEY=<your api key>
python examples/desktop_env.py "Open Firefox"
```

## Cite
Please cite [our paper](https://arxiv.org/abs/2407.01511) if you use anything related in your work:
```
@misc{xu2024crab,
      title={CRAB: Cross-environment Agent Benchmark for Multimodal Language Model Agents}, 
      author={Tianqi Xu and Linyao Chen and Dai-Jie Wu and Yanjun Chen and Zecheng Zhang and Xiang Yao and Zhiqiang Xie and Yongchao Chen and Shilong Liu and Bochen Qian and Philip Torr and Bernard Ghanem and Guohao Li},
      year={2024},
      eprint={2407.01511},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2407.01511}, 
}
```

[slack-url]: https://join.slack.com/t/camel-kwr1314/shared_invite/zt-1vy8u9lbo-ZQmhIAyWSEfSwLCl2r2eKA
[slack-image]: https://img.shields.io/badge/Slack-CAMEL--AI-blueviolet?logo=slack
[discord-url]: https://discord.gg/CNcNpquyDc
[discord-image]: https://img.shields.io/badge/Discord-CAMEL--AI-7289da?logo=discord&logoColor=white&color=7289da
[wechat-url]: https://ghli.org/camel/wechat.png
[wechat-image]: https://img.shields.io/badge/WeChat-CamelAIOrg-brightgreen?logo=wechat&logoColor=white
[twitter-url]: https://twitter.com/CamelAIOrg
[twitter-image]: https://img.shields.io/twitter/follow/CamelAIOrg?style=social&color=brightgreen&logo=twitter
[arxiv-image]: https://img.shields.io/badge/arXiv-2407.01511-b31b1b.svg
[arxiv-url]: https://arxiv.org/abs/2407.01511