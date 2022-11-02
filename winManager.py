from tkinter import *
from tkinter import ttk
import dictUI
from graphUI import GraphUI
from threeQuartersCircularGraph import TQCG
from TQCG_cairo import TQCG_cairo

def initWindow():
	global root
	root = Tk()
	root.title("Arte project")
	root.geometry("1200x800")
	root.tk_setPalette(background="lightgrey")

	frm = ttk.Frame(root)

	dictUI.create()
	global gm
	gm = GraphUI()
	# gm.setGraph(TQCG())
	gm.setGraph(TQCG_cairo())
	
	createTopbar()
	
	frm.pack()


def nothing():
	pass

def createTopbar():
	# Create the menu bar
	topbarMenu = Menu(root)
	root.config(menu=topbarMenu)

	# Create the file menu
	fileMenu = Menu(topbarMenu, tearoff=0)
	topbarMenu.add_cascade(label="File", menu=fileMenu, underline=0)

	fileMenu.add_command(label="New", command=nothing)
	fileMenu.add_command(label="Open...", command=gm.graph.open)
	fileMenu.add_separator()
	fileMenu.add_command(label="Save", command=gm.graph.save)
	fileMenu.add_command(label="Save as...", command=nothing)
	fileMenu.add_command(label="Export", command=gm.graph.export)
	fileMenu.add_separator()
	fileMenu.add_command(label="Exit", command=root.quit)

	# Create the help menu
	helpMenu = Menu(topbarMenu, tearoff=0)
	topbarMenu.add_cascade(label="Help", menu=helpMenu)

	helpMenu.add_command(label="About...", command=nothing)
