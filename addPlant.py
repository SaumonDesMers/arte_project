from calendar import month
from tkinter import *
from tkinter import ttk, colorchooser
import json
import winManager as wm
import dict
import dictUI
import re

def addPlant():
	plant = {
		"name": "",
		"flowering": []
	}
	entryStr = {
		"name": StringVar(),
		"color": [],
	}
	for i in range(12):
		entryStr["color"].append(StringVar())
	addPlantWindow(entryStr, plant)

def readEntry(win, entryStr, plant):
	# Read the entry fields
	plant["name"] = entryStr["name"].get()
	for i in range(12):
		color = entryStr["color"][i].get()
		if re.search(r"#[0-9a-fA-F]{6}", color):
			plant["flowering"].append(color)
	win.destroy()
	print(json.dumps(plant, indent=4))
	# dict.add(plant)
	# dictUI.createItem(plant)
	# dictUI.update()

def addPlantWindow(entryStr, plant):
	# Create the window
	win = Toplevel(wm.root, padx=10, pady=10, width=300, height=200)
	win.title("Add a new plant")
	# win.geometry("500x200")

	frm = ttk.Frame(win)
	frm.grid()

	# Create the entry fields
	ttk.Label(frm, text="Name: ").grid(column=0, row=0, pady=5)
	nameEntry = ttk.Entry(frm, textvariable=entryStr["name"])
	nameEntry.grid(column = 1, columnspan=2, row=0, pady=1)

	# Create the color buttons
	monthNames = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
	colorBtn = [None] * 12
	for i in range(12):
		ttk.Label(frm, text=monthNames[i]).grid(column=0, row=i+1, pady=1, sticky="w")
		colorBtn[i] = Button(frm, command= lambda i=i: chooseColorWithBtn(win, colorBtn[i], entryStr["color"][i]))
		ttk.Entry(
			frm,
			width=7,
			textvariable=entryStr["color"][i],
			# validate="focusout",
			# validatecommand=lambda: colorBtn[i].config(bg=entryStr["color"][i].get())
		).grid(column=1, row=i+1, pady=1, sticky="we")
		entryStr["color"][i].trace("w", lambda x,y,z,i=i: chooseColorWithEntry(colorBtn[i], entryStr["color"][i]))
		colorBtn[i].grid(column=2, row=i+1, pady=1, sticky="we")

	# Create the buttons
	ttk.Button(
		frm,
		text="Add",
		command= lambda: readEntry(win, entryStr, plant)
	).grid(column=1, row=13, sticky="e")

	ttk.Button(
		frm,
		text="Cancel",
		command= lambda: win.destroy()
	).grid(column=0, row=13, sticky="w")


def chooseColorWithBtn(parentWin, btn, colorEntry):
	color = colorchooser.askcolor(parent=parentWin)
	btn.config(bg=color[1])
	colorEntry.set(color[1])

def chooseColorWithEntry(btn, entry):
	color = entry.get()
	if re.search(r"#[0-9a-fA-F]{6}", color):
		btn.config(bg=color)
	else:
		btn.config(bg="lightgray")