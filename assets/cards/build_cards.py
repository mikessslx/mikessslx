"""Generate the Featured projects cards for the profile README."""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent

W, H = 772, 226
SPLIT = 456

THEMES = {
    "light": {
        "bg": "#FFFFFF",
        "border": "#D8D2C2",
        "name": "#121D3E",
        "text": "#4A5266",
        "venue": "#B03B28",
        "metric": "#B03B28",
        "label": "#6B7285",
        "tag_text": "#5E5440",
        "tag_border": "#C9BFA6",
        "rule": "#E4DED0",
        "bar": "#121D3E",
    },
    "dark": {
        "bg": "#121D3E",
        "border": "#2A3760",
        "name": "#FFFFFF",
        "text": "#C9CEDA",
        "venue": "#E0846F",
        "metric": "#E0846F",
        "label": "#A3AABB",
        "tag_text": "#D6CBAE",
        "tag_border": "#847652",
        "rule": "#2E3B66",
        "bar": "#847652",
    },
}

PROJECTS = [
    {
        "slug": "mathtec",
        "name": "MathTEC",
        "venue": "IEEE ICCCS 2026",
        "desc": "Multi-agent framework for mathematical text error correction, with the MathTEC-Bench dataset.",
        "cut": 6,
        "tags": ["Python", "Multi-agent LLMs", "MathJax"],
        "metrics": [
            ("92.4%", "char-F1"),
            ("88.4%", "sentence accuracy"),
            (">3 pts", "over single prompt"),
        ],
    },
    {
        "slug": "mathcorrector",
        "name": "MathCorrector",
        "venue": "ACM CAMMIC 2026",
        "desc": "QLoRA specialization of Qwen2.5-Math-7B-Instruct for mathematical text error correction.",
        "tags": ["PyTorch", "Transformers", "QLoRA"],
        "metrics": [
            ("0.958", "F0.5"),
            ("0.900", "exact match"),
            ("0.0014", "character error rate"),
        ],
    },
    {
        "slug": "knot-studio",
        "name": "Knot Studio",
        "venue": "Live demo at knot.cc.cd",
        "desc": "Quandle coloring and 2-cocycle invariants for distinguishing prime knots with fewer than 10 crossings.",
        "tags": ["Python", "Flask", "Integer programming"],
        "metrics": [
            ("84", "prime knots"),
            ("2,947", "candidate quandles"),
            ("13", "minimum quandles"),
        ],
    },
]

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
SERIF = "'Palatino Linotype', Palatino, 'Book Antiqua', Georgia, serif"


def tag_width(text):
    return round(len(text) * 6.9 + 22)


def wrap(text, cut=None):
    words = text.split()
    if cut is None:
        if len(words) < 8:
            return [text]
        cut = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
    return [" ".join(words[:cut]), " ".join(words[cut:])]


def card(p, t):
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(p["name"])}">',
        f'<title>{escape(p["name"])}</title>',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<rect x="0.5" y="28" width="4" height="{H - 56}" fill="{t["bar"]}"/>',
        f'<text x="36" y="48" font-family="{SANS}" font-size="13" font-weight="600" letter-spacing="0.2" fill="{t["venue"]}">{escape(p["venue"])}</text>',
        f'<text x="36" y="88" font-family="{SERIF}" font-size="32" font-weight="700" fill="{t["name"]}">{escape(p["name"])}</text>',
    ]
    for i, line in enumerate(wrap(p["desc"], p.get("cut"))):
        out.append(f'<text x="36" y="{122 + i * 22}" font-family="{SANS}" font-size="15" fill="{t["text"]}">{escape(line)}</text>')
    x = 36
    for tag in p["tags"]:
        w = tag_width(tag)
        out.append(f'<rect x="{x}" y="164" width="{w}" height="24" rx="12" fill="none" stroke="{t["tag_border"]}"/><text x="{x + w / 2}" y="180.5" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{t["tag_text"]}">{escape(tag)}</text>')
        x += w + 8
    out.append(f'<line x1="{SPLIT}" y1="36" x2="{SPLIT}" y2="{H - 36}" stroke="{t["rule"]}"/>')
    for i, (value, label) in enumerate(p["metrics"]):
        y = 74 + i * 50
        out.append(f'<text x="{SPLIT + 36}" y="{y}" font-family="{SERIF}" font-size="28" font-weight="700" fill="{t["metric"]}">{escape(value)}</text><text x="{SPLIT + 150}" y="{y - 2}" font-family="{SANS}" font-size="13" fill="{t["label"]}">{escape(label)}</text>')
    out.append("</svg>\n")
    return "\n".join(out)


if __name__ == "__main__":
    for p in PROJECTS:
        for mode, theme in THEMES.items():
            (OUT / f'{p["slug"]}-{mode}.svg').write_text(card(p, theme), encoding="utf-8")
    print(f"wrote {len(PROJECTS) * len(THEMES)} cards to {OUT}")
