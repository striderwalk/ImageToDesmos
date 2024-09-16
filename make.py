from PIL import Image, ImageDraw

image = Image.new("RGB", (200, 200))
draw = ImageDraw.Draw(image)
draw.circle((100, 100), 50)

image.save("circle.png")
