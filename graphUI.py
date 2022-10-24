from tkinter import *
from tkinter import ttk
import winManager as wm
from PIL import Image, ImageTk
from graphInterface import GraphInterface

class GraphUI:
	"""Class responsible for managing the canvas upon which the graph is drawn."""

	# create the graph frame and canvas
	def __init__(self, width=800, height=800):

		self.graph : GraphInterface = None
		self.widht = width
		self.height = height

		self.img : ImageTk = None

		# create the graph frame
		self.frame = ttk.Frame(wm.root)
		self.frame.pack(expand=1, fill=BOTH)

		# create the menu frame
		self.menuFrm = Frame(self.frame, width=200, bg="lightgrey", relief="solid")
		self.menuFrm.pack(fill=Y, side=LEFT)

		# create the canvas frame
		self.canvasFrm = ttk.Frame(self.frame)
		self.canvasFrm.pack(expand=1, fill=Y, side=RIGHT)

		# create the canvas
		self.canvas = Canvas(self.canvasFrm, bg="white", width=width, height=height)
		self.canvas.pack(expand=1)

		# bind the mouse wheel event
		# self.canvas.bind("<MouseWheel>", self.mouseWheel)
	
	def setGraph(self, graph : GraphInterface):
		"""Set the graph to be displayed."""
		self.graph = graph
		self.graph.createParamMenu(self.menuFrm).pack()
	
	def update(self):
		"""Update the graph canvas."""
		img = self.graph.getImage()
		resizedImg = img.resize((self.widht, self.height), Image.ANTIALIAS)
		self.img = ImageTk.PhotoImage(resizedImg)
		self.canvas.create_image(0, 0, image=self.img, anchor=NW)