"""Approximate PIL mockup of the TLRA travel GUI (NOT an in-game render).
Vanilla frame/button art is read from an extracted ui_common.dds passed as argv[1];
output is docs/images/gui_mockup.png. Vanilla art is not stored in the repo."""
import sys, os
from PIL import Image, ImageDraw, ImageFont
repo = os.path.join(os.path.dirname(__file__), '..')
common = Image.open(sys.argv[1]).convert('RGBA')
atlas = Image.open(os.path.join(repo, '00 - Core/gamedata/textures/ui/tlra_stalker_atlas.dds')).convert('RGBA')
def tile(x, y, w, h): return common.crop((x, y, x + w, y + h))
def tint(im, c):
    r, g, b = c; px = im.load()
    out = im.copy(); p = out.load()
    for i in range(im.width):
        for j in range(im.height):
            R, G, B, A = px[i, j]; p[i, j] = (R * r // 255, G * g // 255, B * b // 255, A)
    return out
D = {'lt': (826,252), 'l': (826,284), 'lb': (826,316), 'b': (858,316), 'back': (858,284),
     't': (858,252), 'rt': (890,252), 'r': (890,284), 'rb': (890,316)}
def frame(img, x, y, w, h, c=(255,255,255)):
    T = {k: tint(tile(*v, 32, 32), c) for k, v in D.items()}
    P = lambda k, X, Y, W=32, H=32: img.alpha_composite(T[k].resize((max(W,1), max(H,1))), (X, Y))
    P('back', x+32, y+32, w-64, h-64)
    P('t', x+32, y, w-64); P('b', x+32, y+h-32, w-64)
    P('l', x, y+32, 32, h-64); P('r', x+w-32, y+32, 32, h-64)
    for k, (X, Y) in {'lt': (x, y), 'rt': (x+w-32, y), 'lb': (x, y+h-32), 'rb': (x+w-32, y+h-32)}.items(): P(k, X, Y)
def font(sz):
    for f in ('arial.ttf', 'C:/Windows/Fonts/arial.ttf'):
        try: return ImageFont.truetype(f, sz)
        except Exception: pass
    return ImageFont.load_default()
F16, F18, F22 = font(14), font(16), font(20)
img = Image.new('RGBA', (1024, 768), (36, 42, 34, 255))
d = ImageDraw.Draw(img)
# placeholder terrain + route
import random; random.seed(3)
for _ in range(900):
    x, y = random.randrange(1024), random.randrange(768); s = random.randrange(8, 40)
    g = random.randrange(-12, 12); d.rectangle((x, y, x+s, y+s), fill=(40+g, 50+g, 38+g, 255))
route = [(40, 700), (200, 560), (330, 470), (512, 384), (700, 300), (880, 200)]
d.line(route, fill=(230, 190, 90, 255), width=3)
# footprints behind pawn (placeholder dots)
for t in range(6):
    x = 512 - 42 - t*28; y = 384 + 36 + t*20 + (6 if t % 2 else -6)
    d.ellipse((x-6, y-8, x+6, y+8), fill=(25, 22, 18, 220))
d.ellipse((6, 6, 6, 6))
# pawn: 112px, pedestal centre (0.5, 0.72) on route point
pawn = atlas.crop((500, 0, 628, 128)).resize((112, 112), Image.LANCZOS)
img.alpha_composite(pawn, (512 - 56, 384 - round(112 * 0.72)))
d.ellipse((509, 381, 515, 387), outline=(255, 60, 60, 255))  # route point
def hdr(x, y, w, txt):
    b = tint(tile(0, 115, 117, 29), (200, 190, 180)).resize((w-12, 19)); img.alpha_composite(b, (x+6, y+6))
    d.text((x+14, y+7), txt, font=F18, fill=(245, 195, 75))
def panel(x, y, w, h, acc=(200,150,60)):
    frame(img, x, y, w, h)
    for ax, ay, aw, ah in ((5,5,w-10,1), (5,h-6,w-10,1), (5,5,1,h-10), (w-6,5,1,h-10)):
        d.rectangle((x+ax, y+ay, x+ax+aw-1, y+ay+ah-1), fill=acc+(150,))
def T(x, y, s, c, f=F16): d.text((x, y), s, font=f, fill=c)
panel(20, 16, 310, 74); d.rectangle((25, 21, 324, 22), fill=(200,150,60))
T(32, 24, 'EXPEDITION: CORDON', (245,195,75), F18); T(32, 46, 'Route Trek: 597m | Safe Stride Mode Active', (220,215,200)); T(32, 66, 'Slow Pace / ALife Radar Scanning', (190,180,150))
panel(377, 16, 270, 74, (140,135,115)); T(440, 24, '[10x SPEED] 11:26', (255,230,130), F18); T(460, 46, 'Weather: Clear Skies', (140,200,235)); T(450, 66, 'Threat Risk: Clear Route', (255,100,70))
panel(724, 16, 280, 74); T(900, 24, '0% (0m / 0m)', (245,195,75), F18)
d.rectangle((734, 48, 993, 62), fill=(90,95,105)); d.rectangle((735, 49, 992, 61), fill=(34,38,46)); d.rectangle((735, 49, 800, 61), fill=(224,164,60))
d.rectangle((734, 68, 993, 78), fill=(70,75,85)); d.rectangle((735, 69, 992, 77), fill=(75,185,140))
panel(20, 618, 280, 132); hdr(20, 618, 280, 'SURVIVAL TELEMETRY')
for i, (s, c) in enumerate([('Calories: 2,500 kcal', (240,225,190)), ('Hydration: 99%', (130,205,250)), ('Stamina: 99%', (145,235,140))]): T(30, 644+i*22, s, c)
T(30, 712, 'Pack: 34.8 kg / 60 kg [3.4 m/s]', (215,210,200)); T(195, 644, 'Rad: 0.00 mSv', (245,195,80)); T(195, 666, 'Psy-Health', (110,215,200)); d.rectangle((195, 690, 289, 704), fill=(60,190,180))
panel(315, 618, 480, 132); hdr(315, 618, 480, 'ROAD RECONNAISSANCE LOG')
for i, (s, v) in enumerate([('Crossing open terrain... Maintaining low profile.', 245), ('Weather clear. Steady walking rhythm established.', 205), ('ALife Threat Radar scanning road ahead (100m radius).', 175), ('Route plotted: heading towards destination beacon.', 145), ('Terrain clear of anomalies. Stamina holding stable.', 120)]): T(327, 644+i*20, '13:55 - ' + s, (v, v-5, v-20))
panel(815, 618, 189, 132); hdr(815, 618, 189, '   COMMAND')
btn = tile(0, 115, 117, 29).resize((159, 48)); img.alpha_composite(btn, (830, 654)); T(868, 668, 'HALT [ESC]', (230,225,215), F18); T(880, 714, 'Safe Abort', (180,165,130))
# threat modal on a second panel variant: drawn smaller beside as inset note
img.convert('RGB').save(os.path.join(repo, 'docs/images/gui_mockup.png'))
# modal variant
m = Image.new('RGBA', (660, 410), (0, 0, 0, 0)); sv = img; img = m; d = ImageDraw.Draw(m)
frame(m, 0, 0, 660, 410, (255,150,140))
for ax, ay, aw, ah in ((7,7,646,3), (7,400,646,3), (7,7,2,396), (651,7,2,396)): d.rectangle((ax, ay, ax+aw-1, ay+ah-1), fill=(235,60,45,200))
d.text((130, 26), 'HOSTILE CONTACT DETECTED ON ROAD!', font=F22, fill=(255,65,50))
d.text((190, 72), 'Unknown ALife Hostile Squad in proximity!', font=F18, fill=(240,230,210))
d.rectangle((155, 165, 505, 229), fill=(40,34,30,240)); d.text((230, 185), 'STEALTH EVASION: 65%', font=F22, fill=(235,175,65))
for bx, s in ((50, '[E] ATTEMPT EVASION'), (350, '[F] DROP OUT & FIGHT')):
    m.alpha_composite(tile(0, 115, 117, 29).resize((260, 52)), (bx, 295)); d.text((bx+50, 311), s, font=F18, fill=(230,225,215))
m.convert('RGB').save(os.path.join(repo, 'docs/images/gui_mockup_modal.png'))
