class Settings():
    def __init__(self):
        self.ExtDict = {}
        self.file = ""

    def loadSettings(self, file):
        try:
            fileToLoad = open(file, "r")
            if fileToLoad.mode == 'r':
                contents = fileToLoad.readlines()
                contents = list(map(lambda x : x.rstrip("\n\r"), contents))
                if contents[0] == "#FileSortSettings":
                    return self.createStructure(contents)
                print(contents)
            fileToLoad.close()
        except FileNotFoundError:
            print("File Not Found")
            #Throw a custom file not found error

    def createStructure(self, listToConvert):
        directories = []
        fileTypes = {}
        structureList = []
        prevDepth = 0
        prevDir = ""
        for index, value in enumerate(listToConvert):
            if value == "":
                continue
            depth = 0
            type = None
            name = ""
            nameStart = 0
            for i, v in enumerate(value):
                if v == "#":
                    value = value[:i]
                    break
                elif v == " ":
                    depth += 1
                elif v == "*":
                    if type == None:
                        type = "dir"
                        nameStart = i
                    else:
                        print("EXCEPTION: INVALID SYMBOL")
                elif v == "-":
                    if type == None:
                        type = "file"
                        nameStart = i
                    else:
                        print("EXCEPTION: INVALID SYMBOL")
            name = value[nameStart+1:]
            if type == "dir":
                if name in directories:
                    print("EXCEPTION: MULTIPLE DIRECTORIES OF SAME NAME")
                directories.append(name)
                if depth == 0:
                    #print("New")
                    prevDir = "/" + name
                elif depth >= prevDepth:
                    #print("up")
                    prevDir = prevDir + "/" + name
                else:
                    #print("down")
                    prevDir = prevDir.split("/")
                    prevDir = prevDir[1:]
                    prevDir = prevDir[:depth]
                    prevDir = "/".join(prevDir)
                    prevDir = "/" + prevDir + "/" + name
                prevDepth = depth

            # print("Full: " + value)
            #print("Depth: " + str(depth))
            # print("Type: " + str(type))
            #print("Name: " + name)
            if type == "file":
                #print(prevDir)
                tempDir = prevDir
                tempDir = tempDir.split("/")
                #print(tempDir)
                tempDir = tempDir[:depth+1]
                #print(tempDir)
                tempDir = "/".join(tempDir)
                print("Path: " + tempDir + "/" + name)
                if fileTypes.get(name) == None:
                    fileTypes[name] = tempDir[1:]
                else:
                    print("EXCEPTION: DUPLICATE FILE NAME")
                    #TODO THOW CUSTOM EXCEPTION
            else:
                print("Path: " + prevDir + "/")
        # print("This")
        # print(fileTypes.get("SubSubFile"))
        # print(fileTypes.get("awiudhjaoiw"))
        return fileTypes

    def saveSettings(self, fileTypes, saveFile):
        directories = fileTypes.values()
        uniqueDirs = list(set(directories))
        print(directories)
        print(uniqueDirs)
        uniqueDirs = list(map(lambda x : x.split("/"), uniqueDirs))
        print(uniqueDirs)
        uniqueDirs = sorted(uniqueDirs, key = lambda x : len(x))
        print(uniqueDirs)
        fileOutput = self.getDirs(fileTypes, uniqueDirs, "", 0, "")
        print("FileOutput")
        fileOutput = "#FileSortSettings" + fileOutput
        print(fileOutput)

        try:
            fileToLoad = open(saveFile, "w")
            fileToLoad.write(fileOutput)
            fileToLoad.close()
        except FileNotFoundError:
            print("File Not Found")
            #Throw a custom file not found error


    def getDirs(self, fileTypes, uniqueDirs, baseDir, baseDirDepth, THEOUTPUT):
        for index, value in enumerate(uniqueDirs):
            if len(value) == baseDirDepth + 1 and value[baseDirDepth - 1] == baseDir:
                THEOUTPUT += "\n" + " " * (len(value)-1) + "*" + value[len(value)-1]
                for fileType, directory in fileTypes.items():
                    if directory == "/".join(value):
                        THEOUTPUT += "\n" + " " * (len(value)) + "-" + fileType
                THEOUTPUT = self.getDirs(fileTypes, uniqueDirs, value[baseDirDepth], baseDirDepth + 1, THEOUTPUT)
            elif len(value) == baseDirDepth + 1 and len(value) == 1:
                THEOUTPUT += "\n\n" + "*" + value[0]
                for fileType, directory in fileTypes.items():
                    if directory == "/".join(value):
                        THEOUTPUT += "\n" + " " * (len(value)) + "-" + fileType
                THEOUTPUT = self.getDirs(fileTypes, uniqueDirs, value[baseDirDepth], baseDirDepth + 1, THEOUTPUT)
        return(THEOUTPUT)



settings = Settings()
filesTypes = settings.loadSettings("file.txt")
print(filesTypes)
settings.saveSettings(filesTypes, "newsettings.txt")

        # ImgExt = ["ai", "bmp", "gif", "ico", "jpeg", "png", "ps", "psd", "svg", "tif", "jpg"]
        # DictExt = dict.fromkeys(ImgExt, "Images")
        # VidExt = ["webm", "mpg", "mp2", "mpeg", "mpe", "mpv", "ogg", "mp4", "m4p", "m4v", "avi", "wmv", "mov", "qt", "flv", "swf", "avchd"]
        # DictExt.update(dict.fromkeys(VidExt, "Videos"))
        # AudioExt = ["aif", "cda", "mid", "mp3", "mpa", "ogg", "wav", "wma", "wpl"]
        # DictExt.update(dict.fromkeys(AudioExt, "Audio"))
        # CompressedExt = ["7z", "arj", "deb", "pkg", "rar", "rpm", "tar", "z", "zip"]
        # DictExt.update(dict.fromkeys(CompressedExt, "Compressed"))
        # DataExt = ["csv", "dat", "db", "log", "mdb", "sav", "sql", "tar", "xml"]
        # DictExt.update(dict.fromkeys(DataExt, "Data"))
        # ExeExt = ["apk ", "bat", "bin,", "cgi", "com", "exe", "gadget", "jar", "msi", "wsf"]
        # DictExt.update(dict.fromkeys(ExeExt, "Executables"))
        # ProgrammingExt = ["c", "class", "cpp", "cs", "h", "java", "pl", "sh", "swift", "vb", "py"]
        # DictExt.update(dict.fromkeys(ProgrammingExt, "Programming"))
        # TextExt = ["doc", "docx", "odt", "pdf", "tex", "txt", "wpd", "pptx"]
        # DictExt.update(dict.fromkeys(TextExt, "Text"))
        # settingsFile = open()


# Exceptions
# Invalid Naming
# Same Name Directory Exception
# File Name in Two places


# Invalid Formatting
# No File Types In folder Exception
# Invalid Indentation
# Invalid Symbol
