from xcanvas import XCanvas
import tkinter as tk

root = tk.Tk()

canvas = XCanvas(root, width=400, height=400)
canvas.pack(fill="both", expand=True)

# Draw something on the canvas
canvas.create_oval(10, 10, 100, 100)

root.mainloop()