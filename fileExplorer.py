import os
from pathlib import Path


def recursiveExplorer(path):
    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                yield from recursiveExplorer(entry.path)
            elif entry.name == '.SyncLock':
                yield None
            else:
                yield entry
    except Exception as err:
        print("Error: " , err.__class__)
        yield None


def main():
    baseDir = 'F:\Finished Downloads'
    for each in recursiveExplorer(baseDir):
        if each != None:
            res = str(Path(each.path)).replace(baseDir + '\\', '')
            print(res)


if __name__ == '__main__':
    main()
