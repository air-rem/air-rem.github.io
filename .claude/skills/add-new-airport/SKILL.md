---
name: add-new-airport
description: Use when 要给本站 air-rem.github.io / AIRREM 领航 从 0 新增收录一家机场（区别于更新已有机场）——用户给出机场名 / 官网 / 邀请链接 / 优惠码 / 套餐截图，要求把它加进首页榜单、详情页、机场大全、README。触发词：加入新机场、新增机场、收录XX机场、把XX机场加进来、上榜、加个机场、开干加机场。
---

# 加入新机场（AIRREM 领航）

本站是**机场推荐 / 导购**静态站：单一数据源 `data/airports.json` → `python build.py` 生成**全部**页面（首页榜单 / 决策卡 / 对比表 / 机场墙、各机场详情页、机场大全、`README.md`、`sitemap.xml`）。

> **新增一家机场 = 追加一个机场对象（data/airports.json）+ 在 assets/config.js 挂邀请链接与优惠码 + 重新构建 + 推送。**
> **禁止手改任何生成出来的 HTML**（下次 build 会覆盖）。首页/详情页/机场大全/README/sitemap 都是 build 自动更新的，你只动这两个源文件。

姊妹 skill：只改**已有**机场价格/亮点用 `update-airport-plans`。本 skill 专注「从 0 新增一家，并让它**变现**（挂邀请链接+优惠码）+ 让它**被 Google 搜到**（双层 SEO）」。

## 两条铁律（最高优先级，缺一不可）

### 铁律 1 · 差异化
产出**绝不能只是价格表**。必须提炼这家**区别于其他家的 1–2 个独家卖点**，写进 `tagline`（开头就放）/ `verdict` / `pros[0]` / `fit[0]`，让用户"看着就想买"。同类机场务必突出**彼此不同**那一点，别都写"稳定、解锁全、性价比高"。
> 用户原话："一定要表达出每个机场的亮点，要不然每个都一样岂不是很普通？让用户看着就想要买。主打的点是什么、适合什么样的需求，一定要写清楚。"

**找亮点抓手**（挑最突出 1–2 个放 tagline 开头，别用"20XX 年成立"这种平淡开头）：不限设备/客户端 · 低倍率节点(流量翻倍) · 专属 Emby 影视库(`"emby": true`) · 手动切国内入口等独家功能 · 专线类型(全 IEPL/IPLC vs 直连 vs 中转) · 带宽峰值/带宽阶梯 · 抗封新协议(Hysteria2/AnyTLS/VLESS Reality) · 价格定位(超低价口粮 vs 稳定专线) · 计费结构(月付/年付/不限时买断) · **独家解锁平台**(如 MyTVSuper 港剧 / Bahamut 台漫 / HBO) · 有趣的品牌/套餐命名。

### 铁律 2 · 双层 SEO（新增机场务必做）
目标：用户 Google 搜这家机场时能搜到本站 → 经我们的**邀请链接**注册（佣金变现）。每个详情页 SEO 分两层，**都要有**：
- **通用层**（全站共有）：机场推荐、机场评测、科学上网、翻墙机场、Clash 订阅、Netflix 解锁、ChatGPT + 线路类型(IEPL 专线/中转/直连) + 协议。
- **品牌特色层**（这家独有，重点）：`品牌中文名 + 英文名 + 别名/AKA + 拼音` × 长尾意图词。长尾模板：`XX机场`、`XX机场怎么样`、`XX机场靠谱吗`、`XX机场评测`、`XX机场官网`、`XX机场优惠码`、`XX机场跑路`、`XX套餐`、`XX注册`。

把两层揉进 `keywords`（逗号分隔）与 `meta_desc`（自然句：品牌名 + 独家卖点 + 套餐锚点 + 解锁）。`title` 由 build.py 自动带品牌名，无需手写。**每家的 keywords/meta_desc 必须不同**——复制别家只改名字＝违背铁律 2。

## 操作步骤

### 0. 全网搜该机场最新资讯（新增必做，别凭空写）
新机场你未必了解，先研究再动笔。搜：成立年份、线路类型(IEPL 专线/中转/直连)、协议、节点/落地覆盖、解锁能力、**口碑与跑路风险**、是否有同名山寨站/多域名、独家卖点。
- 量大用 **Workflow**（多角度并行搜 → 对抗式核实 → 汇总结构化事实）；轻量直接 WebSearch/WebFetch 官网。
- **套餐以用户提供的截图/文字为准**；研究用于补背景与卖点，**不覆盖**用户给的价格（推广博客价目常与官网面板不一致）。
- 查不到就如实用"公开评测少 / 社区口碑空白，建议先小额验证"的口径（参考 nicecloud、qingfeng 写法），**不要编造**年份/口碑。

### 1. 定 slug 与基础标识
- `slug`：全小写英文/拼音，全站唯一。**config.js 的键、`code_key`、详情页目录名都用它，三处必须一致。**
- `en`(英文名) · `aka`(别名/俗称/全称，无则 `""`) · `initial`(图标单字母) · `accent`([渐变色1, 渐变色2] hex，挑一组不跟数组里相邻机场撞色的)。

### 2. 决定是否上榜 + 排序位置
- `featured: true` → 进首页榜单/对比表/决策卡(决策卡只取前 4)；`false` → 只进机场大全 + 机场墙。用户说"上榜/放榜单/放在 X 附近"就设 `true`；**用户没明确表态时默认 `false`，并主动问一句要不要上榜、放哪家附近**——上榜位置是编辑决策，别自作主张塞进榜首。
- **首页榜单名次 = `airports` 数组里 featured 机场的出现顺序**（第 1 个 featured = 榜 01）。要"放在 A 机场附近/后面"，就把新对象**插入到数组里 A 对象之后**（用 A 对象结尾的唯一文本做 Edit 锚点）。
- `rank_label`：榜位短标签（如"影视之选"），挑一个**没跟别家重复**的短词。

### 3. 追加机场对象到 data/airports.json
在选定位置插入对象，字段照《机场对象字段》逐一填。价格一律**人民币 ¥**（官网美元计价则按约合汇率换算，并在 `plan_note` 注明"官网以美元计价，此处按约合人民币展示"）。保持 JSON 合法。

### 4. 挂邀请链接 + 优惠码到 assets/config.js（新增关键！漏了＝白干不变现）
`aff[slug]` = 邀请/推广链接；`code[slug]` = 优惠码（无优惠码留 `""`，页面自动隐藏优惠码框）。**键必须 = slug。**
```js
aff:  { ..., "stardust": "https://s.rtxk.us/s/xxxxxxx" },
code: { ..., "stardust": "star50" }
```

### 5. 校验 + 构建（Windows 必须带 UTF-8，否则 print 会 GBK 崩）
```bash
python -c "import json; json.load(open('data/airports.json',encoding='utf-8')); print('JSON OK')"
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python build.py
```
> **Bash 工具加 `dangerouslyDisableSandbox: true`**，否则沙箱叠加视图会让 git/python 读到旧文件或报 "not a git repository / could not lock config"。
> **⚠️ CI 不构建**：`.github/workflows/deploy-cloudflare.yml` 只做 `git archive HEAD` 打包**已提交文件** → 发布 Cloudflare Pages，**不跑 build.py / make_images.py**。所以 build 产出的全部文件（`<slug>/index.html`、`airports/index.html`、`index.html`、`sitemap.xml`、`README.md`）与下方 OG 图**必须一并 commit**，否则线上不更新。

### 5b. 生成 OG 分享图（新 slug 必做，否则分享预览 404）
每家详情页 `og:image` 指向 `assets/og/<slug>.png`；新机场没有这张图。build.py **不校验**图片是否存在（缺了不报错），但分享到微信/Telegram 预览会裂。
`make_images.py` 字体路径写死为 Linux（`/usr/share/fonts/opentype/noto/...`），**Windows 本机直接跑会崩**（`OSError: cannot open resource`）。三种应对，按优先级：
1. **Windows 最佳解 —— 用系统字体只画这一家（本次 tapcloud 实测可行，产出专属中文图）**：写个一次性脚本，import `make_images` 后把它的 `font()` monkeypatch 成微软雅黑，只画目标机场，**不改源文件**；跑完删脚本：
   ```python
   import make_images as M
   from PIL import ImageFont
   M.font = lambda size, bold=False: ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc", size)
   M.airport_og(next(a for a in M.AIR if a["slug"] == "<slug>"))   # airport_og 内按模块全局解析 font，patch 生效
   ```
2. 在 Linux / WSL / CI 直接 `python make_images.py`（会重画全部图）。
3. 兜底：复制一张配色相近的现有 `assets/og/*.png` 占位（预览会显示别家名字，尽量少用）。

提交前**务必确认 `assets/og/<slug>.png` 已存在**再 `git add`。

### 6. 核对
`grep` 确认新 slug/机场名已出现在：`<slug>/index.html`（详情页）、`airports/index.html`（机场大全）、`index.html`（若 featured：榜单/对比/机场墙）、`README.md`、`sitemap.xml`。并确认详情页"前往官网"按钮 `data-aff` 已由 config.js 填成邀请链接。
提交前先 `git status` 看**实际** diff：新增一家 featured 机场会连带改动**所有** `<slug>/index.html`（各详情页页脚互链新增这家），这是正常的、全都要提交；以 git 实际改动为准，别只照本清单勾。

### 7. 提交并推送（凭据特殊！默认凭据会 403）
remote 是 `air-rem/air-rem.github.io`，系统默认凭据是 geekoutnet（**无写权限，会 403**）。注意：本站**没有**独立的 `github-air-rem-auth` skill，凭据只走下面 env 文件里的 `GH_AIR_REM_TOKEN`（别去找不存在的 auth skill）：
```bash
source "$HOME/.claude/secrets/github-tokens.env"   # 提供 GH_AIR_REM_TOKEN
git add -A
git commit -m "feat(airport): 新增 XX 机场（榜单+详情页+双层SEO+邀请链接）"
b64=$(printf 'x-access-token:%s' "$GH_AIR_REM_TOKEN" | base64 -w0)
git -c credential.helper= -c http.extraheader="Authorization: Basic $b64" push origin main
```
git 命令同样加 `dangerouslyDisableSandbox: true`。**切勿在任何输出里打印 token 明文。**

## 机场对象字段（照现有对象结构逐一填）

| 字段 | 说明 |
| --- | --- |
| `slug` | 唯一英文/拼音；= config.js 键 = `code_key` = 详情页目录名 |
| `name` / `en` / `aka` | 中文名 / 英文名 / 别名(无则 `""`) |
| `featured` | `true`=上榜；`false`=仅机场大全 |
| `rank_label` | 榜位短标签(featured 时；不与别家重复) |
| `initial` / `accent` | 图标字母 / `[渐变色1,渐变色2]`(挑一组不跟数组相邻机场撞的，可 grep 邻居 `accent` 参考) |
| `year` | 上线年份(查不到留 `""`) |
| `type` / `type_short` | 线路全称(如"公网中转（含 IEPL 专线档）") / 短标签(中转/专线/直连)；混合线路时 `type_short` 取主力/入门档那种(如 tapcloud 主力中转→"中转") |
| `protocols[]` | 协议数组(含 Hysteria2 会自动出对应客户端提示) |
| `unlock[]` | 解锁平台数组(含独家平台如 MyTVSuper/Bahamut 更出彩；首页榜单只显示前 2 个) |
| `regions` | 覆盖地区一句话 |
| `billing` | 计费方式(月付 / 年付 / 不限时买断…) |
| `price_from` / `price_unit` | 入门参考价 `¥12` / 单位 `/ 月 100G`(取最有吸引力的真实价) |
| `code_key` | = `slug` |
| `scene` / `best_for` | 适合场景 / 适合人群短词 |
| `tagline` | 一句话钩子，**独家卖点开头** |
| `verdict` | 一句话点评 = 主打点 + 适合谁 + 注意事项 |
| `meta_desc` | SEO 描述(双层：品牌名+卖点+套餐锚点+解锁) |
| `keywords` | SEO 关键词(双层：品牌长尾 + 通用词) |
| `sections[]` | 正文段落 `{h, p[], list?, note?}`，2–4 段(是什么/线路/协议/解锁) |
| `plans[]` | `[套餐名, 参考价, 说明]`，核心档位列全，说明里写清 计费类型·流量·关键参数 |
| `plan_note` | 计费规则 + 特殊点(倍率/无退款/限设备/优惠码) + "以官网实时价格为准" |
| `pros[]` / `cons[]` | 优点/注意；`pros[0]` 放最独家卖点；`cons` 必含"跑路风险，先小额验证" |
| `fit[]` / `unfit[]` | 适合谁 / 谁要三思 |
| `faq[]` | `{q,a}`，2–3 条，含该机场**独有**疑问(如独家功能怎么用、是不是专线、怎么防山寨) |
| `emby` | 可选，`true`=有 Emby 影视库(进首页 Emby 专区 + 加徽章) |

## 常见错误（Red Flags — 命中即停，回去改）
- ❌ 只加了 airports.json，**忘改 config.js** → 邀请链接/优惠码不生效，白干、不变现。**新增机场第一优先就是挂链接。**
- ❌ 被要求"上榜"却忘设 `featured: true`，或插错数组位置导致名次不对。
- ❌ SEO 复制别家只改名字 → 违背铁律 2，Google 搜品牌名搜不到。`keywords` **必须**含品牌长尾(XX机场怎么样/官网/优惠码…)。
- ❌ `slug` 与 config.js 键 / `code_key` 不一致 → 链接/优惠码错位。
- ❌ 手改生成的 HTML → 下次 build 覆盖。**只改 data/airports.json 与 assets/config.js。**
- ❌ 价格照搬美元没换 ¥；或 JSON 漏逗号/引号导致 build 崩。
- ❌ 编造年份/口碑 → 查不到就写"公开评测少 / 口碑空白，建议先小额验证"。
- ❌ 用默认凭据 push（403）；忘加 `dangerouslyDisableSandbox: true`；输出里打印了 token。

## 参考范例
文案范例可打开这些对象：`candycloud`/`hongxing`（影视差异化）、`shenlong`（IEPL 永久专线）、`qingfeng`（Emby+0.5X 低倍率）、`tapcloud`（中转+全平台解锁、双层 SEO、五折码、放神龙后作首个用本 skill 新增的范例）。
