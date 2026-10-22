import math, os, random
from xml.sax.saxutils import escape

OUT = '/mnt/user-data/outputs/readme-pack'
A = f'{OUT}/assets'
os.makedirs(A, exist_ok=True)
random.seed(7)
MONO = "Consolas, Menlo, 'Courier New', monospace"


def save(name, svg):
    with open(f'{A}/{name}', 'w', encoding='utf-8') as f:
        f.write(svg)


def fmt(v):
    return ';'.join(f'{x:g}' if isinstance(x, (int, float)) else str(x) for x in v)


# ---------- typing (one line at a time, looping) ----------
def typing(name, lines, w, h, size=21, color='#b98cf0', per=4.0):
    n = len(lines)
    T = per * n
    defs, body = [], []
    for i, t in enumerate(lines):
        W = round(len(t) * size * 0.6)
        s, e = i / n, (i + 1) / n
        kt = [0, s, s + 0.35 / n, e - 0.06 / n, e, 1]
        kt = [round(k, 4) for k in kt]
        defs.append(
            f'<clipPath id="c{i}"><rect x="10" y="0" width="0" height="{h}"><animate attributeName="width" '
            f'values="{fmt([0, 0, W, W, 0, 0])}" keyTimes="{fmt(kt)}" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>')
        body.append(
            f'<g clip-path="url(#c{i})"><text x="10" y="{h*0.64:g}" textLength="{W}" lengthAdjust="spacingAndGlyphs">{escape(t)}</text></g>'
            f'<rect y="{h*0.64-size*0.9:g}" width="3" height="{size*1.1:g}" fill="#e0c3ff"><animate attributeName="x" '
            f'values="{fmt([10, 10, 10 + W, 10 + W, 10, 10])}" keyTimes="{fmt(kt)}" dur="{T}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="1;0;1;0;1" dur="0.8s" repeatCount="indefinite"/></rect>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<defs>{"".join(defs)}</defs><g font-family="{MONO}" font-size="{size}" fill="{color}" font-weight="600">{"".join(body)}</g></svg>')
    save(name, svg)


typing('typing.svg', ['52 public repos. Zero chill.', 'Kernels, agents, languages, panels.',
                      'We ship first, document later.', "Sri Lanka's most chaotic build log."], 720, 90, 21, per=4.0)
typing('typing-stack.svg', ["if it has a compiler, we've probably tried it", 'polyglot by accident, not by plan'], 720, 70, 18, '#f0c869', per=5.5)
typing('typing-eso.svg', ['Malbolge took us longer to read than write in', 'yes, we know most Malbolge programs are found, not written',
                          'we still count it'], 720, 70, 17, '#c39bf5', per=4.7)


# ---------- terminal ----------
def terminal(name, title, lines, w, h, color='#7CFC8A', per=2.6):
    n = len(lines)
    T = per * n + 3
    ty = 0.9
    defs, body = [], []
    for i, t in enumerate(lines):
        W = round(len(t) * 18 * 0.6)
        s = (i * per) / T
        d = (per * 0.7) / T
        e = (n * per + 2.2) / T
        kt = fmt([0, round(s, 4), round(s + d, 4), round(e, 4), 1])
        y = 62 + i * 34
        defs.append(f'<clipPath id="t{i}"><rect x="24" y="0" width="0" height="{h}"><animate attributeName="width" '
                    f'values="{fmt([0, 0, W, W, 0])}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>')
        body.append(f'<g clip-path="url(#t{i})"><text x="24" y="{y}" textLength="{W}" lengthAdjust="spacingAndGlyphs">{escape(t)}</text></g>')
        kc = fmt([0, round(s, 4), round(s, 4), round(s + d, 4), round(s + d + 0.001, 4), 1])
        body.append(
            f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kc}" dur="{T}s" repeatCount="indefinite"/>'
            f'<rect y="{y-16}" width="3" height="20" fill="{color}"><animate attributeName="x" values="{fmt([24, 24, 24 + W, 24 + W])}" '
            f'keyTimes="{fmt([0, round(s, 4), round(s + d, 4), 1])}" dur="{T}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="1;0;1" dur="0.7s" repeatCount="indefinite"/></rect></g>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1a1a"/><stop offset="1" stop-color="#0a0a0a"/></linearGradient>'
           f'<clipPath id="win"><rect width="{w}" height="{h}" rx="12"/></clipPath>{"".join(defs)}</defs>'
           f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="url(#bg)" stroke="#DC2626" stroke-opacity=".4"/>'
           f'<g clip-path="url(#win)"><rect width="{w}" height="18" fill="#000"/>'
           f'<circle cx="18" cy="9" r="5" fill="#ff5f56"/><circle cx="36" cy="9" r="5" fill="#ffbd2e"/><circle cx="54" cy="9" r="5" fill="#27c93f"/>'
           f'<text x="{w/2}" y="13" text-anchor="middle" font-family="{MONO}" font-size="10" fill="#666">{escape(title)}</text>'
           f'<g font-family="{MONO}" font-size="18" fill="{color}">{"".join(body)}</g>'
           f'<rect x="0" y="-20" width="{w}" height="20" fill="#DC2626" opacity=".06"><animate attributeName="y" values="-20;{h}" dur="4s" repeatCount="indefinite"/></rect></g></svg>')
    save(name, svg)


terminal('terminal.svg', 'legion@sh:~', ['$ git commit -m "it works on my machine"', '$ git push --force (sorry not sorry)',
                                          '$ TODO: write tests', '$ make kernel && qemu-system-x86_64 -kernel legion.bin'], 680, 190)
terminal('terminal-footer.svg', 'deathlegionteamlk - zsh', ['$ echo "thanks for scrolling this far"', '$ git star deathlegionteamlk',
                                                           '$ echo "Death Legion out"'], 620, 160, '#e0c3ff', 2.8)


# ---------- dividers ----------
def divider(name, w=900):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="14" viewBox="0 0 {w} 14"><defs>'
           '<linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="#0f0c29"/><stop offset=".5" stop-color="#8A2BE2" stop-opacity=".6"/><stop offset="1" stop-color="#0f0c29"/></linearGradient>'
           '<radialGradient id="p"><stop offset="0" stop-color="#fff"/><stop offset=".4" stop-color="#DC2626" stop-opacity=".85"/><stop offset="1" stop-color="#DC2626" stop-opacity="0"/></radialGradient></defs>'
           f'<rect y="6" width="{w}" height="2" fill="url(#l)"/>'
           f'<circle cy="7" r="7" fill="url(#p)"><animate attributeName="cx" values="-20;{w+20}" dur="3.2s" repeatCount="indefinite"/></circle>'
           f'<circle cy="7" r="4" fill="url(#p)"><animate attributeName="cx" values="{w+20};-20" dur="4.6s" repeatCount="indefinite"/></circle>'
           f'<circle cy="7" r="3" fill="url(#p)"><animate attributeName="cx" values="-20;{w+20}" dur="6.1s" begin="-2s" repeatCount="indefinite"/></circle></svg>')
    save(name, svg)


divider('divider.svg')


def ekg(name, w=900, color='#DC2626'):
    pts = []
    x = 0
    d = f'M0 30 '
    seg = w / 6
    for k in range(6):
        b = k * seg
        d += (f'L{b+seg*0.25:g} 30 L{b+seg*0.32:g} 22 L{b+seg*0.38:g} 38 L{b+seg*0.45:g} 4 '
              f'L{b+seg*0.52:g} 54 L{b+seg*0.60:g} 30 L{b+seg*0.7:g} 26 L{b+seg*0.78:g} 30 L{b+seg:g} 30 ')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="60" viewBox="0 0 {w} 60"><defs>'
           '<filter id="g"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
           f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity=".12" stroke-width="2"/>'
           f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" filter="url(#g)" stroke-dasharray="260 {w*3}">'
           f'<animate attributeName="stroke-dashoffset" values="260;-{w*2.4:g}" dur="3.4s" repeatCount="indefinite"/></path></svg>')
    save(name, svg)


ekg('ekg.svg')
ekg('ekg-gold.svg', color='#FBBF24')


# ---------- ticker ----------
def ticker(name, words, w=900):
    t = '  \u2022  '.join(words) + '  \u2022  '
    L = round(len(t) * 16 * 0.6)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="42" viewBox="0 0 {w} 42"><defs>'
           '<linearGradient id="m" x1="0" x2="1"><stop offset="0" stop-color="#09090B"/><stop offset=".5" stop-color="#151022"/><stop offset="1" stop-color="#09090B"/></linearGradient>'
           f'<clipPath id="c"><rect width="{w}" height="42" rx="8"/></clipPath></defs>'
           f'<rect width="{w}" height="42" rx="8" fill="url(#m)" stroke="#DC2626" stroke-opacity=".25"/><g clip-path="url(#c)">'
           f'<g font-family="{MONO}" font-size="16" fill="#f0a1a1" font-weight="600">'
           f'<g><text x="0" y="27" textLength="{L}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{escape(t)}</text><animateTransform attributeName="transform" type="translate" values="0,0;-{L},0" dur="22s" repeatCount="indefinite"/></g>'
           f'<g><text x="{L}" y="27" textLength="{L}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{escape(t)}</text><animateTransform attributeName="transform" type="translate" values="0,0;-{L},0" dur="22s" repeatCount="indefinite"/></g>'
           '</g></g></svg>')
    save(name, svg)


ticker('ticker.svg', ['PYTHON', 'RUST', 'GO', 'KOTLIN', 'BRAINFUCK', 'IDRIS', 'MALBOLGE', 'TYPESCRIPT', 'C++', 'ERLANG', 'ZIG', 'OCAML', 'CRYSTAL'])


# ---------- matrix hero with glitch title ----------
def hero(name, w=900, h=200):
    cols = []
    chars = '01ABCDEF<>{}/\\$#'
    for i in range(0, w, 14):
        dur = random.uniform(3.5, 7)
        begin = -random.uniform(0, 7)
        n = random.randint(7, 13)
        tsp = ''
        for k in range(n):
            op = 0.08 + 0.9 * (k / n) ** 2
            tsp += f'<tspan x="{i}" dy="14" fill-opacity="{op:.2f}">{escape(random.choice(chars))}</tspan>'
        cols.append(f'<g><text font-size="13" fill="#9b5cf0">{tsp}</text>'
                    f'<animateTransform attributeName="transform" type="translate" values="0,-{n*14};0,{h+10}" dur="{dur:.1f}s" begin="{begin:.1f}s" repeatCount="indefinite"/></g>')
    title = 'DEATH LEGION'
    glitch = lambda col, dx, dur: (f'<text x="{w/2}" y="{h/2+22}" text-anchor="middle" font-size="64" font-weight="800" fill="{col}" '
                                    f'textLength="560" lengthAdjust="spacingAndGlyphs" opacity=".75"><animateTransform attributeName="transform" type="translate" '
                                    f'values="0,0;{dx},1;{-dx},-1;0,0;{dx*2},0;0,0;0,0;0,0" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/>{title}</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>'
           f'<clipPath id="r"><rect width="{w}" height="{h}" rx="14"/></clipPath>'
           '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f0c29"/><stop offset=".5" stop-color="#1b1442"/><stop offset="1" stop-color="#0a0810"/></linearGradient>'
           '<filter id="gl"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
           f'<rect width="{w}" height="{h}" rx="14" fill="url(#bg)"/><g clip-path="url(#r)" font-family="{MONO}">{"".join(cols)}'
           f'<g font-family="{MONO}">{glitch("#DC2626", 4, 2.4)}{glitch("#22d3ee", -4, 2.9)}'
           f'<text x="{w/2}" y="{h/2+22}" text-anchor="middle" font-size="64" font-weight="800" fill="#fff" textLength="560" lengthAdjust="spacingAndGlyphs" filter="url(#gl)">{title}</text></g>'
           f'<rect width="{w}" height="3" fill="#fff" opacity=".08"><animate attributeName="y" values="0;{h}" dur="3.5s" repeatCount="indefinite"/></rect></g>'
           f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="none" stroke="#8A2BE2" stroke-opacity=".5"><animate attributeName="stroke-opacity" values=".2;.8;.2" dur="3s" repeatCount="indefinite"/></rect></svg>')
    save(name, svg)


hero('hero.svg')


# ---------- counters ----------
def counters(name):
    w, h = 760, 130
    items = [('52', 52, 'PUBLIC REPOS'), ('4', 4, 'KERNELS'), ('25+', 25, 'LANGUAGES TOUCHED'), ('\u221e', None, 'UNFINISHED BRANCHES')]
    out = []
    cw = w / 4
    for idx, (label, target, cap) in enumerate(items):
        cx = cw * idx + cw / 2
        if target is None:
            out.append(f'<text x="{cx}" y="68" text-anchor="middle" font-size="46" font-weight="800" fill="#fbbf24">{label}'
                       f'<animate attributeName="opacity" values="1;.35;1" dur="2.2s" repeatCount="indefinite"/></text>')
        else:
            step = 2.4 / (target + 1)
            T = 8
            for v in range(target + 1):
                a = v * step / T
                b = (v + 1) * step / T if v < target else 1
                suffix = '+' if label.endswith('+') else ''
                kt = fmt([0, round(a, 5), round(b, 5), 1]) if v < target else fmt([0, round(a, 5), 1])
                vals = '0;1;0;0' if v < target else '0;1;1'
                out.append(f'<text x="{cx}" y="68" text-anchor="middle" font-size="46" font-weight="800" fill="#f0a1a1" opacity="0">{v}{suffix}'
                           f'<animate attributeName="opacity" calcMode="discrete" values="{vals}" keyTimes="{kt}" dur="{T}s" repeatCount="indefinite"/></text>')
        out.append(f'<text x="{cx}" y="98" text-anchor="middle" font-size="11" fill="#9b8ac4" letter-spacing="2">{cap}</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="#0b0914" stroke="#8A2BE2" stroke-opacity=".4"/>'
           f'<g font-family="{MONO}">{"".join(out)}</g></svg>')
    save(name, svg)




# ---------- orbit ----------
def orbit(name):
    w, h = 680, 380
    cx, cy = w / 2, h / 2
    rings = [(270, 70, -18, 14, [('AI AGENTS', '#DC2626', 0), ('KERNELS', '#FBBF24', .5)]),
             (200, 125, 28, 19, [('ANDROID', '#3DDC84', 0), ('PANELS', '#2496ED', .33), ('WEB', '#9b5cf0', .66)]),
             (120, 120, 0, 11, [('RUST', '#dea584', 0), ('C++', '#659ad2', .25), ('PY', '#ffd43b', .5), ('KT', '#b98cf0', .75)])]
    parts = []
    for rx, ry, rot, dur, planets in rings:
        d = f'M{cx-rx:g},{cy:g} a{rx},{ry} 0 1,0 {2*rx},0 a{rx},{ry} 0 1,0 {-2*rx},0'
        parts.append(f'<g transform="rotate({rot} {cx:g} {cy:g})"><path d="{d}" fill="none" stroke="#8A2BE2" stroke-opacity=".35" stroke-dasharray="4 6"/>')
        for lab, col, frac in planets:
            r = 7 if len(lab) < 4 else 6
            parts.append(f'<g><animateMotion dur="{dur*3}s" begin="-{frac*dur*3:.2f}s" repeatCount="indefinite" path="{d}"/>'
                         f'<circle r="{r+6}" fill="{col}" opacity=".18"><animate attributeName="r" values="{r+3};{r+9};{r+3}" dur="2.4s" repeatCount="indefinite"/></circle>'
                         f'<circle r="{r}" fill="{col}"/></g>')
        parts.append('</g>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>'
           '<radialGradient id="c"><stop offset="0" stop-color="#fff"/><stop offset=".35" stop-color="#8A2BE2"/><stop offset="1" stop-color="#8A2BE2" stop-opacity="0"/></radialGradient></defs>'
           f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="#0b0914" stroke="#8A2BE2" stroke-opacity=".35"/>'
           f'<g font-family="{MONO}">{"".join(parts)}'
           f'<circle cx="{cx}" cy="{cy}" r="34" fill="url(#c)"><animate attributeName="r" values="30;40;30" dur="3s" repeatCount="indefinite"/></circle>'
           f'</g></svg>')
    save(name, svg)


orbit('orbit.svg')


# ---------- 3D wireframes (true projected rotation, SMIL path morph) ----------
def rot(p, th, ph, th2=0.0):
    x, y, z = p
    c, s = math.cos(th), math.sin(th)
    x, z = x * c + z * s, -x * s + z * c
    if th2:
        c2, s2 = math.cos(th2), math.sin(th2)
        y, z = y * c2 - z * s2, y * s2 + z * c2
    c, s = math.cos(ph), math.sin(ph)
    y, z = y * c - z * s, y * s + z * c
    return x, y, z


def proj(p, scale, cx, cy, d=5.0):
    s = d / (d + p[2])
    return cx + p[0] * scale * s, cy + p[1] * scale * s


def model3d(name, segs, frames, scale, tilt, label='', dur=14, double=False, marker=None, W=300, H=300, pre=None, spin=1.0):
    cx, cy = W / 2, H / 2
    back_vals, front_vals, mk = [], [], ([], [], [])
    for f in range(frames + 1):
        th = 2 * math.pi * f / frames
        th2 = th if double else 0.0
        back, front = [], []
        for a, b in segs:
            if pre:
                a, b = pre(a, th), pre(b, th)
            ra, rb = rot(a, th * spin, tilt, th2), rot(b, th * spin, tilt, th2)
            pa, pb = proj(ra, scale, cx, cy), proj(rb, scale, cx, cy)
            seg = f'M{pa[0]:.1f} {pa[1]:.1f}L{pb[0]:.1f} {pb[1]:.1f}'
            back.append(seg)
            if (ra[2] + rb[2]) / 2 < 0:
                front.append(seg)
            else:
                front.append(f'M{pa[0]:.1f} {pa[1]:.1f}L{pa[0]:.1f} {pa[1]:.1f}')
        back_vals.append(''.join(back))
        front_vals.append(''.join(front))
        if marker:
            rm = rot(marker, th * spin, tilt, th2)
            px, py = proj(rm, scale, cx, cy)
            mk[0].append(f'{px:.1f}')
            mk[1].append(f'{py:.1f}')
            mk[2].append('1' if rm[2] < 0 else '0')
    anim = lambda attr, vals, extra='': f'<animate attributeName="{attr}" values="{";".join(vals)}" dur="{dur}s" repeatCount="indefinite" {extra}/>'
    m = ''
    if marker:
        m = (f'<g><circle r="4" fill="#fbbf24">{anim("cx", mk[0])}{anim("cy", mk[1])}{anim("opacity", mk[2], "calcMode=\"discrete\"")}</circle>'
             f'<circle r="8" fill="none" stroke="#fbbf24">{anim("cx", mk[0])}{anim("cy", mk[1])}{anim("opacity", mk[2], "calcMode=\"discrete\"")}'
             f'<animate attributeName="r" values="4;14;4" dur="2s" repeatCount="indefinite"/></circle></g>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>'
           '<filter id="g" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
           '<radialGradient id="bgg" cx=".5" cy=".5" r=".7"><stop offset="0" stop-color="#1b1442"/><stop offset="1" stop-color="#0b0914"/></radialGradient></defs>'
           f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16" fill="url(#bgg)" stroke="#8A2BE2" stroke-opacity=".4"/>'
           f'<ellipse cx="{cx}" cy="{H-40}" rx="90" ry="12" fill="#8A2BE2" opacity=".18"><animate attributeName="rx" values="80;100;80" dur="{dur/3:g}s" repeatCount="indefinite"/></ellipse>'
           f'<path d="{back_vals[0]}" fill="none" stroke="#DC2626" stroke-opacity=".38" stroke-width="1.1" stroke-linecap="round">{anim("d", back_vals)}</path>'
           f'<path d="{front_vals[0]}" fill="none" stroke="#c9a2ff" stroke-width="1.8" stroke-linecap="round" filter="url(#g)">{anim("d", front_vals)}</path>'
           f'{m}</svg>')
    save(name, svg)


# icosahedron
phi = (1 + 5 ** .5) / 2
V = [(-1, phi, 0), (1, phi, 0), (-1, -phi, 0), (1, -phi, 0), (0, -1, phi), (0, 1, phi), (0, -1, -phi), (0, 1, -phi),
     (phi, 0, -1), (phi, 0, 1), (-phi, 0, -1), (-phi, 0, 1)]
V = [tuple(c / math.sqrt(1 + phi * phi) for c in v) for v in V]
edges = [(V[i], V[j]) for i in range(12) for j in range(i + 1, 12) if abs(math.dist(V[i], V[j]) - 2 / math.sqrt(1 + phi * phi)) < 1e-6]
model3d('3d-ico.svg', edges, 72, 105, 0.45, 'LEGION CORE', 14)


for f in sorted(os.listdir(A)):
    print(f, os.path.getsize(f'{A}/{f}') // 1024, 'KB')
