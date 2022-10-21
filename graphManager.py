from tkinter import *
from tkinter import ttk
import winManager as wm
from PIL import Image, EpsImagePlugin, ImageDraw, ImageTk, ImageFont

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
	
	# save the image
	graph["image"].save("graph.png", "PNG")

	# print the image in canvas
	tkImg = ImageTk.PhotoImage(graph["image"])
	graph["canvas"].create_image(0, 0, image=tkImg, anchor="nw")

# draw a raw for each plant
def drawRaw(draw, x, y, r, width, color, name):
	arcLen = 20.7
	for i in range(0, 12):
		start = -90 + i * (arcLen + 2)
		circular_arc(draw, x, y, r, start, arcLen, width, color[i])

	font = ImageFont.truetype("arial.ttf", 15)
	draw.text((x-5-font.getlength(text=name), y-r), name, fill="black", font=font)

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
