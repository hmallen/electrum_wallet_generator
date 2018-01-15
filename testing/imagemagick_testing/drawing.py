from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

test_file = 'draw-arc.gif'


def draw_arc():
    with Drawing() as draw:
        draw.stroke_color = Color('black')
        draw.stroke_width = 2
        draw.fill_color = Color('white')
        draw.arc(( 25, 25),  # Stating point
                 ( 75, 75),  # Ending point
                 (135,-45))  # From bottom left around to top right
        with Image(width=100,
                   height=100,
                   background=Color('lightblue')) as img:
            draw.draw(img)
            img.save(filename=test_file)


if __name__ == '__main__':
    draw_arc()
