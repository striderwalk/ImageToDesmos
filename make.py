from PIL import Image, ImageDraw

image = Image.new("RGB", (50, 50))
draw = ImageDraw.Draw(image)
draw.line([(0, 0), (0, 50)])
draw.line([(10, 0), (10, 50)])
draw.line([(20, 0), (20, 50)])
draw.line([(30, 0), (30, 50)])
draw.line([(40, 0), (40, 50)])

draw.line([(0, 0), (50, 0)])
draw.line([(0, 10), (50, 10)])
draw.line([(0, 20), (50, 20)])
draw.line([(0, 30), (50, 30)])
draw.line([(0, 40), (50, 40)])


image.save("line_cross.png")
