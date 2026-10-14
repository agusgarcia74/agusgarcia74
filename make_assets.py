"""Genera los SVG del perfil de GitHub (banner y ticket) en versión oscura y clara.
Uso: python make_assets.py  -> escribe en assets/
Los SVG usan solo fuentes del sistema (GitHub no deja cargar fuentes externas dentro de un <img>).
"""
import random
from pathlib import Path

OUT = Path(__file__).parent / 'assets'
OUT.mkdir(exist_ok=True)

THEMES = {
    'dark': dict(bg='#0b0c0a', ink='#efeee7', ink2='#a9aa9e', ink3='#6f7166', accent='#ff5a1f',
                 paper='#f4f1e8', paper_ink='#151511', planet='jupiter'),
    'light': dict(bg='#efebe1', ink='#151511', ink2='#4a4a42', ink3='#8a897e', accent='#e24a10',
                  paper='#fbfaf6', paper_ink='#151511', planet='moon'),
}

SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "Consolas, 'SFMono-Regular', Menlo, monospace"

DARK_BANDS = ['#151612', '#1d1e19', '#121310', '#24251f', '#181915', '#101110',
              '#212219', '#171814', '#2a2620', '#1a1b16', '#131411', '#22201b']
BAND_H = [10, 7, 6, 9, 7, 12, 8, 6, 7, 8, 10, 10]


def planet(t, cx, cy, r):
    """Júpiter "en negro" con bandas que giran, o la Luna en modo claro."""
    if t['planet'] == 'moon':
        craters = ''.join(
            f'<circle cx="{cx + dx * r}" cy="{cy + dy * r}" r="{rr * r}" fill="#d6d1c2"/>'
            for dx, dy, rr in [(-.3, -.35, .22), (.2, .2, .3), (.35, -.4, .12), (-.4, .4, .14), (.05, .6, .1)]
        )
        return f'''
  <clipPath id="pc"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
  <g clip-path="url(#pc)">
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="#e2ddcf"/>{craters}
    <circle cx="{cx + r * .55}" cy="{cy - r * .1}" r="{r * 1.05}" fill="{t['bg']}" opacity=".55"/>
  </g>'''
    rows, y = [], cy - r
    scale = 2 * r / sum(BAND_H)
    for c, h in zip(DARK_BANDS, BAND_H):
        rows.append(f'<rect x="{cx - r}" y="{y:.1f}" width="{4 * r}" height="{h * scale + .5:.1f}" fill="{c}"/>')
        y += h * scale
    spot_y = cy + r * .05
    return f'''
  <clipPath id="pc"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
  <g clip-path="url(#pc)">
    <g transform="rotate(-8 {cx} {cy})">
      <g class="bands">{''.join(rows)}
        <ellipse cx="{cx + r * .25}" cy="{spot_y}" rx="{r * .18}" ry="{r * .1}" fill="#3a2015"/>
        <ellipse cx="{cx + r * 2.25}" cy="{spot_y}" rx="{r * .18}" ry="{r * .1}" fill="#3a2015"/>
      </g>
    </g>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#shade)"/>
  </g>'''


def birds(t, n=16, seed=7):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, y = rnd.uniform(-80, 1180), rnd.uniform(30, 250)
        s = rnd.uniform(.6, 1.3)
        dur = rnd.uniform(14, 26)
        delay = -rnd.uniform(0, dur)
        flap = rnd.uniform(.35, .6)
        out.append(
            f'<g class="bird" style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s">'
            f'<g transform="translate({x:.0f} {y:.0f}) scale({s:.2f})">'
            f'<path class="wing" style="animation-duration:{flap:.2f}s" d="M-8 -4 Q-3 -1 0 2 Q3 -1 8 -4" '
            f'fill="none" stroke="{t["ink"]}" stroke-width="1.6" stroke-linecap="round" opacity=".7"/></g></g>'
        )
    return ''.join(out)


def header(name, t):
    roles = ['Full Stack Developer', 'Systems Engineering + AI @ UTN', 'From the database to the printer']
    role_txt = ''.join(
        f'<text class="role r{i}" x="64" y="236" font-family="{SANS}" font-size="22" font-weight="600" fill="{t["accent"]}">{r}</text>'
        for i, r in enumerate(roles)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="1200" height="300" role="img" aria-label="Juan Agustín García — Full Stack Developer">
  <style>
    .bands {{ animation: spin 40s linear infinite; }}
    @keyframes spin {{ to {{ transform: translateX(-{2 * 230}px); }} }}
    .bird {{ animation: fly linear infinite; }}
    @keyframes fly {{ from {{ transform: translateX(-260px); }} to {{ transform: translateX(260px); }} }}
    .wing {{ animation: flap ease-in-out infinite alternate; transform-box: fill-box; transform-origin: center; }}
    @keyframes flap {{ to {{ transform: scaleY(-.6); }} }}
    .role {{ opacity: 0; animation: roles 9s infinite; }}
    .r1 {{ animation-delay: 3s; }} .r2 {{ animation-delay: 6s; }}
    @keyframes roles {{ 0% {{ opacity: 0; transform: translateY(8px); }} 5%, 30% {{ opacity: 1; transform: none; }} 35%, 100% {{ opacity: 0; }} }}
    .dot {{ animation: pulse 1.8s ease-out infinite; transform-box: fill-box; transform-origin: center; }}
    @keyframes pulse {{ from {{ transform: scale(1); opacity: .7; }} to {{ transform: scale(3); opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} .r0 {{ opacity: 1; }} }}
  </style>
  <defs>
    <radialGradient id="shade" cx="30%" cy="30%" r="80%">
      <stop offset="0" stop-color="#fff" stop-opacity=".06"/><stop offset=".6" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity=".6"/>
    </radialGradient>
    <clipPath id="frame"><rect width="1200" height="300" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="1200" height="300" fill="{t['bg']}"/>
    {planet(t, 1010, 190, 230)}
    {birds(t)}
    <text x="64" y="104" font-family="{SANS}" font-size="38" font-weight="600" fill="{t['ink']}" letter-spacing="-1">Juan Agustín</text>
    <text x="58" y="196" font-family="{SANS}" font-size="104" font-weight="800" fill="{t['ink']}" letter-spacing="-5">García</text>
    {role_txt}
    <g transform="translate(64 268)">
      <circle r="4" fill="#61d67a"/><circle class="dot" r="4" fill="#61d67a"/>
      <text x="14" y="5" font-family="{SANS}" font-size="15" fill="{t['ink2']}">Open to projects · Córdoba, Argentina</text>
    </g>
  </g>
</svg>'''
    (OUT / name).write_text(svg, encoding='utf-8')


def ticket(name, t):
    rows = [('Role', 'Full Stack Dev'), ('Based in', 'Córdoba, AR'), ('Degrees', 'Systems + AI'),
            ('English', 'B2'), ('Portuguese', 'Advanced'), ('Currently', 'UTN Manager'),
            ('Building', 'UTN Hub · Gavia'), ('Available', 'Now')]
    W = 360
    y0 = 92
    body = []
    for i, (k, v) in enumerate(rows):
        y = y0 + i * 24
        body.append(
            f'<text x="24" y="{y}" class="m k">{k}</text>'
            f'<text x="{W - 24}" y="{y}" class="m v" text-anchor="end">{v}</text>'
            f'<line x1="{24 + len(k) * 8 + 6}" x2="{W - 30 - len(v) * 8.2}" y1="{y - 4}" y2="{y - 4}" class="dots"/>'
        )
    y_total = y0 + len(rows) * 24 + 10
    bars = ''.join(
        f'<rect x="{24 + i * 5.4:.1f}" y="{y_total + 34}" width="{(i * 7 % 4) * .9 + 1:.1f}" height="38" fill="{t["paper_ink"]}"/>'
        for i in range(58)
    )
    H = y_total + 110
    teeth_top = ''.join(f'<circle cx="{6 + i * 12}" cy="0" r="6" fill="{t["bg"]}"/>' for i in range(31))
    teeth_bot = ''.join(f'<circle cx="{6 + i * 12}" cy="{H}" r="6" fill="{t["bg"]}"/>' for i in range(31))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -20 {W + 40} {H + 40}" width="{W + 40}" height="{H + 40}" role="img" aria-label="About Juan: Full Stack Developer from Córdoba, studying Systems Engineering and AI at UTN">
  <style>
    .m {{ font-family: {MONO}; font-size: 13px; fill: {t['paper_ink']}; }}
    .v {{ font-weight: 700; }}
    .dots {{ stroke: {t['paper_ink']}; stroke-dasharray: 1 4; opacity: .35; }}
    .sway {{ animation: sway 6s ease-in-out infinite; transform-origin: 50% 0; transform-box: fill-box; }}
    @keyframes sway {{ 0%, 100% {{ transform: rotate(-1.5deg) translateY(0); }} 50% {{ transform: rotate(.8deg) translateY(-4px); }} }}
    @media (prefers-reduced-motion: reduce) {{ .sway {{ animation: none; }} }}
  </style>
  <rect x="-20" y="-20" width="{W + 40}" height="{H + 40}" fill="{t['bg']}" rx="14"/>
  <g class="sway">
    <rect width="{W}" height="{H}" fill="{t['paper']}"/>
    {teeth_top}{teeth_bot}
    <text x="{W / 2}" y="34" class="m v" text-anchor="middle" font-size="15">JAG · RECEIPT #2005</text>
    <text x="{W / 2}" y="54" class="m" text-anchor="middle" opacity=".6">github.com/agusgarcia74</text>
    <line x1="24" x2="{W - 24}" y1="68" y2="68" stroke="{t['paper_ink']}" stroke-dasharray="4 4" opacity=".6"/>
    {''.join(body)}
    <line x1="24" x2="{W - 24}" y1="{y_total - 6}" y2="{y_total - 6}" stroke="{t['paper_ink']}" stroke-dasharray="4 4" opacity=".6"/>
    <text x="24" y="{y_total + 16}" class="m v" font-size="15">TOTAL</text>
    <text x="{W - 24}" y="{y_total + 16}" class="m v" text-anchor="end" font-size="15" fill="{t['accent']}">HIRE ME</text>
    {bars}
    <text x="{W / 2}" y="{y_total + 94}" class="m" text-anchor="middle" opacity=".6">thanks for stopping by</text>
  </g>
</svg>'''
    (OUT / name).write_text(svg, encoding='utf-8')


for mode, t in THEMES.items():
    header(f'header-{mode}.svg', t)
    ticket(f'ticket-{mode}.svg', t)
print('ok:', sorted(p.name for p in OUT.iterdir()))
