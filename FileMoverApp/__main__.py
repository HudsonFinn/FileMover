from watchdog.observers import Observer

import time
import tkinter as tk

from settings import Settings
from fileMover import FileMover
from UI import Application
from eventHandler import MyHandler

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    run = app.run
    # FileMover.sortDirectory("D:/University/Personal/Projects/Python/FileMover/target", filesTypes)

    if run:
        print(app.FOLDER_TO_SORT)
        fileTypes = app.fileTypes
        decompression = bool(app.decompressionEnabled.get())
        event_handler = MyHandler(app.FOLDER_TO_SORT, fileTypes, decompression)
        observer = Observer()
        observer.schedule(event_handler, app.FOLDER_TO_SORT, recursive=False)
        observer.start()
        try:
            while run:
                time.sleep(2)
                print("Hi")
        except KeyboardInterrupt:
            observer.stop()

main()
