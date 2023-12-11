import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from tkinter import Entry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import matplotlib.pyplot as plt
# from your_module import plot_file

figure = Figure(figsize=(6, 4), dpi=100)
ax = figure.add_subplot(111)
from utils.plot_functions import plot_file

selected_files = []
checkbox_lines = {}

def plot_selected_file():
    file_path = filedialog.askopenfilename(filetypes=[("TXT files", "*.txt")])  # Modify file types as needed
    if file_path:
        shift_scale = float(shift_scale_entry.get())
        selected_files.append((file_path, shift_scale))
        update_plot()
        update_file_listbox()
        print(file_listbox)

def update_file_listbox():
    file_listbox.delete(0, tk.END)  # Clear the listbox
    for file_path in selected_files:
        file_name = os.path.basename(file_path)
        file_listbox.insert(tk.END, file_name)

def update_plot():
    # Clear previous plot if exists
    if hasattr(update_plot, 'canvas_frame'):
        update_plot.canvas_frame.destroy()

    ax.clear()
    checkbox_lines.clear()  # Clear stored checkbox-line associations
    #plot
    from utils.input_output import shift_data_lab
    for file_path, scale in selected_files:
        print(file_path)
        from utils.plot_functions import plot_file, plot_shift_iso_area
        #area, pressure = plot_file(file_path, legend=os.path.basename(file_path), c = 'red')
        area, pressure = plot_shift_iso_area(file_path, shift_scale = float(scale), legend=os.path.basename(file_path), c = 'red')
        full_name = os.path.basename(file_path)
        file_name = os.path.splitext(full_name)[0]
        line, =ax.plot(area, pressure, label = file_name)  # Call your plot function with the subplot
        checkbox_lines[file_name] = line  # Store the line in the dictionary
        ax.legend()

    canvas.draw()

def save_figure():
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if save_path:
        plt.savefig(save_path)
        print(f"Figure saved as '{save_path}'")

def toggle_curve_visibility(file_name):
    if file_name in checkbox_lines:
        line = checkbox_lines[file_name]
        line.set_visible(not line.get_visible())
        canvas.draw()

def remove_selected_file():
    selected_index = file_listbox.curselection()
    print("Selected index:", selected_index)  # Debug print
    if selected_index:
        selected_index = selected_index[0]
        selected_file_name = file_listbox.get(selected_index)
        print("Selected file name:", selected_file_name)  # Debug print
        print(checkbox_lines)
        if selected_file_name in checkbox_lines:
            line = checkbox_lines.pop(selected_file_name)
            print(line)
            line.remove()
            print(line)
            update_plot()
            selected_files.pop(selected_index)
            print(selected_files)
            update_file_listbox()

# Create the main window
window = tk.Tk()
window.title("File Plotter")

# Create a button to select and plot a file
select_button = tk.Button(window, text="Select File", command=plot_selected_file)
select_button.pack()

# Create a Listbox to display the selected files
file_listbox = tk.Listbox(window)
file_listbox.pack(side=tk.LEFT, fill=tk.Y)

#Create a label and an input box for shift_scale in your main window
shift_scale_label = tk.Label(window, text="Shift Scale:")
shift_scale_label.pack()

shift_scale_entry = Entry(window)
shift_scale_entry.pack()

# Create a button to save the figure
save_button = tk.Button(window, text="Save Figure", command=save_figure)
save_button.pack()

# Create a canvas to display the plot
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a button to remove the selected file
remove_button = tk.Button(window, text="Remove File", command=remove_selected_file)
remove_button.pack()

# Start the main loop
window.mainloop()

