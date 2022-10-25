from tkinter import *
from tkinter import ttk
import winManager as wm
import addPlant
import dict

itemColorDefault = "lightgrey"
itemColorFocus = "#e5e5e5"
itemColorSelected = "#c0c0c0"

def create():
	frm = ttk.Frame(wm.root, relief="solid", borderwidth=2)
	frm.pack(side="right", fill="y")

	createMenu(frm)

	# Create the frame for canvas and scrollbar
	canvasFrm = ttk.Frame(frm)
	canvasFrm.pack(side="top", fill="y", expand=True)

	# Create the canvas
	canvas = Canvas(canvasFrm)
	canvas.pack(side="left", fill="both", expand=True)

	# Create the scrollbar
	scrollbar = ttk.Scrollbar(canvasFrm, orient="vertical", command=canvas.yview)
	scrollbar.pack(side="right", fill="y")

	# Create the list
	global listFrm
	listFrm = ttk.Frame(canvas)
	listFrm.pack(side="bottom", fill="both", expand=True)

	# Configure the canvas and scrollbar
	canvas.configure(yscrollcommand=scrollbar.set)
	canvas.create_window((0, 0), window=listFrm, anchor="nw")
	listFrm.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

	# Create the items
	global itemList
	itemList = []
	for plant in dict.data:
		createItem(plant)
		
	# Update the canvas width
	listFrm.update()
	listWidth = listFrm.winfo_width()
	canvas.configure(width=listWidth)

# Create an item
def createItem(plant):
	# Create the item frame
	itemFrm = Frame(listFrm, relief="raised", borderwidth=1, bg=itemColorDefault)
	itemFrm.pack(fill="x", pady=2)

	# Create the item label
	name = Label(itemFrm, text=plant["name"], font=("Helvetica 9 bold"), bg=itemColorDefault)
	name.grid(column=0, row=0, columnspan=12, sticky="w")

	# create the colors
	colors = []
	for i in range(12):
		color = plant["flowering"][i]
		lbl = Label(itemFrm, background=color if color != "" else itemColorDefault, width=1)
		lbl.grid(column=i, row=1)
		colors.append({"plantColor": color, "widget": lbl})

	# Create the item object
	item = {
		"data": plant,
		"frame": itemFrm,
		"name": name,
		"colors": colors,
		"selected": False,
		"hidden": False
	}
	global itemList
	itemList.append(item)

	# Bind functions to the item
	itemFrm.bind("<Enter>", lambda e: enterBtn(e, item))
	itemFrm.bind("<Leave>", lambda e: leaveBtn(e, item))
	itemFrm.bind("<Button-1>", lambda e, item=item: selectItem(e, item))
	name.bind("<Button-1>", lambda e, item=item: selectItem(e, item))
	# period.bind("<Button-1>", lambda e, item=item: selectItem(e, item))
	for color in colors:
		color["widget"].bind("<Button-1>", lambda e, item=item: selectItem(e, item))

# Handle the selection of an item
def selectItem(event, item):
	if item["selected"]:
		wm.gm.graph.removePlant(item["data"])
		item["frame"].configure(relief="raised", borderwidth=1)
		item["selected"] = False
	else:
		wm.gm.graph.addPlant(item["data"])
		item["frame"].configure(relief="sunken", borderwidth=2)
		item["selected"] = True
	wm.gm.graph.update()

def enterBtn(e, item):
	item["frame"].configure(bg=itemColorFocus)
	item["name"].configure(bg=itemColorFocus)
	for color in item["colors"]:
		if color["plantColor"] == "":
			color["widget"].configure(bg=itemColorFocus)

def leaveBtn(e, item):
	bgColor = itemColorSelected if item["selected"] else itemColorDefault
	item["frame"].configure(bg=bgColor)
	item["name"].configure(bg=bgColor)
	for color in item["colors"]:
		if color["plantColor"] == "":
			color["widget"].configure(bg=bgColor)

# Create the menu
def createMenu(frm):
	# Create the add plant button
	btnFrm = ttk.Frame(frm)
	btnFrm.pack(side="top", fill="x")
	ttk.Button(btnFrm, text="add new plant", command=addPlant.addPlant).pack(side="top")

	# Create the filter bar
	filterFrm = ttk.Frame(frm)
	filterFrm.pack(side="top", fill="x")

	filterLbl = ttk.Label(filterFrm, text="Filter:")
	filterLbl.pack(side="left")

	filterEntry = ttk.Combobox(filterFrm, values=["name", "period"])
	filterEntry.pack(side="left")

	# Create the search bar
	searchFrm = ttk.Frame(frm)
	searchFrm.pack(side="top", fill="x")

	searchLbl = ttk.Label(searchFrm, text="Search:")
	searchLbl.pack(side="left")

	searchEntry = ttk.Entry(searchFrm)
	searchEntry.pack(side="left", fill="x", expand=True)

	# Create the search button frame
	searchBtnFrm = ttk.Frame(frm)
	searchBtnFrm.pack(side="top", fill="x")

	# Create the search button
	searchBtn = ttk.Button(searchBtnFrm, text="search", command=lambda: filterItemList(filterEntry.get(), searchEntry.get()))
	searchBtn.pack(side="right")

	# Create the clear button
	clearBtn = ttk.Button(searchBtnFrm, text="clear", command=lambda: filterItemList("", ""))
	clearBtn.pack(side="left")

# Filter the item list
def filterItemList(filterStr, searchStr):
	for item in itemList:
		hide = False
		if filterStr == "name":
			if not searchStr.lower() in item["data"]["name"].lower():
				hide = True
		elif filterStr == "period":
			if not searchStr.lower() in item["data"]["flowering"][0]["period"].lower():
				hide = True
		
		if hide:
			# item["frame"].pack_forget()
			item["hidden"] = True
		else:
			# item["frame"].pack(fill="x", pady=2)
			item["hidden"] = False
	update()

def sortItemList():
	global itemList
	itemList = sorted(itemList, key=lambda item: item["data"]["name"])

def update():
	sortItemList()
	for item in itemList:
		item["frame"].pack_forget()
	for item in itemList:
		if not item["hidden"]:
			item["frame"].pack(fill="x", pady=2)