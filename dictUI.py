from tkinter import *
from tkinter import ttk
import winManager as wm
import json
import addPlant
import dict

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
	itemFrm = Frame(listFrm, relief="raised", borderwidth=1)
	itemFrm.pack(fill="x", pady=2)

	# Create the item label
	name = Label(itemFrm, text=plant["name"])
	name.grid(column=0, row=0, columnspan=2, sticky="w")

	period = Label(itemFrm, text=plant["flowering"][0]["period"], width=20, anchor="w")
	period.grid(column=0, row=1)

	color = Label(itemFrm, background=plant["flowering"][0]["color"], width=5)
	color.grid(column=1, row=1)

	# Create the item object
	item = {
		"data": plant,
		"frame": itemFrm,
		"name": name,
		"period": period,
		"color": color,
		"selected": False,
		"hidden": False
	}
	global itemList
	itemList.append(item)

	# Bind functions to the item
	itemFrm.bind("<Enter>", lambda e, itemFrm=itemFrm: itemFrm.configure(relief="sunken"))
	itemFrm.bind("<Leave>", lambda e, itemFrm=itemFrm: itemFrm.configure(relief="raised"))
	itemFrm.bind("<Button-1>", lambda e, item=item: selectItem(e, item))
	name.bind("<Button-1>", lambda e, item=item: selectItem(e, item))
	period.bind("<Button-1>", lambda e, item=item: selectItem(e, item))
	color.bind("<Button-1>", lambda e, item=item: selectItem(e, item))


# Handle the selection of an item
def selectItem(event, item):
	if item["selected"]:
		item["frame"].configure(bg="lightgrey")
		item["name"].configure(bg="lightgrey")
		item["period"].configure(bg="lightgrey")
		item["selected"] = False
	else:
		item["frame"].configure(bg="grey")
		item["name"].configure(bg="grey")
		item["period"].configure(bg="grey")
		item["selected"] = True


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
			item["frame"].pack_forget()
			item["hidden"] = True
		else:
			item["frame"].pack(fill="x")
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
			item["frame"].pack(fill="x")