import os
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(folder_to_track):
            path = os.path.join(folder_to_track, filename)
            if path in paths.values():
                continue
            ext = filename.rpartition('.')[-1].lower()
            ext = '.'+ext
            src = folder_to_track + "/" + filename
            new_destination = paths[(extension_type[ext] if ext in extension_type else "misc")] + "/" + filename
            os.rename(src, new_destination)


folder_to_track = sys.argv[1]
if not os.path.isdir(folder_to_track):
    print("This Folder does not exist")
    raise SystemExit

paths = {
    "images": os.path.join(folder_to_track, "images"),
    "videos": os.path.join(folder_to_track, "videos"),
    "zip": os.path.join(folder_to_track, "zip"),
    "exe": os.path.join(folder_to_track, "exe"),
    "documents": os.path.join(folder_to_track, "documents"),
    "html": os.path.join(folder_to_track, "html"),
    "music": os.path.join(folder_to_track, "music"),
    "misc": os.path.join(folder_to_track, "misc")
}
extensions_folders = {
    "images": ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.tiff', '.psd', '.raw', '.bmp', '.heif', '.indd'],
    "videos": [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg", ".mp4", ".m4p", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv"],
    "zip": [".zip", ".rar", ".7z", ".gz", '.7zip'],
    "exe": [".exe", ".app", ".vb", ".scr", '.bat', ".jar"],
    "documents": [".pdf", ".txt", ".doc", ".docx", '.xls', '.xlsx', '.ppt', '.pptx'],
    "html": [".html", ".css"],
    "music": [".aac", ".wma", ".wav", '.mp3', '.flac', '.m4a']
}
extension_type = dict((ext, folder) for folder, extensions in extensions_folders.items() for ext in extensions)
for newpath in paths.values():
    if not os.path.isdir(newpath):
        os.makedirs(newpath)
event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
