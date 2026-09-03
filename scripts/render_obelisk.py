#!/usr/bin/env python3
"""Рендер «Обелиска OSI»: центральный шпиль-треугольник с рунами уровней,
малые обелиски по бокам и вдали. Данные - config/osi.json.

Запуск:  python scripts/render_obelisk.py
Результат:  assets/obelisk.svg
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "osi.json"
OUT = ROOT / "assets" / "obelisk.svg"

# Геометрия
W = 1000
H = 560
M = 40              # отступ слева для подписей уровней
CX = 500
TIP_Y = 48          # вершина шпиля
BASE_Y = 490        # базовая линия, на которой всё стоит
HW_TOP = 4          # полуширина шпиля у вершины
HW_BASE = 62        # полуширина у основания
SEG_TOP = 128       # верх зоны уровней


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def hw(y: float) -> float:
    # полуширина шпиля на высоте y
    t = (y - TIP_Y) / (BASE_Y - TIP_Y)
    return HW_TOP + (HW_BASE - HW_TOP) * t


def wrap_protocols(text: str, limit: int = 32) -> list:
    # одна строка, если влезает; иначе сбалансированный перенос на две
    if len(text) <= limit:
        return [text]
    words = text.split(" · ")
    best, best_diff = None, None
    for i in range(1, len(words)):
        a = " · ".join(words[:i])
        b = " · ".join(words[i:])
        diff = abs(len(a) - len(b))
        if best_diff is None or diff < best_diff:
            best, best_diff = [a, b], diff
    return best


def main() -> None:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    p = data["palette"]
    layers = sorted(data["layers"], key=lambda l: -l["level"])
    domain = set(data.get("domain", [2, 3, 4, 5, 6, 7]))

    out = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" '
        'font-family="\'JetBrains Mono\',\'Fira Code\',Consolas,monospace">'
    )
    out.append("<defs>")
    out.append('<linearGradient id="spire" x1="0" y1="0" x2="0" y2="1">'
               f'<stop offset="0" stop-color="#151B2A"/>'
               f'<stop offset="1" stop-color="#0C0F16"/></linearGradient>')
    out.append('<filter id="soft" x="-60%" y="-60%" width="220%" height="220%">'
               '<feGaussianBlur stdDeviation="26"/></filter>')
    out.append("</defs>")
    out.append(f'<rect width="{W}" height="{H}" rx="12" fill="{p["bg"]}"/>')

    # варп-аура за шпилем (размытая, края диска не видны)
    out.append(
        f'<circle cx="{CX}" cy="270" r="200" fill="{p["warp_purple"]}" opacity="0.09" filter="url(#soft)">'
        '<animate attributeName="opacity" values="0.09;0.13;0.09" dur="8s" repeatCount="indefinite"/>'
        "</circle>"
    )
    out.append(
        f'<circle cx="{CX}" cy="270" r="120" fill="{p["warp_purple"]}" opacity="0.06" filter="url(#soft)"/>'
    )

    # малые обелиски по бокам и вдали: (cx, tip_y, полуширина, цвет, точка на вершине)
    minor = [
        (150, 258, 16, "#0D1017", True),
        (255, 338, 11, "#10141C", False),
        (745, 338, 11, "#10141C", False),
        (850, 258, 16, "#0D1017", True),
    ]
    for x, ty, hwd, color, dot in minor:
        out.append(
            f'<polygon points="{x - hwd},{BASE_Y} {x},{ty} {x + hwd},{BASE_Y}" fill="{color}"/>'
        )
        if dot:
            out.append(
                f'<circle cx="{x}" cy="{ty + 4}" r="1.6" fill="{p["terminal_green"]}" opacity="0.5">'
                '<animate attributeName="opacity" values="0.5;0.15;0.5" dur="5s" repeatCount="indefinite"/>'
                "</circle>"
            )

    # базовая линия + зелёное свечение под шпилем
    out.append(f'<rect x="60" y="{BASE_Y}" width="880" height="1" fill="#1A1E26"/>')
    out.append(
        f'<ellipse cx="{CX}" cy="{BASE_Y}" rx="110" ry="6" fill="{p["terminal_green"]}" '
        f'opacity="0.08" filter="url(#soft)"/>'
    )

    # центральный шпиль
    out.append(
        f'<polygon points="{CX},{TIP_Y} {CX + HW_BASE},{BASE_Y} {CX - HW_BASE},{BASE_Y}" '
        'fill="url(#spire)" stroke="#1C2230" stroke-width="1"/>'
    )
    out.append(
        f'<line x1="{CX}" y1="{TIP_Y}" x2="{CX - HW_BASE}" y2="{BASE_Y}" '
        f'stroke="{p["warp_purple"]}" stroke-width="1" opacity="0.25"/>'
    )
    out.append(
        f'<line x1="{CX}" y1="{TIP_Y}" x2="{CX + HW_BASE}" y2="{BASE_Y}" '
        f'stroke="{p["teal"]}" stroke-width="1" opacity="0.4"/>'
    )

    # светящаяся вершина
    out.append(
        f'<circle cx="{CX}" cy="{TIP_Y + 6}" r="7" fill="{p["terminal_green"]}" '
        f'opacity="0.18" filter="url(#soft)">'
        '<animate attributeName="opacity" values="0.1;0.32;0.1" dur="5s" repeatCount="indefinite"/>'
        "</circle>"
    )

    # уровни: сегменты шпиля, у каждого подпись слева и протоколы справа
    seg_h = (BASE_Y - SEG_TOP) / len(layers)
    for i, layer in enumerate(layers):
        y_top = SEG_TOP + i * seg_h
        yc = y_top + seg_h / 2
        lv = layer["level"]
        name = esc(layer["name"])
        mine = lv in domain

        if mine:
            # граница сегмента поперёк шпиля
            hwd = hw(y_top)
            out.append(
                f'<line x1="{CX - hwd:.1f}" y1="{y_top:.1f}" x2="{CX + hwd:.1f}" '
                f'y2="{y_top:.1f}" stroke="{p["teal"]}" stroke-opacity="0.3"/>'
            )
            # рунный ромб с пульсирующим ядром
            out.append(
                f'<g transform="rotate(45 {CX} {yc:.1f})">'
                f'<rect x="{CX - 5}" y="{yc - 5:.1f}" width="10" height="10" '
                f'fill="none" stroke="{p["terminal_green"]}" stroke-width="1.5" opacity="0.9"/></g>'
            )
            out.append(
                f'<circle cx="{CX}" cy="{yc:.1f}" r="2.2" fill="{p["terminal_green"]}">'
                '<animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite"/>'
                "</circle>"
            )
        else:
            # латунный фундамент: нижний сегмент шпиля
            out.append(
                f'<polygon points="{CX - hw(y_top):.1f},{y_top:.1f} {CX + hw(y_top):.1f},{y_top:.1f} '
                f'{CX + HW_BASE},{BASE_Y} {CX - HW_BASE},{BASE_Y}" fill="{p["brass"]}"/>'
            )
            out.append(
                f'<text x="{CX}" y="{(y_top + BASE_Y) / 2 + 4:.1f}" fill="#261C04" font-size="12" '
                f'font-weight="bold" letter-spacing="2" text-anchor="middle">ФУНДАМЕНТ</text>'
            )

        # подпись уровня слева
        label_color = p["terminal_green"] if mine else p["brass"]
        out.append(
            f'<text x="{M}" y="{yc + 2:.1f}" fill="{label_color}" '
            f'font-size="20" font-weight="bold">L{lv}</text>'
        )
        out.append(
            f'<text x="{M}" y="{yc + 18:.1f}" fill="{p["muted"]}" '
            f'font-size="10.5">{name}</text>'
        )

        # протоколы справа
        proto_color = p["bone"] if mine else p["brass"]
        proto_opacity = "0.9" if mine else "0.8"
        lines = wrap_protocols(layer["protocols"])
        for j, ln in enumerate(lines):
            ly = yc + 4 if len(lines) == 1 else yc - 3 + j * 16
            size = 12.5 if len(lines) == 1 else 11.5
            out.append(
                f'<text x="690" y="{ly:.1f}" fill="{proto_color}" font-size="{size}" '
                f'opacity="{proto_opacity}">{esc(ln)}</text>'
            )

    out.append("</svg>")
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"OK -> {OUT}")


if __name__ == "__main__":
    main()
