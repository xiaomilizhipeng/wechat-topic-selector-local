# wechat-topic-selector-local

一个本地净化版的微信公众号选题助手，基于当前可用热榜源自动生成 3 个公众号选题。

## 当前稳定热榜来源

- GitHub Trending
- CSDN 全站综合热榜
- B站热门
- 百度热搜

## 仓库内容

- `skill/wechat-topic-selector/`：OpenClaw Skill

## 用法

```bash
python3 skill/wechat-topic-selector/scripts/topic_selector.py -d "AI 技术"
python3 skill/wechat-topic-selector/scripts/topic_selector.py -d "职场成长" -p baidu,github
python3 skill/wechat-topic-selector/scripts/topic_selector.py -d "公众号运营" -n 5
```

静默模式 + JSON 文件输出：

```bash
python3 skill/wechat-topic-selector/scripts/topic_selector.py \
  -d "AI 技术" \
  -p github,csdn,bilibili,baidu \
  -n 3 \
  --quiet \
  --output-json ./topic_results.json
```

## 说明

- 本仓库是本地净化版，不包含上游 README 中的 star 诱导内容。
- 本仓库默认只使用已在当前机器验证稳定的来源。
- 依赖本地热榜技能：`china-hot-ranks-local`。
