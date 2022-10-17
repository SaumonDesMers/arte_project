from tkinter import *
from tkinter import ttk
import json
import addPlant
from winManager import initWindow
import dict

if __name__ == "__main__":
	dict.load()
	initWindow()
	mainloop()
