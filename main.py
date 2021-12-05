import os
import sys
from configparser import ConfigParser
from pathlib import Path

from telethon.sync import TelegramClient, events

API_ID = 0
API_HASH = ''
DIR = ''
CHANNEL_ID = 0
MAX_FILE_SIZE = 2097152000

def configure(channelName : str, baseDir : str):
    global DIR
    global API_ID
    global API_HASH
    global CHANNEL_ID

    # Reading authentication params from config.ini
    config = ConfigParser()

    try:
        config.read('config.ini')		#try to read config file
    except Exception as err:
        print("Error : " , err.__class__)

    API_ID = config.getint('authentication', 'api_id')
    API_HASH = config.get('authentication', 'api_hash')

    # reading channels from config.ini
    if channelName != '':
        CHANNEL_ID = config.getint('channels', channelName)
    else:
        print("Specify channel name")
        exit()

    # base directory for current job
    if baseDir != '':
        DIR = baseDir
    else:
        print("Specify ROOT folder!")
        exit()


def progressBar(current, total, barLength = 50):	# Draws a progress bar
    percent = float(current) * 100 / total
    bar   = '█' * int(percent/100 * barLength - 1) + '█'
    spaces  = ' ' * (barLength - len(bar))
    print('Progress: |%s%s| %d %%' % (bar, spaces, percent), end='\r')

def deleteFile(file):	# delete file method
    try:
        os.remove(file.path)
    except Exception as err:
        print("Error on Delete: " , err.__class__)
        exit()

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

def uploadFile(delete_on_complete = False):
    for file in recursiveExplorer(DIR):    #recursively iter thru all the files in the base directory
        if file != None:
            fileSize = os.path.getsize(file.path)
            if fileSize < MAX_FILE_SIZE:      #check if the file at hand is larger than 2GiB
                cleaned_dir_name = DIR.replace('//','\\')
                fileName = str(Path(file.path)).replace(cleaned_dir_name + '\\', '')     # cleaning file name by removing base directory and trailing '\'
                
                print('Uploading: ' + fileName)
                with TelegramClient('session', API_ID, API_HASH) as client:
                    client.send_file(entity=CHANNEL_ID, file=file.path, caption=fileName, force_document=False, progress_callback=progressBar, supports_streaming=True, fileSize=fileSize)

                    if delete_on_complete:
                        print('\nDeleting: ' + fileName)
                        deleteFile(file)
                    print('\n')
            else:
                print("FILE TOO BIG!:", fileName)

def getDirName():	# GUI prompt to select Base Directory
    import tkinter
    from tkinter import filedialog

    root = tkinter.Tk()
    root.withdraw()

    path = ''
    while path == '':
        print('SELECT BASE DIRETORY!')
        path = filedialog.askdirectory()

    return str.replace(path, '/','//')

def main():
    configure(channelName= 'homework', baseDir= getDirName())

    delete_on_complete = input("Delete on complete? Y/N \n")
    if delete_on_complete in ['Y','y','Yes','YES','yes','True','TRUE','true'] : delete_on_complete = True
    else: delete_on_complete = False

    uploadFile(delete_on_complete=delete_on_complete)

if __name__ == '__main__':
	#handle args
    main()
    exit()
