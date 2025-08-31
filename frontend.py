import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import platform
import sys
import os
import time
from ctypes import c_ulonglong, c_double

# --- Load the Zig Compiled Library ---
# Get the current directory where the script is running
current_dir = os.path.dirname(os.path.abspath(__file__))

# Determine the correct library filename for the OS
os_name = platform.system()
lib_filename = ""

if os_name == 'Linux':
    lib_filename = 'libbackend.so'
elif os_name == 'Darwin':  # macOS
    lib_filename = 'libbackend.dylib'
elif os_name == 'Windows':
    lib_filename = 'backend.dll'
else:
    messagebox.showerror("Error", f"Unsupported operating system: {os_name}")
    sys.exit(1)

# Create the full path to the library file
lib_path = os.path.join(current_dir, lib_filename)

# Check if the library file exists before trying to load it
if not os.path.exists(lib_path):
    messagebox.showerror("Error", f"Library file not found at: {lib_path}")
    messagebox.showinfo("Info", "Please make sure you've compiled the Zig / C++ / Fortran code with:\nZig: zig build-lib backend.zig -dynamic -lc -target x86_64-windows \nOR C++: g++ -shared -o backend.dll backend.cpp -std=c++11 \nOR Fortran: gfortran -shared -o backend.dll backend.f90 -fPIC")
    sys.exit(1)

try:
    # Load the shared library using the full path
    lib = ctypes.CDLL(lib_path)
    print(f"Successfully loaded library: {lib_path}")
except Exception as e:
    messagebox.showerror("Error", f"Could not load library {lib_path}: {e}")
    messagebox.showinfo("Info", "This might be due to missing DLL dependencies.\nTry installing Visual Studio Redistributable: https://aka.ms/vs/17/release/vc_redist.x64.exe")
    sys.exit(1)

# --- Define the function signature for the Zig function ---
lib.calculate_pi.argtypes = [c_ulonglong]  # u64 in Zig maps to c_ulonglong
lib.calculate_pi.restype = c_double         # f64 in Zig maps to c_double

# --- GUI Application ---
class PiApp:
    def __init__(self, root):
        self.root = root
        root.title("Zig + Python Demo")
        root.geometry("400x200")

        # Create and pack widgets
        ttk.Label(root, text="Enter number of iterations:").pack(pady=10)
        
        self.entry = ttk.Entry(root)
        self.entry.insert(0, "1000000")  # Default value
        self.entry.pack(pady=5)
        
        self.calc_button = ttk.Button(root, text="Calculate π", command=self.calculate)
        self.calc_button.pack(pady=10)
        
        self.result_label = ttk.Label(root, text="Result will be shown here.")
        self.result_label.pack(pady=20)

    def calculate(self):
        """Gets iterations from the entry, calls the Zig function, and displays the result with calculation time."""
        try:
            iterations = int(self.entry.get())
            if iterations <= 0:
                messagebox.showerror("Error", "Iterations must be a positive number.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer.")
            return

        # Measure calculation time
        start_time = time.time()
        # Call the function from the Zig library
        result = lib.calculate_pi(iterations)
        end_time = time.time()
        calc_time = end_time - start_time

        # Update the GUI with the result and calculation time
        self.result_label.config(text=f"Approximation of π: {result}\nCalculation time: {calc_time:.6f} seconds")

# Start the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PiApp(root)
    root.mainloop()