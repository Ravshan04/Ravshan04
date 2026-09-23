from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONT_DIR = Path("C:/Windows/Fonts")

BG = "#0d1117"
PANEL = "#111a23"
BORDER = "#334155"
MUTED = "#91a4b8"
WHITE = "#edf6fa"
GREEN = "#47e0aa"
CYAN = "#6ee7f9"
AMBER = "#f8c768"


def font(size: int, bold: bool = False):
    path = FONT_DIR / ("consolab.ttf" if bold else "consola.ttf")
    return ImageFont.truetype(str(path), size)


def base(size):
    image = Image.new("RGB", size, BG)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1, 1, size[0] - 2, size[1] - 2), radius=7, outline=BORDER, width=2)
    return image, draw


def save_gif(frames, path, duration=100):
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0,
        optimize=True,
        disposal=2,
    )


def terminal_frame(step):
    image, draw = base((960, 280))
    draw.rectangle((2, 2, 957, 42), fill=PANEL)
    draw.line((2, 43, 957, 43), fill=BORDER, width=2)
    for x, color in ((23, "#fa7185"), (44, AMBER), (65, GREEN)):
        draw.ellipse((x - 5, 17, x + 5, 27), fill=color)
    draw.text((382, 14), "ravshan@github: ~", font=font(17), fill=MUTED)

    draw.text((38, 71), "$ whoami", font=font(21), fill=GREEN)
    draw.text((38, 111), "Ravshanbek Nazarov", font=font(52, bold=True), fill=WHITE)

    roles = ("C# / .NET engineer", "DevOps / infrastructure", "AI & developer tooling")
    phase = (step % 90) / 30
    role = roles[int(phase)]
    part = phase % 1
    if part < 0.4:
        count = int(len(role) * part / 0.4)
    elif part < 0.8:
        count = len(role)
    else:
        count = int(len(role) * (1 - (part - 0.8) / 0.2))
    typed = role[:count]
    draw.text((39, 190), "> " + typed, font=font(25), fill=CYAN)
    cursor_x = 39 + draw.textlength("> " + typed, font=font(25)) + 4
    if step % 10 < 7:
        draw.rectangle((cursor_x, 193, cursor_x + 12, 218), fill=GREEN)

    draw.text((39, 241), "Tashkent, Uzbekistan", font=font(17), fill=MUTED)
    draw.rectangle((643, 253, 920, 257), fill=BORDER)
    draw.rectangle((643, 253, 643 + int(277 * (step % 90) / 89), 257), fill=GREEN)
    return image


def pipeline_frame(step):
    image, draw = base((960, 145))
    draw.text((32, 15), "$ route --from idea --to production", font=font(19), fill=GREEN)

    nodes = ((148, "BACKEND", GREEN), (480, "INFRA", CYAN), (812, "TOOLS", AMBER))
    signal_x = 148 + (664 * (step % 60) / 59)
    draw.line((148, 120, 812, 120), fill=BORDER, width=3)
    draw.line((148, 120, signal_x, 120), fill=CYAN, width=3)

    for x, label, color in nodes:
        active = abs(signal_x - x) < 95
        draw.line((x, 103, x, 119), fill=color if active else BORDER, width=2)
        draw.rounded_rectangle((x - 116, 57, x + 116, 103), radius=5, fill=PANEL, outline=color if active else BORDER, width=2)
        label_width = draw.textlength(label, font=font(20, bold=True))
        draw.text((x - label_width / 2, 68), label, font=font(20, bold=True), fill=color if active else MUTED)

    draw.ellipse((signal_x - 6, 114, signal_x + 6, 126), fill=WHITE)
    return image


def main():
    ASSETS.mkdir(exist_ok=True)
    save_gif([terminal_frame(step) for step in range(90)], ASSETS / "terminal.gif")
    save_gif([pipeline_frame(step) for step in range(60)], ASSETS / "pipeline.gif")


if __name__ == "__main__":
    main()
