import time
from fileMover import FileMover
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def __init__(self, folder, fileTypeDict, decompressionEnabled):
        super(MyHandler, self).__init__()
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
        self.fileTypes = fileTypeDict
        self.folder = folder
        self.decompressionEnabled = decompressionEnabled


    def on_any_event(self, event):
        time.sleep(0.2)
        FileMover.sortDirectory(self.folder, self.fileTypes, self.decompressionEnabled)
