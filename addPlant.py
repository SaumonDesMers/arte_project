from tkinter import *
from tkinter import ttk, colorchooser
import json
import winManager as wm
import dict
import dictUI

def addPlant():
	plant = {
		"name": "",
		"flowering": []
	}
	entryStr = {
		"name": StringVar(),
		"color": StringVar(),
		"period": StringVar()
	}
	addPlantWindow(entryStr, plant)

def readNewPlantEntry(win, entryStr, plant):
	# Read the entry fields
	plant["name"] = entryStr["name"].get()
	plant["flowering"].append({
		"color": entryStr["color"].get(),
		"period": entryStr["period"].get()
	})
	win.destroy()
	print(json.dumps(plant, indent=4))
	dict.add(plant)
	dictUI.createItem(plant)
	dictUI.update()

def chooseColor(parentWin, btn, plantColor):
	color = colorchooser.askcolor(parent=parentWin)
	btn.config(bg=color[1])
	plantColor.set(color[1])

def addPlantWindow(entryStr, plant):
	# Create the window
	newPlantWindow = Toplevel(wm.root, padx=10, pady=10, width=300, height=200)
	newPlantWindow.title("Add a new plant")
	# newPlantWindow.geometry("500x200")

	frm = ttk.Frame(newPlantWindow)
	frm.grid()

	# Create the entry fields
	ttk.Label(frm, text="Name: ").grid(column=0, row=0, pady=5)
	nameEntry = ttk.Entry(frm, textvariable=entryStr["name"])
	nameEntry.grid(column=1, row=0, pady=5)

	ttk.Label(frm, text="Color: ").grid(column=0, row=1, pady=5)
	colorBtn = Button(frm, bg="#ffffff", command= lambda: chooseColor(newPlantWindow, colorBtn, entryStr["color"]))
	colorBtn.grid(column=1, row=1, pady=5, sticky="we")

	ttk.Label(frm, text="Period: ").grid(column=0, row=2, pady=5)
	periodEntry = ttk.Entry(frm, textvariable=entryStr["period"])
	periodEntry.grid(column=1, row=2, pady=5)

	# Create the buttons
	ttk.Button(
		frm,
		text="Add",
		command= lambda: readNewPlantEntry(newPlantWindow, entryStr, plant)
	).grid(column=1, row=3, sticky="e")

	ttk.Button(
		frm,
		text="Cancel",
		command= lambda: newPlantWindow.destroy()
	).grid(column=0, row=3, sticky="w")
