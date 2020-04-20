import os
import re
from datetime import datetime
from zipfile import ZipFile

class FileMover():
    def __init__(self):
        pass

    def sortDirectory(folderToSort, filterDict, decompressionEnabled):
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
            type = filterDict.get(fileExt.lower(), "Other")
            targetFolder = os.path.join(folderToSort, type + "/")
            if not (os.path.isdir(targetFolder)):
                os.makedirs(targetFolder)
            fileName = FileMover.getName(fileName, fileExt, targetFolder)
            #Reform into a fill file name
            fullFile = (fileName + "." + fileExt)
            print(targetFolder + fullFile)
            print(type)
            #Move it to the target folder
            os.rename(fullPath, targetFolder + fullFile)
            #Check if its a compressed file
            if type == "Compressed" and decompressionEnabled == True:
                try:
                    with ZipFile(targetFolder + fullFile, 'r') as zipObj:
                        #Extract it to the unzipped folder
                        zipObj.extractall(os.path.join(folderToSort, "Unzipped" + "/" + fileName))
                        #TODO Try Catch to ensure
                except:
                    print("Cant uncompress")

    def getName(fileName, fileExt, targetFolder):
        dateTimeMod = re.compile(r'\[\d{2}-\d{2}-\d{4}\]$')
        dateTimeMulMod = re.compile(r'\[\d{2}-\d{2}-\d{4}\]\(\d+\)$')
        # Checks if file is already in folder
        while (fileName + "." + fileExt) in os.listdir(targetFolder):
            # Check if file already has a datetime stamp at the end
            containsDatetime = dateTimeMod.search(fileName) != None;
            # Checks if file already has datetime stamp and there are multiple
            # files of the same name with the datetime stamp
            containsDatetimeMul = dateTimeMulMod.search(fileName) != None;

            # If it already ends in a date
            if containsDatetime == True:
                print("File has Date")
                # Remove current date and add the current date
                fileName = re.sub(dateTimeMod, "", fileName)
                print(fullFile)
                saveTime = datetime.now()
                saveTime = saveTime.strftime("%d-%m-%Y")
                # If it already ends in the same date
                if (fileName + "." + fileExt) in os.listdir(targetFolder):
                    print("File already ends in date")
                    # Make it a duplicate file
                    fileName = re.sub(dateTimeMod, "", fileName)
                    fileName = fileName + "[" + saveTime + "]" + "(1)"
                    continue
                fileName = fileName + "[" + saveTime + "]"
            #If it ends in a date and there are already multiple files with that date
            elif containsDatetimeMul == True:
                print("File has Date and multiple")
                nextAvaliableEnd = dateTimeMulMod.search(fileName)
                print(nextAvaliableEnd)
                nextAvaliableEnd = nextAvaliableEnd[0]
                nextAvaliableEnd = int(nextAvaliableEnd[13:len(nextAvaliableEnd)-1])
                print(nextAvaliableEnd)
                nextAvaliableEnd += 1
                nextAvaliableEnd = str(nextAvaliableEnd)
                fileName = re.sub(dateTimeMulMod, "", fileName)
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
        return fileName
