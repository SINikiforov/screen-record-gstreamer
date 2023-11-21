import tkinter as tk
from tkinter import ttk


class ScreencastGUI:
    def __init__(self, root, start_recording, pause_recording, unpause_recording, stop_recording):
        self.root = root
        self.root.title("Screen Recorder")

        style = ttk.Style()
        style.configure("TButton",
                        foreground="white",
                        background="black",
                        font=("Helvetica", 12))

        self.start_button = ttk.Button(root, text="Start Recording", command=start_recording, style="TButton").grid(row=0, column=0, padx=10, pady=10)
        self.pause_button = ttk.Button(root, text="Pause Recording", command=pause_recording, style="TButton").grid(row=1, column=1, padx=10, pady=10)
        self.unpause_button = ttk.Button(root, text="Resume Recording", command=unpause_recording, style="TButton").grid(row=1, column=0, padx=10, pady=10)
        self.stop_button = ttk.Button(root, text="Stop Recording", command=stop_recording, style="TButton").grid(row=0, column=1, padx=10, pady=10)


        self.status_label = tk.Label(self.root, text="Готово", fg="green")
        self.status_label.grid(row=3, column=0, padx=10, pady=10)


    def update_recording_state(self, state, color):
        self.status_label.config(text=state, fg=color)


    def run(self):
        self.root.mainloop()
