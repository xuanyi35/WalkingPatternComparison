import tkinter as tk
import pygubu

class Application:
    def __init__(self, master):
        self.master = master

        # Create builder
        self.builder = builder = pygubu.Builder()

        # Load ui file
        builder.add_from_file("PdAnimation.ui")

        # Create a widget, using master as parent
        self.mainWindow = builder.get_object('mainWindow', master)

        # Connect callbacks
        builder.connect_callbacks(self)

    def on_quit_button_click(self):
        '''
        Quit Button Callback
        '''
        self.master.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()