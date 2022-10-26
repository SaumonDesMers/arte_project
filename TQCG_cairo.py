from pydoc import plain
from PIL import Image, ImageDraw, ImageFont, ImageColor
from math import cos, radians, sin
from platform import system
from graphInterface import GraphInterface
from tkinter import StringVar, ttk, colorchooser, Button
import winManager as wm
import cairo


class TQCG_cairo(GraphInterface):
	"""Implementation of the three quarters circular graph (SVG)."""

	def __init__(self):
		"""Initialize the three quarters circular graph."""
		self.data = []

		self.width = 1600
		self.height = 1600

		self.x = self.width/2
		self.y = self.height/2
		self.bgColor = "#ffffff"
		self.noColor = "#d3d3d3"
		self.arcWidth = 30
		self.arcLen = 20.7
		self.sep = 10
		self.radius = 300
		self.fontSize = 30

		# create the cairo svg surface
		self.surface = cairo.SVGSurface("workInProgress.svg", self.width, self.height)
		self.ctx = cairo.Context(self.surface)
	
		# create the font
		fontName = ""
		if system() == "Windows":
			fontName = "Arial"
		elif system() == "Linux":
			fontName = "FreeSans"
		self.txtFont = cairo.ToyFontFace(fontName)
	

	def update(self):
		"""Update graph"""

		# sort the plants by name
		self.data.sort(key=lambda plant: plant["name"])

		# draw the background
		# print("drawing background: ", self.hexToRGB(self.bgColor))
		self.ctx.set_source_rgb(*self.hexToRGB(self.bgColor, 255))
		self.ctx.rectangle(0, 0, self.width, self.height)
		self.ctx.fill()

		# print the month
		self.printMonth()

		# draw the raws
		for i, plant in enumerate(self.data):
			self.drawRaw(
				r = self.radius + i * (self.arcWidth + self.sep),
				color = plant["flowering"],
				name = plant["name"]
			)

		# save the image
		self.surface.write_to_png("workInProgress.png")

		# call the update function of the graph manager to update the graph on the screen
		wm.gm.update()

		pass


	def save(self, path):
		"""Save the graph."""
		self.surface.write_to_png(path)

	
	def export(self, path=".svg"):
		"""Export the graph with the given path and format."""
		if path.endswith(".png"):
			self.surface.write_to_png(path)
		elif path.endswith(".svg"):
			self.surface.finish()
	

	def createParamMenu(self, parent):
		"""Create the parameter menu"""
		frm = ttk.Frame(parent)

		# create the background color button
		ttk.Label(frm, text="Background:").grid(row=0, column=0, sticky="w")
		bgColorBtn = Button(frm, bg=self.bgColor, width=5, command=lambda: self.changeBgColor(bgColorBtn))
		bgColorBtn.grid(row=0, column=1, sticky="w")

		# create the no color button
		ttk.Label(frm, text="No color:").grid(row=1, column=0, sticky="w")
		noColorBtn = Button(frm, bg=self.noColor, width=5, command=lambda: self.changeNoColor(noColorBtn))
		noColorBtn.grid(row=1, column=1, sticky="w")

		# create the scale for the radius
		ttk.Label(frm, text="Radius:").grid(row=2, column=0, sticky="w")
		radiusScale = ttk.Scale(frm, from_=100, to=500, orient="horizontal", command=lambda event: self.changeRadius(radiusScale))
		radiusScale.set(self.radius)
		radiusScale.grid(row=2, column=1, sticky="w")

		# create the scale for the arc width
		ttk.Label(frm, text="Arc width:").grid(row=3, column=0, sticky="w")
		arcWidthScale = ttk.Scale(frm, from_=10, to=50, orient="horizontal", command=lambda event: self.changeArcWidth(arcWidthScale))
		arcWidthScale.set(self.arcWidth)
		arcWidthScale.grid(row=3, column=1, sticky="w")

		# create the entry for font size
		ttk.Label(frm, text="Font size:").grid(row=4, column=0, sticky="w")
		fontSizeVar = StringVar()
		fontSizeVar.set(self.fontSize)
		ttk.Entry(frm, textvariable=fontSizeVar).grid(row=4, column=1, sticky="w")
		fontSizeVar.trace_add("write", lambda *args: self.changeFontSize(fontSizeVar))

		return frm


	def changeBgColor(self, btn):
		"""Change the background color."""
		color = colorchooser.askcolor()[1]
		self.bgColor = color
		btn.config(bg=color)
		print("bg color changed to", color)
		self.update()


	def changeNoColor(self, btn):
		"""Change the no color."""
		color = colorchooser.askcolor()[1]
		self.noColor = color
		btn.config(bg=color)
		self.update()


	def changeRadius(self, scale):
		"""Change the radius."""
		self.radius = int(scale.get())
		self.update()


	def changeArcWidth(self, scale):
		"""Change the arc width."""
		self.arcWidth = int(scale.get())
		self.update()


	def changeFontSize(self, var):
		"""Change the font size."""
		size = var.get()
		if size.isdigit() and int(size) > 0:
			self.fontSize = int(size)
			self.update()


	def drawRaw(self, r, color, name):
		"""Draw a raw for each plant."""
		# draw the arcs
		for i in range(12):
			start = -90 + i * (self.arcLen + 2)
			self.drawArc(r, start, color[i])
		
		# get text size
		self.ctx.set_font_face(self.txtFont)
		self.ctx.set_font_size(self.fontSize)
		x_bearing, y_bearing, width, height, x_advance, y_advance = self.ctx.text_extents(name)

		# print the plant name
		self.ctx.new_path()
		self.ctx.set_source_rgb(0, 0, 0)
		self.ctx.move_to(self.x-10-width, self.y-r+height/2)
		self.ctx.show_text(name)
	

	def drawArc(self, radius, start, color):
		"""Draw an arc."""
		# draw the arc
		self.ctx.new_path()
		self.ctx.set_line_width(self.arcWidth)
		self.ctx.set_source_rgb(*self.hexToRGB(color if color else self.noColor, 255))
		self.ctx.arc(self.x, self.y, radius, radians(start), radians(start + self.arcLen))
		self.ctx.stroke()


	def printMonth(self):
		"""Print the month."""
		months = ["Jan", "Fev", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
		textRotation = 10
		anglePos = -80

		self.ctx.new_path()
		self.ctx.set_source_rgb(0, 0, 0)
		self.ctx.set_font_face(self.txtFont)
		self.ctx.set_font_size(self.fontSize)
		for i in range(12):
			x_bearing, y_bearing, width, height, x_advance, y_advance = self.ctx.text_extents(months[i])
			self.ctx.save()
			radiusToTextCenter = self.radius + len(self.data) * (self.sep+self.arcWidth) - 5
			cx = self.x + radiusToTextCenter * cos(radians(anglePos + i * (self.arcLen + 2)))
			cy = self.y + radiusToTextCenter * sin(radians(anglePos + i * (self.arcLen + 2)))
			self.ctx.translate(cx, cy)
			self.ctx.rotate(radians(textRotation + i * 23))
			self.ctx.move_to(-width/2, 0)
			self.ctx.show_text(months[i])
			self.ctx.restore()


	def removePlant(self, plant):
		"""Remove a plant from the graph."""
		self.data.remove(plant)


	def addPlant(self, plant):
		"""Add a plant to the graph."""
		self.data.append(plant)


	def getImage(self) -> Image:
		"""Get the image with PIL library."""
		return Image.open("workInProgress.png")


	def hexToRGB(self, hexColor, mod=1):
		"""Convert a hex color to a rgb color."""
		r, g, b = hexColor[1:3], hexColor[3:5], hexColor[5:7]
		return (int(r, 16)/mod, int(g, 16)/mod, int(b, 16)/mod)
