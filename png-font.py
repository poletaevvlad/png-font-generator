import click
from PIL import Image
import aggdraw

horizontal_alignment = dict(left=0.0, center=0.5, right=1.0)
vertical_alignment = dict(top=0.0, center=0.5, bottom=1.0)


@click.command()
@click.argument("input", type=click.File("r"))
@click.argument("output", type=click.File("wb"))
@click.option("--font", "-f", help="TTF font file", required=True)
@click.option("--size", "-s", help="Font size", default=14)
@click.option("--cell-width", "-w", help="Cell width", default=24)
@click.option("--cell-height", "-h", help="Cell height", default=24)
@click.option("--v-align", help="Vertical alignment", default="center",
              type=click.Choice(["top", "center", "bottom"]))
@click.option("--h-align", help="Horizontal alignment", default="center",
              type=click.Choice(["left", "center", "right"]))
@click.option("--color", help="Text color in RGBA format", nargs=4,
              type=click.IntRange(min=0, max=255), default=(0, 0, 0, 255))
@click.option("--background", help="Background color in RGBA format", nargs=4,
              type=click.IntRange(min=0, max=255), default=(0, 0, 0, 0))
@click.option("--debug", default=False, help="Enables drawing grid line",
              is_flag=True)
def main(input, output, font, size, cell_width, cell_height, v_align, h_align,
         color, background, debug):
    """
    Bitmap font generator with uniform character spacing.

    This script generates png image divided into uniformly spaced 'cells' in
    which the characters are rendered. The set of characters is loaded from
    text file. The order of characters and line breaks is preserved.
    """
    text = input.read()
    input.close()

    max_columns = 0
    lines = list()
    line = ""
    for char in text:
        if char == "\n" or char == "\r":
            if len(line) > 0:
                lines.append(line)
                if max_columns < len(line):
                    max_columns = len(line)
                line = ""
        else:
            line += char
    if line != "":
        lines.append(line)
        if max_columns < len(line):
                    max_columns = len(line)

    canvas_size = (max_columns * cell_width, len(lines) * cell_height)
    image = Image.new("RGBA", canvas_size, background)
    font = aggdraw.Font(color, font, size)
    draw = aggdraw.Draw(image)

    if debug:
        pen = aggdraw.Pen((255, 0, 255, 255))
        for x in range(0, max_columns * cell_width, cell_width):
            draw.line((x + 0.5, 0, x + 0.5, canvas_size[1]), pen)
        for y in range(0, len(lines) * cell_height, cell_height):
            draw.line((0, y + 0.5, canvas_size[0], y + 0.5), pen)

    y = 0
    for row in lines:
        x = 0
        for char in row:
            tsize = draw.textsize(char, font)
            tx = x + (cell_width - tsize[0]) * horizontal_alignment[h_align]
            ty = y + (cell_height - tsize[1]) * vertical_alignment[v_align]
            draw.text((tx, ty), char, font)
            x += cell_width
        y += cell_height
    draw.flush()
    image.save(output, "PNG")


if __name__ == "__main__":
    main()
