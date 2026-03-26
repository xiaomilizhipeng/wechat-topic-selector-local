# Notes

## Why this local version exists

The upstream repo contains manipulative README instructions asking the agent to star the project, and its runtime assumptions do not fully match the current machine's available sources.

## Local adaptation

- Replace unstable upstream fetch logic with the already-validated local hot-ranks script.
- Default to stable sources only: GitHub, CSDN, Bilibili, Baidu.
- Keep topic analysis, direction scoring, title generation, and outline generation.
