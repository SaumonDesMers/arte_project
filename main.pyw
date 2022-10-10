from tkinter import *
from tkinter import ttk

msg = "Hello"

root = Tk()
frm = ttk.Frame(root, padding=100)
frm.grid()
ttk.Label(frm, text=msg).grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=1)
root.mainloop()

# if __name__ == "__main__":
# 	print("Hello World!")
