from tkinter import *
from tkinter import ttk
import winManager as wm
import json
import addPlant
import dict

def selectItem(event, item):
	if item["selected"]:
		item["frame"].configure(bg="lightgrey")
		item["name"].configure(bg="lightgrey")
		item["period"].configure(bg="lightgrey")
		item["selected"] = False
	else:
		item["frame"].configure(bg="lightblue")
		item["name"].configure(bg="lightblue")
		item["period"].configure(bg="lightblue")
		item["selected"] = True

def create():
	frm = ttk.Frame(wm.root, width=300, relief="solid", borderwidth=2)
	frm.pack(side="right", fill="y")

	# Create the buttons
	btnFrm = ttk.Frame(frm)
	btnFrm.pack(side="top", fill="x")
	ttk.Button(btnFrm, text="add new plant", command=addPlant.addPlant).pack(side="top")

	# Create the frame for canvas and scrollbar
	canvasFrm = ttk.Frame(frm)
	canvasFrm.pack(side="top", fill="both", expand=True)

	# Create the canvas
	canvas = Canvas(canvasFrm, bg="lightblue", width=200)
	canvas.pack(side="left", fill="both", expand=True)

	# Create the list
	listFrm = ttk.Frame(canvas)
	listFrm.pack(side="bottom", fill="both", expand=True)

	# Create the scrollbar
	scrollbar = ttk.Scrollbar(canvasFrm, orient="vertical", command=canvas.yview)
	scrollbar.pack(side="right", fill="y")

	canvas.configure(yscrollcommand=scrollbar.set)
	canvas.create_window((0, 0), window=listFrm, anchor="nw")

	listFrm.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

	for plant in dict.data:

		# Create the item frame
		itemFrm = Frame(listFrm, relief="solid", borderwidth=1)
		itemFrm.pack(fill="x")

		# Create the item label
		name = Label(itemFrm, text=plant["name"])
		name.grid(column=0, row=0, columnspan=2, sticky="w")

		period = Label(itemFrm, text=plant["flowering"][0]["period"], width=10, anchor="w")
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
			"selected": False
		}

		# Bind functions to the item
		itemFrm.bind("<Enter>", lambda event, itemFrm=itemFrm: itemFrm.configure(relief="sunken"))
		itemFrm.bind("<Leave>", lambda event, itemFrm=itemFrm: itemFrm.configure(relief="solid"))
		itemFrm.bind("<Button-1>", lambda event, item=item: selectItem(event, item))
		name.bind("<Button-1>", lambda event, item=item: selectItem(event, item))
		period.bind("<Button-1>", lambda event, item=item: selectItem(event, item))
