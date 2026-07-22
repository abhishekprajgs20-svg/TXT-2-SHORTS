"""
Pillow-based slide renderer â€” 30 gamified dark themes.
Linux-compatible: uses DejaVu fonts (installed via apt fonts-dejavu-core).
"""
from PIL import Image, ImageDraw, ImageFont
import os

# â”€â”€ 30 Gamified Dark Themes â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
THEMES = [
    {"bg":(8,16,26),   "card":(15,23,42),  "border":(0,206,201),   "title":(0,206,201),  "accent":(253,203,110), "bt":(8,16,26),   "name":"Cyber Teal"},
    {"bg":(6,24,14),   "card":(10,31,20),  "border":(16,185,129),  "title":(52,211,153), "accent":(251,191,36),  "bt":(6,24,14),   "name":"Emerald Mana"},
    {"bg":(17,11,41),  "card":(24,15,54),  "border":(168,85,247),  "title":(192,132,252),"accent":(244,114,182), "bt":(17,11,41),  "name":"Cosmic Purple"},
    {"bg":(31,9,13),   "card":(38,12,18),  "border":(244,63,94),   "title":(251,113,133),"accent":(251,191,36),  "bt":(31,9,13),   "name":"Crimson Fire"},
    {"bg":(28,20,4),   "card":(36,26,8),   "border":(245,158,11),  "title":(251,191,36), "accent":(56,189,248),  "bt":(28,20,4),   "name":"Golden Blaze"},
    {"bg":(15,23,42),  "card":(22,33,58),  "border":(99,102,241),  "title":(129,140,248),"accent":(52,211,153),  "bt":(15,23,42),  "name":"Indigo Neon"},
    {"bg":(4,28,30),   "card":(8,38,41),   "border":(45,212,191),  "title":(45,212,191), "accent":(244,114,182), "bt":(4,28,30),   "name":"Aqua Surge"},
    {"bg":(31,16,19),  "card":(41,19,24),  "border":(251,113,133), "title":(253,164,175),"accent":(56,189,248),  "bt":(31,16,19),  "name":"Rose Neon"},
    {"bg":(26,8,26),   "card":(36,12,36),  "border":(236,72,153),  "title":(244,114,182),"accent":(245,158,11),  "bt":(26,8,26),   "name":"Hot Pink Wave"},
    {"bg":(12,31,19),  "card":(16,41,25),  "border":(74,222,128),  "title":(74,222,128), "accent":(251,191,36),  "bt":(12,31,19),  "name":"Matrix Green"},
    {"bg":(30,27,75),  "card":(40,36,100), "border":(129,140,248), "title":(165,180,252),"accent":(56,189,248),  "bt":(30,27,75),  "name":"Midnight Indigo"},
    {"bg":(49,46,129), "card":(65,61,160), "border":(192,132,252), "title":(233,213,255),"accent":(244,63,94),   "bt":(49,46,129), "name":"Ultra Violet"},
    {"bg":(131,24,67), "card":(155,32,80), "border":(244,114,182), "title":(251,207,232),"accent":(251,191,36),  "bt":(80,10,35),  "name":"Magenta Fire"},
    {"bg":(112,26,117),"card":(135,35,140),"border":(232,121,249), "title":(245,208,254),"accent":(52,211,153),  "bt":(60,10,65),  "name":"Violet Storm"},
    {"bg":(20,83,45),  "card":(28,105,58), "border":(74,222,128),  "title":(187,247,208),"accent":(251,191,36),  "bt":(10,40,22),  "name":"Jungle Electric"},
    {"bg":(22,78,99),  "card":(30,100,128),"border":(34,211,238),  "title":(207,250,254),"accent":(244,114,182), "bt":(10,40,55),  "name":"Ocean Cyber"},
    {"bg":(30,41,59),  "card":(40,58,85),  "border":(56,189,248),  "title":(186,230,253),"accent":(245,158,11),  "bt":(15,23,42),  "name":"Sapphire Neon"},
    {"bg":(46,16,101), "card":(62,22,135), "border":(168,85,247),  "title":(233,213,255),"accent":(45,212,191),  "bt":(25,8,55),   "name":"Dark Nebula"},
    {"bg":(76,29,149), "card":(98,40,190), "border":(192,132,252), "title":(243,232,255),"accent":(244,63,94),   "bt":(40,15,80),  "name":"Grape Surge"},
    {"bg":(136,19,55), "card":(165,25,68), "border":(251,113,133), "title":(255,228,230),"accent":(251,191,36),  "bt":(80,8,30),   "name":"Neon Rose"},
    {"bg":(124,45,18), "card":(155,58,24), "border":(251,146,60),  "title":(255,237,213),"accent":(56,189,248),  "bt":(65,22,8),   "name":"Lava Orange"},
    {"bg":(113,63,18), "card":(140,80,22), "border":(250,204,21),  "title":(254,240,138),"accent":(45,212,191),  "bt":(60,30,5),   "name":"Sunstorm Gold"},
    {"bg":(54,83,20),  "card":(68,105,26), "border":(163,230,53),  "title":(236,252,203),"accent":(244,114,182), "bt":(25,40,8),   "name":"Acid Lime"},
    {"bg":(6,78,59),   "card":(9,105,80),  "border":(52,211,153),  "title":(209,250,229),"accent":(251,191,36),  "bt":(3,40,30),   "name":"Forest Pulse"},
    {"bg":(19,78,74),  "card":(25,105,100),"border":(45,212,191),  "title":(204,251,241),"accent":(244,63,94),   "bt":(8,38,36),   "name":"Teal Blaze"},
    {"bg":(39,39,42),  "card":(55,55,60),  "border":(161,161,170), "title":(244,244,245),"accent":(56,189,248),  "bt":(20,20,22),  "name":"Monochrome Neo"},
    {"bg":(28,25,23),  "card":(42,38,35),  "border":(245,158,11),  "title":(254,243,199),"accent":(244,114,182), "bt":(15,12,10),  "name":"Amber Dark"},
    {"bg":(2,44,34),   "card":(5,58,45),   "border":(16,185,129),  "title":(209,250,229),"accent":(251,191,36),  "bt":(1,22,17),   "name":"Deep Forest"},
    {"bg":(23,37,84),  "card":(32,52,115), "border":(59,130,246),  "title":(219,234,254),"accent":(244,63,94),   "bt":(12,20,45),  "name":"Deep Blue Neo"},
    {"bg":(59,7,100),  "card":(80,12,135), "border":(217,70,239),  "title":(250,232,255),"accent":(45,212,191),  "bt":(30,3,55),   "name":"Dark Galaxy"},
]

# â”€â”€ Font Loader â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
_FONT_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/calibrib.ttf",
]
_FONT_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/calibri.ttf",
]

def _font(size, bold=False):
    pool = _FONT_BOLD if bold else _FONT_REG
    for p in pool:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()


def _wrap(text, font, max_w, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        bb   = draw.textbbox((0,0), test, font=font)
        if bb[2]-bb[0] <= max_w: cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


def _rr(draw, xy, r, fill, outline=None, width=3):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def _text_block(draw, text, font, color, x, y, max_w, gap=10):
    lines = _wrap(text, font, max_w, draw)
    dy = 0
    for line in lines:
        draw.text((x, y+dy), line, font=font, fill=color)
        bb  = draw.textbbox((0,0), line, font=font)
        dy += (bb[3]-bb[1]) + gap
    return dy


class PillowRenderer:
    def __init__(self, W=1080, H=1920):
        self.W = W; self.H = H; self.pad = 52

    def _t(self, idx):
        return THEMES[idx % len(THEMES)]

    def _bg(self, t):
        img  = Image.new("RGB", (self.W, self.H), t["bg"])
        draw = ImageDraw.Draw(img)
        dot  = tuple(min(255, c+20) for c in t["bg"])
        for x in range(0, self.W, 36):
            for y in range(0, self.H, 36):
                draw.ellipse([x-2,y-2,x+2,y+2], fill=dot)
        return img, draw

    def _footer(self, draw, t):
        W, H, pad = self.W, self.H, self.pad
        fy1 = H-92; fy2 = H-18
        _rr(draw, [pad, fy1, W-pad, fy2], 44, (10,16,28), t["border"], 4)
        f = _font(28, bold=True)
        txt = "ðŸ‘  LIKE, SHARE AND SUBSCRIBE  ðŸ””"
        bb  = draw.textbbox((0,0), txt, font=f)
        draw.text((W//2-(bb[2]-bb[0])//2, fy1+(fy2-fy1)//2-(bb[3]-bb[1])//2),
                  txt, font=f, fill=t["border"])

    def render_hook(self, idx):
        t = self._t(idx)
        img, draw = self._bg(t)
        W, H, pad = self.W, self.H, self.pad
        cx1, cy1 = pad+10, H//4
        cx2, cy2 = W-pad-10, H*3//4
        _rr(draw, [cx1,cy1,cx2,cy2], 40, t["card"], t["border"], 6)
        cx = (cx1+cx2)//2
        data = [
            ("ðŸŽ¯ IQ TEST TIME!", _font(54,True), t["title"]),
            ("Test Your Knowledge!",  _font(44,True), (255,255,255)),
            ("Guess in 10 Seconds â°", _font(36,True), t["accent"]),
            ("Are You Smarter Than 90%?", _font(32,False), (180,190,210)),
        ]
        dy = cy1+64
        for txt, f, col in data:
            bb  = draw.textbbox((0,0), txt, font=f)
            draw.text((cx-(bb[2]-bb[0])//2, dy), txt, font=f, fill=col)
            dy += (bb[3]-bb[1]) + 30
        self._footer(draw, t)
        return img

    def render_question(self, q, idx):
        t = self._t(idx)
        img, draw = self._bg(t)
        W, H, pad = self.W, self.H, self.pad
        letters = ["A","B","C","D"]
        # Badge
        f_badge = _font(28, True)
        bt = "QUIZ QUESTION"
        bb = draw.textbbox((0,0), bt, font=f_badge)
        bw, bh = bb[2]-bb[0]+52, bb[3]-bb[1]+26
        _rr(draw, [pad, pad, pad+bw, pad+bh+8], 32, t["border"])
        draw.text((pad+26, pad+13), bt, font=f_badge, fill=t["bt"])
        # Question
        qt = q.get("questionText",""); ql = len(qt)
        qfs = (48 if ql<120 else 38 if ql<250 else 30 if ql<450 else 24 if ql<700 else 20)
        f_q = _font(qfs, True)
        qy1 = pad+bh+26
        wlines = _wrap(qt, f_q, W-pad*2-40, draw)
        lh = draw.textbbox((0,0),"A",font=f_q)[3]+10
        qh = max(lh*len(wlines)+60, 120)
        _rr(draw, [pad, qy1, W-pad, qy1+qh], 28, t["card"], t["border"], 5)
        _text_block(draw, qt, f_q, (255,255,255), pad+22, qy1+22, W-pad*2-44)
        # Options
        opts = q.get("options",[])
        n_opts = len(opts)
        tol = sum(len(o) for o in opts)
        ofs = (32 if tol<100 else 26 if tol<250 else 22 if tol<400 else 18)
        f_opt = _font(ofs, True); f_bl = _font(28, True)
        footer_h = 100
        avail = H - (qy1+qh) - footer_h - 24
        oh = max(80, avail//max(n_opts,1)-16)
        for i, opt in enumerate(opts):
            oy1 = qy1+qh+18+i*(oh+12); oy2 = oy1+oh
            _rr(draw, [pad,oy1,W-pad,oy2], 22, t["card"], (80,95,120), 3)
            cx_b = pad+46; cy_b = (oy1+oy2)//2; r = 32
            draw.ellipse([cx_b-r,cy_b-r,cx_b+r,cy_b+r], fill=t["border"])
            lbb = draw.textbbox((0,0), letters[i], font=f_bl)
            draw.text((cx_b-(lbb[2]-lbb[0])//2, cy_b-(lbb[3]-lbb[1])//2),
                      letters[i], font=f_bl, fill=t["bt"])
            _text_block(draw, opt, f_opt, (235,240,252),
                        cx_b+r+18, oy1+14, W-cx_b-r-18-pad-10)
        self._footer(draw, t)
        return img

    def render_timer(self, q, idx, sec_val=10):
        t = self._t(idx)
        img, draw = self._bg(t)
        W, H, pad = self.W, self.H, self.pad
        letters = ["A","B","C","D"]
        f_badge = _font(28, True)
        bt = "â± THINK FAST!"
        bb = draw.textbbox((0,0), bt, font=f_badge)
        bw, bh = bb[2]-bb[0]+52, bb[3]-bb[1]+26
        _rr(draw, [pad,pad,pad+bw,pad+bh+8], 32, t["accent"])
        draw.text((pad+26, pad+13), bt, font=f_badge, fill=(10,10,10))
        qt = q.get("questionText",""); ql = len(qt)
        qfs = (44 if ql<120 else 36 if ql<250 else 28 if ql<450 else 22 if ql<700 else 18)
        f_q = _font(qfs, True)
        qy1 = pad+bh+26
        wlines = _wrap(qt, f_q, W-pad*2-40, draw)
        lh = draw.textbbox((0,0),"A",font=f_q)[3]+10
        qh = max(lh*len(wlines)+60, 110)
        _rr(draw, [pad,qy1,W-pad,qy1+qh], 28, t["card"], (80,95,120), 4)
        _text_block(draw, qt, f_q, (200,210,230), pad+22, qy1+22, W-pad*2-44)
        opts = q.get("options",[]); n_opts = len(opts)
        tol = sum(len(o) for o in opts)
        ofs = (28 if tol<100 else 23 if tol<250 else 19 if tol<400 else 16)
        f_opt = _font(ofs, True); f_bl = _font(24, True)
        timer_h = 135; footer_h = 100
        avail = H-(qy1+qh)-footer_h-timer_h-28
        oh = max(65, avail//max(n_opts,1)-12)
        for i, opt in enumerate(opts):
            oy1 = qy1+qh+14+i*(oh+10); oy2 = oy1+oh
            _rr(draw, [pad,oy1,W-pad,oy2], 20, t["card"], (80,95,120), 3)
            cx_b = pad+40; cy_b = (oy1+oy2)//2; r = 28
            draw.ellipse([cx_b-r,cy_b-r,cx_b+r,cy_b+r], fill=t["border"])
            lbb = draw.textbbox((0,0), letters[i], font=f_bl)
            draw.text((cx_b-(lbb[2]-lbb[0])//2, cy_b-(lbb[3]-lbb[1])//2),
                      letters[i], font=f_bl, fill=t["bt"])
            _text_block(draw, opt, f_opt, (235,240,252),
                        cx_b+r+16, oy1+10, W-cx_b-r-16-pad-10)
        opts_bot = qy1+qh+14+n_opts*(oh+10)
        # Timer box
        tb1 = opts_bot+8; tb2 = tb1+timer_h
        _rr(draw, [pad,tb1,W-pad,tb2], 24, t["card"], t["accent"], 5)
        ring_cx = pad+72; ring_cy = (tb1+tb2)//2; rr = 44
        draw.arc([ring_cx-rr,ring_cy-rr,ring_cx+rr,ring_cy+rr], 0, 360, fill=(55,65,85), width=9)
        frac = sec_val/10.0
        end_a = -90+frac*360
        if end_a > -90:
            draw.arc([ring_cx-rr,ring_cy-rr,ring_cx+rr,ring_cy+rr], -90, end_a, fill=t["accent"], width=9)
        f_num = _font(52, True)
        nbb   = draw.textbbox((0,0), str(sec_val), font=f_num)
        draw.text((ring_cx-(nbb[2]-nbb[0])//2, ring_cy-(nbb[3]-nbb[1])//2),
                  str(sec_val), font=f_num, fill=t["accent"])
        f_lbl = _font(30, True)
        lbl = "GUESS THE ANSWER!"
        lbb   = draw.textbbox((0,0), lbl, font=f_lbl)
        draw.text((ring_cx+rr+22, (tb1+tb2)//2-(lbb[3]-lbb[1])//2), lbl, font=f_lbl, fill=t["accent"])
        self._footer(draw, t)
        return img

    def render_answer(self, q, idx):
        t = self._t(idx)
        img, draw = self._bg(t)
        W, H, pad = self.W, self.H, self.pad
        letters = ["A","B","C","D"]
        correct = q.get("correctIndex", 0)
        f_badge = _font(28, True)
        bt = "âœ… ANSWER REVEAL"
        bb = draw.textbbox((0,0), bt, font=f_badge)
        bw, bh = bb[2]-bb[0]+52, bb[3]-bb[1]+26
        _rr(draw, [pad,pad,pad+bw,pad+bh+8], 32, (16,185,129))
        draw.text((pad+26, pad+13), bt, font=f_badge, fill=(255,255,255))
        qt = q.get("questionText",""); ql = len(qt)
        qfs = (42 if ql<120 else 34 if ql<250 else 27 if ql<450 else 22 if ql<700 else 18)
        f_q = _font(qfs, True)
        qy1 = pad+bh+26
        wlines = _wrap(qt, f_q, W-pad*2-40, draw)
        lh = draw.textbbox((0,0),"A",font=f_q)[3]+10
        qh = max(lh*len(wlines)+55, 105)
        _rr(draw, [pad,qy1,W-pad,qy1+qh], 28, t["card"], (80,95,120), 4)
        _text_block(draw, qt, f_q, (190,200,225), pad+22, qy1+22, W-pad*2-44)
        opts = q.get("options",[]); n_opts = len(opts)
        tol = sum(len(o) for o in opts)
        ofs = (30 if tol<100 else 25 if tol<250 else 21 if tol<400 else 17)
        f_opt = _font(ofs, True); f_bl = _font(28, True)
        avail = H-(qy1+qh)-110
        oh = max(82, avail//max(n_opts,1)-16)
        for i, opt in enumerate(opts):
            oy1 = qy1+qh+18+i*(oh+13); oy2 = oy1+oh
            is_c = (i == correct)
            cc   = (14,55,38) if is_c else t["card"]
            bc   = (16,185,129) if is_c else (70,85,105)
            bw_b = 5 if is_c else 3
            _rr(draw, [pad,oy1,W-pad,oy2], 22, cc, bc, bw_b)
            if is_c:
                for gw in [9,6,3]:
                    draw.rounded_rectangle([pad-gw,oy1-gw,W-pad+gw,oy2+gw],
                                           radius=26, outline=(10,200,120), width=1)
            bg_b = (16,185,129) if is_c else t["border"]
            fg_b = (255,255,255) if is_c else t["bt"]
            cx_b = pad+46; cy_b = (oy1+oy2)//2; r = 32
            draw.ellipse([cx_b-r,cy_b-r,cx_b+r,cy_b+r], fill=bg_b)
            lbb = draw.textbbox((0,0), letters[i], font=f_bl)
            draw.text((cx_b-(lbb[2]-lbb[0])//2, cy_b-(lbb[3]-lbb[1])//2),
                      letters[i], font=f_bl, fill=fg_b)
            txt_c = (195,255,218) if is_c else (230,235,248)
            ot    = opt + (" âœ… CORRECT!" if is_c else "")
            _text_block(draw, ot, f_opt, txt_c, cx_b+r+18, oy1+13, W-cx_b-r-18-pad-10)
        self._footer(draw, t)
        return img

    def render_explanation(self, chunk, idx):
        t = self._t(idx)
        img, draw = self._bg(t)
        W, H, pad = self.W, self.H, self.pad
        f_title = _font(46, True)
        title   = "ðŸ“– Explanation"
        tbb     = draw.textbbox((0,0), title, font=f_title)
        draw.text((W//2-(tbb[2]-tbb[0])//2, pad+8), title, font=f_title, fill=t["title"])
        ty_bot  = pad+8+(tbb[3]-tbb[1])+18
        draw.line([(pad+28,ty_bot),(W-pad-28,ty_bot)], fill=t["border"], width=4)
        f_exp   = _font(30, False)
        n       = len(chunk); avail = H-ty_bot-130
        ch      = avail//max(n,1)-18
        for i, sent in enumerate(chunk):
            cy1 = ty_bot+22+i*(ch+16); cy2 = cy1+ch
            _rr(draw, [pad,cy1,W-pad,cy2], 22, t["card"], t["border"], 4)
            dx  = pad+28; dy_b = cy1+22
            draw.ellipse([dx-10,dy_b-10,dx+10,dy_b+10], fill=t["accent"])
            _text_block(draw, sent, f_exp, (228,234,248),
                        dx+22, cy1+12, W-dx-22-pad-14, gap=10)
        self._footer(draw, t)
        return img

    def render_ending(self, idx):
        t = self._t(idx)
        img, draw = self._bg(t)
        W, H, pad = self.W, self.H, self.pad
        cx1,cy1 = pad+18, H//3; cx2,cy2 = W-pad-18, H*2//3+58
        _rr(draw, [cx1,cy1,cx2,cy2], 50, t["card"], (255,71,87), 6)
        for gw in [12,8,4]:
            draw.rounded_rectangle([cx1-gw,cy1-gw,cx2+gw,cy2+gw],
                                   radius=54, outline=(255,max(0,71-gw*4),80), width=1)
        f_fire = _font(88, True)
        fstr   = "ðŸ”¥"
        fbb    = draw.textbbox((0,0), fstr, font=f_fire)
        draw.text((W//2-(fbb[2]-fbb[0])//2, cy1+38), fstr, font=f_fire, fill=(255,71,87))
        f_fol  = _font(50, True)
        fol    = "Follow for Daily Quiz!"
        flbb   = draw.textbbox((0,0), fol, font=f_fol)
        fy     = cy1+38+(fbb[3]-fbb[1])+26
        draw.text((W//2-(flbb[2]-flbb[0])//2, fy), fol, font=f_fol, fill=(255,255,255))
        f_sub  = _font(32, False)
        sub    = "LIKE Â· SHARE Â· SUBSCRIBE ðŸ””"
        sbb    = draw.textbbox((0,0), sub, font=f_sub)
        draw.text((W//2-(sbb[2]-sbb[0])//2, fy+(flbb[3]-flbb[1])+22),
                  sub, font=f_sub, fill=t["accent"])
        self._footer(draw, t)
        return img