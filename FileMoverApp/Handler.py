class MyHandler(FileSystemEventHandler):
    def __init__(self, folder):
        self.folder = folder
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
        folderToSort = self.folder
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
