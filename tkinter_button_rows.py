import tkinter as tk

root = tk.Tk()
root.title("Two Columns with Output Display")

# Function to create a row of buttons inside a frame
def create_button_row(parent, button_labels):
    frame = tk.Frame(parent)
    frame.pack(pady=5, anchor="w")  # Aligns row to the left
    for label in button_labels:
        tk.Button(frame, text=label, command=lambda lbl=label: print_to_text(lbl)).pack(side="left", padx=5)

# Function to print button label to the text output area
def print_to_text(text):
    output_box.insert(tk.END, f"{text} clicked!\n")  # Append text
    output_box.see(tk.END)  # Auto-scroll to the latest entry

# Create frames for the left and right columns
left_frame = tk.Frame(root)
left_frame.pack(side="left", padx=20, pady=10, anchor="n")

right_frame = tk.Frame(root)
right_frame.pack(side="left", padx=20, pady=10, anchor="n")

# Create frame for the output column
output_frame = tk.Frame(root)
output_frame.pack(side="left", padx=20, pady=10, anchor="n")

# Add button rows to the left column
create_button_row(left_frame, ["L1A", "L1B"])  # Row 1
create_button_row(left_frame, ["L2A", "L2B"])  # Row 2
create_button_row(left_frame, ["L3A", "L3B"])  # Row 3
create_button_row(left_frame, ["L4A", "L4B"])  # Row 4
create_button_row(left_frame, ["L5A", "L5B"])  # Row 5

# Add button rows to the right column
create_button_row(right_frame, ["R1A", "R1B"])  # Row 1
create_button_row(right_frame, ["R2A", "R2B"])  # Row 2
create_button_row(right_frame, ["R3A", "R3B"])  # Row 3
create_button_row(right_frame, ["R4A", "R4B"])  # Row 4
create_button_row(right_frame, ["R5A", "R5B"])  # Row 5

# Add a Text widget to display output
output_box = tk.Text(output_frame, height=15, width=30, wrap="word")
output_box.pack()

root.mainloop()
