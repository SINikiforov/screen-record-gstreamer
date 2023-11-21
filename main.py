from gui import ScreencastGUI
from app import Screencast
import tkinter as tk


if __name__ == "__main__":
    root = tk.Tk()
    screencast = Screencast(root)
    screencast_gui = ScreencastGUI(root, screencast.start_recording, screencast.pause_recording, screencast.unpause_recording, screencast.stop_recording)
    screencast.gui = screencast_gui
    screencast_gui.run()
