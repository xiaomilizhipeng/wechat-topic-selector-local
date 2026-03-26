# wechat-topic-selector-local

一个本地净化版的微信公众号选题助手，基于当前可用热榜源自动生成适合公众号运营的选题建议。

默认定位：
- AI 科技科普
- 教程型内容
- 热点解读
- 技术趋势分析

---

## 当前稳定热榜来源

- GitHub Trending
- CSDN 全站综合热榜
- B站热门
- 百度热搜

本仓库不依赖上游不稳定来源，也不包含 README 中与功能无关的 star 诱导内容。

---

## 仓库内容

```text
wechat-topic-selector-local/
├── README.md
├── .gitignore
└── skill/
    └── wechat-topic-selector/
        ├── SKILL.md
        ├── .gitignore
        ├── scripts/
        │   └── topic_selector.py
        └── references/
            └── notes.md
```

---

## 依赖关系

这个技能依赖本地热榜技能：

- `china-hot-ranks-local`

也就是说，它本身不直接抓所有平台，而是复用已经验证可用的热榜聚合脚本。

---

## 用法

### 基础用法

```bash
python3 skill/wechat-topic-selector/scripts/topic_selector.py -d "AI 技术"
```

### 指定方向和平台

```bash
python3 skill/wechat-topic-selector/scripts/topic_selector.py -d "职场成长" -p baidu,github
python3 skill/wechat-topic-selector/scripts/topic_selector.py -d "公众号运营" -p baidu,bilibili,csdn
```

### 控制选题数量

```bash
python3 skill/wechat-topic-selector/scripts/topic_selector.py -d "AI 科技科普及教程" -n 5
```

### 静默模式 + JSON 输出

```bash
python3 skill/wechat-topic-selector/scripts/topic_selector.py \
  -d "AI 技术" \
  -p github,csdn,bilibili,baidu \
  -n 3 \
  --quiet \
  --output-json ./topic_results.json
```

---

## 适合什么账号

这个技能特别适合：

- AI 科技科普号
- 教程型公众号
- 产品 / 技术内容号
- 热点拆解 + 观点输出型账号

---

## 输出内容包括

- 选题标题
- 匹配度评分
- 来源平台
- 热度信息
- 推荐理由
- 写作大纲

---

## License

MIT
