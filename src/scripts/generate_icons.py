#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyLaTeX 图标生成脚本（零第三方依赖）

package.json 的 electron-builder 配置里引用了 icon.ico / icon.icns / icon.png，
main/index.js 也用 icon.png 作为窗口图标，但 src/frontend/assets/icons/ 目录
从来就不存在。手动去下载素材不现实，这里直接用纯 Python 画出图标。

实现思路：
  * 只依赖标准库 zlib / struct，手写 PNG 编码器；
  * 先在 4 倍超采样画布上按「有符号距离场」绘制形状，再盒式降采样，
    得到平滑的抗锯齿边缘；
  * ICO 直接内嵌 PNG（Vista 起支持），ICNS 用 ic07/ic08 条目拼装。

用法：
    python src/scripts/generate_icons.py [输出目录]
"""

import math
import os
import struct
import sys
import zlib

# ---------------------------------------------------------------------------
# 画布
# ---------------------------------------------------------------------------

class Canvas(object):
    """RGBA 浮点画布，坐标为像素中心。"""

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.buf = bytearray(w * h * 4)

    def blend(self, x, y, r, g, b, a):
        """
        在整数像素 (x, y) 上做源覆盖混合。

        颜色参数使用 0~1 浮点，缓冲区是 0~255 字节，必须乘 255 换算 ——
        否则 int(0.965) == 0，整个图标会被压成一块黑色。
        """
        if a <= 0 or x < 0 or y < 0 or x >= self.w or y >= self.h:
            return
        if a > 1.0:
            a = 1.0
        i = (y * self.w + x) * 4
        buf = self.buf
        ia = 1.0 - a
        buf[i] = min(255, int(buf[i] * ia + r * 255 * a))
        buf[i + 1] = min(255, int(buf[i + 1] * ia + g * 255 * a))
        buf[i + 2] = min(255, int(buf[i + 2] * ia + b * 255 * a))
        buf[i + 3] = min(255, int(buf[i + 3] * ia + 255 * a))

    def to_png_bytes(self):
        return encode_png(self.w, self.h, bytes(self.buf))


# ---------------------------------------------------------------------------
# PNG 编码
# ---------------------------------------------------------------------------

def _chunk(tag, data):
    return (struct.pack('>I', len(data)) + tag + data +
            struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF))


def encode_png(width, height, rgba):
    raw = bytearray()
    stride = width * 4
    for y in range(height):
        raw.append(0)  # filter type 0 (None)
        raw += rgba[y * stride:(y + 1) * stride]

    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n' +
            _chunk(b'IHDR', ihdr) +
            _chunk(b'IDAT', zlib.compress(bytes(raw), 9)) +
            _chunk(b'IEND', b''))


# ---------------------------------------------------------------------------
# 形状：有符号距离场
# ---------------------------------------------------------------------------

def sd_rounded_rect(px, py, cx, cy, hw, hh, r):
    """圆角矩形的 SDF，内部为负、外部为正。"""
    qx = abs(px - cx) - hw + r
    qy = abs(py - cy) - hh + r
    return math.hypot(max(qx, 0.0), max(qy, 0.0)) + min(max(qx, qy), 0.0) - r


def sd_circle(px, py, cx, cy, r):
    return math.hypot(px - cx, py - cy) - r


def sd_triangle(px, py, ax, ay, bx, by, cx, cy):
    """三角形 SDF（用于折角缺口）。"""
    def seg(px, py, x1, y1, x2, y2):
        ex, ey = x2 - x1, y2 - y1
        wx, wy = px - x1, py - y1
        t = max(0.0, min(1.0, (wx * ex + wy * ey) / (ex * ex + ey * ey)))
        return math.hypot(wx - ex * t, wy - ey * t)

    d = min(seg(px, py, ax, ay, bx, by),
            seg(px, py, bx, by, cx, cy),
            seg(px, py, cx, cy, ax, ay))
    # 奇偶规则判断内外：用叉积符号一致性
    def sign(x1, y1, x2, y2, x3, y3):
        return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)
    b1 = sign(px, py, ax, ay, bx, by) < 0
    b2 = sign(px, py, bx, by, cx, cy) < 0
    b3 = sign(px, py, cx, cy, ax, ay) < 0
    inside = (b1 == b2) and (b2 == b3)
    return -d if inside else d


# ---------------------------------------------------------------------------
# 图标绘制
# ---------------------------------------------------------------------------

BG_TOP = (0.098, 0.518, 0.965)      # #197FDB
BG_BOTTOM = (0.027, 0.298, 0.694)   # #074CB1
PAPER = (1.0, 1.0, 1.0)
INK = (0.42, 0.47, 0.53)            # 正文灰
ACCENT = (0.098, 0.518, 0.965)      # 强调蓝


def draw_icon(size, supersample=4):
    """绘制一张 size x size 的 RGBA 图标。"""
    s = size * supersample
    canvas = Canvas(s, s)
    inv = 1.0 / s

    # 画布坐标统一归一化到 [0,1]，再乘回超采样尺寸，便于跨尺寸复用
    def X(u):
        return u * s

    # ---- 背景：圆角方形 + 竖向渐变 ----
    bg_radius = 0.22
    for y in range(s):
        py = (y + 0.5) * inv
        for x in range(s):
            px = (x + 0.5) * inv
            sd = sd_rounded_rect(px, py, 0.5, 0.5, 0.5, 0.5, bg_radius)
            cov = max(0.0, min(1.0, 0.5 - sd * s * 0.5))
            if cov <= 0:
                continue
            t = py
            r = BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * t
            g = BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * t
            b = BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * t
            canvas.blend(x, y, r, g, b, cov)

    # ---- 白色文档纸：圆角矩形减去右上角折角三角 ----
    paper_left, paper_top = 0.235, 0.155
    paper_right, paper_bottom = 0.765, 0.845
    pcx = (paper_left + paper_right) / 2
    pcy = (paper_top + paper_bottom) / 2
    phw = (paper_right - paper_left) / 2
    phh = (paper_bottom - paper_top) / 2
    fold_size = 0.185
    fx0, fy0 = paper_right - fold_size, paper_top
    fx1, fy1 = paper_right, paper_top
    fx2, fy2 = paper_right, paper_top + fold_size

    for y in range(s):
        py = (y + 0.5) * inv
        if py < paper_top - 0.02 or py > paper_bottom + 0.02:
            continue
        for x in range(s):
            px = (x + 0.5) * inv
            if px < paper_left - 0.02 or px > paper_right + 0.02:
                continue
            sd = sd_rounded_rect(px, py, pcx, pcy, phw, phh, 0.035)
            cov = max(0.0, min(1.0, 0.5 - sd * s * 0.5))
            if cov <= 0:
                continue
            # 折角：落在三角形内部的地方抠掉
            sd_tri = sd_triangle(px, py, fx0, fy0, fx1, fy1, fx2, fy2)
            cut = max(0.0, min(1.0, 0.5 - sd_tri * s * 0.5))
            cov *= (1.0 - cut)
            if cov <= 0:
                continue
            canvas.blend(x, y, PAPER[0], PAPER[1], PAPER[2], cov)

    # ---- 折角三角（右上角补一小块浅色） ----
    for y in range(s):
        py = (y + 0.5) * inv
        if py < paper_top - 0.02 or py > paper_top + fold_size + 0.02:
            continue
        for x in range(s):
            px = (x + 0.5) * inv
            if px < fx0 - 0.02 or px > paper_right + 0.02:
                continue
            sd_tri = sd_triangle(px, py, fx0, fy0, fx1, fy1, fx2, fy2)
            cov = max(0.0, min(1.0, 0.5 - sd_tri * s * 0.5))
            if cov <= 0:
                continue
            canvas.blend(x, y, 0.80, 0.86, 0.93, cov * 0.95)

    # ---- 文档内的文本行与公式占位条 ----
    lines = [
        (0.315, 0.385, 0.36, 0.021, INK),      # 标题行
        (0.315, 0.470, 0.50, 0.017, INK),      # 正文行 1
        (0.315, 0.535, 0.44, 0.017, INK),      # 正文行 2
        (0.315, 0.655, 0.62, 0.030, ACCENT),   # 公式条（蓝色强调）
        (0.315, 0.735, 0.38, 0.017, INK),      # 正文行 3
    ]
    for lx, ly, lw, lh, color in lines:
        _draw_capsule(canvas, s, inv, X(lx), X(ly), X(lw), X(lh), color)

    return downsample(canvas, supersample)


def _draw_capsule(canvas, s, inv, x0, y0, w, h, color):
    """画一个胶囊形（两端半圆）色条。"""
    r = h / 2.0
    cx1, cy = x0 + r, y0 + r
    cx2 = x0 + w - r
    x_min = max(0, int(x0 - 1))
    x_max = min(s, int(x0 + w + 2))
    y_min = max(0, int(y0 - 1))
    y_max = min(s, int(y0 + h + 2))
    for y in range(y_min, y_max):
        py = y + 0.5
        for x in range(x_min, x_max):
            px = x + 0.5
            if px < cx1:
                sd = sd_circle(px, py, cx1, cy, r)
            elif px > cx2:
                sd = sd_circle(px, py, cx2, cy, r)
            else:
                sd = abs(py - cy) - r
            cov = max(0.0, min(1.0, 0.5 - sd * 0.5))
            if cov > 0:
                canvas.blend(x, y, color[0], color[1], color[2], cov)


def downsample(canvas, factor):
    """盒式降采样，得到抗锯齿效果。"""
    out_size = canvas.w // factor
    out = Canvas(out_size, out_size)
    src = canvas.buf
    n = factor * factor
    for oy in range(out_size):
        for ox in range(out_size):
            r = g = b = a = 0
            for dy in range(factor):
                base = ((oy * factor + dy) * canvas.w + ox * factor) * 4
                for dx in range(factor):
                    i = base + dx * 4
                    r += src[i]
                    g += src[i + 1]
                    b += src[i + 2]
                    a += src[i + 3]
            o = (oy * out_size + ox) * 4
            out.buf[o] = r // n
            out.buf[o + 1] = g // n
            out.buf[o + 2] = b // n
            out.buf[o + 3] = a // n
    return out


# ---------------------------------------------------------------------------
# ICO / ICNS 容器
# ---------------------------------------------------------------------------

def encode_ico(png_sizes):
    """
    组装 ICO 文件。每个条目内嵌一张 PNG（Vista+ 支持 PNG 压缩的图标条目）。
    :param png_sizes: [(size, png_bytes), ...]
    """
    header = struct.pack('<HHH', 0, 1, len(png_sizes))
    entries = []
    offset = 6 + 16 * len(png_sizes)
    for size, data in png_sizes:
        # 尺寸 >= 256 时 ICO 里记录为 0
        dim = 0 if size >= 256 else size
        entries.append(struct.pack('<BBBBHHII',
                                   dim, dim, 0, 0, 1, 32,
                                   len(data), offset))
        offset += len(data)
    return header + b''.join(entries) + b''.join(d for _, d in png_sizes)


def encode_icns(entries):
    """
    组装 ICNS 文件。
    :param entries: [(四字节类型, bytes), ...]，如 ('ic08', 256x256 PNG)
    """
    body = b''
    for tag, data in entries:
        body += tag + struct.pack('>I', len(data) + 8) + data
    return b'icns' + struct.pack('>I', len(body) + 8) + body


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------

def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'assets', 'icons')
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)

    print('生成图标到: %s' % out_dir)

    main_png = draw_icon(256)
    with open(os.path.join(out_dir, 'icon.png'), 'wb') as f:
        f.write(main_png.to_png_bytes())
    print('  icon.png  256x256')

    # ICO：Windows 需要多尺寸，这里给 16/24/32/48/64/128/256
    sizes = [16, 24, 32, 48, 64, 128, 256]
    pngs = []
    for size in sizes:
        ss = 4 if size <= 128 else 3      # 大图降低超采样倍数，避免耗时过长
        pngs.append((size, draw_icon(size, ss).to_png_bytes()))
        print('  ico 条目  %dx%d' % (size, size))
    with open(os.path.join(out_dir, 'icon.ico'), 'wb') as f:
        f.write(encode_ico(pngs))
    print('  icon.ico  (%d 个尺寸)' % len(pngs))

    # ICNS：macOS，ic07=128x128 PNG，ic08=256x256 PNG
    icns_entries = [
        (b'ic07', draw_icon(128).to_png_bytes()),
        (b'ic08', draw_icon(256).to_png_bytes()),
    ]
    with open(os.path.join(out_dir, 'icon.icns'), 'wb') as f:
        f.write(encode_icns(icns_entries))
    print('  icon.icns (ic07 + ic08)')

    # 托盘/窗口用的小尺寸图标，方便前端直接引用
    for size in (16, 32, 48):
        with open(os.path.join(out_dir, 'icon_%d.png' % size), 'wb') as f:
            f.write(draw_icon(size, 4).to_png_bytes())
        print('  icon_%d.png' % size)

    print('完成。')


if __name__ == '__main__':
    main()
