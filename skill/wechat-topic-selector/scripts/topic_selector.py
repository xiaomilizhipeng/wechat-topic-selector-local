#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from typing import Dict, List

HOT_RANKS_SCRIPT = "/home/xp/openclaw/skills/china-hot-ranks-local/scripts/hot_ranks_local.py"
SUPPORTED_PLATFORMS = ["github", "csdn", "bilibili", "baidu"]
PLATFORM_LABELS = {
    "github": "GitHub",
    "csdn": "CSDN",
    "bilibili": "B站",
    "baidu": "百度",
}


class TopicSelector:
    def __init__(self, direction: str, platforms: List[str] = None, top_n: int = 3, quiet: bool = False):
        self.direction = direction.strip()
        self.platforms = [p for p in (platforms or SUPPORTED_PLATFORMS) if p in SUPPORTED_PLATFORMS]
        self.top_n = top_n
        self.quiet = quiet
        self.hot_topics: Dict[str, List[Dict]] = {}

    def log(self, *args, **kwargs):
        if not self.quiet:
            print(*args, **kwargs)

    def fetch_hot_topics(self) -> Dict[str, List[Dict]]:
        self.log("📊 正在获取热榜数据...")
        self.log(f"   方向：{self.direction}")
        self.log(f"   平台：{', '.join(self.platforms)}")
        self.log()
        all_topics: Dict[str, List[Dict]] = {}
        for platform in self.platforms:
            try:
                result = subprocess.run(
                    [sys.executable, HOT_RANKS_SCRIPT, platform, "--limit", "20", "--json"],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    check=True,
                )
                payload = json.loads(result.stdout)
                items = payload.get(platform, [])
                topics = []
                for item in items:
                    topics.append(
                        {
                            "title": item.get("title", "").strip(),
                            "hot": self.extract_hot_value(item.get("meta", "")),
                            "meta": item.get("meta", ""),
                            "url": item.get("url", ""),
                            "platform": PLATFORM_LABELS.get(platform, platform),
                        }
                    )
                all_topics[platform] = topics
                self.log(f"✅ {PLATFORM_LABELS.get(platform, platform)}：{len(topics)}条")
            except Exception as e:
                self.log(f"❌ {PLATFORM_LABELS.get(platform, platform)} 获取失败：{e}")
                all_topics[platform] = []
        self.hot_topics = all_topics
        return all_topics

    @staticmethod
    def extract_hot_value(meta: str) -> int:
        nums = re.findall(r"\d+", meta or "")
        if not nums:
            return 0
        try:
            return int(max(nums, key=lambda x: len(x)))
        except Exception:
            return 0

    def analyze_topic(self, topic: str) -> Dict:
        analysis = {"keywords": [], "emotion": "neutral", "type": "热点", "angle": []}
        direction_keywords = [
            "AI", "人工智能", "大模型", "Agent", "技术", "产品", "职场", "成长", "管理",
            "Python", "GitHub", "OpenClaw", "公众号", "内容", "流量"
        ]
        analysis["keywords"] = [kw for kw in direction_keywords if kw.lower() in topic.lower()] or ["热点"]

        emotion_words = {
            "positive": ["突破", "成功", "增长", "上涨", "发布", "利好", "爆", "火"],
            "negative": ["下跌", "失败", "危机", "风险", "警告", "反对", "崩"],
            "neutral": ["分析", "解读", "揭秘", "实战", "指南", "复盘"],
        }
        for emo, words in emotion_words.items():
            if any(word in topic for word in words):
                analysis["emotion"] = emo
                break

        if any(x in topic for x in ["实战", "教程", "指南", "入门"]):
            analysis["type"] = "教程"
        elif any(x in topic for x in ["解读", "分析", "揭秘", "复盘"]):
            analysis["type"] = "解读"
        elif any(x in topic for x in ["发布", "上线", "开源"]):
            analysis["type"] = "新闻"
        else:
            analysis["type"] = "热点"

        angles = []
        if any(x in topic for x in ["如何", "怎么", "指南", "方法"]):
            angles.append("方法论")
        if any(x in topic for x in ["案例", "复盘", "实战"]):
            angles.append("案例拆解")
        if any(x in topic for x in ["趋势", "未来", "变天"]):
            angles.append("趋势预测")
        analysis["angle"] = angles or ["热点追踪"]
        return analysis

    def match_direction(self, topic: str, analysis: Dict, hot: int = 0) -> int:
        score = 0
        direction_lower = self.direction.lower()
        topic_lower = topic.lower()
        direction_keywords = {
            "AI": ["ai", "人工智能", "大模型", "agent", "llm", "gpt", "claude", "openclaw"],
            "技术": ["技术", "开发", "编程", "代码", "架构", "python", "linux", "github"],
            "产品": ["产品", "需求", "功能", "用户", "pm", "交互"],
            "职场": ["职场", "工作", "面试", "晋升", "简历", "管理"],
            "成长": ["成长", "学习", "提升", "技能", "认知", "习惯"],
            "运营": ["运营", "增长", "流量", "转化", "私域", "公众号", "内容"],
        }
        for key, keywords in direction_keywords.items():
            if key.lower() in direction_lower and any(kw in topic_lower for kw in keywords):
                score += 18
        if direction_lower in topic_lower:
            score += 20
        if analysis.get("emotion") == "positive":
            score += 8
        if analysis.get("type") in ["教程", "解读"]:
            score += 10
        if hot >= 1000000:
            score += 12
        elif hot >= 100000:
            score += 8
        if "方法论" in analysis.get("angle", []):
            score += 12
        if "案例拆解" in analysis.get("angle", []):
            score += 10
        if "趋势预测" in analysis.get("angle", []):
            score += 10
        return min(score, 100)

    def generate_wechat_title(self, candidate: Dict, angle: str) -> str:
        original = candidate["original"]
        direction = self.direction
        clean_original = re.split(r"[（(]", original)[0].strip()
        if angle == "方法论":
            return f"《{direction}人必看：{clean_original[:24]}的 3 个关键方法》"
        if angle == "案例拆解":
            return f"案例复盘 | {clean_original[:22]}，给{direction}人的 5 点启示"
        if angle == "趋势预测":
            return f"{clean_original[:24]}，{direction}赛道要变天了？"
        return f"热评 | {clean_original[:26]}，{direction}人怎么看？"

    def generate_topic_reason(self, candidate: Dict, angle: str) -> str:
        reasons = []
        hot = candidate.get("hot", 0)
        platform = candidate["platform"]
        if hot > 1000000:
            reasons.append(f"🔥 高热度（{hot}）")
        elif hot > 100000:
            reasons.append(f"📈 热点话题（{hot}）")
        if platform == "CSDN":
            reasons.append("💻 技术垂直平台，开发者浓度高")
        elif platform == "GitHub":
            reasons.append("🌐 开源风向标，适合做技术洞察")
        elif platform == "B站":
            reasons.append("🎬 内容传播感强，适合做案例拆解")
        elif platform == "百度":
            reasons.append("📰 大众关注度高，适合追热点")
        if angle == "方法论":
            reasons.append("📚 容易写成可收藏干货")
        elif angle == "案例拆解":
            reasons.append("🔍 适合做结构化复盘")
        elif angle == "趋势预测":
            reasons.append("🔮 有利于建立专业判断感")
        return " | ".join(reasons) or "📊 可作为备选选题"

    def generate_outline(self, angle: str) -> List[str]:
        if angle == "方法论":
            return [
                "1. 痛点引入：读者为什么要关注这个问题",
                "2. 核心判断：先给出结论",
                "3. 方法拆解：分 3 点展开",
                "4. 实操建议：给出可执行动作",
                "5. 总结升华：强调价值与下一步",
            ]
        if angle == "案例拆解":
            return [
                "1. 背景介绍：案例发生了什么",
                "2. 关键节点：哪里值得看",
                "3. 成败因素：拆出 3-5 个要点",
                "4. 可复制经验：读者怎么借鉴",
                "5. 避坑提醒：容易误判的地方",
            ]
        if angle == "趋势预测":
            return [
                "1. 现象描述：当前发生了什么",
                "2. 驱动因素：为什么会这样",
                "3. 影响判断：会影响谁",
                "4. 应对建议：读者该怎么准备",
                "5. 机会展望：下一步能做什么",
            ]
        return [
            "1. 事件概述：5W1H 讲清楚",
            "2. 热点来源：为什么会爆",
            "3. 深度解读：背后的逻辑",
            "4. 行业影响：与你的方向关系",
            "5. 观点输出：形成自己的判断",
        ]

    def generate_topics(self) -> List[Dict]:
        self.log("\n🤖 正在分析热榜并生成选题...\n")
        candidates = []
        for _platform, topics in self.hot_topics.items():
            for topic in topics:
                if not topic.get("title"):
                    continue
                analysis = self.analyze_topic(topic["title"])
                score = self.match_direction(topic["title"], analysis, topic.get("hot", 0))
                if score >= 25:
                    candidates.append(
                        {
                            "original": topic["title"],
                            "platform": topic["platform"],
                            "hot": topic.get("hot", 0),
                            "url": topic.get("url", ""),
                            "meta": topic.get("meta", ""),
                            "analysis": analysis,
                            "match_score": score,
                        }
                    )
        candidates.sort(key=lambda x: (x["match_score"], x["hot"]), reverse=True)
        final_topics = []
        used_angles = set()
        for candidate in candidates:
            angle = candidate["analysis"]["angle"][0]
            if angle in used_angles and len(final_topics) >= 2:
                continue
            final_topics.append(
                {
                    "title": self.generate_wechat_title(candidate, angle),
                    "angle": angle,
                    "source": candidate["original"],
                    "platform": candidate["platform"],
                    "match_score": candidate["match_score"],
                    "url": candidate["url"],
                    "meta": candidate["meta"],
                    "keywords": candidate["analysis"]["keywords"],
                    "emotion": candidate["analysis"]["emotion"],
                    "type": candidate["analysis"]["type"],
                    "reason": self.generate_topic_reason(candidate, angle),
                    "outline": self.generate_outline(angle),
                }
            )
            used_angles.add(angle)
            if len(final_topics) >= self.top_n:
                break
        return final_topics

    def format_results(self, topics: List[Dict]) -> str:
        lines = []
        lines.append("=" * 70)
        lines.append(f"📝 微信公众号选题推荐 - {self.direction}")
        lines.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 70)
        lines.append("")
        for i, topic in enumerate(topics, 1):
            lines.append(f"【选题{i}】匹配度：{topic['match_score']}分 🔥")
            lines.append(f"标题：{topic['title']}")
            lines.append(f"角度：{topic['angle']}")
            lines.append(f"来源：{topic['platform']} 热榜 - {topic['source'][:40]}...")
            lines.append(f"关键词：{', '.join(topic['keywords'])}")
            lines.append(f"情绪：{topic['emotion']} | 类型：{topic['type']}")
            if topic.get('url'):
                lines.append(f"链接：{topic['url']}")
            if topic.get('meta'):
                lines.append(f"热度信息：{topic['meta']}")
            lines.append("")
            lines.append(f"推荐理由：{topic['reason']}")
            lines.append("")
            lines.append("写作大纲：")
            for line in topic['outline']:
                lines.append(f"  {line}")
            lines.append("")
            lines.append("-" * 70)
            lines.append("")
        lines.append("✅ 选题生成完成！")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='微信公众号选题助手（本地净化版）')
    parser.add_argument('-d', '--direction', type=str, required=True, help='用户方向/领域')
    parser.add_argument('-p', '--platforms', type=str, default=','.join(SUPPORTED_PLATFORMS), help='平台列表，逗号分隔')
    parser.add_argument('-n', '--top', type=int, default=3, help='返回选题数量')
    parser.add_argument('--json', action='store_true', help='输出 JSON')
    parser.add_argument('--quiet', action='store_true', help='静默模式，不输出抓取过程日志')
    parser.add_argument('--output-json', type=str, default='topic_results.json', help='JSON 输出文件路径')
    args = parser.parse_args()

    platforms = [p.strip() for p in args.platforms.split(',') if p.strip()]
    selector = TopicSelector(direction=args.direction, platforms=platforms, top_n=args.top, quiet=args.quiet)
    selector.fetch_hot_topics()
    topics = selector.generate_topics()

    with open(args.output_json, 'w', encoding='utf-8') as f:
        json.dump(topics, f, ensure_ascii=False, indent=2)

    if args.json:
        print(json.dumps(topics, ensure_ascii=False, indent=2))
    else:
        print(selector.format_results(topics))


if __name__ == '__main__':
    main()
