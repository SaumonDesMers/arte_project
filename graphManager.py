from platform import platform
from tkinter import *
from tkinter import ttk
import winManager as wm
from PIL import Image, EpsImagePlugin, ImageDraw, ImageTk, ImageFont
import platform

EpsImagePlugin.gs_windows_binary = r'C:\Program Files\gs\gs10.00.0\bin\gswin64c.exe'


def create():
	global graph
	graph = {
		"frame": None,
		"canvas": None,
		"data": [],
		"width": 800,
		"height": 800,
		"image": None,
		"draw": None,
	}
	
	# Create the graph frame
	graph["frame"] = ttk.Frame(wm.root)
	graph["frame"].pack(expand=1)

	# Create the canvas
	graph["canvas"] = Canvas(graph["frame"], bg="white", width=graph["width"], height=graph["height"])
	graph["canvas"].pack()

	# create the PIL image
	graph["image"] = Image.new("RGB", (graph["width"], graph["height"]))
	graph["draw"] = ImageDraw.Draw(graph["image"])

	global txtFont
	fontName = ""
	if platform.system() == "Windows":
		fontName = "Arial.ttf"
	elif platform.system() == "Linux":
		fontName = "noto-sans/NotoSans-Regular.ttf"
	txtFont = ImageFont.truetype(fontName, 20)
	
	# bind the mouse wheel event
	# graph["canvas"].bind("<MouseWheel>", mouseWheel)


# draw the graph
def update():
	noColor = ["lightgrey"] * 12
	width = 15
	sep = 5
	r = 150

	# clear the draw
	graph["draw"].rectangle((0, 0, graph["width"], graph["height"]), fill="white")

	# draw the raw
	for i, plant in enumerate(graph["data"]):
		color = [plant["flowering"][0]["color"]] * 12
		drawRaw(
			draw = graph["draw"],
			x = graph["width"]/2,
			y = graph["height"]/2,
			r = r+i*(sep+width),
			width = width,
			color = color,
			name = plant["name"]
		)

	# draw months name
	months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
	for i in range(0, 12):
		month = rotateText(months[i], -90)
		graph["image"].paste(month, (graph["width"]/2-r-20, graph["height"]/2-r+i*(sep+width)+width/2-month.size[1]/2))
	
	# save the image
	graph["image"].save("graph.png", "PNG")

	# print the image in canvas
	tkImg = ImageTk.PhotoImage(graph["image"])
	graph["canvas"].create_image(0, 0, image=tkImg, anchor="nw")


# create text in temporary image and rotate it
def rotateText(text, angle):
	# create the temporary image
	tmpImg = Image.new("RGB", (500, 500))
	tmpDraw = ImageDraw.Draw(tmpImg)

	# draw the text
	tmpDraw.text((0, 0), text, fill="black", font=txtFont)

	# rotate the image
	tmpImg = tmpImg.rotate(angle, expand=1)

	# crop the image
	tmpImg = tmpImg.crop(tmpImg.getbbox())

	return tmpImg

# draw a raw for each plant
def drawRaw(draw, x, y, r, width, color, name):
	arcLen = 20.7
	for i in range(0, 12):
		start = -90 + i * (arcLen + 2)
		circular_arc(draw, x, y, r, start, arcLen, width, color[i])

	draw.text((x-5-txtFont.getlength(text=name), y-r), name, fill="black", font=txtFont)

# draw a circular arc for each month
def circular_arc(draw, x, y, r, start, arcLen, width, color):
	draw.arc((x-r, y-r, x+r, y+r), start, start+arcLen, fill=color, width=width)

# mouse wheel event
def mouseWheel(event):
	global canvas
	# resize the canvas
	if event.delta > 0:
		graph["width"] *= 1.1
		graph["height"] *= 1.1
	else:
		graph["width"] *= 0.9
		graph["height"] *= 0.9
	graph["canvas"].config(width=graph["width"], height=graph["height"])

def addPlant(plant):
	global graph
	graph["data"].append(plant)
	update()

def removePlant(plant):
	global graph
	graph["data"].remove(plant)
	update()
