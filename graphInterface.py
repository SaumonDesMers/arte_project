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

	def save(self):
		"""(Interface) Save the graph."""
		pass

	def open(self):
		"""(Interface) Open a graph from a file."""
		pass

	def close(self, force=False):
		"""(Interface) Close the graph."""
		pass

	def export(self):
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