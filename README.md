# AIRREM 领航 · 机场推荐榜

独立的机场（科学上网）推荐与评测站 —— 数据驱动、SEO 友好、可「一键」新增机场。
线上地址：https://air-rem.github.io/

## 目录结构
- `index.html` —— 首页（榜单 / 决策 / 对比 / FAQ；标注区块由生成器注入）
- `airports/` —— 机场大全索引页（生成）
- `<slug>/index.html` —— 每个机场的独立 SEO 评测页（生成）
- `data/airports.json` —— **唯一数据源**（所有机场内容都在这里）
- `build.py` —— 生成器：详情页 / 首页注入 / 机场大全 / sitemap
- `make_images.py` —— 生成站点与各机场 OG 分享图、favicon 图标
- `assets/` —— `style.css`、`config.js`（推广位配置）、`app.js`、OG 图
- `robots.txt` `sitemap.xml` `site.webmanifest` `favicon.svg` `404.html`

## 新增一个机场（3 步）
1. 在 `data/airports.json` 的 `airports` 数组追加一个对象（字段参照现有条目）。
2. 在 `assets/config.js` 填该机场的推广链接与优惠码（用 slug 作为键）。
3. 运行：`rm -rf __pycache__ && python3 build.py && python3 make_images.py`，提交推送即可。

新机场会自动获得：独立 SEO 页、专属 OG 分享图、品牌 emblem、首页榜单/对比/大全收录、sitemap 收录。

## 设计
暗色「夜航 / 全球航线」主题：午夜靛蓝 + 极光青·紫·粉 + 跑道琥珀。
字体 Space Grotesk / 系统中文 / JetBrains Mono。

## 免责声明
本站为第三方信息与推荐平台，非任何机场官方，页面含推广链接。各机场线路 / 价格 / 优惠以官网为准。
代理 / 加密技术的使用需遵守你所在地区的法律法规，内容仅供学习与技术研究参考。
