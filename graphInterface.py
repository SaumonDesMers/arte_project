from tkinter import *
from tkinter import ttk
import winManager as wm
from PIL import Image, ImageDraw, ImageTk, ImageFont

class GraphInterface:
	"""Interface for the graph."""

	def getImage() -> Image:
		"""(Interface) Return the graph PIL image."""
		pass

	def update(self):
		"""(Interface) Update the graph."""
		pass

	def save(self, path):
		"""(Interface) Save the graph."""
		pass

	def export(self, path):
		"""(Interface) Export the graph."""
		pass

	def createParamMenu(self, parent):
		"""(Interface) Create the parameter menu"""
		pass
	
	def addPlant(self, plant):
		"""(Interface) Add a plant to the graph."""
		pass
	
	def removePlant(self, plant):
		"""(Interface) Remove a plant from the graph."""
		pass