import os
import winreg
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from functools import partial
from settings import Settings
from fileMover import FileMover
from settingsExceptions import SettingsException

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.FOLDER_TO_SORT = None
        self.master = master
        self.master.title("File Sorter")
        self.master.iconbitmap('./Media/icon.ico')
        self.master.configure(bg="green")
        self.run = False
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.titleLabel = tk.Label(self, text="FILE SORTER", font="none 24 bold")
        self.titleLabel.grid(row=0, column=0, pady=5, padx=5, columnspan=2)

        self.folderLabel = tk.Label(self, text="Select folder to sort:",
                                anchor=tk.W,
                                font="none 10 bold")
        self.folderLabel.grid(row=1, column=0, pady=5, padx=5)

        self.inputContent = tk.StringVar()
        self.inputText = tk.Entry(self, textvariable=self.inputContent, width=30)
        self.inputText.grid(row=2, column=0, pady=5, padx=10, columnspan=2)
        self.inputText.insert(0, Application.getDownloadPath())

        self.selectFolderBtn = tk.Button(self, width=20)
        self.selectFolderBtn["text"] = "Select Folder"
        self.selectFolderBtn["command"] = self.selectDir
        self.selectFolderBtn.grid(row=2, column=2, pady=5, padx=5, columnspan=2)

        self.settingsLabel = tk.Label(self, text="Select sorting profile:",
                                    anchor=tk.W,
                                    font="none 10 bold")
        self.settingsLabel.grid(row=3, column=0, pady=5, padx=5)

        self.inputContentSettings = tk.StringVar()
        self.inputTextSettings = tk.Entry(self, textvariable=self.inputContentSettings, width=30)
        self.inputTextSettings.grid(row=4, column=0, pady=5, padx=10, columnspan=2)
        self.inputTextSettings.insert(0, Application.getDownloadPath())

        self.selectSettingsBtn = tk.Button(self, width=20)
        self.selectSettingsBtn["text"] = "Select Profile"
        self.selectSettingsBtn["command"] = self.selectFile
        self.selectSettingsBtn.grid(row=4, column=2, pady=5, padx=5, columnspan=2)

        self.errorLabel = tk.Label(self, text = "")

        self.decompressionEnabled = tk.IntVar()
        self.decompressionEnabledCheck = tk.Checkbutton(self, text="Unzip all", variable=self.decompressionEnabled).grid(row=6, pady=5, padx=5)

        self.submit = tk.Button(self, width=15)
        self.submit["text"] = "Start Monitor"
        self.submit["command"] = self.startMonitor
        self.submit.grid(row=7, column=0, pady=5, padx=5)

        self.singleSortBtn = tk.Button(self, width=10)
        self.singleSortBtn["text"] = "Single Sort"
        self.singleSortBtn["command"] = self.singleSort
        self.singleSortBtn.grid(row=7, column=1, pady=5, padx=5)

        self.quitBtn = tk.Button(self, text="CANCEL", fg="red",
                              command=self.master.destroy,
                              width=10)
        self.quitBtn.grid(row=7, column=2, pady=5, padx=5)

        self.helpBtn = tk.Button(self, text="HELP",
                              command=self.showHelp,
                              width=10)
        self.helpBtn.grid(row=7, column=3, pady=5, padx=5)


    def startMonitor(self):
        self.FOLDER_TO_SORT = self.inputContent.get()
        self.fileTypes = self.inputContentSettings.get()
        if self.FOLDER_TO_SORT != "" and os.path.isdir(self.FOLDER_TO_SORT):
            settings = Settings()
            try:
                self.fileTypes = settings.loadSettings(self.fileTypes)
            except SettingsException as e:
                self.errorLabel["text"] = e
                self.errorLabel.grid(row = 5, columnspan=3)
            else:
                self.run = True
                self.master.destroy()

    def singleSort(self):
        self.FOLDER_TO_SORT = self.inputContent.get()
        self.fileTypes = self.inputContentSettings.get()
        decompression = bool(self.decompressionEnabled.get())
        if self.FOLDER_TO_SORT != "" and os.path.isdir(self.FOLDER_TO_SORT):
            settings = Settings()
            try:
                fileTypes = settings.loadSettings(self.fileTypes)
            except SettingsException as e:
                self.errorLabel["text"] = e
                self.errorLabel.grid(row = 5, columnspan=3)
            else:
                FileMover.sortDirectory(self.FOLDER_TO_SORT, fileTypes, decompression)

    def selectDir(self):
        print("This")
        input = filedialog.askdirectory(initialdir = "/",title = "Select file")
        if input != "":
            self.inputText.delete(0, "end")
            self.inputText.insert(0, input)

    def selectFile(self):
        print("This")
        input = filedialog.askopenfilename(initialdir = "./Settings",title = "Select file", filetypes = [("text files","*.txt")])
        if input != "":
            self.inputTextSettings.delete(0, "end")
            self.inputTextSettings.insert(0, input)
            self.errorLabel.grid_forget()

    def showHelp(self):
        messagebox.showinfo("Instructions on use", "")


    # Credit https://stackoverflow.com/questions/35851281/python-finding-the-users-downloads-folder
    def getDownloadPath():
        """Returns the default downloads path for linux or windows"""
        if os.name == 'nt':
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'downloads')
