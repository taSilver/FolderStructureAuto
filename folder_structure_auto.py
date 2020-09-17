import os
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class MyHandler(FileSystemEventHandler):
    def __init__(self, folder_to_track, ext_type_path):
        self.folder_to_track = folder_to_track
        self.ext_type_path = ext_type_path

    def on_modified(self, event):
        redo_dir(self.folder_to_track, self.ext_type_path)


def redo_dir(folder_to_track, ext_type_path):
    print("Reformatting " + folder_to_track)
    paths = set(ext_type_path.values())
    chk_folders(paths)
    for filename in os.listdir(folder_to_track):
        path = os.path.join(folder_to_track, filename)
        if path in paths:
            continue
        ext = filename.rpartition('.')[-1].lower()
        src = folder_to_track + "/" + filename
        new_destination = ext_type_path[ext if ext in ext_type_path else "other"] + "/" + filename
        os.rename(src, new_destination)
    print("Complete")


def org_mod_date(folder):
    pass  # TODO Create function to organise into folders by last modified by 6 months


def chk_folders(paths):
    for new_path in paths:
        if not os.path.isdir(new_path):
            os.makedirs(new_path)


def set_observer(folder_to_track, ext_type_path):
    event_handler = MyHandler(folder_to_track, ext_type_path)
    observer = Observer()
    observer.schedule(event_handler, folder_to_track, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Exiting")
        observer.stop()
    observer.join()


if __name__ == '__main__':
    folder_to_track = sys.argv[1]
    if not os.path.isdir(folder_to_track):
        print("This Folder does not exist")
        raise SystemExit

    extensions_folders = {
        "images": ['jpg', 'jpeg', 'png', 'gif', 'webp', 'tiff', 'psd', 'raw', 'bmp', 'heif', 'indd'],
        "videos": ["webm", "mpg", "mp2", "mpeg", "mpe", "mpv", "ogg", "mp4", "m4p", "m4v", "avi", "wmv", "mov", "qt",
                   "flv"],
        "zip": ["zip", "rar", "7z", "gz", '7zip'],
        "exe": ["exe", "app", "vb", "scr", 'bat', "jar"],
        "documents": ["pdf", "txt", "doc", "docx", 'xls', 'xlsx', 'ppt', 'pptx'],
        "html": ["html", "css"],
        "music": ["aac", "wma", "wav", 'mp3', 'flac', 'm4a'],
        "misc": ["other"]
    }
    ext_type_path = dict(
        (ext, os.path.join(folder_to_track, folder)) for folder, extensions in extensions_folders.items() for ext in
        extensions)

    if input("Reformat existing directory? [Y/N]").lower() == "y":
        redo_dir(folder_to_track, ext_type_path)
    set_observer(folder_to_track, ext_type_path)


