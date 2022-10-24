from tkinter import *
from tkinter import ttk
import winManager as wm
from PIL import Image, ImageDraw, ImageTk, ImageFont

class GraphInterface:
	"""Interface for the graph."""

	def getImage() -> Image:
		"""(Interface) Return the graph PIL image."""
		pass

	def update():
		"""(Interface) Update the graph."""
		pass

	def createParamMenu(self):
		"""(Interface) Create the parameter menu"""
		pass
	
	def addPlant(plant):
		"""(Interface) Add a plant to the graph."""
		pass
	
	def removePlant(plant):
		"""(Interface) Remove a plant from the graph."""
		pass