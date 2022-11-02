from tkinter import *
from tkinter import ttk
import winManager as wm

def someErrorOccurred(errMsg):
	"""Open an generic error window."""
	win = Toplevel(wm.root)
	win.title("Error")
	win.resizable(False, False)

	# Create the error message
	Label(win, text=errMsg, bg="lightgrey").pack(expand=True, fill="both", padx=10, pady=10)

	# Create the OK button
	ttk.Button(win, text="OK", command=win.destroy).pack(side="bottom")