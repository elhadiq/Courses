#!/usr/bin/env python3
"""Add SVG figures to the single-page masters in _source/, and convert the
existing hardcoded SVG colours to CSS variables so diagrams work in light mode.

Idempotent: each figure carries an id, and is skipped if already present.
Run, then run split.py to regenerate the site.
"""
import re, os, sys

SRC = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- theming fix
COLOR = {
    '#e6edf3': 'var(--txt)',
    '#9fb0c0': 'var(--muted)',
    '#2dd4bf': 'var(--accent)',
    '#38bdf8': 'var(--accent2)',
    '#3b4b5c': 'var(--line)',
    '#fbbf24': 'var(--warn)',
}

F = 'font-family="ui-monospace,monospace"'

def fig(fid, viewbox, body, caption):
    return (f'\n<figure id="{fid}">\n'
            f'<svg viewBox="{viewbox}" xmlns="http://www.w3.org/2000/svg" {F} font-size="11">\n'
            f'{body}\n</svg>\n'
            f'<figcaption>{caption}</figcaption>\n</figure>\n')

def arrow(defid, color='var(--accent2)'):
    return (f'<defs><marker id="{defid}" markerWidth="8" markerHeight="8" refX="7" refY="4" '
            f'orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{color}"/></marker></defs>')

FIGURES = []   # (module_file, anchor_string, figure_html)

def add(mod, anchor, fid, vb, body, cap):
    FIGURES.append((mod, anchor, fid, fig(fid, vb, body, cap)))

# ============================================================ MODULE 1
add('module-1.html',
    '<p>Redirection sends streams to files instead:</p>',
    'fig-pipes', '0 0 720 170', f'''
  {arrow('ap1')}
  <text x="10" y="18" fill="var(--muted)" font-size="10">each stage reads the previous stage's stdout — the data shrinks as you narrow the question</text>
  <g stroke="var(--accent)" fill="none" stroke-width="1.3">
    <rect x="8"   y="40" width="104" height="42" rx="6"/>
    <rect x="150" y="40" width="104" height="42" rx="6"/>
    <rect x="292" y="40" width="104" height="42" rx="6"/>
    <rect x="434" y="40" width="104" height="42" rx="6"/>
    <rect x="576" y="40" width="136" height="42" rx="6"/>
  </g>
  <g fill="var(--txt)" text-anchor="middle" font-size="11">
    <text x="60"  y="60">access.log</text>
    <text x="202" y="60">awk '{{print $1}}'</text>
    <text x="344" y="60">sort</text>
    <text x="486" y="60">uniq -c</text>
    <text x="644" y="60">sort -rn | head -5</text>
  </g>
  <g fill="var(--muted)" text-anchor="middle" font-size="9">
    <text x="60"  y="74">40 000 lines</text>
    <text x="202" y="74">40 000 IPs</text>
    <text x="344" y="74">sorted</text>
    <text x="486" y="74">820 unique</text>
    <text x="644" y="74">5 rows</text>
  </g>
  <g stroke="var(--accent2)" stroke-width="1.4" marker-end="url(#ap1)">
    <line x1="114" y1="61" x2="146" y2="61"/><line x1="256" y1="61" x2="288" y2="61"/>
    <line x1="398" y1="61" x2="430" y2="61"/><line x1="540" y1="61" x2="572" y2="61"/>
  </g>
  <g fill="var(--accent2)" text-anchor="middle" font-size="12">
    <text x="130" y="57">|</text><text x="272" y="57">|</text>
    <text x="414" y="57">|</text><text x="556" y="57">|</text>
  </g>
  <g fill="var(--muted)" font-size="10">
    <text x="8" y="112">stdout ──▶ stdin of the next command. stderr (2&gt;) bypasses the pipe entirely,</text>
    <text x="8" y="128">which is why an error message still reaches your terminal mid-pipeline.</text>
    <text x="8" y="152" fill="var(--warn)">Read a pipeline right-to-left to recover the question it answers.</text>
  </g>''',
    'A pipeline is a series of filters, each narrowing the data.')

add('module-1.html',
    '<p>When both branches changed the same lines, Git stops and marks the file:</p>',
    'fig-branch', '0 0 720 200', f'''
  <g stroke="var(--line)" stroke-width="2" fill="none">
    <path d="M40 60 H660"/>
  </g>
  <g stroke="var(--accent2)" stroke-width="2" fill="none">
    <path d="M180 60 C210 60 210 130 240 130 H460 C500 130 490 62 540 60"/>
  </g>
  <g fill="var(--bg)" stroke="var(--accent)" stroke-width="2">
    <circle cx="60" cy="60" r="9"/><circle cx="180" cy="60" r="9"/>
    <circle cx="360" cy="60" r="9"/><circle cx="540" cy="60" r="11"/><circle cx="650" cy="60" r="9"/>
  </g>
  <g fill="var(--bg)" stroke="var(--accent2)" stroke-width="2">
    <circle cx="300" cy="130" r="9"/><circle cx="420" cy="130" r="9"/>
  </g>
  <text x="40" y="36" fill="var(--accent)" font-size="11">main</text>
  <text x="110" y="134" fill="var(--accent2)" font-size="11">feat/rate-limit</text>
  <g fill="var(--muted)" font-size="9" text-anchor="middle">
    <text x="60" y="84">C1</text><text x="180" y="84">C2</text><text x="360" y="84">C3</text>
    <text x="650" y="84">C6</text>
    <text x="300" y="152">C4</text><text x="420" y="152">C5</text>
  </g>
  <text x="540" y="40" fill="var(--txt)" font-size="10" text-anchor="middle">merge commit</text>
  <text x="40" y="188" fill="var(--muted)" font-size="10">Branch at C2, work at C4–C5, merge at C6. Main moved too (C3) — that overlap is where conflicts come from.</text>''',
    'A branch is a pointer. Merging reconciles two lines of history.')

# ============================================================ MODULE 2
add('module-2.html',
    '<p>Two addresses in every subnet are reserved:',
    'fig-cidr', '0 0 720 190', f'''
  <text x="8" y="16" fill="var(--muted)" font-size="10">192.168.1.34/24 — the /24 says: the first 24 bits identify the NETWORK, the rest identify the HOST</text>
  <g stroke="var(--line)" stroke-width="1">
    {''.join(f'<rect x="{8+i*21.5}" y="30" width="20" height="26" fill="{"color-mix(in srgb,var(--accent) 30%,transparent)" if i<24 else "color-mix(in srgb,var(--accent2) 30%,transparent)"}"/>' for i in range(32))}
  </g>
  <g fill="var(--txt)" font-size="9" text-anchor="middle">
    {''.join(f'<text x="{18+i*21.5}" y="47">{b}</text>' for i,b in enumerate("11000000101010000000000100100010"))}
  </g>
  <g stroke="var(--accent)" stroke-width="1.5" fill="none"><path d="M8 64 V72 H524 V64"/></g>
  <g stroke="var(--accent2)" stroke-width="1.5" fill="none"><path d="M532 64 V72 H700 V64"/></g>
  <text x="266" y="87" fill="var(--accent)" text-anchor="middle" font-size="11">network · 24 bits · fixed</text>
  <text x="616" y="87" fill="var(--accent2)" text-anchor="middle" font-size="11">host · 8 bits</text>
  <text x="616" y="101" fill="var(--muted)" text-anchor="middle" font-size="10">2⁸ = 256 addresses</text>
  <g fill="var(--muted)" font-size="10">
    <text x="8" y="127">192 . 168 . 1 .</text>
    <text x="120" y="127" fill="var(--accent2)">0</text>
    <text x="140" y="127">← network address, reserved</text>
    <text x="8" y="145">192 . 168 . 1 .</text>
    <text x="120" y="145" fill="var(--ok)">1 – 254</text>
    <text x="180" y="145">← the 254 usable hosts</text>
    <text x="8" y="163">192 . 168 . 1 .</text>
    <text x="120" y="163" fill="var(--accent2)">255</text>
    <text x="150" y="163">← broadcast, reserved</text>
    <text x="8" y="182" fill="var(--warn)">Bigger prefix = smaller network. /25 halves it to 128; /23 doubles it to 512.</text>
  </g>''',
    'CIDR splits the 32 bits into a network part and a host part.')

add('module-2.html',
    '<div class="box why">\n<b>Why NAT explains a whole class of problems</b>',
    'fig-nat', '0 0 720 208', f'''
  {arrow('an1')}
  <g stroke="var(--line)" fill="none" stroke-width="1.2"><rect x="8" y="30" width="210" height="140" rx="8"/></g>
  <text x="18" y="48" fill="var(--muted)" font-size="10">private LAN · 192.168.1.0/24</text>
  <g stroke="var(--accent)" fill="none" stroke-width="1.3">
    <rect x="24" y="58" width="120" height="30" rx="5"/>
    <rect x="24" y="98" width="120" height="30" rx="5"/>
    <rect x="24" y="136" width="120" height="26" rx="5"/>
  </g>
  <g fill="var(--txt)" font-size="10">
    <text x="34" y="77">192.168.1.34</text><text x="34" y="117">192.168.1.35</text><text x="34" y="153">192.168.1.36</text>
  </g>
  <g stroke="var(--accent2)" fill="none" stroke-width="1.5"><rect x="270" y="78" width="120" height="52" rx="8"/></g>
  <text x="330" y="100" fill="var(--accent2)" text-anchor="middle" font-size="11">router / NAT</text>
  <text x="330" y="116" fill="var(--muted)" text-anchor="middle" font-size="9">public 203.0.113.7</text>
  <g stroke="var(--accent2)" stroke-width="1.2" marker-end="url(#an1)">
    <line x1="146" y1="73" x2="266" y2="96"/><line x1="146" y1="113" x2="266" y2="106"/>
  </g>
  <g stroke="var(--accent2)" stroke-width="1.2" marker-end="url(#an1)"><line x1="392" y1="104" x2="500" y2="104"/></g>
  <g stroke="var(--line)" fill="none" stroke-width="1.3"><rect x="506" y="78" width="200" height="52" rx="8"/></g>
  <text x="606" y="108" fill="var(--txt)" text-anchor="middle" font-size="11">the internet</text>
  <g fill="var(--muted)" font-size="9">
    <text x="238" y="150">translation table</text>
    <text x="238" y="163">192.168.1.34:51234 → 203.0.113.7:40001</text>
    <text x="238" y="172">192.168.1.35:49900 → 203.0.113.7:40002</text>
  </g>
  <text x="8" y="186" fill="var(--warn)" font-size="10">Outbound creates the mapping, so replies find their way home.</text>
  <text x="8" y="199" fill="var(--warn)" font-size="10">Inbound has none — hence port forwarding, and hence -p 8080:80.</text>''',
    'NAT multiplexes many private addresses onto one public address.')

add('module-2.html',
    '<p>If you see <b>SYN</b> repeated with no reply',
    'fig-handshake', '0 0 720 250', f'''
  {arrow('ah1','var(--ok)')}
  <g stroke="var(--line)" stroke-dasharray="3 3"><line x1="90" y1="34" x2="90" y2="228"/><line x1="300" y1="34" x2="300" y2="228"/></g>
  <g stroke="var(--line)" stroke-dasharray="3 3"><line x1="430" y1="34" x2="430" y2="228"/><line x1="640" y1="34" x2="640" y2="228"/></g>
  <g fill="var(--txt)" text-anchor="middle" font-size="10">
    <text x="90" y="26">client</text><text x="300" y="26">server</text>
    <text x="430" y="26">client</text><text x="640" y="26">server</text>
  </g>
  <text x="195" y="48" fill="var(--ok)" text-anchor="middle" font-size="11">success</text>
  <g stroke="var(--ok)" stroke-width="1.4" marker-end="url(#ah1)">
    <line x1="92" y1="70" x2="296" y2="70"/><line x1="298" y1="104" x2="94" y2="104"/>
    <line x1="92" y1="138" x2="296" y2="138"/>
  </g>
  <g fill="var(--txt)" text-anchor="middle" font-size="10">
    <text x="195" y="64">SYN</text><text x="195" y="98">SYN, ACK</text><text x="195" y="132">ACK</text>
  </g>
  <text x="195" y="166" fill="var(--muted)" text-anchor="middle" font-size="10">connection established</text>
  <text x="535" y="48" fill="var(--err)" text-anchor="middle" font-size="11">the two failures</text>
  <defs><marker id="ah2" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="var(--err)"/></marker></defs>
  <g stroke="var(--err)" stroke-width="1.4" marker-end="url(#ah2)">
    <line x1="432" y1="76" x2="626" y2="76"/><line x1="628" y1="104" x2="434" y2="104"/>
  </g>
  <g fill="var(--txt)" text-anchor="middle" font-size="10">
    <text x="530" y="70">SYN</text><text x="530" y="98">RST</text>
  </g>
  <text x="535" y="122" fill="var(--err)" text-anchor="middle" font-size="10">refused — instant</text>
  <g stroke="var(--warn)" stroke-width="1.4" stroke-dasharray="5 4">
    <line x1="432" y1="160" x2="560" y2="160"/><line x1="432" y1="182" x2="560" y2="182"/>
  </g>
  <text x="575" y="164" fill="var(--warn)" font-size="16">✕</text><text x="575" y="186" fill="var(--warn)" font-size="16">✕</text>
  <g fill="var(--txt)" font-size="10"><text x="440" y="154">SYN</text><text x="440" y="176">SYN (retry)</text></g>
  <text x="535" y="206" fill="var(--warn)" text-anchor="middle" font-size="10">dropped — hangs to timeout</text>
  <text x="8" y="242" fill="var(--muted)" font-size="10">The timing is the diagnosis: an RST returns in milliseconds; a silent drop burns your whole timeout.</text>''',
    'The three-way handshake, and the two ways it fails.')

add('module-2.html',
    '<p>A connection is uniquely identified by a four-tuple',
    'fig-ports', '0 0 720 170', f'''
  <text x="8" y="16" fill="var(--muted)" font-size="10">the 16-bit port space — 1 to 65535</text>
  <g stroke="var(--line)" stroke-width="1">
    <rect x="8"   y="28" width="106" height="34" rx="4" fill="color-mix(in srgb,var(--warn) 26%,transparent)"/>
    <rect x="116" y="28" width="330" height="34" rx="4" fill="color-mix(in srgb,var(--accent) 26%,transparent)"/>
    <rect x="448" y="28" width="264" height="34" rx="4" fill="color-mix(in srgb,var(--accent2) 26%,transparent)"/>
  </g>
  <g fill="var(--txt)" text-anchor="middle" font-size="10">
    <text x="61"  y="49">0 – 1023</text><text x="281" y="49">1024 – 49151</text><text x="580" y="49">49152 – 65535</text>
  </g>
  <g text-anchor="middle" font-size="10">
    <text x="61"  y="78" fill="var(--warn)">well-known</text>
    <text x="281" y="78" fill="var(--accent)">registered</text>
    <text x="580" y="78" fill="var(--accent2)">ephemeral</text>
  </g>
  <g fill="var(--muted)" text-anchor="middle" font-size="9">
    <text x="61"  y="93">root to bind</text>
    <text x="281" y="93">where your services live</text>
    <text x="580" y="93">your CLIENT gets one of these</text>
    <text x="61"  y="106">22 · 80 · 443</text>
    <text x="281" y="106">3000 · 5432 · 6379 · 8000</text>
    <text x="580" y="106">picked at random per connection</text>
  </g>
  <text x="8" y="132" fill="var(--txt)" font-size="10">One connection = (src IP, src port, dst IP, dst port):</text>
  <text x="8" y="150" fill="var(--accent2)" font-size="11">(192.168.1.34, <tspan fill="var(--accent2)">51234</tspan>, 93.184.216.34, <tspan fill="var(--warn)">443</tspan>)</text>
  <text x="8" y="164" fill="var(--muted)" font-size="9">Thousands of clients share port 443 because the source port differs — that is what makes the tuple unique.</text>''',
    'Port ranges, and the four-tuple that identifies a connection.')

add('module-2.html',
    '<table>\n<tr><th>Record</th>',
    'fig-dns', '0 0 720 210', f'''
  {arrow('ad1')}
  <g stroke="var(--accent)" fill="none" stroke-width="1.3"><rect x="8" y="60" width="108" height="42" rx="6"/></g>
  <text x="62" y="78" fill="var(--txt)" text-anchor="middle" font-size="10">your app</text>
  <text x="62" y="92" fill="var(--muted)" text-anchor="middle" font-size="9">curl example.com</text>
  <g stroke="var(--accent2)" fill="none" stroke-width="1.4"><rect x="160" y="55" width="120" height="52" rx="6"/></g>
  <text x="220" y="76" fill="var(--accent2)" text-anchor="middle" font-size="10">resolver</text>
  <text x="220" y="92" fill="var(--muted)" text-anchor="middle" font-size="9">caches by TTL</text>
  <g stroke="var(--line)" fill="none" stroke-width="1.2">
    <rect x="340" y="14" width="150" height="34" rx="6"/>
    <rect x="340" y="64" width="150" height="34" rx="6"/>
    <rect x="340" y="114" width="150" height="34" rx="6"/>
  </g>
  <g fill="var(--txt)" font-size="10">
    <text x="352" y="35">root servers  (.)</text>
    <text x="352" y="85">.com servers</text>
    <text x="352" y="135">example.com NS</text>
  </g>
  <g fill="var(--muted)" font-size="9" text-anchor="end">
    <text x="700" y="35">"ask .com"</text><text x="700" y="85">"ask example.com"</text>
    <text x="700" y="135" fill="var(--ok)">A 93.184.216.34</text>
  </g>
  <g stroke="var(--accent2)" stroke-width="1.3" marker-end="url(#ad1)">
    <line x1="118" y1="80" x2="156" y2="80"/>
    <line x1="282" y1="72" x2="336" y2="34"/><line x1="282" y1="80" x2="336" y2="80"/>
    <line x1="282" y1="92" x2="336" y2="128"/>
  </g>
  <text x="300" y="52" fill="var(--muted)" font-size="9">1</text>
  <text x="304" y="74" fill="var(--muted)" font-size="9">2</text>
  <text x="300" y="112" fill="var(--muted)" font-size="9">3</text>
  <g stroke="var(--warn)" fill="none" stroke-width="1.3"><rect x="8" y="130" width="108" height="40" rx="6"/></g>
  <text x="62" y="147" fill="var(--warn)" text-anchor="middle" font-size="10">/etc/hosts</text>
  <text x="62" y="161" fill="var(--muted)" text-anchor="middle" font-size="9">checked FIRST</text>
  <g stroke="var(--warn)" stroke-width="1.2" stroke-dasharray="3 3"><line x1="62" y1="128" x2="62" y2="106"/></g>
  <text x="8" y="192" fill="var(--muted)" font-size="10">Every hop caches the answer for its TTL — which is why a record you just changed can still serve the old value.</text>
  <text x="8" y="205" fill="var(--warn)" font-size="10">Lower the TTL a day BEFORE a migration, not at the moment you cut over.</text>''',
    'Recursive resolution, with /etc/hosts short-circuiting the whole thing.')

# ============================================================ MODULE 3
add('module-3.html',
    '<h3>.dockerignore</h3>',
    'fig-cache', '0 0 720 260', f'''
  <text x="8" y="16" fill="var(--err)" font-size="10">✗ source copied first — one edit rebuilds all</text>
  <g stroke="var(--line)" stroke-width="1.2" fill="none">
    <rect x="8" y="28" width="300" height="26" rx="4" fill="color-mix(in srgb,var(--ok) 20%,transparent)"/>
    <rect x="8" y="58" width="300" height="26" rx="4" fill="color-mix(in srgb,var(--err) 22%,transparent)"/>
    <rect x="8" y="88" width="300" height="26" rx="4" fill="color-mix(in srgb,var(--err) 22%,transparent)"/>
    <rect x="8" y="118" width="300" height="26" rx="4" fill="color-mix(in srgb,var(--err) 22%,transparent)"/>
  </g>
  <g fill="var(--txt)" font-size="10">
    <text x="18" y="45">FROM python:3.12-slim</text>
    <text x="18" y="75">COPY . .</text>
    <text x="18" y="105">RUN pip install -r requirements.txt</text>
    <text x="18" y="135">CMD [...]</text>
  </g>
  <g fill="var(--muted)" font-size="9" text-anchor="end">
    <text x="300" y="45">CACHED</text><text x="300" y="75">rebuild</text>
    <text x="300" y="105">rebuild ~60s</text><text x="300" y="135">rebuild</text>
  </g>
  <text x="380" y="16" fill="var(--ok)" font-size="10">✓ dependencies first — only the last rebuilds</text>
  <g stroke="var(--line)" stroke-width="1.2" fill="none">
    <rect x="380" y="28" width="332" height="26" rx="4" fill="color-mix(in srgb,var(--ok) 20%,transparent)"/>
    <rect x="380" y="58" width="332" height="26" rx="4" fill="color-mix(in srgb,var(--ok) 20%,transparent)"/>
    <rect x="380" y="88" width="332" height="26" rx="4" fill="color-mix(in srgb,var(--ok) 20%,transparent)"/>
    <rect x="380" y="118" width="332" height="26" rx="4" fill="color-mix(in srgb,var(--err) 22%,transparent)"/>
  </g>
  <g fill="var(--txt)" font-size="10">
    <text x="390" y="45">FROM python:3.12-slim</text>
    <text x="390" y="75">COPY requirements.txt .</text>
    <text x="390" y="105">RUN pip install -r requirements.txt</text>
    <text x="390" y="135">COPY app/ ./app/</text>
  </g>
  <g fill="var(--muted)" font-size="9" text-anchor="end">
    <text x="704" y="45">CACHED</text><text x="704" y="75">CACHED</text>
    <text x="704" y="105">CACHED</text><text x="704" y="135">rebuild ~2s</text>
  </g>
  <text x="8" y="172" fill="var(--muted)" font-size="10">Docker caches layer by layer, top to bottom. The moment one layer changes, every layer below it is invalidated —</text>
  <text x="8" y="187" fill="var(--muted)" font-size="10">so the ordering rule is simply: put what rarely changes above what changes on every commit.</text>
  <g stroke="var(--accent)" fill="none" stroke-width="1.2"><rect x="8" y="202" width="704" height="44" rx="6"/></g>
  <text x="20" y="221" fill="var(--accent)" font-size="10">Same four instructions. Same result. ~30× difference in rebuild time, paid on every single push.</text>
  <text x="20" y="237" fill="var(--muted)" font-size="10">This is the highest-leverage line-ordering decision you will make in a Dockerfile.</text>''',
    'Layer-cache invalidation cascades downward — so ordering is everything.')

add('module-3.html',
    '<div class="box warn">\n<b>localhost inside a container means the container</b>',
    'fig-net', '0 0 720 258', f'''
  {arrow('ac1')}
  <defs><marker id="ac2" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
    <path d="M0,0 L8,4 L0,8 z" fill="var(--ok)"/></marker></defs>
  <g stroke="var(--accent)" fill="none" stroke-width="1.4" stroke-dasharray="5 4">
    <rect x="150" y="40" width="430" height="122" rx="10"/>
  </g>
  <text x="162" y="60" fill="var(--accent)" font-size="10">network "appnet" — Docker runs a DNS server here</text>
  <g stroke="var(--accent2)" fill="none" stroke-width="1.4">
    <rect x="180" y="78" width="155" height="62" rx="8"/>
    <rect x="405" y="78" width="150" height="62" rx="8"/>
  </g>
  <text x="257" y="100" fill="var(--txt)" text-anchor="middle" font-size="11">api</text>
  <text x="257" y="116" fill="var(--muted)" text-anchor="middle" font-size="9">172.18.0.3:8000</text>
  <text x="257" y="131" fill="var(--muted)" text-anchor="middle" font-size="9">has its own localhost</text>
  <text x="480" y="100" fill="var(--txt)" text-anchor="middle" font-size="11">redis</text>
  <text x="480" y="116" fill="var(--muted)" text-anchor="middle" font-size="9">172.18.0.2:6379</text>
  <text x="480" y="131" fill="var(--muted)" text-anchor="middle" font-size="9">has its own localhost</text>
  <g stroke="var(--line)" fill="none" stroke-width="1.3"><rect x="8" y="78" width="112" height="62" rx="8"/></g>
  <text x="64" y="104" fill="var(--txt)" text-anchor="middle" font-size="10">your host</text>
  <text x="64" y="120" fill="var(--muted)" text-anchor="middle" font-size="9">:8000</text>
  <g stroke="var(--accent2)" stroke-width="1.4" marker-end="url(#ac1)"><line x1="122" y1="109" x2="176" y2="109"/></g>
  <text x="64" y="156" fill="var(--accent2)" text-anchor="middle" font-size="9">-p 8000:8000</text>
  <g stroke="var(--ok)" stroke-width="1.5" marker-end="url(#ac2)"><line x1="339" y1="109" x2="401" y2="109"/></g>
  <text x="370" y="102" fill="var(--ok)" text-anchor="middle" font-size="11">✓</text>
  <g font-size="10">
    <text x="12" y="192" fill="var(--ok)" font-size="12">✓</text>
    <text x="30" y="192" fill="var(--txt)">redis://redis:6379</text>
    <text x="230" y="192" fill="var(--muted)">Docker's DNS answers 172.18.0.2 — works</text>
    <text x="12" y="216" fill="var(--err)" font-size="12">✗</text>
    <text x="30" y="216" fill="var(--txt)">redis://localhost:6379</text>
    <text x="230" y="216" fill="var(--muted)">never leaves api — connection refused</text>
  </g>
  <line x1="8" y1="172" x2="712" y2="172" stroke="var(--line)" stroke-width="1"/>
  <text x="8" y="244" fill="var(--muted)" font-size="10">Each container has its own network namespace, so each has its own localhost.</text>''',
    'Service names resolve; localhost does not cross the container boundary.')

# ============================================================ MODULE 4
add('module-4.html',
    '<h2 id="build">',
    'fig-shiftleft', '0 0 720 230', f'''
  <text x="8" y="16" fill="var(--muted)" font-size="10">relative cost to fix one defect, by the stage that catches it (log scale)</text>
  <g stroke="var(--line)" stroke-width="1"><line x1="60" y1="180" x2="700" y2="180"/></g>
  <g stroke="var(--line)" stroke-dasharray="2 4" stroke-width=".8">
    <line x1="60" y1="150" x2="700" y2="150"/><line x1="60" y1="110" x2="700" y2="110"/>
    <line x1="60" y1="70" x2="700" y2="70"/><line x1="60" y1="30" x2="700" y2="30"/>
  </g>
  <g fill="var(--muted)" font-size="9" text-anchor="end">
    <text x="54" y="153">1×</text><text x="54" y="113">10×</text>
    <text x="54" y="73">100×</text><text x="54" y="33">1000×</text>
  </g>
  <g>
    <rect x="100" y="150" width="90" height="30" rx="3" fill="var(--ok)" opacity=".8"/>
    <rect x="252" y="110" width="90" height="70" rx="3" fill="var(--accent)" opacity=".8"/>
    <rect x="404" y="70"  width="90" height="110" rx="3" fill="var(--warn)" opacity=".8"/>
    <rect x="556" y="30"  width="90" height="150" rx="3" fill="var(--err)" opacity=".8"/>
  </g>
  <g fill="var(--txt)" text-anchor="middle" font-size="10">
    <text x="145" y="198">linter</text><text x="297" y="198">CI</text>
    <text x="449" y="198">code review</text><text x="601" y="198">production</text>
  </g>
  <g fill="var(--muted)" text-anchor="middle" font-size="9">
    <text x="145" y="211">in your editor</text><text x="297" y="211">minutes later</text>
    <text x="449" y="211">hours later</text><text x="601" y="211">days later + users</text>
  </g>
  <g fill="var(--txt)" text-anchor="middle" font-size="9">
    <text x="145" y="145">seconds</text><text x="297" y="105">minutes</text>
    <text x="449" y="65">hours</text><text x="601" y="25">days</text>
  </g>
  <text x="8" y="226" fill="var(--warn)" font-size="10">"Shift left" is this chart: every gate you add earlier buys down an order-of-magnitude multiplier.</text>''',
    'The cost of a defect grows roughly tenfold at each stage it survives.')

add('module-4.html',
    '<h2 id="design">',
    'fig-deploystrat', '0 0 720 250', f'''
  <g fill="var(--accent)" font-size="11">
    <text x="8" y="20">rolling</text><text x="8" y="100">blue / green</text><text x="8" y="180">canary</text>
  </g>
  <g fill="var(--muted)" font-size="9">
    <text x="8" y="34">replace a few at a time</text>
    <text x="8" y="114">flip all traffic at once</text>
    <text x="8" y="194">ramp by percentage</text>
  </g>
  <g font-size="9" fill="var(--muted)" text-anchor="middle">
    <text x="220" y="14">t0</text><text x="340" y="14">t1</text><text x="460" y="14">t2</text><text x="580" y="14">t3</text>
  </g>
  <g stroke="var(--line)" stroke-width="1">
    {''.join(f'<rect x="{180+c*120}" y="{22+r*80}" width="100" height="34" rx="4" fill="none"/>' for r in range(3) for c in range(4))}
  </g>
  <!-- rolling -->
  {''.join(f'<rect x="{186+c*120+i*23}" y="28" width="19" height="22" rx="2" fill="{ "var(--accent2)" if i < 3-c else "var(--ok)"}"/>' for c in range(4) for i in range(4))}
  <!-- blue/green -->
  {''.join(f'<rect x="{186+c*120}" y="108" width="42" height="22" rx="2" fill="var(--accent2)" opacity="{1 if c<3 else .25}"/><rect x="{234+c*120}" y="108" width="42" height="22" rx="2" fill="var(--ok)" opacity="{.25 if c<3 else 1}"/>' for c in range(4))}
  <!-- canary -->
  {''.join(f'<rect x="{186+c*120}" y="188" width="{88-c*28}" height="22" rx="2" fill="var(--accent2)"/><rect x="{186+c*120+(88-c*28)}" y="188" width="{c*28}" height="22" rx="2" fill="var(--ok)"/>' for c in range(4))}
  <g fill="var(--muted)" font-size="9" text-anchor="middle">
    <text x="230" y="70">25% new</text><text x="350" y="70">50%</text><text x="470" y="70">75%</text><text x="590" y="70">100%</text>
    <text x="230" y="150">idle green</text><text x="350" y="150">warming</text><text x="470" y="150">tested</text><text x="590" y="150">switch!</text>
    <text x="230" y="230">0%</text><text x="350" y="230">~30%</text><text x="470" y="230">~60%</text><text x="590" y="230">100%</text>
  </g>
  <g font-size="9"><rect x="440" y="238" width="12" height="9" fill="var(--accent2)"/><text x="458" y="246" fill="var(--muted)">old version</text>
  <rect x="540" y="238" width="12" height="9" fill="var(--ok)"/><text x="558" y="246" fill="var(--muted)">new version</text></g>''',
    'Three ways to replace a running version, in increasing order of safety and cost.')

# ============================================================ MODULE 5
add('module-5.html',
    '<div class="box warn">\n<b><code>plan</code> is the safety mechanism',
    'fig-plan', '0 0 720 170', f'''
  <text x="8" y="16" fill="var(--muted)" font-size="10">read these four symbols before you ever type "yes"</text>
  <g stroke="var(--line)" fill="none" stroke-width="1.2">
    <rect x="8" y="28" width="172" height="86" rx="7"/><rect x="188" y="28" width="172" height="86" rx="7"/>
    <rect x="368" y="28" width="172" height="86" rx="7"/><rect x="548" y="28" width="164" height="86" rx="7"/>
  </g>
  <g font-size="22" text-anchor="middle">
    <text x="94" y="60" fill="var(--ok)">+</text><text x="274" y="60" fill="var(--accent2)">~</text>
    <text x="454" y="60" fill="var(--warn)">-</text><text x="630" y="60" fill="var(--err)">-/+</text>
  </g>
  <g fill="var(--txt)" text-anchor="middle" font-size="11">
    <text x="94" y="84">create</text><text x="274" y="84">update in place</text>
    <text x="454" y="84">destroy</text><text x="630" y="84">replace</text>
  </g>
  <g fill="var(--muted)" text-anchor="middle" font-size="9">
    <text x="94" y="102">safe</text><text x="274" y="102">usually safe</text>
    <text x="454" y="102">intended? check</text><text x="630" y="102">destroy THEN create</text>
  </g>
  <g stroke="var(--err)" fill="none" stroke-width="1.4"><rect x="548" y="122" width="164" height="38" rx="6"/></g>
  <text x="630" y="139" fill="var(--err)" text-anchor="middle" font-size="10">data loss lives here</text>
  <text x="630" y="153" fill="var(--muted)" text-anchor="middle" font-size="9">find the forcing attribute</text>
  <text x="8" y="134" fill="var(--muted)" font-size="10">Terraform always tells you what it is about to do, before it does it.</text>
  <text x="8" y="152" fill="var(--warn)" font-size="10">A plan you did not read is an apply you did not authorise.</text>''',
    'The four plan symbols. Only one of them can lose your data.')

add('module-5.html',
    '<p><code>ansible/inventory.ini</code>',
    'fig-ansible', '0 0 720 198', f'''
  {arrow('aa1')}
  <g stroke="var(--accent)" fill="none" stroke-width="1.4"><rect x="8" y="60" width="150" height="66" rx="8"/></g>
  <text x="83" y="84" fill="var(--accent)" text-anchor="middle" font-size="11">control node</text>
  <text x="83" y="100" fill="var(--muted)" text-anchor="middle" font-size="9">your laptop / CI</text>
  <text x="83" y="114" fill="var(--muted)" text-anchor="middle" font-size="9">playbook.yml</text>
  <g stroke="var(--accent2)" stroke-width="1.3" marker-end="url(#aa1)">
    <line x1="162" y1="80" x2="316" y2="40"/><line x1="162" y1="93" x2="316" y2="93"/>
    <line x1="162" y1="106" x2="316" y2="146"/>
  </g>
  <text x="238" y="52" fill="var(--accent2)" text-anchor="middle" font-size="9">SSH</text>
  <text x="238" y="86" fill="var(--accent2)" text-anchor="middle" font-size="9">SSH</text>
  <g stroke="var(--line)" fill="none" stroke-width="1.2">
    <rect x="320" y="20" width="180" height="40" rx="6"/>
    <rect x="320" y="73" width="180" height="40" rx="6"/>
    <rect x="320" y="126" width="180" height="40" rx="6"/>
  </g>
  <g fill="var(--txt)" font-size="10">
    <text x="334" y="45">web1</text><text x="334" y="98">web2</text><text x="334" y="151">web3</text>
  </g>
  <g fill="var(--ok)" font-size="9" text-anchor="end">
    <text x="490" y="45">changed=4</text><text x="490" y="98">changed=4</text><text x="490" y="151">changed=4</text>
  </g>
  <g stroke="var(--ok)" fill="none" stroke-width="1.2"><rect x="520" y="60" width="192" height="66" rx="8"/></g>
  <text x="616" y="82" fill="var(--ok)" text-anchor="middle" font-size="10">run it again</text>
  <text x="616" y="100" fill="var(--txt)" text-anchor="middle" font-size="11">changed=0</text>
  <text x="616" y="116" fill="var(--muted)" text-anchor="middle" font-size="9">that is idempotency</text>
  <text x="8" y="176" fill="var(--muted)" font-size="10">Agentless: plain SSH, no state kept between runs.</text>
  <text x="8" y="191" fill="var(--muted)" font-size="10">It inspects each host and acts only where reality differs.</text>''',
    'Agentless push over SSH; the second run should change nothing.')

# ============================================================ MODULE 6
add('module-6.html',
    '<h3>Rollouts</h3>',
    'fig-owner', '0 0 720 200', f'''
  {arrow('ak1')}
  <g stroke="var(--accent)" fill="none" stroke-width="1.4"><rect x="8" y="20" width="704" height="170" rx="10"/></g>
  <text x="22" y="40" fill="var(--accent)" font-size="11">Deployment · urlshort-api · "3 replicas of this image should exist"</text>
  <g stroke="var(--accent2)" fill="none" stroke-width="1.3"><rect x="26" y="52" width="668" height="82" rx="8"/></g>
  <text x="40" y="70" fill="var(--accent2)" font-size="10">ReplicaSet (rev 2) — owns exactly these pods</text>
  <g stroke="var(--line)" fill="none" stroke-width="1.2">
    <rect x="46" y="80" width="200" height="42" rx="6"/>
    <rect x="262" y="80" width="200" height="42" rx="6"/>
    <rect x="478" y="80" width="196" height="42" rx="6"/>
  </g>
  <g fill="var(--txt)" text-anchor="middle" font-size="10">
    <text x="146" y="98">Pod api-x7k2</text><text x="362" y="98">Pod api-9fp1</text><text x="576" y="98">Pod api-m3q8</text>
  </g>
  <g fill="var(--muted)" text-anchor="middle" font-size="9">
    <text x="146" y="113">node 1 · Ready</text><text x="362" y="113">node 2 · Ready</text><text x="576" y="113">node 2 · Ready</text>
  </g>
  <g stroke="var(--line)" fill="none" stroke-width="1" stroke-dasharray="3 3"><rect x="26" y="142" width="668" height="36" rx="8"/></g>
  <text x="40" y="164" fill="var(--muted)" font-size="10">ReplicaSet (rev 1) — scaled to 0, kept so `kubectl rollout undo` has something to go back to</text>
  <text x="8" y="14" fill="var(--muted)" font-size="10">you declare the top box; everything below is created and maintained for you</text>''',
    'Deployment owns ReplicaSets; ReplicaSets own Pods. You only declare the top.')

add('module-6.html',
    '<h2 id="svc">',
    'fig-rollout', '0 0 720 230', f'''
  <text x="8" y="16" fill="var(--muted)" font-size="10">maxSurge: 1 · maxUnavailable: 0 — capacity never drops below 3 Ready</text>
  <g fill="var(--muted)" font-size="9">
    <text x="8" y="46">step 1</text><text x="8" y="86">step 2</text><text x="8" y="126">step 3</text><text x="8" y="166">step 4</text>
  </g>
  {''.join(
    ''.join(
      f'<rect x="{70+i*74}" y="{32+r*40}" width="64" height="24" rx="4" fill="{c}" opacity=".85"/>'
      for i,c in enumerate(row))
    for r,row in enumerate([
      ['var(--accent2)']*3+['var(--warn)'],
      ['var(--accent2)']*3+['var(--ok)'],
      ['var(--accent2)']*2+['var(--ok)','var(--warn)'],
      ['var(--accent2)','var(--ok)','var(--ok)','var(--ok)'],
    ]))}
  <g fill="var(--muted)" font-size="9">
    <text x="368" y="48">new pod starting — not Ready, gets no traffic</text>
    <text x="368" y="88">new pod passes readiness → joins the Service</text>
    <text x="368" y="128">one old pod removed, next new pod starts</text>
    <text x="368" y="168">…repeat until all replicas are new</text>
  </g>
  <g font-size="9">
    <rect x="70" y="188" width="12" height="9" fill="var(--accent2)"/><text x="88" y="196" fill="var(--muted)">old, Ready</text>
    <rect x="180" y="188" width="12" height="9" fill="var(--ok)"/><text x="198" y="196" fill="var(--muted)">new, Ready</text>
    <rect x="290" y="188" width="12" height="9" fill="var(--warn)"/><text x="308" y="196" fill="var(--muted)">starting, NOT Ready</text>
  </g>
  <text x="8" y="220" fill="var(--warn)" font-size="10">Deploy a broken image and step 2 never happens: the rollout stalls with the old pods still serving. Users see nothing.</text>''',
    'A zero-downtime rolling update, gated on the readiness probe.')

add('module-6.html',
    '<h2 id="res">',
    'fig-probes', '0 0 720 235', f'''
  {arrow('ap2')}
  <g stroke="var(--line)" fill="none" stroke-width="1.3"><rect x="250" y="16" width="220" height="38" rx="6"/></g>
  <text x="360" y="40" fill="var(--txt)" text-anchor="middle" font-size="11">probe fails</text>
  <g stroke="var(--accent2)" stroke-width="1.3" marker-end="url(#ap2)">
    <line x1="300" y1="58" x2="180" y2="90"/><line x1="420" y1="58" x2="540" y2="90"/>
  </g>
  <g stroke="var(--accent2)" fill="none" stroke-width="1.4"><rect x="30" y="94" width="300" height="112" rx="8"/></g>
  <text x="180" y="116" fill="var(--accent2)" text-anchor="middle" font-size="11">readinessProbe</text>
  <text x="180" y="134" fill="var(--muted)" text-anchor="middle" font-size="10">"can I serve traffic right now?"</text>
  <g stroke="var(--ok)" fill="none" stroke-width="1.2"><rect x="46" y="146" width="268" height="48" rx="6"/></g>
  <text x="180" y="165" fill="var(--ok)" text-anchor="middle" font-size="10">removed from Service endpoints</text>
  <text x="180" y="182" fill="var(--ok)" text-anchor="middle" font-size="10">NOT restarted · returns by itself</text>
  <g stroke="var(--err)" fill="none" stroke-width="1.4"><rect x="390" y="94" width="300" height="112" rx="8"/></g>
  <text x="540" y="116" fill="var(--err)" text-anchor="middle" font-size="11">livenessProbe</text>
  <text x="540" y="134" fill="var(--muted)" text-anchor="middle" font-size="10">"am I wedged beyond recovery?"</text>
  <g stroke="var(--err)" fill="none" stroke-width="1.2"><rect x="406" y="146" width="268" height="48" rx="6"/></g>
  <text x="540" y="165" fill="var(--err)" text-anchor="middle" font-size="10">container KILLED and restarted</text>
  <text x="540" y="182" fill="var(--err)" text-anchor="middle" font-size="10">restart counter increments</text>
  <text x="8" y="224" fill="var(--warn)" font-size="10">Put the dependency check in readiness. If liveness checks the database, one DB blip restarts your entire fleet at once.</text>''',
    'Same failing check, opposite consequences. This is the outage most people cause once.')

# ============================================================ MODULE 7
add('module-7.html',
    '<div class="box">\n<b>Never graph a counter directly</b>',
    'fig-mtypes', '0 0 720 200', f'''
  <g stroke="var(--line)" fill="none" stroke-width="1">
    <rect x="8" y="26" width="225" height="120" rx="7"/>
    <rect x="247" y="26" width="225" height="120" rx="7"/>
    <rect x="486" y="26" width="226" height="120" rx="7"/>
  </g>
  <g text-anchor="middle" font-size="11" fill="var(--accent)">
    <text x="120" y="18">counter</text><text x="359" y="18">gauge</text><text x="599" y="18">histogram</text>
  </g>
  <polyline points="24,132 50,120 76,106 102,92 128,78 128,132 154,120 180,106 206,94"
            fill="none" stroke="var(--accent2)" stroke-width="1.8"/>
  <text x="120" y="162" fill="var(--muted)" text-anchor="middle" font-size="9">only goes up · resets on restart</text>
  <text x="120" y="177" fill="var(--warn)" text-anchor="middle" font-size="9">always wrap in rate()</text>
  <polyline points="263,100 289,78 315,112 341,66 367,94 393,72 419,118 445,88"
            fill="none" stroke="var(--accent2)" stroke-width="1.8"/>
  <text x="359" y="162" fill="var(--muted)" text-anchor="middle" font-size="9">up and down</text>
  <text x="359" y="177" fill="var(--muted)" text-anchor="middle" font-size="9">memory · queue depth · replicas</text>
  <g fill="var(--accent2)" opacity=".85">
    <rect x="502" y="112" width="22" height="26"/><rect x="528" y="88" width="22" height="50"/>
    <rect x="554" y="60" width="22" height="78"/><rect x="580" y="76" width="22" height="62"/>
    <rect x="606" y="100" width="22" height="38"/><rect x="632" y="118" width="22" height="20"/>
    <rect x="658" y="128" width="22" height="10"/>
  </g>
  <text x="599" y="162" fill="var(--muted)" text-anchor="middle" font-size="9">observations bucketed</text>
  <text x="599" y="177" fill="var(--muted)" text-anchor="middle" font-size="9">gives you percentiles</text>
  <text x="8" y="196" fill="var(--muted)" font-size="10">"how often?" → counter · "how much now?" → gauge · "how slow, for whom?" → histogram</text>''',
    'The three metric types you will actually use, and their shapes.')

add('module-7.html',
    '<h2 id="grafana">',
    'fig-p95', '0 0 720 242', f'''
  <text x="8" y="16" fill="var(--muted)" font-size="10">distribution of request latency — why the average is a comforting lie</text>
  <g stroke="var(--line)" stroke-width="1"><line x1="50" y1="170" x2="700" y2="170"/></g>
  <path d="M50,170 C110,170 120,60 175,58 C230,56 245,140 300,156 C360,172 420,166 470,164
           C540,162 600,163 700,163"
        fill="color-mix(in srgb,var(--accent2) 22%,transparent)" stroke="var(--accent2)" stroke-width="1.6"/>
  <g stroke="var(--ok)" stroke-width="1.6" stroke-dasharray="5 3"><line x1="205" y1="40" x2="205" y2="170"/></g>
  <text x="205" y="34" fill="var(--ok)" text-anchor="middle" font-size="10">average 55 ms</text>
  <text x="205" y="186" fill="var(--muted)" text-anchor="middle" font-size="9">"everything is fine"</text>
  <g stroke="var(--warn)" stroke-width="1.6" stroke-dasharray="5 3"><line x1="470" y1="40" x2="470" y2="170"/></g>
  <text x="470" y="34" fill="var(--warn)" text-anchor="middle" font-size="10">p95 = 1.2 s</text>
  <g stroke="var(--err)" stroke-width="1.6" stroke-dasharray="5 3"><line x1="620" y1="40" x2="620" y2="170"/></g>
  <text x="620" y="34" fill="var(--err)" text-anchor="middle" font-size="10">p99 = 4 s</text>
  <path d="M470 150 H700 V170 H470 Z" fill="color-mix(in srgb,var(--err) 30%,transparent)"/>
  <text x="585" y="186" fill="var(--err)" text-anchor="middle" font-size="9">the tail — 1 user in 20 lives here</text>
  <g fill="var(--muted)" font-size="9" text-anchor="middle">
    <text x="120" y="186">fast</text><text x="300" y="186">typical</text>
  </g>
  <text x="8" y="208" fill="var(--muted)" font-size="10">95% at 50 ms and 5% at 10 s averages to a healthy-looking 550 ms —</text>
  <text x="8" y="220" fill="var(--muted)" font-size="10">while one user in twenty is having a terrible time.</text>
  <text x="8" y="233" fill="var(--warn)" font-size="10">Alert on p95/p99. Those are real people, and often your heaviest users.</text>''',
    'Averages hide the tail. Percentiles are where user pain actually shows up.')

add('module-7.html',
    '<h2 id="logs">',
    'fig-budget', '0 0 720 230', f'''
  <text x="8" y="16" fill="var(--muted)" font-size="10">error budget for a 99.5% / 30-day SLO — you may fail 0.5% of requests (~3.6 h)</text>
  <g stroke="var(--line)" stroke-width="1"><line x1="52" y1="176" x2="700" y2="176"/><line x1="52" y1="30" x2="52" y2="176"/></g>
  <g fill="var(--muted)" font-size="9" text-anchor="end">
    <text x="46" y="36">100%</text><text x="46" y="106">50%</text><text x="46" y="180">0%</text>
  </g>
  <g fill="var(--muted)" font-size="9" text-anchor="middle">
    <text x="52" y="192">day 0</text><text x="376" y="192">day 15</text><text x="700" y="192">day 30</text>
  </g>
  <line x1="52" y1="32" x2="700" y2="176" stroke="var(--muted)" stroke-dasharray="4 4" stroke-width="1"/>
  <text x="250" y="104" fill="var(--muted)" font-size="9">sustainable burn</text>
  <polyline points="52,32 130,50 200,62 270,70 340,92 380,150 420,158 500,163 580,168 700,172"
            fill="none" stroke="var(--accent2)" stroke-width="2"/>
  <circle cx="340" cy="92" r="4" fill="var(--err)"/>
  <text x="330" y="62" fill="var(--err)" text-anchor="end" font-size="9">bad deploy</text>
  <g stroke="var(--err)" stroke-width="1.2" stroke-dasharray="3 3"><line x1="380" y1="30" x2="380" y2="176"/></g>
  <path d="M380 150 H700 V176 H380 Z" fill="color-mix(in srgb,var(--err) 18%,transparent)"/>
  <text x="596" y="64" fill="var(--err)" text-anchor="middle" font-size="10">budget nearly gone</text>
  <text x="596" y="78" fill="var(--muted)" text-anchor="middle" font-size="9">freeze features, fix reliability</text>
  <text x="150" y="120" fill="var(--ok)" font-size="10">budget healthy</text>
  <text x="150" y="134" fill="var(--muted)" font-size="9">ship aggressively</text>
  <text x="8" y="212" fill="var(--muted)" font-size="10">The budget turns "how fast should we ship?" from an argument into a number that both sides can read off a chart.</text>
  <text x="8" y="226" fill="var(--warn)" font-size="10">This is why 100% is the wrong target: a zero budget means you can never deploy anything.</text>''',
    'An error budget makes release pace a measurement rather than an opinion.')

add('module-7.html',
    '<h2 id="slo">',
    'fig-alertstate', '0 0 720 165', f'''
  {arrow('as1')}
  <g stroke="var(--ok)" fill="none" stroke-width="1.4"><rect x="8" y="46" width="150" height="52" rx="8"/></g>
  <text x="83" y="68" fill="var(--ok)" text-anchor="middle" font-size="11">Inactive</text>
  <text x="83" y="84" fill="var(--muted)" text-anchor="middle" font-size="9">expr is false</text>
  <g stroke="var(--warn)" fill="none" stroke-width="1.4"><rect x="248" y="46" width="150" height="52" rx="8"/></g>
  <text x="323" y="68" fill="var(--warn)" text-anchor="middle" font-size="11">Pending</text>
  <text x="323" y="84" fill="var(--muted)" text-anchor="middle" font-size="9">true, but not yet for 5m</text>
  <g stroke="var(--err)" fill="none" stroke-width="1.4"><rect x="488" y="46" width="150" height="52" rx="8"/></g>
  <text x="563" y="68" fill="var(--err)" text-anchor="middle" font-size="11">Firing</text>
  <text x="563" y="84" fill="var(--muted)" text-anchor="middle" font-size="9">pages a human</text>
  <g stroke="var(--accent2)" stroke-width="1.4" marker-end="url(#as1)">
    <line x1="162" y1="72" x2="244" y2="72"/><line x1="402" y1="72" x2="484" y2="72"/>
  </g>
  <g fill="var(--accent2)" text-anchor="middle" font-size="9">
    <text x="203" y="64">expr true</text><text x="443" y="64">held for: 5m</text>
  </g>
  <path d="M323 100 C323 124 83 124 83 102" stroke="var(--ok)" fill="none" stroke-width="1.3" marker-end="url(#as1)"/>
  <text x="203" y="142" fill="var(--ok)" text-anchor="middle" font-size="9">resolved before 5m — nobody woken</text>
  <text x="8" y="26" fill="var(--muted)" font-size="10">the <tspan fill="var(--txt)">for:</tspan> clause is what stands between a 30-second blip and a 3 a.m. phone call</text>
  <text x="8" y="158" fill="var(--warn)" font-size="10">Every paging alert must be urgent, actionable, and carry a runbook. If it fails any one of those, make it a ticket.</text>''',
    'The for: clause filters transient spikes out of your pager.')

# --------------------------------------------- fixes to the ORIGINAL figures
TEXT_FIXES = [
    ('module-1.html',
     '<g fill="var(--accent2)" text-anchor="middle" font-size="11">\n'
     '    <text x="179" y="82">add</text>\n'
     '    <text x="369" y="82">commit</text>\n'
     '    <text x="551" y="82">push</text>\n'
     '  </g>',
     '<g fill="var(--accent2)" text-anchor="middle" font-size="9">\n'
     '    <text x="179" y="80">add</text>\n'
     '    <text x="369" y="80">commit</text>\n'
     '    <text x="551" y="80">push</text>\n'
     '  </g>'),
    ('module-2.html',
     '<text x="390" y="222">curl fails but ping works  → layer 3 fine, layer 4/7 not</text>',
     '<text x="390" y="222">ping ok, curl fails → layer 3 fine, 4/7 not</text>'),
    ('module-2.html',
     '<text x="390" y="238">ping fails by name, works by IP → DNS (layer 7)</text>',
     '<text x="390" y="238">fails by name, works by IP → DNS</text>'),
]

# ---------------------------------------------------------------- apply
def main():
    total_fig = 0
    for mod in sorted({f[0] for f in FIGURES}):
        path = os.path.join(SRC, mod)
        s = open(path, encoding='utf-8').read()
        for old, new in COLOR.items():
            s = s.replace(f'"{old}"', f'"{new}"')
        for tmod, told, tnew in TEXT_FIXES:
            if tmod == mod and told in s:
                s = s.replace(told, tnew)
        n = 0
        for m, anchor, fid, html in FIGURES:
            if m != mod:
                continue
            if f'id="{fid}"' in s:
                continue
            if anchor not in s:
                print(f"  !! anchor not found in {mod}: {anchor[:60]!r}")
                continue
            s = s.replace(anchor, html + '\n' + anchor, 1)
            n += 1
        open(path, 'w', encoding='utf-8').write(s)
        total_fig += n
        print(f"  {mod}: +{n} figures")
    print(f"total new figures: {total_fig}")

if __name__ == '__main__':
    main()
