from re import S
from turtle import color
from PIL import Image, ImageDraw, ImageChops
import random as r
import colorsys







def random_color():
    h = r.random()
    s = 1
    v = 1


    float_rgb = colorsys.hsv_to_rgb(h,s,v)

    rgb = [int(x * 255) for x in float_rgb]


    return  tuple(rgb)






def interpolate(start_color, end_color, factor: float):
    recip = 1 - factor
    return(
        int(start_color[0] * recip + end_color[0] * factor),
        int(start_color[1] * recip + end_color[1] * factor),
        int(start_color[2] * recip + end_color[2] * factor)
    )


def generate_art(path: str):
    print("generating image")
    target_size = 256
    scale_fator = 2
    image_size = target_size * scale_fator
    padding_px = 16
    imagebgc = (0,0,0)
    start_color = random_color()
    end_color = random_color()
    lines = 10
    image = Image.new("RGB", size = (image_size, image_size), color = imagebgc)


    draw = ImageDraw.Draw(image)

    points = []



    #generate points
    for _ in range(lines):
        random_point = r.randint(padding_px, image_size-padding_px), r.randint(padding_px, image_size-padding_px)
        
        points.append(random_point)


    #bounding box
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])


    draw.rectangle((min_x, min_y, max_x, max_y), outline=(230,230,230))

    #center image
    delta_x = min_x - (image_size - max_x)
    delta_y = min_y - (image_size - max_y)

    for i, point in enumerate(points):
        points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)

    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    draw.rectangle((min_x, min_y, max_x, max_y), outline=(random_color()))

    #plot points
    thickness = 0
    n_points = len(points) -1
    for i, point in enumerate(points):

        #overlay canvas
        overlay_image = Image.new("RGB", size = (image_size, image_size), color = imagebgc)

        overlay_draw = ImageDraw.Draw(overlay_image)


        p1 = point

        if i == n_points:
            p2 = points[0]
        else:
            p2 = points[i - 1]


        line_xy = (p1,p2)
        color_factor = i/n_points
        line_color = interpolate(start_color, end_color, color_factor)
        thickness += scale_fator
        overlay_draw.line(line_xy, fill=line_color, width=thickness)
        image = ImageChops.add(image, overlay_image)

    image = image.resize((target_size,target_size), resample=Image.ANTIALIAS)
    image.save(path)



if __name__ == "__main__":
    for i in range(10):
        generate_art(f"text_image{i}.png")
