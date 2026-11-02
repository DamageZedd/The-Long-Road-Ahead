"""Verify every <texture> id in the TLRA travel-map XML resolves.
Usage: python tools/check_ui_textures.py <vanilla textures_descr dir>
Frame bases (InitFrame) resolve if all of _back,_l,_r,_t,_b,_lt,_rt,_lb,_rb exist."""
import re, sys, glob, os
root = os.path.join(os.path.dirname(__file__), '..', '00 - Core', 'gamedata', 'configs', 'ui')
ids = set()
for f in glob.glob(os.path.join(sys.argv[1], '*.xml')) + [os.path.join(root, 'textures_descr', 'tlra_maps.xml')]:
    ids |= set(re.findall(r'<texture\s+id="([^"]+)"', open(f, encoding='utf-8', errors='replace').read()))
xml = open(os.path.join(root, 'ui_tlra_travel_map.xml'), encoding='utf-8').read()
used = sorted(set(re.findall(r'<texture[^>]*>([^<]+)</texture>', xml)))
bad = 0
for u in used:
    ok = u in ids
    if not ok and all(u + s in ids for s in ('_back','_l','_r','_t','_b','_lt','_rt','_lb','_rb')): ok = 'frame'
    if not ok and all(u + s in ids for s in ('_d','_e','_h','_t')): ok = 'button'
    print(('OK  ' if ok else 'MISSING ') + u + (f' [{ok}]' if isinstance(ok, str) else ''))
    bad += not ok
sys.exit(1 if bad else 0)
