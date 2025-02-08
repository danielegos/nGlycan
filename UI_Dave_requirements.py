import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageGrab
import pandas as pd


class DrawingCanvasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Drawing Canvas")

        # Create main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create Canvas
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(self.main_frame, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.grid(row=0, column=1, rowspan=3)

        # Create menus
        self.create_sugar_menu()
        self.create_linkage_menu()
        self.create_analysis_tools()

        # Data tracking
        self.shapes = []  # Store shape info
        self.lines = []  # Store line connections

    def create_sugar_menu(self):
        sugar_menu = tk.Frame(self.main_frame, width=200, height=self.canvas_height, bg='lightgray')
        sugar_menu.grid(row=0, column=0, sticky='ns')
        tk.Label(sugar_menu, text="Sugar Menu", font=("Arial", 12, "bold"), bg='lightgray').pack()

        self.shapes_data = {
            "Blue Square": "blue",
            "Green Circle": "green",
            "Yellow Circle": "yellow",
            "Red Triangle": "red",
            "Purple Diamond": "purple",
            "Sky Blue Square": "skyblue"
        }

        for shape, color in self.shapes_data.items():
            btn = tk.Button(sugar_menu, text=shape, bg=color, command=lambda s=shape, c=color: self.add_shape(s, c))
            btn.pack(pady=5, fill=tk.X)

    def add_shape(self, shape, color):
        x, y = 100, 100  # Default position
        shape_id = self.canvas.create_rectangle(x, y, x + 40, y + 40, fill=color, tags=shape) if "Square" in shape else \
            self.canvas.create_oval(x, y, x + 40, y + 40, fill=color, tags=shape) if "Circle" in shape else \
                self.canvas.create_polygon(x, y + 40, x + 20, y, x + 40, y + 40, fill=color,
                                           tags=shape) if "Triangle" in shape else \
                    self.canvas.create_polygon(x + 20, y, x + 40, y + 20, x + 20, y + 40, x, y + 20, fill=color,
                                               tags=shape)

        self.shapes.append((shape_id, shape, x, y))

    def create_linkage_menu(self):
        linkage_menu = tk.Frame(self.main_frame, width=200, height=self.canvas_height, bg='lightgray')
        linkage_menu.grid(row=1, column=0, sticky='ns')
        tk.Label(linkage_menu, text="Linkage Menu", font=("Arial", 12, "bold"), bg='lightgray').pack()

        self.linkages = {
            "α-2": "red", "α-3": "blue", "α-4": "green", "α-6": "purple",
            "β-2": "orange", "β-3": "brown", "β-4": "pink", "β-6": "black"
        }

        for label, color in self.linkages.items():
            btn = tk.Button(linkage_menu, text=label, bg=color, command=lambda l=label, c=color: self.start_line(l, c))
            btn.pack(pady=5, fill=tk.X)

    def start_line(self, label, color):
        self.canvas.bind("<Button-1>", lambda event: self.draw_line(event, label, color))

    def draw_line(self, event, label, color):
        x1, y1 = event.x, event.y
        x2, y2 = x1 + 50, y1  # Default straight line
        line_id = self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)
        self.lines.append((line_id, label, x1, y1, x2, y2))

    def create_analysis_tools(self):
        analysis_menu = tk.Frame(self.main_frame, width=200, height=self.canvas_height, bg='lightgray')
        analysis_menu.grid(row=2, column=0, sticky='ns')
        tk.Label(analysis_menu, text="Analysis Tools", font=("Arial", 12, "bold"), bg='lightgray').pack()

        tk.Button(analysis_menu, text="Export Image", command=self.export_image).pack(pady=5, fill=tk.X)
        tk.Button(analysis_menu, text="DC Index", command=lambda: self.export_csv("DC_Index.csv")).pack(pady=5,
                                                                                                        fill=tk.X)
        tk.Button(analysis_menu, text="PC Index", command=lambda: self.export_csv("PC_Index.csv")).pack(pady=5,
                                                                                                        fill=tk.X)

    def export_image(self):
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        image = ImageGrab.grab(bbox=(x, y, x1, y1))
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            image.save(file_path)

    def export_csv(self, filename):
        data = []
        for shape_id, shape, x, y in self.shapes:
            connections = [line for line in self.lines if (line[2], line[3]) == (x, y)]
            data.append(
                [shape, "Layer X", "Connected Shape", len(connections), len(set(conn[1] for conn in connections)),
                 "Yes" if connections else "No"])

        df = pd.DataFrame(data,
                          columns=["Shape Name", "Layer", "Connected To", "Total Connections", "Distinct Link Types",
                                   "Connected to Previous Layer"])
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")],
                                                 initialfile=filename)
        if file_path:
            df.to_csv(file_path, index=False)


if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingCanvasApp(root)
    root.mainloop()
