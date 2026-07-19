# -*- coding: utf-8 -*-
# 一次性脚本：Windows 缺 Noto CJK，临时用微软雅黑生成 tifa 的 OG 图。用完即删。
import make_images as M
from PIL import ImageFont

M.font = lambda size, bold=False: ImageFont.truetype(
    r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc", size)
M.airport_og(next(a for a in M.AIR if a["slug"] == "tifa"))
print("tifa og generated")
