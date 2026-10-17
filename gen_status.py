"""Draw the os-xgs-npu status board: one card per appliance, the stage the
project is at, the families without hardware, and the figures that keep it
honest. Writes assets/status-dark.svg and assets/status-light.svg.

Every number here is copied from the driver repository's own status pages
(badges, octeon-tx-reference.md's weighted table, the measurement pages).
Update the DATA block, run it, commit the two SVGs.
"""
import pathlib

# ---------------------------------------------------------------- data ----
STAGES = [  # (label, state)  state: done | now | next
    ("Discovery", "done"),
    ("Front ports", "done"),
    ("Offload", "done"),
    ("Integration &amp; testing", "now"),
    ("Notice lifted", "next"),
]
STAGE_NOTE = "“What is left is engineering rather than discovery.”"

CARDS = [
    {
        "name": "XGS 3300",
        "chip": "Cavium OCTEON TX &#183; CN83XX",
        "ports": 12,
        "rows": [  # (state, label, value)  state: ok | wip | no
            ("ok", "Front ports", "12 of 12, and the module&#8217;s"),
            ("ok", "Flow offload", "99.6 % of frames in hardware"),
            ("ok", "IPsec offload", "GCM &#183; CBC &#183; NAT-T &#183; IPv6"),
            ("ok", "Best IPsec here", "7.41 Gbit/s, one stream"),
            ("ref", "Vendor rates it", "31.1 Gbit/s, many tunnels"),
            ("ok", "Appliance", "sensors &#183; panel &#183; first boot"),
            ("ok", "Built image", "installed, booted from disk"),
        ],
        "done": 92,  # octeon-tx-reference.md, re-weighed 2026-10-12
    },
    {
        "name": "XGS 136",
        "chip": "Marvell CN9131 &#183; ARMADA",
        "ports": 14,
        "rows": [
            ("ok", "Front ports", "14 of 14"),
            ("ok", "Flow offload", "in hardware, by the sweep"),
            ("ok", "IPsec offload", "GCM &#183; CBC &#183; NAT-T"),
            ("ok", "Best IPsec here", "982 Mbit/s, one 1G link"),
            ("ref", "Vendor rates it", "4.8 Gbit/s, many tunnels"),
            ("ok", "First boot", "ports by the chassis names"),
            ("wip", "Integration", "into the tree and plugins"),
        ],
        "done": None,  # no weighted table published for the ARMADA yet
    },
]

FAMILIES = [
    ("OCTEON TX2", "described from vendor binaries, no hardware"),
    ("OCTEON TX2 98XX", "described from vendor binaries, no hardware"),
    ("TOPAZ &#183; GR", "no coprocessor, nothing to drive"),
]

STATS = [
    ("2,391 GiB", "over TLS, not a byte changed"),
    ("6,100", "give-backs revived, none refused"),
    ("10 &#183; 19", "claims withdrawn &#183; dead ends recorded"),
]

# --------------------------------------------------------------- theme ----
THEMES = {
    "dark": dict(bg="#0D1117", card="#161B22", line="#30363D", fg="#E6EDF3", sub="#8B949E",
                 kk="#6E7681", acc="#F97316", ok="#3FB950", wip="#D29922", no="#6E7681",
                 track="#21262D"),
    "light": dict(bg="#FFFFFF", card="#F6F8FA", line="#D0D7DE", fg="#1F2328", sub="#59636E",
                  kk="#6E7781", acc="#C2410C", ok="#1A7F37", wip="#9A6700", no="#8C959F",
                  track="#EAEEF2"),
}
SANS = "ui-sans-serif,-apple-system,Segoe UI,Inter,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

W = 900
CARD_Y, CARD_H, CARD_W = 214, 390, 400
NOTE_Y = CARD_Y + CARD_H + 26
FAM_Y = NOTE_Y + 20
STAT_Y = FAM_Y + 74
H = STAT_Y + 74


def text(x, y, s, size, fill, weight=400, anchor="start", mono=False, extra=""):
    fam = MONO if mono else SANS
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{extra}>{s}</text>')


def state_icon(cx, cy, state, t):
    if state == "ok":
        return (f'<circle cx="{cx}" cy="{cy}" r="8" fill="{t["ok"]}"/>'
                f'<path d="M{cx-3.6} {cy+0.2} l2.4 2.5 l4.8 -5" fill="none" stroke="{t["card"]}" '
                f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"/>')
    if state == "wip":
        return (f'<circle cx="{cx}" cy="{cy}" r="7.2" fill="none" stroke="{t["wip"]}" stroke-width="1.6"/>'
                f'<path d="M{cx} {cy-7.2} A7.2 7.2 0 0 1 {cx} {cy+7.2} Z" fill="{t["wip"]}"/>')
    if state == "ref":
        return (f'<path d="M{cx} {cy-7} L{cx+7} {cy} L{cx} {cy+7} L{cx-7} {cy} Z" fill="none" '
                f'stroke="{t["sub"]}" stroke-width="1.4"/>')
    return f'<circle cx="{cx}" cy="{cy}" r="7.2" fill="none" stroke="{t["no"]}" stroke-width="1.6"/>'


def chip_tile(x, y, t):
    """A coprocessor glyph in a rounded tile: the package, its die, three
    pins a side and a pin-one mark."""
    size, body, die = 56, 28, 12
    cx, cy = x + size / 2, y + size / 2
    bx, by = cx - body / 2, cy - body / 2
    out = [f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="12" fill="{t["bg"]}" stroke="{t["line"]}"/>']
    for k in (-8, 0, 8):
        out.append(f'<path d="M{cx+k} {by-2} v-5 M{cx+k} {by+body+2} v5 M{bx-2} {cy+k} h-5 M{bx+body+2} {cy+k} h5" '
                   f'stroke="{t["sub"]}" stroke-width="1.6" stroke-linecap="round" fill="none"/>')
    out.append(f'<rect x="{bx}" y="{by}" width="{body}" height="{body}" rx="5" fill="{t["acc"]}" fill-opacity="0.10" '
               f'stroke="{t["acc"]}" stroke-width="1.8"/>')
    out.append(f'<rect x="{cx-die/2}" y="{cy-die/2}" width="{die}" height="{die}" rx="2.5" fill="{t["acc"]}"/>')
    out.append(f'<circle cx="{bx+5}" cy="{by+5}" r="1.6" fill="{t["acc"]}"/>')
    return "".join(out)


def card(x, c, t):
    y = CARD_Y
    out = [f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="12" fill="{t["card"]}" stroke="{t["line"]}"/>',
           chip_tile(x + 22, y + 14, t),
           text(x + 92, y + 39, c["name"], 20, t["fg"], 700),
           text(x + 92, y + 59, c["chip"], 12.5, t["sub"]),
           f'<line x1="{x+22}" y1="{y+80}" x2="{x+CARD_W-22}" y2="{y+80}" stroke="{t["line"]}"/>']
    for i, (state, label, value) in enumerate(c["rows"]):
        ry = y + 108 + i * 30
        out.append(state_icon(x + 30, ry - 4, state, t))
        out.append(text(x + 48, ry, label, 13.5, t["sub"] if state == "ref" else t["fg"], 600))
        out.append(text(x + CARD_W - 22, ry, value, 12.5, t["sub"], anchor="end", mono=True))
    by = y + CARD_H - 52
    out.append(f'<line x1="{x+22}" y1="{by-18}" x2="{x+CARD_W-22}" y2="{by-18}" stroke="{t["line"]}"/>')
    out.append(text(x + 22, by, "Weighted completion", 12.5, t["sub"]))
    bw = CARD_W - 44
    if c["done"] is None:
        out.append(text(x + CARD_W - 22, by, "not weighed yet", 12.5, t["wip"], 600, anchor="end", mono=True))
        out.append(f'<rect x="{x+22}" y="{by+12}" width="{bw}" height="9" rx="4.5" fill="none" '
                   f'stroke="{t["wip"]}" stroke-width="1.2" stroke-dasharray="4 4"/>')
    else:
        out.append(text(x + CARD_W - 22, by + 1, f'{c["done"]} %', 17, t["fg"], 700, anchor="end"))
        out.append(f'<rect x="{x+22}" y="{by+12}" width="{bw}" height="9" rx="4.5" fill="{t["track"]}"/>')
        out.append(f'<rect x="{x+22}" y="{by+12}" width="{bw*c["done"]/100:.1f}" height="9" rx="4.5" fill="{t["ok"]}"/>')
    return "".join(out)


def stage_track(t):
    xs = [100, 275, 450, 625, 800]
    y = 132
    out = [f'<line x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="{t["line"]}" stroke-width="2"/>']
    last_done = max(i for i, (_, s) in enumerate(STAGES) if s in ("done", "now"))
    out.append(f'<line x1="{xs[0]}" y1="{y}" x2="{xs[last_done]}" y2="{y}" stroke="{t["ok"]}" stroke-width="2"/>')
    for x, (label, state) in zip(xs, STAGES):
        if state == "done":
            out.append(state_icon(x, y, "ok", dict(t, card=t["bg"])))
            colour, weight = t["fg"], 500
        elif state == "now":
            out.append(f'<circle cx="{x}" cy="{y}" r="12" fill="{t["bg"]}" stroke="{t["acc"]}" stroke-width="2"/>'
                       f'<circle cx="{x}" cy="{y}" r="5" fill="{t["acc"]}"/>')
            colour, weight = t["acc"], 700
        else:
            out.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{t["bg"]}" stroke="{t["no"]}" stroke-width="1.6"/>')
            colour, weight = t["sub"], 500
        out.append(text(x, y + 30, label, 12.5, colour, weight, anchor="middle"))
    out.append(text(W / 2, y + 58, STAGE_NOTE, 12.5, t["sub"], anchor="middle", extra=' font-style="italic"'))
    return "".join(out)


def build(theme):
    t = THEMES[theme]
    alt = ("os-xgs-npu status. Stage: discovery, front ports and offload done; integration and testing "
           "in progress; the repository notice not yet lifted. XGS 3300, Cavium OCTEON TX: 12 of 12 front "
           "ports and the module's, flow offload with 99.6 per cent of frames in hardware, IPsec offload "
           "with GCM, CBC, NAT-T and IPv6, best IPsec measured here 7.41 Gbit/s on one stream while the vendor rates the appliance at 31.1 Gbit/s across many tunnels, sensors, front panel and "
           "first boot, a built image booted from disk, weighted completion 92 per cent. XGS 136, Marvell "
           "CN9131: 14 of 14 front ports, flow offload by the sweep, IPsec offload with GCM, CBC and NAT-T, "
           "best IPsec measured here 982 Mbit/s over one gigabit link while the vendor rates it at 4.8 Gbit/s across many tunnels, first boot by the chassis names, integration in progress, not "
           "weighed yet. OCTEON TX2 and TX2 98XX described only; TOPAZ and GR have no coprocessor. "
           "2,391 GiB over TLS with no byte changed; 6,100 give-backs revived, none refused; ten claims "
           "withdrawn and nineteen dead ends recorded. Vendor figures come from its datasheets under lab load across many tunnels; the figures measured here are one TCP stream ending on the appliance host.")
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'role="img" aria-label="{alt}">',
           f'<rect width="{W}" height="{H}" rx="14" fill="{t["bg"]}"/>',
           f'<rect x="40" y="34" width="3" height="20" rx="1.5" fill="{t["acc"]}"/>',
           text(56, 51, "os-xgs-npu &#8212; where it stands", 20, t["fg"], 700),
           text(56, 74, "WHAT RUNS ON EACH APPLIANCE, AND HOW FAR ALONG IT IS", 11.5, t["kk"],
                mono=True, extra=' letter-spacing="1.4"'),
           f'<rect x="672" y="33" width="188" height="28" rx="14" fill="none" stroke="{t["wip"]}" stroke-width="1.4"/>',
           text(766, 52, "EXPERIMENTAL", 11.5, t["wip"], 700, anchor="middle", mono=True, extra=' letter-spacing="1.6"'),
           stage_track(t),
           card(40, CARDS[0], t),
           card(460, CARDS[1], t)]
    out.append(text(40, NOTE_Y, "&#9671; Vendor figures are from its datasheets: Ixia lab load, many tunnels across all ports, its own firmware. "
                    "Figures here are one TCP stream ending on the appliance&#8217;s host.", 11.5, t["sub"]))
    for i, (name, desc) in enumerate(FAMILIES):
        fx = 40 + i * 280
        out.append(f'<rect x="{fx}" y="{FAM_Y}" width="260" height="52" rx="10" fill="none" stroke="{t["line"]}" stroke-dasharray="4 4"/>')
        out.append(state_icon(fx + 22, FAM_Y + 20, "no", t))
        out.append(text(fx + 40, FAM_Y + 24, name, 13, t["fg"], 600))
        out.append(text(fx + 40, FAM_Y + 42, desc, 11.5, t["sub"]))
    for i, (big, small) in enumerate(STATS):
        sx = 40 + i * 280
        out.append(text(sx, STAT_Y + 26, big, 22, t["acc"], 700))
        out.append(text(sx, STAT_Y + 48, small, 12, t["sub"]))
    out.append("</svg>")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    for theme in THEMES:
        pathlib.Path("assets", f"status-{theme}.svg").write_text(build(theme), encoding="utf-8")
    print(f"wrote assets/status-dark.svg and assets/status-light.svg ({W}x{H})")
