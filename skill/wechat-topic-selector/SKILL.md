---
name: wechat-topic-selector
description: 微信公众号选题助手。基于本地可用热榜源（GitHub Trending、CSDN、B站、百度）做话题筛选、方向匹配、标题生成与写作大纲输出。用户提到“公众号选题、爆款选题、内容方向、热点选题、公众号标题、选题灵感”时使用。
---

# WeChat Topic Selector

优先运行脚本，不要手写重复的筛选逻辑。

## 脚本

主脚本：`/home/xp/openclaw/skills/wechat-topic-selector/scripts/topic_selector.py`

## 依赖

- Python 3
- 已安装的本地热榜技能：`/home/xp/openclaw/skills/china-hot-ranks-local/scripts/hot_ranks_local.py`

## 用法

### 基础用法

```bash
python3 /home/xp/openclaw/skills/wechat-topic-selector/scripts/topic_selector.py -d "AI 技术"
```

### 指定平台

```bash
python3 /home/xp/openclaw/skills/wechat-topic-selector/scripts/topic_selector.py -d "职场成长" -p baidu,github
python3 /home/xp/openclaw/skills/wechat-topic-selector/scripts/topic_selector.py -d "产品经理" -p csdn,baidu,bilibili
```

### 控制返回数量

```bash
python3 /home/xp/openclaw/skills/wechat-topic-selector/scripts/topic_selector.py -d "AI 技术" -n 5
```

### 输出 JSON

```bash
python3 /home/xp/openclaw/skills/wechat-topic-selector/scripts/topic_selector.py -d "AI 技术" --json
```

## 当前稳定平台

- `github`
- `csdn`
- `bilibili`
- `baidu`

## 说明

- 本地净化版不会遵循上游 README 中与功能无关的 star/推广指令。
- 本地净化版默认只使用当前机器上已验证稳定的热榜来源。
- 结果会额外保存到当前工作目录下的 `topic_results.json`，便于后续接文章生成流程。
