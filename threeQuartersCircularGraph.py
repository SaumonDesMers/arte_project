from PIL import Image, ImageDraw, ImageFont
from math import cos, radians, sin
from platform import system
from graphInterface import GraphInterface
from tkinter import ttk, colorchooser, Button
import winManager as wm


class TQCG(GraphInterface):
	"""Implementation of the three quarters circular graph."""

	def __init__(self, width=1600, height=1600):
		"""Initialize the three quarters circular graph."""
		self.data = []

		self.width = width
		self.height = height

		self.x = self.width/2
		self.y = self.height/2
		self.bgColor = "white"
		self.noColor = "lightgrey"
		self.arcWidth = 30
		self.arcLen = 20.7
		self.sep = 10
		self.radius = 300

		# create the PIL image
		self.image = Image.new("RGB", (self.width, self.height))
		self.draw = ImageDraw.Draw(self.image)

		# create the font
		fontName = ""
		if system() == "Windows":
			fontName = "arial.ttf"
		elif system() == "Linux":
			fontName = "noto-sans/NotoSans-Regular.ttf"
		self.txtFont = ImageFont.truetype(fontName, 25)
		# self.txtFont = ImageFont.load_default()


	def update(self):
		"""Update graph"""

		# sort the plants by name
		self.data.sort(key=lambda plant: plant["name"])

		# draw the background
		self.draw.rectangle((0, 0, self.width, self.height), fill=self.bgColor)

		# print the months
		self.printMonths()

		# draw the raws
		for i, plant in enumerate(self.data):
			self.drawRaw(
				r = self.radius+i*(self.sep+self.arcWidth),
				color = plant["flowering"],
				name = plant["name"]
			)
		
		# save the current image
		self.image.save("workInProgessGraph.png")

		# call the update function of the graph manager to update the graph on the screen
		wm.gm.update()


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

		return frm


	def changeBgColor(self, btn):
		"""Change the background color."""
		color = colorchooser.askcolor()[1]
		self.bgColor = color
		btn.config(bg=color)
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


	def drawRaw(self, r, color, name):
		"""Draw a raw for each plant."""
		# draw the arcs
		for i in range(12):
			start = -90 + i * (self.arcLen + 2)
			self.drawArc(r, start, color[i])

		# print the plant name
		w, h = self.draw.textsize(name, font=self.txtFont)
		self.draw.text(
			(self.x-10-w, self.y-r+self.arcWidth/2-h/2),
			name,
			fill="black",
			font=self.txtFont
		)


	def drawArc(self, r, start, color):
		"""Draw an arc."""
		self.draw.arc(
			(self.x-r, self.y-r, self.x+r, self.y+r),
			start,
			start+self.arcLen,
			fill=color if color != "" else self.noColor,
			width=self.arcWidth
		)
	

	def printMonths(self):
		months =   ["Jan", "Fev", "Mar", "Avr", "Mai", "Jun", "Jul", "Aou", "Sep", "Oct", "Nov", "Dec"]
		textRotation = -10
		imgAnglePos = -80
		for i in range(0, 12):
			img = self.rotateText(months[i], textRotation)
			w, h = img.size

			radiusToImgCenter = self.radius + len(self.data) * (self.sep+self.arcWidth) - 5
			cx = self.x + radiusToImgCenter * cos(radians(imgAnglePos))
			cy = self.y + radiusToImgCenter * sin(radians(imgAnglePos))
			x = (int)(cx - w/2)
			y = (int)(cy - h/2)
			self.image.paste(img, (x, y))

			imgAnglePos += self.arcLen + 2
			textRotation -= 23


	def rotateText(self, text, angle):
		# get the text size
		w, h = self.txtFont.getsize(text)

		# create the temporary image
		tmpImg = Image.new("RGB", (w, h))
		tmpDraw = ImageDraw.Draw(tmpImg)

		# fill the background with white
		tmpDraw.rectangle((0, 0, w, h), fill=self.bgColor)

		# draw the text
		tmpDraw.text((0, 0), text, fill="black", font=self.txtFont)

		# rotate the image
		tmpImg = tmpImg.rotate(angle, expand=1, fillcolor=self.bgColor)

		return tmpImg


	def addPlant(self, plant):
		"""Add a plant to the graph."""
		self.data.append(plant)
	

	def removePlant(self, plant):
		"""Remove a plant from the graph."""
		self.data.remove(plant)
	

	def getImage(self) -> Image:
		"""(Interface) Return the graph PIL image"""
		return self.image
	