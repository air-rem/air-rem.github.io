#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AIRREM 领航 —— 静态站生成器
------------------------------------------------------------
单一数据源 data/airports.json  ->  生成全部页面：
  · 每个机场的独立 SEO 详情页  /<slug>/index.html
  · 机场大全索引页            /airports/index.html
  · 首页注入：榜单卡 / 决策卡 / 对比表 / 页脚链接
  · sitemap.xml

用法：  python3 build.py
新增机场：编辑 data/airports.json 追加一个对象 -> 运行本脚本 -> 发布
"""
import os, re, json, html

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(BASE, "data", "airports.json"), encoding="utf-8"))
SITE = DATA["site"]
AIRPORTS = DATA["airports"]
B = SITE["base"].rstrip("/")
UPDATED = SITE.get("updated", "2026-07")
esc = html.escape

# ----------------------------------------------------------------------------- helpers
def chips(items, cls=""):
    return "".join('<span class="chip %s">%s</span>' % (cls, esc(x)) for x in items)

def emblem(a, size=64):
    s, slug = size, a["slug"]
    c1, c2 = a["accent"]
    return (
      '<svg class="emb" width="%d" height="%d" viewBox="0 0 64 64" role="img" aria-label="%s 图标">'
      '<defs><linearGradient id="em-%s" x1="0" y1="0" x2="64" y2="64">'
      '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>'
      '<rect width="64" height="64" rx="16" fill="url(#em-%s)"/>'
      '<text x="32" y="43" text-anchor="middle" font-family="Space Grotesk,sans-serif" '
      'font-size="30" font-weight="700" fill="#08122b">%s</text></svg>'
    ) % (s, s, esc(a["name"]), slug, c1, c2, slug, esc(a["initial"]))

def client_hint(a):
    p = " ".join(a["protocols"]).lower()
    if "hysteria2" in p:
        return ('<div class="callout"><b>客户端提示：</b>本机场含 Hysteria2 节点，请使用 '
                'v2rayN / Hiddify / Karing 等支持该协议的客户端；Xray-core、老版本 Clash '
                '无法连接，导入会报错。</div>')
    if "trojan" in p:
        return ('<div class="callout"><b>客户端提示：</b>Trojan 协议兼容性好，'
                'Clash Verge / v2rayN / Shadowrocket 等主流客户端均可直接导入使用。</div>')
    return ('<div class="callout"><b>客户端提示：</b>主流协议，'
            'Clash 系 / Shadowrocket 等常见客户端都可导入，粘贴订阅即可。</div>')

# ----------------------------------------------------------------------------- shared chrome
def nav_html():
    return (
'<header class="nav"><nav class="wrap nav-in" aria-label="主导航">'
'<a class="brand" href="/" aria-label="AIRREM 领航 首页">'
'<svg class="mark" viewBox="0 0 40 40" fill="none" aria-hidden="true">'
'<defs><linearGradient id="bg1" x1="0" y1="0" x2="40" y2="40">'
'<stop offset="0" stop-color="#35E0D4"/><stop offset=".5" stop-color="#7E7BFF"/><stop offset="1" stop-color="#FF6AD5"/>'
'</linearGradient></defs><circle cx="20" cy="20" r="18" stroke="url(#bg1)" stroke-width="1.6" opacity=".5"/>'
'<path d="M20 5 L26 32 L20 27 L14 32 Z" fill="url(#bg1)"/><circle cx="20" cy="20" r="2.4" fill="#fff"/></svg>'
'<span>AIRREM<small>领航 · 机场推荐榜</small></span></a>'
'<button class="nav-toggle" aria-label="展开菜单" aria-expanded="false">☰</button>'
'<div class="nav-links">'
'<a href="/#board">机场榜单</a><a href="/airports/">机场大全</a>'
'<a href="/#guide">怎么选</a><a href="/#compare">参数对比</a><a href="/#faq">常见问题</a>'
'<a class="btn btn-primary nav-cta" href="/airports/">全部机场</a></div></nav></header>')

def footer_html():
    links = "\n".join('<a href="/%s/">%s %s</a>' % (a["slug"], esc(a["name"]), esc(a["en"]))
                      for a in AIRPORTS if a.get("featured"))
    return (
'<footer class="foot"><div class="wrap"><div class="foot-grid">'
'<div><a class="brand" href="/" style="margin-bottom:14px">'
'<svg class="mark" viewBox="0 0 40 40" fill="none" aria-hidden="true">'
'<circle cx="20" cy="20" r="18" stroke="url(#bg1)" stroke-width="1.6" opacity=".5"/>'
'<path d="M20 5 L26 32 L20 27 L14 32 Z" fill="url(#bg1)"/></svg>'
'<span>AIRREM<small>领航 · 机场推荐榜</small></span></a>'
'<p style="color:var(--ink-2);font-size:14px;max-width:34ch">' + esc(SITE["tagline"]) + '</p></div>'
'<div><h5>机场评测</h5>' + links + '</div>'
'<div><h5>指南</h5><a href="/#guide">怎么选机场</a><a href="/#compare">参数对比</a>'
'<a href="/airports/">机场大全</a><a href="/#faq">常见问题</a></div></div>'
'<div class="disc"><p><b>免责声明：</b>本站为第三方信息与推荐平台，非任何机场官方；页面内含推广链接，'
'若你通过链接注册或购买，我们可能获得一定佣金，但<b>不会增加你的任何成本</b>。'
'各机场的线路、价格、优惠码可能随时变动，请以对应官网实时信息为准。'
'代理/加密技术的使用需遵守你所在国家或地区的法律法规，本站内容仅供学习与技术研究参考。</p>'
'<p style="margin-top:10px">© <span data-year>2026</span> AIRREM 领航 · air-rem.github.io</p></div></div></footer>')

SKIP_STYLE = ('<style>.skip{position:absolute;left:-999px;top:0;z-index:100;background:var(--amber);'
              'color:#241300;padding:10px 16px;border-radius:0 0 10px 0;font-weight:600}.skip:focus{left:0}</style>')

def head(title, desc, canonical, keywords, og_image, jsonld, og_type="article"):
    j = json.dumps(jsonld, ensure_ascii=False, separators=(",", ":"))
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta name="keywords" content="%s">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#060917">
<link rel="canonical" href="%s">
<link rel="alternate" hreflang="zh-CN" href="%s">
<link rel="alternate" hreflang="x-default" href="%s">
<meta property="og:type" content="%s">
<meta property="og:site_name" content="AIRREM 领航 · 机场推荐榜">
<meta property="og:locale" content="zh_CN">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<meta name="twitter:image" content="%s">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
%s
<script type="application/ld+json">%s</script>
</head>
<body>
<a class="skip" href="#main">跳到主内容</a>
<div class="bg-grid" aria-hidden="true"></div>
""" % (esc(title), esc(desc), esc(keywords), canonical, canonical, canonical, og_type,
       esc(title), esc(desc), canonical, og_image, esc(title), esc(desc), og_image,
       SKIP_STYLE, j)

SCRIPTS = '<script src="/assets/config.js"></script>\n<script src="/assets/app.js" defer></script>\n</body>\n</html>\n'

# ----------------------------------------------------------------------------- detail page
def render_detail(a):
    slug, name, en = a["slug"], a["name"], a["en"]
    url = "%s/%s/" % (B, slug)
    og = "%s/assets/og/%s.png" % (B, slug)
    full = name if (not en or en == name) else name + " " + en
    en_disp = "" if (not en or en == name) else en
    title = "%s 机场评测 2026｜线路 · 套餐 · 优惠 · 教程 · AIRREM 领航" % full

    # spec strip
    spec = [
        ("上线年份", a["year"]),
        ("线路类型", a["type"]),
        ("主要协议", " · ".join(a["protocols"])),
        ("覆盖地区", a["regions"]),
        ("计费方式", a["billing"]),
        ("流媒体解锁", " · ".join(a["unlock"])),
    ]
    spec_html = "".join('<div><dt>%s</dt><dd>%s</dd></div>' % (esc(k), esc(v)) for k, v in spec)

    # TOC + sections
    toc, body = [], []
    for i, sec in enumerate(a["sections"]):
        sid = "s%d" % i
        toc.append('<a href="#%s">%s</a>' % (sid, esc(sec["h"])))
        body.append('<h2 id="%s">%s</h2>' % (sid, esc(sec["h"])))
        for para in sec.get("p", []):
            body.append('<p>%s</p>' % esc(para))
        if sec.get("list"):
            body.append('<ul class="dots">' + "".join('<li>%s</li>' % esc(x) for x in sec["list"]) + '</ul>')
        if sec.get("note"):
            body.append('<div class="callout">%s</div>' % esc(sec["note"]))

    # plans
    rows = "".join('<tr><td>%s</td><td class="p">%s</td><td class="muted">%s</td></tr>'
                   % (esc(r[0]), esc(r[1]), esc(r[2])) for r in a["plans"])
    toc.append('<a href="#plans">套餐与价格</a>')
    plans_html = (
        '<h2 id="plans">套餐与价格</h2>'
        '<table class="plan-table"><thead><tr><th>套餐</th><th>参考价</th><th>说明</th></tr></thead>'
        '<tbody>%s</tbody></table><p class="muted" style="font-size:13px">%s</p>' % (rows, esc(a["plan_note"])))

    # pros / cons
    toc.append('<a href="#pc">优点与缺点</a>')
    pc_html = (
        '<h2 id="pc">优点与缺点</h2><div class="pc">'
        '<div class="col pros"><h4>优点</h4><ul>%s</ul></div>'
        '<div class="col cons"><h4>要注意</h4><ul>%s</ul></div></div>'
    ) % ("".join('<li>%s</li>' % esc(x) for x in a["pros"]),
         "".join('<li>%s</li>' % esc(x) for x in a["cons"]))

    # fit / unfit
    toc.append('<a href="#fit">适合谁</a>')
    fit_html = (
        '<h2 id="fit">适合谁 / 谁要三思</h2><div class="grid-2">'
        '<div class="card"><h3>适合入手</h3><ul class="dots">%s</ul></div>'
        '<div class="card"><h3>建议三思</h3><ul class="dots">%s</ul></div></div>'
    ) % ("".join('<li>%s</li>' % esc(x) for x in a["fit"]),
         "".join('<li>%s</li>' % esc(x) for x in a["unfit"]))

    # tutorial
    toc.append('<a href="#howto">新手上手</a>')
    howto_html = (
        '<h2 id="howto">新手上手：4 步开用</h2>' + client_hint(a) +
        '<ol class="steps">'
        '<li><b>注册并购买套餐。</b>打开 %s 官网注册账号，按需求选一档套餐下单。</li>'
        '<li><b>复制订阅链接。</b>在用户中心找到“一键订阅 / 复制订阅地址”，复制你的专属链接。</li>'
        '<li><b>安装客户端。</b>Windows 用 Clash Verge / v2rayN，安卓用 Hiddify / Karing，iOS 用 Shadowrocket。</li>'
        '<li><b>导入并选节点。</b>把订阅粘贴进客户端、更新节点，挑一个延迟低的节点开启即可。</li>'
        '</ol>' % esc(name))

    # faq
    faq_items = a.get("faq", [])
    toc.append('<a href="#faq">常见问题</a>')
    faq_html = '<h2 id="faq">常见问题</h2><div class="faq">' + "".join(
        '<details%s><summary>%s</summary><div class="a">%s</div></details>'
        % (" open" if i == 0 else "", esc(q["q"]), esc(q["a"])) for i, q in enumerate(faq_items)
    ) + '</div>'

    prose = "\n".join(body) + plans_html + pc_html + fit_html + howto_html + faq_html
    toc_html = '<aside class="toc"><div class="lb">本页目录</div>' + "".join(toc) + '</aside>'

    # jsonld
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": B + "/"},
            {"@type": "ListItem", "position": 2, "name": "机场大全", "item": B + "/airports/"},
            {"@type": "ListItem", "position": 3, "name": full, "item": url}]},
        {"@type": "Article", "headline": title, "description": a["meta_desc"], "inLanguage": "zh-CN",
         "author": {"@type": "Organization", "name": "AIRREM 领航"},
         "publisher": {"@type": "Organization", "name": "AIRREM 领航", "logo": {"@type": "ImageObject", "url": B + "/assets/og.png"}},
         "mainEntityOfPage": url, "image": og, "datePublished": "2026-06-01", "dateModified": UPDATED + "-01"},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
            for q in faq_items]},
    ]}

    label = ('<span class="chip hot">%s</span>' % esc(a["rank_label"])) if a.get("rank_label") else ""
    out = head(title, a["meta_desc"], url, a["keywords"], og, jsonld)
    out += nav_html()
    out += '<main id="main"><section class="section wrap" style="padding-bottom:0">'
    out += ('<nav class="crumbs" aria-label="面包屑"><a href="/">首页</a><span>/</span>'
            '<a href="/airports/">机场大全</a><span>/</span><span>%s</span></nav>' % esc(name))
    # hero-detail
    out += '<div class="hero-detail">'
    out += '<div>'
    en_span = ('<span style="color:var(--ink-3);font-family:var(--font-mono);font-size:.5em;font-weight:400">%s</span>' % esc(en_disp)) if en_disp else ""
    out += '<div style="display:flex;align-items:center;gap:16px;margin-bottom:18px">%s<div><h1 style="font-size:clamp(30px,5vw,46px)">%s %s</h1><div class="tagrow" style="margin-top:8px">%s%s</div></div></div>' % (
        emblem(a, 64), esc(name), en_span,
        '<span class="chip cy">%s · %s</span>' % (esc(a["type_short"]), esc(a["year"])), label)
    out += '<p class="lead" style="color:var(--ink-2);font-size:17px;margin:8px 0 18px">%s</p>' % esc(a["tagline"])
    out += '<div class="verdict"><b>一句话点评：</b>%s</div>' % esc(a["verdict"])
    out += '<div class="tagrow" style="margin-top:18px">%s%s</div>' % (
        chips(a["protocols"]), chips(a["unlock"], "on"))
    out += '</div>'
    # buybox
    out += ('<aside class="buybox"><div class="price-lead">起步参考价</div>'
            '<div class="price-big">%s<span>%s</span></div>'
            '<div class="tagrow" style="margin:12px 0 16px">%s</div>'
            '<a class="btn btn-primary btn-block btn-lg" data-aff="%s" href="#plans" rel="nofollow sponsored noopener">前往%s官网 ↗</a>'
            '<a class="btn btn-ghost btn-block" href="#plans" style="margin-top:10px">查看套餐</a>'
            '<div data-codebox><div class="price-lead" style="margin-top:18px">专属优惠码</div>'
            '<div class="codebox"><code data-code="%s">—</code><button class="copybtn" type="button">复制</button></div></div>'
            '<p class="muted" style="font-size:12px;margin-top:14px">通过本站链接注册不额外收费；价格 / 优惠以官网为准。</p></aside>'
            ) % (esc(a["price_from"]), esc(a["price_unit"]), chips(a["unlock"], "on"),
                 slug, esc(name), slug)
    out += '</div>'  # hero-detail
    # spec strip
    out += '<dl class="spec" style="margin-top:36px">%s</dl>' % spec_html
    out += '</section>'
    # doc
    out += '<section class="section wrap"><div class="doc">%s<div class="prose">%s</div></div></section>' % (toc_html, prose)
    # cta band
    out += ('<section class="section-sm wrap"><div class="band"><span class="eyebrow center">准备起飞</span>'
            '<h2>觉得 %s 合适？<span class="grad-text">月付先试一档</span></h2>'
            '<p>新机场先小额验证再续费，试错成本很低。价格与优惠以官网实时为准。</p>'
            '<a class="btn btn-primary btn-lg" data-aff="%s" href="#plans" rel="nofollow sponsored noopener">前往 %s 官网 ↗</a>'
            '<div style="margin-top:16px"><a class="chip" href="/airports/">← 返回机场大全</a></div></div></section>'
            ) % (esc(name), slug, esc(name))
    out += '</main>'
    out += footer_html()
    out += SCRIPTS
    return out

# ----------------------------------------------------------------------------- airports hub
def render_hub():
    url = B + "/airports/"
    title = "机场大全｜全部科学上网机场推荐与评测榜单 · AIRREM 领航"
    desc = "AIRREM 领航机场大全：汇总我们实测收录的全部机场（%s 等），按线路类型、协议、解锁能力与价格对比，点进各家看完整评测。持续更新。" % "、".join(a["name"] for a in AIRPORTS if a.get("featured"))
    cards = []
    for a in AIRPORTS:
        cards.append(
            '<article class="card air-card">'
            '<div style="display:flex;gap:14px;align-items:center;margin-bottom:14px">%s'
            '<div><h3 style="font-size:19px">%s <small>%s</small></h3>'
            '<div class="tagrow" style="margin-top:6px"><span class="chip cy">%s</span></div></div></div>'
            '<p style="color:var(--ink-2);font-size:14.5px;min-height:63px">%s</p>'
            '<div class="tagrow" style="margin:12px 0">%s</div>'
            '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:16px">'
            '<span style="font-family:var(--font-mono);font-size:14px"><b>%s</b><span class="muted">%s</span></span>'
            '<a class="btn btn-aurora" href="/%s/">查看评测 →</a></div></article>'
            % (emblem(a, 52), esc(a["name"]), esc(a["en"]), esc(a["type"]),
               esc(a["tagline"]), chips(a["unlock"], "on"),
               esc(a["price_from"]), esc(a["price_unit"]), a["slug"]))
    jsonld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": B + "/"},
            {"@type": "ListItem", "position": 2, "name": "机场大全", "item": url}]},
        {"@type": "CollectionPage", "name": "机场大全", "url": url, "description": desc,
         "inLanguage": "zh-CN"},
        {"@type": "ItemList", "numberOfItems": len(AIRPORTS), "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": "%s %s" % (a["name"], a["en"]),
             "url": "%s/%s/" % (B, a["slug"])} for i, a in enumerate(AIRPORTS)]},
    ]}
    out = head(title, desc, url, "机场大全,机场推荐,机场评测,科学上网,翻墙机场,机场榜单", B + "/assets/og.png", jsonld, "website")
    out += nav_html()
    out += '<main id="main"><section class="section wrap">'
    out += ('<nav class="crumbs" aria-label="面包屑"><a href="/">首页</a><span>/</span><span>机场大全</span></nav>')
    out += ('<div class="sec-head"><span class="eyebrow">机场大全 · 持续更新</span>'
            '<h2>全部收录机场<span class="grad-text">总览</span></h2>'
            '<p>我们实测收录的机场都在这里，按需求点进去看完整评测。共 %d 家，持续增加中。</p></div>' % len(AIRPORTS))
    out += '<div class="grid-3">%s</div>' % "\n".join(cards)
    out += ('<div style="text-align:center;margin-top:44px"><a class="btn btn-ghost" href="/#guide">还不知道怎么选？看选购指南 →</a></div>')
    out += '</section></main>'
    out += footer_html()
    out += SCRIPTS
    return out

# ----------------------------------------------------------------------------- homepage fragments
def render_board():
    out = []
    for i, a in enumerate(AIRPORTS):
        if not a.get("featured"):
            continue
        gate = "%02d" % (i + 1)
        best = '<span class="best">%s</span>' % esc(a["rank_label"]) if a.get("rank_label") and i == 0 else ""
        label = '<span class="chip cy">%s</span>' % esc(a["rank_label"]) if a.get("rank_label") else ""
        tags = chips([a["type_short"] + " 线路"] + a["protocols"]) + chips(a["unlock"][:2], "on")
        out.append(
            '<article class="rank">%s<div class="gate"><span class="no">%s</span><span class="lb">GATE</span></div>'
            '<div class="rank-main"><h3>%s %s %s</h3><p class="tagline">%s</p><div class="tagrow">%s</div></div>'
            '<div class="rank-side"><div class="price"><b>%s</b>起 %s</div>'
            '<a class="btn btn-aurora btn-block" href="/%s/">查看评测</a>'
            '<a class="btn btn-ghost btn-block" data-aff="%s" href="/%s/#plans">前往官网 ↗</a></div></article>'
            % (best, gate, esc(a["name"]), esc(a["en"]) if a["en"] != a["name"] else "", label,
               esc(a["tagline"]), tags, esc(a["price_from"]), esc(a["price_unit"]),
               a["slug"], a["slug"], a["slug"]))
    return "\n".join(out)

def render_pick():
    out = []
    for a in AIRPORTS:
        if not a.get("featured"):
            continue
        out.append(
            '<a class="pick-card" href="/%s/"><div class="q">// %s</div><h3>%s</h3>'
            '<p>%s</p><span class="rec">推荐 %s'
            '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4">'
            '<path d="M5 12h14M13 6l6 6-6 6" stroke-linecap="round"/></svg></span></a>'
            % (a["slug"], esc(a["best_for"]), esc(a["scene"]), esc(a["tagline"][:40] + "…"), esc(a["name"])))
    return "\n".join(out)

def render_compare():
    out = []
    for a in [x for x in AIRPORTS if x.get("featured")]:
        out.append(
            '<tr><td class="name">%s</td><td>%s</td><td class="mono">%s</td><td>%s</td>'
            '<td class="mono">%s %s</td><td>%s</td><td><a class="chip cy" href="/%s/">评测 →</a></td></tr>'
            % (esc(a["name"]), esc(a["type"]), esc(" · ".join(a["protocols"])),
               esc(" · ".join(a["unlock"])), esc(a["price_from"]), esc(a["price_unit"]),
               esc(a["best_for"]), a["slug"]))
    return "\n".join(out)

def render_footer_airports():
    return "\n".join('<a href="/%s/">%s %s</a>' % (a["slug"], esc(a["name"]), esc(a["en"]))
                     for a in AIRPORTS if a.get("featured"))

def inject(text, name, inner):
    pat = re.compile(r"(<!--GEN:%s:START-->).*?(<!--GEN:%s:END-->)" % (name, name), re.S)
    return pat.sub(lambda m: m.group(1) + "\n" + inner + "\n" + m.group(2), text)

# ----------------------------------------------------------------------------- sitemap
def render_sitemap():
    today = "2026-07-04"
    urls = [(B + "/", "1.0", "weekly"), (B + "/airports/", "0.8", "weekly")]
    urls += [("%s/%s/" % (B, a["slug"]), "0.7", "monthly") for a in AIRPORTS]
    items = "".join(
        '<url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>'
        % (u, today, cf, pr) for (u, pr, cf) in urls)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % items

def render_wall():
    chips = "".join('<a class="wall-chip" href="/%s/">%s<span>%s</span></a>' % (a["slug"], emblem(a, 26), esc(a["name"])) for a in AIRPORTS)
    n = len(AIRPORTS)
    return ('<section class="section-sm"><div class="wrap center">'
            '<span class="eyebrow center">机场墙 · 持续增加</span>'
            '<h2 style="font-size:clamp(22px,3.2vw,34px)">已收录 <span class="grad-text">%d</span> 家机场，一站挑齐</h2>'
            '<p class="muted" style="max-width:52ch;margin:12px auto 0">从老牌 IEPL 专线到平价大流量，点任意一家看完整评测与最新价格。</p>'
            '</div><div class="wall"><div class="wall-track">%s%s</div>'
            '<div class="wall-track rev">%s%s</div></div></section>') % (n, chips, chips, chips, chips)

def render_readme():
    A = B
    L = []
    L.append('<p align="center"><img src="assets/og.png" alt="AIRREM 领航 · 机场推荐榜" width="820"></p>')
    L.append("")
    L.append('<h1 align="center">AIRREM 领航 · 机场推荐榜</h1>')
    L.append('<p align="center">独立的机场（科学上网）推荐与评测 · 按需求快速选对高速稳定机场<br>')
    L.append('线上站点：<a href="%s/">air-rem.github.io</a></p>' % A)
    L.append("")
    L.append("---")
    L.append("")
    L.append("## 2026 精选机场榜单")
    L.append("")
    L.append("按「综合稳定性 + 性价比 + 场景适配」精选。价格 / 优惠码可能随官网调整，请以各机场官网为准。")
    L.append("")
    for i, a in enumerate(AIRPORTS):
        title = a["name"] if a["en"] == a["name"] else "%s %s" % (a["name"], a["en"])
        label = "  ·  " + ("「%s」" % a["rank_label"]) if a.get("rank_label") else ""
        L.append("### %02d. %s%s" % (i + 1, title, label))
        L.append("")
        L.append('<img src="assets/og/%s.png" alt="%s" width="720">' % (a["slug"], title))
        L.append("")
        L.append("> %s" % a["tagline"])
        L.append("")
        L.append("- **线路类型**：%s" % a["type"])
        L.append("- **主要协议**：%s" % " · ".join(a["protocols"]))
        L.append("- **流媒体解锁**：%s" % " · ".join(a["unlock"]))
        L.append("- **覆盖地区**：%s" % a["regions"])
        L.append("- **起步价**：%s 起 %s（%s）" % (a["price_from"], a["price_unit"], a["billing"]))
        L.append("- **最适合**：%s" % a["best_for"])
        L.append("")
        L.append(a["verdict"])
        L.append("")
        L.append("**完整评测 → %s/%s/**" % (A, a["slug"]))
        L.append("")
    L.append("## 快速对比")
    L.append("")
    L.append("| 机场 | 线路类型 | 主要协议 | 解锁 | 起步价 | 最适合 |")
    L.append("| --- | --- | --- | --- | --- | --- |")
    for a in AIRPORTS:
        L.append("| [%s](%s/%s/) | %s | %s | %s | %s %s | %s |" % (
            a["name"], A, a["slug"], a["type"], " · ".join(a["protocols"]),
            " · ".join(a["unlock"]), a["price_from"], a["price_unit"], a["best_for"]))
    L.append("")
    L.append("## 30 秒教你怎么选")
    L.append("")
    for a in AIRPORTS:
        if a.get("featured"):
            L.append("- **%s** → 选 [%s](%s/%s/)" % (a["scene"], a["name"], A, a["slug"]))
    L.append("")
    L.append("## 新手小提示")
    L.append("")
    L.append("- 先买月付 / 小流量档验证稳定性，别一上来就大额年付。")
    L.append("- 老牌机场更稳；新机场先小档试水。")
    L.append("- 同时备用 2–3 家机场互为容灾，避免踩到跑路。")
    L.append("- 新协议（如 Hysteria2）要用支持它的客户端，否则导入会报错。")
    L.append("")
    L.append("## 免责声明")
    L.append("")
    L.append("本仓库与站点为第三方信息与推荐平台，非任何机场官方；页面内含推广链接，若你通过链接注册或购买，我们可能获得一定佣金，但不会增加你的任何成本。各机场的线路、价格、优惠码可能随时变动，请以对应官网实时信息为准。代理 / 加密技术的使用需遵守你所在国家或地区的法律法规，本站内容仅供学习与技术研究参考。")
    L.append("")
    return "\n".join(L) + "\n"

# ----------------------------------------------------------------------------- main
def write(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)
    print("  ✓", path)

def main():
    print("AIRREM build — %d airports" % len(AIRPORTS))
    for a in AIRPORTS:
        write("%s/index.html" % a["slug"], render_detail(a))
    write("airports/index.html", render_hub())
    write("sitemap.xml", render_sitemap())
    write("README.md", render_readme())
    idx_path = os.path.join(BASE, "index.html")
    idx = open(idx_path, encoding="utf-8").read()
    idx = inject(idx, "BOARD", render_board())
    idx = inject(idx, "PICK", render_pick())
    idx = inject(idx, "COMPARE", render_compare())
    idx = inject(idx, "WALL", render_wall())
    idx = inject(idx, "FOOTER_AIRPORTS", render_footer_airports())
    idx = inject(idx, "COUNT", str(len(AIRPORTS)))
    open(idx_path, "w", encoding="utf-8").write(idx)
    print("  ✓ index.html (injected)")
    print("Done.")


if __name__ == "__main__":
    main()
