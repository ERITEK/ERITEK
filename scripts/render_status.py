#!/usr/bin/env python3
"""Рендер «System Status»: карта галактики + счётчик дней аптайма.

Запуск:  python scripts/render_status.py
Результат:  assets/system-status.svg
Дни считаются с 2025-11-05, экшен перегенерирует файл раз в сутки.
"""
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "system-status.svg"

UPTIME_START = date(2025, 11, 5)

BG = "#0A0C10"
PANEL = "#12151C"
FRAME = "#1C2230"
BONE = "#E6E1D0"
MUTED = "#8A8577"
GREEN = "#33FF66"
PURPLE = "#C77DFF"
TEAL = "#2ED1C0"

# звёзды на карте: (x, y, r, opacity, color)
STARS = [
    (70, 100, 1.0, 0.45, BONE), (95, 210, 1.0, 0.35, BONE),
    (130, 90, 1.2, 0.5, BONE), (160, 250, 1.0, 0.3, BONE),
    (185, 170, 1.1, 0.4, BONE), (240, 90, 1.2, 0.5, BONE),
    (265, 230, 1.0, 0.35, BONE), (290, 150, 1.1, 0.45, BONE),
    (315, 105, 1.2, 0.5, BONE), (340, 240, 1.0, 0.3, BONE),
    (355, 160, 1.1, 0.4, BONE), (395, 130, 1.2, 0.5, BONE),
    (415, 210, 1.0, 0.35, BONE), (60, 160, 1.0, 0.35, BONE),
    (120, 270, 1.0, 0.3, BONE), (200, 260, 1.0, 0.3, BONE),
    (250, 180, 1.1, 0.4, BONE), (310, 80, 1.2, 0.5, BONE),
    (375, 180, 1.1, 0.4, BONE), (405, 95, 1.0, 0.4, BONE),
    (430, 170, 1.0, 0.35, BONE), (80, 240, 1.0, 0.3, BONE),
    (150, 130, 1.1, 0.4, BONE), (225, 145, 1.0, 0.35, BONE),
    (360, 225, 1.0, 0.35, BONE), (95, 155, 1.0, 0.35, BONE),
    (135, 105, 1.4, 0.8, GREEN), (285, 205, 1.4, 0.8, TEAL),
    (390, 240, 1.4, 0.7, PURPLE), (250, 250, 1.3, 0.7, GREEN),
]

# узлы-миры: (x, y, имя)
NODES = [(110, 140, "TERRA"), (210, 118, "MACRAGGE"), (300, 192, "CADIA"), (372, 100, "BAAL")]
ROUTE = " ".join(f"{x},{y}" for x, y, _ in NODES)


def main() -> None:
    days = (date.today() - UPTIME_START).days

    out = []
    out.append(
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="300" '
        'viewBox="0 0 1000 300" '
        'font-family="\'JetBrains Mono\',\'Fira Code\',Consolas,monospace">'
    )
    out.append("<defs>")
    out.append('<filter id="blur18" x="-60%" y="-60%" width="220%" height="220%">'
               '<feGaussianBlur stdDeviation="18"/></filter>')
    out.append('<clipPath id="map"><rect x="40" y="76" width="400" height="214"/></clipPath>')
    out.append("</defs>")
    out.append(f'<rect width="1000" height="300" rx="12" fill="{BG}"/>')

    # заголовок + чип WARP
    out.append(
        f'<text x="40" y="44" fill="{BONE}" font-size="20" font-weight="bold" '
        f'letter-spacing="2">SYSTEM STATUS</text>'
    )
    out.append(
        f'<rect x="826" y="28" width="134" height="26" rx="13" fill="{PURPLE}" '
        f'opacity="0.1" stroke="{PURPLE}" stroke-opacity="0.5"/>'
    )
    out.append(
        f'<text x="893" y="46" fill="{PURPLE}" font-size="13" '
        f'text-anchor="middle">&#9679; WARP</text>'
    )
    out.append(f'<rect x="40" y="58" width="920" height="1" fill="{MUTED}" opacity="0.4"/>')

    # карта галактики
    out.append('<rect x="40" y="76" width="400" height="214" fill="#0B0E14"/>')
    out.append('<g clip-path="url(#map)">')
    out.append(
        f'<ellipse cx="180" cy="200" rx="95" ry="42" fill="{PURPLE}" opacity="0.07" filter="url(#blur18)"/>'
    )
    out.append(
        f'<ellipse cx="335" cy="120" rx="85" ry="38" fill="{TEAL}" opacity="0.06" filter="url(#blur18)"/>'
    )
    out.append(
        f'<ellipse cx="240" cy="165" rx="195" ry="15" fill="{PURPLE}" opacity="0.14" '
        f'filter="url(#blur18)" transform="rotate(-16 240 165)"/>'
    )
    for x, y, r, op, color in STARS:
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}" opacity="{op}"/>')
    out.append(
        f'<polyline points="{ROUTE}" fill="none" stroke="{TEAL}" stroke-opacity="0.55" '
        'stroke-width="1.2" stroke-dasharray="4 5">'
        '<animate attributeName="stroke-dashoffset" values="0;-18" dur="1.8s" repeatCount="indefinite"/>'
        "</polyline>"
    )
    for x, y, name in NODES:
        out.append(
            f'<circle cx="{x}" cy="{y}" r="7" fill="none" stroke="{GREEN}" stroke-opacity="0.4"/>'
        )
        out.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{GREEN}"/>')
        out.append(
            f'<text x="{x}" y="{y + 20}" fill="{MUTED}" font-size="8" '
            f'letter-spacing="1" text-anchor="middle">{name}</text>'
        )
    out.append("</g>")
    out.append(
        f'<rect x="40" y="76" width="400" height="214" fill="none" stroke="{FRAME}"/>'
    )
    out.append(f'<text x="54" y="94" fill="{MUTED}" font-size="9" letter-spacing="2">GALACTIC CHART</text>')

    # метрики
    def panel(x: int, y: int, label: str, value: str, value_color: str, value_size: int = 15) -> None:
        out.append(f'<rect x="{x}" y="{y}" width="235" height="52" rx="8" fill="{PANEL}" stroke="{FRAME}"/>')
        out.append(f'<text x="{x + 16}" y="{y + 20}" fill="{MUTED}" font-size="11" letter-spacing="2">{label}</text>')
        out.append(
            f'<text x="{x + 16}" y="{y + 41}" fill="{value_color}" font-size="{value_size}" '
            f'font-weight="bold">{value}</text>'
        )

    panel(470, 84, "UPTIME", f"{days} days", BONE)
    panel(717, 84, "FOCUS", "100%", GREEN)
    panel(470, 148, "COFFEE", "&#8734;", BONE, value_size=21)
    panel(717, 148, "MOOD", "Tzeentch", TEAL)

    # низ
    out.append(
        f'<text x="470" y="268" fill="{GREEN}" font-size="16" font-weight="bold" '
        f'letter-spacing="2">SYSTEMS ALL GREEN</text>'
    )
    out.append(
        f'<polyline points="690,264 718,258 746,268 774,252 802,266 830,250 858,262 886,256 914,266 942,254 960,260" '
        f'fill="none" stroke="{GREEN}" stroke-opacity="0.7" stroke-width="2"/>'
    )

    out.append("</svg>")
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"OK -> {OUT} ({days} days)")


if __name__ == "__main__":
    main()
