from tkinter import *
from tkinter import ttk
import json
import addPlant
import dict
import dictUI

def initWindow():
	global root
	root = Tk()
	root.title("Arte project")
	root.geometry("1600x1200")
	root.tk_setPalette(background="lightgrey")

	frm = ttk.Frame(root)

	createTopbar()
	dictUI.create()
	
	frm.pack()


def nothing():
	print("Nothing here for now")

def createTopbar():
	# Create the menu bar
	topbarMenu = Menu(root)
	root.config(menu=topbarMenu)

	# Create the file menu
	fileMenu = Menu(topbarMenu, tearoff=0)
	topbarMenu.add_cascade(label="File", menu=fileMenu, underline=0)

	fileMenu.add_command(label="New", command=nothing)
	fileMenu.add_command(label="Open...", command=nothing)
	fileMenu.add_separator()
	fileMenu.add_command(label="Exit", command=root.quit)

	# Create the help menu
	helpMenu = Menu(topbarMenu, tearoff=0)
	topbarMenu.add_cascade(label="Help", menu=helpMenu)

	helpMenu.add_command(label="About...", command=nothing)
