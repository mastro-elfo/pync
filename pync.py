#!/usr/bin/env python3

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from os import makedirs, remove
from os.path import join
from shutil import copy, move, rmtree
from time import sleep
from watchdog.observers import Observer
from watchdog.events import (
    DirCreatedEvent,
    DirDeletedEvent,
    # DirModifiedEvent,
    DirMovedEvent,
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    FileSystemEventHandler,
)


class Handler(FileSystemEventHandler):
    def __init__(self, src, dst, *args, **kwargs):
        self.src, self.dst = src, dst
        super().__init__(*args, **kwargs)
        print("Pyncing", self.src, "to", self.dst)
        print("Press CTRL+C to stop")

    def on_created(self, event):
        print("Created", event)
        if isinstance(event, DirCreatedEvent):
            makedirs(event.src_path.replace(self.src, self.dst), exist_ok=True)
        elif isinstance(event, FileCreatedEvent):
            copy(event.src_path, event.src_path.replace(self.src, self.dst))

    def on_deleted(self, event):
        print("Deleted", event)
        try:
            if isinstance(event, DirDeletedEvent):
                rmtree(event.src_path.replace(self.src, self.dst))
            elif isinstance(event, FileDeletedEvent):
                remove(event.src_path.replace(self.src, self.dst))
        except FileNotFoundError:
            print("File or directory not found in ", self.dst)

    def on_modified(self, event):
        print("Modified", event)
        if isinstance(event, FileModifiedEvent):
            copy(event.src_path, join(self.dst, event.src_path.replace(self.src, "")))

    def on_moved(self, event):
        print("Moved", event)
        try:
            if isinstance(event, FileMovedEvent) or isinstance(event, DirMovedEvent):
                move(
                    event.src_path.replace(self.src, self.dst),
                    event.dest_path.replace(self.src, self.dst),
                )
        except FileNotFoundError:
            print("File or directory not found in ", self.dst)


def main():
    parser = ArgumentParser(
        prog="pync",
        usage=None,
        description="\n".join(
            ["Keep two directories in sync with Python", "Version 1.1"]
        ),
        epilog="\n".join(
            [
                "To install execute:",
                "cp pync.py ~/.local/bin/pync",
                "chmod u+x ~/.local/bin/pync",
            ]
        ),
        parents=[],
        prefix_chars="-",
        fromfile_prefix_chars=None,
        argument_default=None,
        conflict_handler="error",
        add_help=True,
        formatter_class=RawDescriptionHelpFormatter,
    )

    parser.add_argument("src", metavar="SRC", help="Source directory")
    parser.add_argument("dst", metavar="DST", help="Destination directory")
    parser.add_argument(
        "--no-recursion",
        default=False,
        action="store_const",
        const=True,
        help="Monitor only source directory",
    )

    args = parser.parse_args()

    observer = Observer()
    handler = Handler(args.src, args.dst)
    observer.schedule(handler, args.src, recursive=not args.no_recursion)
    observer.start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    # Wait until the thread terminates.
    observer.join()


if __name__ == "__main__":
    main()
