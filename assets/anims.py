import math, os, random, json
OUT = '/mnt/user-data/outputs/readme-pack/assets/anim'
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    os.remove(f'{OUT}/{f}')
R = random.Random(11)
PAL = ['#8A2BE2', '#DC2626', '#FBBF24', '#22d3ee', '#3DDC84', '#f472b6', '#2496ED', '#c39bf5']
MONO = "Consolas, Menlo, 'Courier New', monospace"
meta = {'strips': [], 'smalls': []}


def svg(w, h, body, defs=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{defs}</defs>{body}</svg>'


def save(name, s, kind, width):
    with open(f'{OUT}/{name}.svg', 'w') as f:
        f.write(s)
    meta[kind].append({'src': f'./assets/anim/{name}.svg', 'width': width})


GLOW = '<filter id="g" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'

# ---------------- strips ----------------
# 1 flow bars (8)
for i in range(8):
    a, b = PAL[i], PAL[(i + 3) % 8]
    d = f'<linearGradient id="f" gradientUnits="userSpaceOnUse" x1="0" x2="300" spreadMethod="repeat"><stop offset="0" stop-color="{a}" stop-opacity=".1"/><stop offset=".5" stop-color="{b}"/><stop offset="1" stop-color="{a}" stop-opacity=".1"/>' \
        f'<animateTransform attributeName="gradientTransform" type="translate" values="0 0;{300 if i%2 else -300} 0" dur="{2+i*.3:.1f}s" repeatCount="indefinite"/></linearGradient>'
    save(f'flow{i}', svg(900, 8, '<rect y="2" width="900" height="4" rx="2" fill="url(#f)"/>', d), 'strips', '100%')

# 2 waves (10)
for i in range(10):
    c = PAL[i % 8]; fq = 1.5 + (i % 5); amp = 8 + (i % 4) * 4; N = 12
    vals = []
    for k in range(N + 1):
        ph = 2 * math.pi * k / N
        vals.append('M' + 'L'.join(f'{x},{25+amp*math.sin(x/900*2*math.pi*fq+ph):.1f}' for x in range(0, 901, 15)))
    vals2 = []
    for k in range(N + 1):
        ph = -2 * math.pi * k / N + 1
        vals2.append('M' + 'L'.join(f'{x},{25+amp*.7*math.sin(x/900*2*math.pi*(fq+1)+ph):.1f}' for x in range(0, 901, 15)))
    body = (f'<path d="{vals[0]}" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" filter="url(#g)"><animate attributeName="d" values="{";".join(vals)}" dur="{4+i*.5}s" repeatCount="indefinite"/></path>'
            f'<path d="{vals2[0]}" fill="none" stroke="{PAL[(i+4)%8]}" stroke-opacity=".45" stroke-width="1.5"><animate attributeName="d" values="{";".join(vals2)}" dur="{5+i*.4}s" repeatCount="indefinite"/></path>')
    save(f'wave{i}', svg(900, 50, body, GLOW), 'strips', '100%')

# 3 equalizers (8)
for i in range(8):
    c = PAL[i]; n = 28; bars = ''
    for k in range(n):
        vs = [R.randint(4, 46) for _ in range(6)]; vs.append(vs[0])
        dur = R.uniform(.7, 1.8)
        bars += (f'<rect x="{k*11+2}" width="7" rx="2" fill="{c}" fill-opacity="{.45+.5*(k%4)/3:.2f}"><animate attributeName="height" values="{";".join(map(str,vs))}" dur="{dur:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{";".join(str(50-v) for v in vs)}" dur="{dur:.2f}s" repeatCount="indefinite"/></rect>')
    save(f'eq{i}', svg(312, 50, bars), 'strips', '34%')

# 4 particles (8)
for i in range(8):
    c = PAL[i]; body = ''
    for k in range(34):
        x = R.randint(5, 895); r = R.uniform(1, 3.2); dur = R.uniform(3, 8); beg = -R.uniform(0, 8)
        body += (f'<circle cx="{x}" r="{r:.1f}" fill="{c}"><animate attributeName="cy" values="66;-6" dur="{dur:.1f}s" begin="{beg:.1f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0;.9;0" dur="{dur:.1f}s" begin="{beg:.1f}s" repeatCount="indefinite"/></circle>')
    save(f'particles{i}', svg(900, 60, body), 'strips', '100%')

# 5 circuits (8)
for i in range(8):
    c = PAL[i]; r = random.Random(100 + i); x, y = 0, 20; d = 'M0 20'; nodes = []
    while x < 900:
        x += r.randint(40, 110); d += f'L{min(x,900)} {y}'; nodes.append((min(x, 900), y))
        ny = r.choice([8, 20, 32]);
        if ny != y:
            y = ny; d += f'L{min(x,900)} {y}'; nodes.append((min(x, 900), y))
    body = (f'<path d="{d}" fill="none" stroke="{c}" stroke-opacity=".2" stroke-width="2" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.4" stroke-linejoin="round" stroke-dasharray="60 900" filter="url(#g)"><animate attributeName="stroke-dashoffset" values="60;-1500" dur="{3+i*.4:.1f}s" repeatCount="indefinite"/></path>')
    for k, (nx, ny) in enumerate(nodes[::2]):
        body += f'<circle cx="{nx}" cy="{ny}" r="3" fill="{c}"><animate attributeName="opacity" values=".2;1;.2" dur="{1.5+k%3*.5}s" begin="-{k*.3:.1f}s" repeatCount="indefinite"/></circle>'
    save(f'circuit{i}', svg(900, 40, body, GLOW), 'strips', '100%')

# 6 grid scan (6)
for i in range(6):
    c = PAL[i]; body = ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="24" stroke="{c}" stroke-opacity=".12"/>' for x in range(0, 901, 30))
    body += f'<line x1="0" y1="12" x2="900" y2="12" stroke="{c}" stroke-opacity=".12"/>'
    body += (f'<rect y="0" width="70" height="24" fill="{c}" opacity=".35"><animate attributeName="x" values="-70;900" dur="{2.5+i*.5}s" repeatCount="indefinite"/></rect>'
             f'<rect y="0" width="2" height="24" fill="{c}"><animate attributeName="x" values="-2;968" dur="{2.5+i*.5}s" repeatCount="indefinite"/></rect>')
    save(f'grid{i}', svg(900, 24, body), 'strips', '100%')

# 7 glitch strips (8)
for i in range(8):
    r = random.Random(200 + i); body = ''
    for k in range(16):
        x = r.randint(0, 800); w = r.randint(20, 140); y = r.randint(0, 12); h = r.randint(2, 5); c = r.choice(PAL)
        t = sorted(r.sample(range(1, 99), 3)); kt = ';'.join(['0'] + [f'{v/100:g}' for v in t] + ['1'])
        body += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}" opacity="0"><animate attributeName="opacity" calcMode="discrete" values="0;1;0;1;0" keyTimes="{kt}" dur="{r.uniform(1,3):.1f}s" begin="-{r.uniform(0,3):.1f}s" repeatCount="indefinite"/></rect>')
    save(f'glitch{i}', svg(900, 16, body), 'strips', '100%')

# 8 knight rider (7)
for i in range(7):
    c = PAL[i]
    body = (f'<rect width="400" height="2" y="4" fill="{c}" fill-opacity=".15"/>'
            f'<rect y="1" width="90" height="8" rx="4" fill="{c}" filter="url(#g)"><animate attributeName="x" values="0;310;0" keyTimes="0;.5;1" calcMode="spline" keySplines=".5 0 .5 1;.5 0 .5 1" dur="{1.6+i*.2:.1f}s" repeatCount="indefinite"/></rect>')
    save(f'rider{i}', svg(400, 10, body, GLOW), 'strips', '50%')

# 9 binary streams (5)
for i in range(5):
    r = random.Random(300 + i); t = ''.join(r.choice('01') for _ in range(150)); L = 1800
    d = f'<linearGradient id="m" x1="0" x2="1"><stop offset="0" stop-color="{PAL[i]}" stop-opacity="0"/><stop offset=".5" stop-color="{PAL[i]}"/><stop offset="1" stop-color="{PAL[i]}" stop-opacity="0"/></linearGradient><mask id="k"><rect width="900" height="30" fill="url(#m)"/></mask>'
    body = (f'<g mask="url(#k)" font-family="{MONO}" font-size="16" fill="{PAL[i]}"><g><text y="21" textLength="{L}" lengthAdjust="spacing" xml:space="preserve">{t}</text>'
            f'<animateTransform attributeName="transform" type="translate" values="{0 if i%2 else -L+900},0;{-L+900 if i%2 else 0},0" dur="{14+i*3}s" repeatCount="indefinite"/></g></g>')
    save(f'binary{i}', svg(900, 30, body, d), 'strips', '100%')

# ---------------- smalls ----------------
def poly(n, r, rotd=0):
    return ' '.join(f'{r*math.cos(2*math.pi*k/n+rotd):.1f},{r*math.sin(2*math.pi*k/n+rotd):.1f}' for k in range(n))

# spinners (12)
for i in range(12):
    c, c2 = PAL[i % 8], PAL[(i + 3) % 8]; t = i % 6
    if t == 0:
        b = f'<circle cx="32" cy="32" r="22" fill="none" stroke="{c}" stroke-opacity=".2" stroke-width="4"/><circle cx="32" cy="32" r="22" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-dasharray="40 100"><animateTransform attributeName="transform" type="rotate" values="0 32 32;360 32 32" dur="{.9+i*.05:.2f}s" repeatCount="indefinite"/></circle>'
    elif t == 1:
        b = f'<circle cx="32" cy="32" r="24" fill="none" stroke="{c}" stroke-width="3" stroke-dasharray="30 120" stroke-linecap="round"><animateTransform attributeName="transform" type="rotate" values="0 32 32;360 32 32" dur="1.4s" repeatCount="indefinite"/></circle><circle cx="32" cy="32" r="16" fill="none" stroke="{c2}" stroke-width="3" stroke-dasharray="20 80" stroke-linecap="round"><animateTransform attributeName="transform" type="rotate" values="360 32 32;0 32 32" dur="1s" repeatCount="indefinite"/></circle>'
    elif t == 2:
        b = ''.join(f'<circle cx="{32+22*math.cos(2*math.pi*k/8):.1f}" cy="{32+22*math.sin(2*math.pi*k/8):.1f}" r="4" fill="{c}"><animate attributeName="opacity" values="1;.1;1" dur="1.2s" begin="{k*.15:.2f}s" repeatCount="indefinite"/></circle>' for k in range(8))
    elif t == 3:
        b = f'<circle cx="32" cy="32" r="6" fill="{c}"/><circle cx="32" cy="32" r="8" fill="none" stroke="{c}" stroke-width="2"><animate attributeName="r" values="6;28" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="1.6s" repeatCount="indefinite"/></circle><circle cx="32" cy="32" r="8" fill="none" stroke="{c2}" stroke-width="2"><animate attributeName="r" values="6;28" dur="1.6s" begin=".8s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="1.6s" begin=".8s" repeatCount="indefinite"/></circle>'
    elif t == 4:
        b = ''.join(f'<rect x="{10+k*10}" width="6" rx="2" fill="{c if k%2 else c2}"><animate attributeName="height" values="8;40;8" dur="1s" begin="{k*.12:.2f}s" repeatCount="indefinite"/><animate attributeName="y" values="28;12;28" dur="1s" begin="{k*.12:.2f}s" repeatCount="indefinite"/></rect>' for k in range(5))
    else:
        b = f'<circle cx="32" cy="32" r="22" fill="none" stroke="{c}" stroke-opacity=".25" stroke-dasharray="3 5"/><g><circle cx="32" cy="10" r="5" fill="{c}"/><circle cx="32" cy="54" r="3.5" fill="{c2}"/><animateTransform attributeName="transform" type="rotate" values="0 32 32;360 32 32" dur="{2+i*.1:.1f}s" repeatCount="indefinite"/></g>'
    save(f'spin{i}', svg(64, 64, b), 'smalls', 56)

# hexagons (8)
for i in range(8):
    c = PAL[i]; b = ''
    for k in range(4):
        b += (f'<polygon points="{poly(6, 14+k*10)}" transform="translate(48 48)" fill="none" stroke="{c}" stroke-width="2" stroke-opacity="{.9-k*.18:.2f}">'
              f'<animateTransform attributeName="transform" type="rotate" additive="sum" values="0;{360 if k%2 else -360}" dur="{6+k*2+i*.3:.1f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="stroke-opacity" values=".15;1;.15" dur="2.4s" begin="{k*.3}s" repeatCount="indefinite"/></polygon>')
    save(f'hex{i}', svg(96, 96, b), 'smalls', 64)

# radar pings (8)
for i in range(8):
    c = PAL[i]; b = f'<circle cx="48" cy="48" r="4" fill="{c}"/>'
    for k in range(3):
        b += f'<circle cx="48" cy="48" r="6" fill="none" stroke="{c}" stroke-width="2"><animate attributeName="r" values="6;44" dur="2.4s" begin="{k*.8}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".9;0" dur="2.4s" begin="{k*.8}s" repeatCount="indefinite"/></circle>'
    save(f'ping{i}', svg(96, 96, b), 'smalls', 56)

# loading dots (8)
for i in range(8):
    c = PAL[i]; n = 3 + i % 3
    b = ''.join(f'<circle cx="{12+k*(96-24)/(n-1):.1f}" cy="14" r="5" fill="{c}"><animate attributeName="cy" values="14;5;14" dur=".9s" begin="{k*.12:.2f}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".4;1;.4" dur=".9s" begin="{k*.12:.2f}s" repeatCount="indefinite"/></circle>' for k in range(n))
    save(f'dots{i}', svg(96, 24, b), 'smalls', 64)

# nested polygons (10)
for i in range(10):
    sides = [3, 4, 5, 6, 8][i % 5]; c, c2 = PAL[i % 8], PAL[(i + 4) % 8]; b = ''
    for k in range(3):
        rr = 30 - k * 8
        b += (f'<polygon points="{poly(sides, rr)}" transform="translate(40 40)" fill="{c if k%2==0 else "none"}" fill-opacity=".12" stroke="{c if k%2==0 else c2}" stroke-width="2">'
              f'<animateTransform attributeName="transform" type="rotate" additive="sum" values="0;{360 if k%2==0 else -360}" dur="{4+k*2+i*.2:.1f}s" repeatCount="indefinite"/></polygon>')
    save(f'poly{i}', svg(80, 80, b), 'smalls', 56)

# diamonds / pulsing shapes (6)
for i in range(6):
    c = PAL[i + 1]
    b = (f'<rect x="20" y="20" width="24" height="24" fill="none" stroke="{c}" stroke-width="3" transform="rotate(45 32 32)"><animate attributeName="x" values="20;12;20" dur="1.8s" repeatCount="indefinite"/><animate attributeName="y" values="20;12;20" dur="1.8s" repeatCount="indefinite"/><animate attributeName="width" values="24;40;24" dur="1.8s" repeatCount="indefinite"/><animate attributeName="height" values="24;40;24" dur="1.8s" repeatCount="indefinite"/>'
         f'<animateTransform attributeName="transform" type="rotate" values="45 32 32;405 32 32" dur="{5+i}s" repeatCount="indefinite"/></rect>'
         f'<circle cx="32" cy="32" r="4" fill="{c}"><animate attributeName="r" values="3;7;3" dur="1.8s" repeatCount="indefinite"/></circle>')
    save(f'diamond{i}', svg(64, 64, b), 'smalls', 52)

json.dump(meta, open('/home/claude/anim_meta.json', 'w'))
print(len(meta['strips']), 'strips', len(meta['smalls']), 'smalls', len(meta['strips']) + len(meta['smalls']), 'total')
print(sum(os.path.getsize(f'{OUT}/{f}') for f in os.listdir(OUT)) // 1024, 'KB')
