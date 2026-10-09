import threading
import time
import tkinter as tk
import pynvml
import numpy as np


class TemperatureOverlay:

    def __init__(self, res = "QHD"):
        # Setup GPU handle
        pynvml.nvmlInit()
        self.gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)

        # Setup GUI Window
        self.root = tk.Tk()
        self.root.title("GPU Temp Overlay")

        # 1. Keep window always on top
        self.root.attributes("-topmost", True)

        # Remove window border, title bar, and close buttons
        self.root.overrideredirect(True)

        # 3. Sindow position  
        if res.lower() == "qhd":
            self.root.geometry(f"+2400+20")
        else:
            self.root.geometry(f"+1750+20")

        # 4. Styling
        self.root.configure(bg="#1e1e1e")
        self.label = tk.Label(
            self.root,
            text="GPU: --°C",
            font=("Consolas", 14, "bold"),
            fg="#00e5ff",
            bg="#1e1e1e",
            padx=10,
            pady=5,
        )
        self.label.pack()

        # Window transparency
        self.root.attributes("-alpha", 0.5)

        # Allow dragging the window with the mouse
        self.label.bind("<Button-1>", self.start_move)
        self.label.bind("<B1-Motion>", self.do_move)

        # Start update loop in background
        self.running = True
        self.thread = threading.Thread(target=self.update_loop, daemon=True)
        self.thread.start()

        # Peak temperature 
        self.peak = 0

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def update_loop(self):
        while self.running:
            temp = pynvml.nvmlDeviceGetTemperature(
                self.gpu_handle, pynvml.NVML_TEMPERATURE_GPU
            )
            self.peak = max(temp, self.peak)
            # Update label
            self.root.after(0, self.label.config, {"text": f"GPU: {temp}°C\nPeak: {self.peak}°C"})
            time.sleep(1)

    def run(self):
        try:
            self.root.mainloop()
        finally:
            self.running = False
            pynvml.nvmlShutdown()

