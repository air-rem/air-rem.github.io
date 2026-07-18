---
name: update-airport-plans
description: 更新本站(air-rem.github.io / AIRREM 领航)某个机场的价格套餐表与差异化亮点。触发词：更新XX机场/XX云的套餐、价格套餐表、亮点、卖点、主打点、适合人群；用户发来某机场官网购买页截图要求更新。每次做这类更新都必须走本 skill。
---

# 更新机场套餐与亮点（AIRREM 领航）

本站是**机场推荐/导购**静态站，单一数据源 `data/airports.json` → `build.py` 生成全部页面。
更新某机场的「价格套餐 + 亮点」时，**只改数据源再重新构建**，禁止手改生成出来的 HTML。

## 铁律：每家机场必须差异化（最高优先级）

> 用户原话：**"一定要表达出每个机场的亮点，要不然每个都一样岂不是很普通？让用户看着就想要买。主打的点是什么、适合什么样的需求，一定要写清楚，每个机场都需要这么搞。"**

因此本 skill 的产出**绝不能只是价格表**。每次更新都要提炼这家机场**区别于其他家的那一个（或几个）独家卖点**，并让它出现在 `tagline` / `verdict` 里，让用户"看着就想买"。

**找亮点的抓手**（挑最突出的 1–2 个，放到 tagline 开头）：
- 设备/客户端数是否**不限制**（如卷王机场）
- **低倍率节点**（如清风云 0.5X，流量实际翻倍用）
- **专属 Emby 影视库**（追剧党，字段 `"emby": true`）
- 可**手动切换国内入口**等独家功能（如蛋挞云）
- 专线类型：全 IEPL/IPLC 专线（稳定）vs 直连（便宜）vs 中转
- **带宽峰值**、带宽/设备随档位递增（如良心云、极速 20000Mbps）
- 协议新旧与**抗封**（Hysteria2 / AnyTLS / VLESS Reality）
- **价格定位**：超低价口粮（¥2~¥5 起）vs 稳定专线
- 计费结构：月付 / 年付 / **不限时一次性买断**
- 有趣的品牌/套餐命名，可点出个性

同类机场之间，务必突出**彼此不同**的那一点，不要每家都写"稳定、解锁全、性价比高"。

## 操作步骤

### 1. 定位机场 slug
```bash
grep -n '"name": "机场中文名"' data/airports.json   # 或按 slug 直接搜
```
常见对应：西部数据=westdata、蛋挞云=danta、游隼云=yousun、极速机场=jisu、良心云=liangxin、卷王机场=juanwang、清风云=qingfeng、飞狗=feigou … 名字对不上就先 grep 确认。

### 2. 读官网截图，提取套餐
逐档记下：套餐名、价格、计费类型（月付/季付/半年/年付/一次性买断）、每月/一次性流量、倍率、限速/带宽、设备数、有效期、年付立减等。

### 3. 编辑 data/airports.json（只改这个机场对象）
- **价格/套餐**：
  - `plans`：数组，每项 `[套餐名, 参考价, 说明]`。说明里写清"计费类型 · 流量 · 关键参数（限速/设备/倍率/年付立减）"。档位多时可合并同类（如"普通不限时 · 200G/500G/1000G（¥15/¥40/¥70）"），但**核心档位要列全**。
  - `price_from` / `price_unit`：起步参考价 + 单位，单位统一写成 **`/ 月 XXG`**（或 `/ 年 XXG`、`/ 次` 等），例如 `"¥12"` + `"/ 月 100G"`。取最有吸引力的真实入门价。
  - `billing`：如 `月付 / 年付 / 不限时买断`。
  - `plan_note`：一句话交代计费规则（月付按月重置 / 一次性永久买断）+ 特殊点（倍率、无退款、限设备数）+ "以官网实时价格为准"。
- **亮点/描述（务必打磨，见上文铁律）**：
  - `tagline`：一句话钩子，**以最强卖点开头**（别用"20XX 年成立"这种平淡开头）。
  - `verdict`：一句话点评 = 主打点 + 适合谁 + 注意事项。
  - `scene` / `best_for`：适合场景与人群。
  - `pros` / `fit`：优点、适合入手的人，第一条就放最独家的卖点。
  - 需要时更新 `sections`（正文段落/list/note）、`unlock`、`protocols`、`keywords`、`meta_desc` 使之与新卖点一致。
- 保持 JSON 合法（逗号、引号、中文用全角括号无妨）。

### 4. 校验 + 构建（Windows 必须带 UTF-8，否则 print 会 GBK 崩）
```bash
python -c "import json; json.load(open('data/airports.json',encoding='utf-8')); print('JSON OK')"
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python build.py
```
> **Bash 工具要加 `dangerouslyDisableSandbox: true`**，否则沙箱下 `.git`/文件系统是叠加视图，git 会报 "not a git repository / could not lock config"，python 也可能读到旧文件。

构建会重生成：`<slug>/index.html`（内页）、`airports/index.html`（机场大全卡片）、首页注入块、`README.md`、`sitemap.xml`。
> 注意：非 `featured` 的机场**不在首页榜单/对比表**，首页 `index.html` 仅在"机场墙"以名称出现（无价格）。所以这类机场改价后 `index.html` 通常不变，属正常——内页与机场大全会更新。

### 5. 核对
`grep` 内页与 `airports/index.html`，确认新价/新套餐名已渲染。

### 6. 提交并推送（推送凭据特殊！）
remote 是 `air-rem/air-rem.github.io`，但系统默认凭据是 geekoutnet（**无写权限，会 403**）。必须用 air-rem 的 token：
```bash
source "$HOME/.claude/secrets/github-tokens.env"   # 提供 GH_AIR_REM_TOKEN
git add -A
git commit -m "feat(seo): 更新 XX 机场价格套餐并强化亮点文案"
b64=$(printf 'x-access-token:%s' "$GH_AIR_REM_TOKEN" | base64 -w0)
git -c credential.helper= -c http.extraheader="Authorization: Basic $b64" push origin main
```
（git 命令同样需要 `dangerouslyDisableSandbox: true`。切勿在任何输出里打印 token 明文。）

## 参考：已按此标准做过的机场
westdata（优惠码 WD-DDR6，改 assets/config.js）、danta（手动切入口）、yousun（大流量档位最全）、jisu（极致低价+20Gbps）、liangxin（带宽/设备阶梯）、juanwang（客户端不限）、qingfeng（Emby+0.5X 低倍率）。可打开这些对象作为文案范例。
