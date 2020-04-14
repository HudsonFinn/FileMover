from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from zipfile import ZipFile
import os
import json
import time
from datetime import datetime
import re
import tkinter as tk
from tkinter import filedialog
import winreg

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        super(MyHandler, self).__init__()
        ImgExt = ["ai", "bmp", "gif", "ico", "jpeg", "png", "ps", "psd", "svg", "tif", "jpg"]
        DictExt = dict.fromkeys(ImgExt, "Images")
        VidExt = ["webm", "mpg", "mp2", "mpeg", "mpe", "mpv", "ogg", "mp4", "m4p", "m4v", "avi", "wmv", "mov", "qt", "flv", "swf", "avchd"]
        DictExt.update(dict.fromkeys(VidExt, "Videos"))
        AudioExt = ["aif", "cda", "mid", "mp3", "mpa", "ogg", "wav", "wma", "wpl"]
        DictExt.update(dict.fromkeys(AudioExt, "Audio"))
        CompressedExt = ["7z", "arj", "deb", "pkg", "rar", "rpm", "tar", "z", "zip"]
        DictExt.update(dict.fromkeys(CompressedExt, "Compressed"))
        DataExt = ["csv", "dat", "db", "log", "mdb", "sav", "sql", "tar", "xml"]
        DictExt.update(dict.fromkeys(DataExt, "Data"))
        ExeExt = ["apk ", "bat", "bin,", "cgi", "com", "exe", "gadget", "jar", "msi", "wsf"]
        DictExt.update(dict.fromkeys(ExeExt, "Executables"))
        ProgrammingExt = ["c", "class", "cpp", "cs", "h", "java", "pl", "sh", "swift", "vb", "py"]
        DictExt.update(dict.fromkeys(ProgrammingExt, "Programming"))
        TextExt = ["doc", "docx", "odt", "pdf", "tex", "txt", "wpd", "pptx"]
        DictExt.update(dict.fromkeys(TextExt, "Text"))
        self.DictExt = DictExt
        self.DateTimeMod = re.compile(r'\[\d{2}-\d{2}-\d{4}\]$')
        self.DateTimeMulMod = re.compile(r'\[\d{2}-\d{2}-\d{4}\]\(\d+\)$')


    def on_any_event(self, event):
        time.sleep(0.2)
        folderToSort = app.FOLDER_TO_SORT
        #Get all files in directory
        dirFiles = os.listdir(folderToSort)
        #Loop through all the files
        for fullFile in dirFiles:
            #Create the string for the full path name
            fullPath = os.path.join(folderToSort, fullFile)
            #Check if the full path is a folder and if it is skip the file
            if os.path.isdir(fullPath):
                continue
            #split filename into its actual name and its extension
            splitName = fullFile.split(".")
            fileName = ".".join(splitName[0:len(splitName)-1])
            fileExt = splitName[len(splitName)-1]
            print(fileName)
            print(fileExt)
            #Get the type of file from a dict of all common file types
            type = self.DictExt.get(fileExt.lower(), "Other")
            targetFolder = os.path.join(folderToSort, type + "/")
            if not (os.path.isdir(targetFolder)):
                os.mkdir(targetFolder)
            while (fileName + "." + fileExt) in os.listdir(targetFolder):
                print("Already Saved")
                #Check if file already has a datetime stamp at the end
                containsDatetime = self.DateTimeMod.search(fileName) != None;
                containsDatetimeMul = self.DateTimeMulMod.search(fileName) != None;
                #If it already ends in a date
                if containsDatetime == True:
                    print("File has Date")
                    fileName = re.sub(self.DateTimeMod, "", fileName)
                    print(fullFile)
                    saveTime = datetime.now()
                    saveTime = saveTime.strftime("%d-%m-%Y")
                    #If it already ends in the same date
                    if (fileName + "." + fileExt) in os.listdir(targetFolder):
                        print("File already ends in date")
                        fileName = re.sub(self.DateTimeMod, "", fileName)
                        fileName = fileName + "[" + saveTime + "]" + "(1)"
                        continue
                    fileName = fileName + "[" + saveTime + "]"
                #If it ends in a date and there are already multiple files with that date
                elif containsDatetimeMul == True:
                    print("File has Date and multiple")
                    nextAvaliableEnd = self.DateTimeMulMod.search(fileName)
                    print(nextAvaliableEnd)
                    nextAvaliableEnd = nextAvaliableEnd[0]
                    nextAvaliableEnd = int(nextAvaliableEnd[13:len(nextAvaliableEnd)-1])
                    print(nextAvaliableEnd)
                    nextAvaliableEnd += 1
                    nextAvaliableEnd = str(nextAvaliableEnd)
                    fileName = re.sub(self.DateTimeMulMod, "", fileName)
                    saveTime = datetime.now()
                    saveTime = saveTime.strftime("%d-%m-%Y")
                    fileName = fileName + "[" + saveTime + "]" + "(" + nextAvaliableEnd + ")"
                    continue
                #If it doesn't end in a date append one
                else:
                    print("Else")
                    saveTime = datetime.now()
                    saveTime = saveTime.strftime("%d-%m-%Y")
                    fileName = fileName + "[" + saveTime + "]"
                    continue
                break
            #Reform into a fill file name
            fullFile = (fileName + "." + fileExt)
            print(targetFolder + fullFile)
            print(type)
            #Move it to the target folder
            os.rename(fullPath, targetFolder + fullFile)
            #Check if its a compressed file
            if type == "Compressed":
                try:
                    with ZipFile(targetFolder + fullFile, 'r') as zipObj:
                        #Extract it to the unzipped folder
                        zipObj.extractall(os.path.join(folderToSort, "Unzipped" + "/" + fullFile))
                        #TODO Try Catch to ensure
                except:
                    print("Cant uncompress")


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.FOLDER_TO_SORT = None
        self.master = master
        self.run = False
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.inputContent = tk.StringVar()
        self.inputText = tk.Entry(self, textvariable=self.inputContent)
        self.inputText.grid(row=0, column=0)
        self.inputText.insert(0, get_download_path())

        self.selectFileBtn = tk.Button(self)
        self.selectFileBtn["text"] = "Select File"
        self.selectFileBtn["command"] = self.selectFile
        self.selectFileBtn.grid(row=0, column=1)

        self.submit = tk.Button(self)
        self.submit["text"] = "Start"
        self.submit["command"] = self.startMonitor
        self.submit.grid(row=1, column=0)

        self.quit = tk.Button(self, text="CANCEL", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=1, column=1)


    def startMonitor(self):
        self.FOLDER_TO_SORT = self.inputContent.get()
        if self.FOLDER_TO_SORT != "" and os.path.isdir(self.FOLDER_TO_SORT):
            print(self.FOLDER_TO_SORT)
            self.run = True
            self.master.destroy()

    def selectFile(self):
        print("This")
        input = filedialog.askdirectory(initialdir = "/",title = "Select file")
        if input != "":
            self.inputText.delete(0, "end")
            self.inputText.insert(0, input)


# Credit https://stackoverflow.com/questions/35851281/python-finding-the-users-downloads-folder
def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    run = app.run

    if run:
        print(app.FOLDER_TO_SORT)
        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, app.FOLDER_TO_SORT, recursive=False)
        observer.start()
        try:
            while run:
                time.sleep(2)
                print("Hi")
                observer.stop()
        except KeyboardInterrupt:
            observer.stop()
