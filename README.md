# File Moving Project
This is a little project I worked on over a couple of weekends to make sorting my downloads/all folders easier!

This is my first full python programme and I have tried to keep the code managable and reasonably readable. All code is run from the __main__.py file and I have attempted to modualise all the parts of the programme into classes. I have also built some custom exceptions which can be found in the settingsExceptions.py file.

Please feel free to use or edit the program in any way you you want to. Also if you would like to extend the functionality feel free to make a pull request and I'll grant anything that seems generally useful to anyone.

# Instructions of use

## Basic Program Use

![Example UI](https://github.com/HudsonFinn/FileMover/blob/master/FileMoverApp/Media/UI.JPG)

This is the basic UI it allows you to control the programme.

Folder to sort:
Select any folder on your system, this is the target folder that will be sorted. All files in the folder will be sorted but BASIC (see unzip below) folders are ignored as I concider folders to already be a sorting mechanism for most users and/or programmes, if there are requests I may change this in the future.

Sorting profile:
More of an advanced feature, the program allows you to create a multiple profiles as to how you want your folders sorted, there are multiple default profiles in the default directory but if your not sure just use the default profile.txt this is already in the search bar on startup. Profiles are explained in the profiles section.

Unzip:
This is a toggle that allows you to enable the automatic unzipping of all files within the folder. In all standard sorting profiles all compressed folders are placed in the compressed folder, when this option is enables all avaliable folders will be unzipped and placed in the unzipped folder.

Single sort:
This will perform a full sort of the specified directory with the specified profile once. It will keep the application open and can be performed as may times as you want.

Start Monitor: This will close the UI of the application and run it in the background, whenever a change is made to the deirectory specified it will perform as single sort of that directory, this may be useful to run on startup and then monitor the downloads folder so that you dont have to worry about manually sorting it.

## Setting up profiles
Profile work based on a .txt file in which you can specify any folder structure, the programme will debug the .txt files for you 
