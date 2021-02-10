import os
from configparser import ConfigParser
from pathlib import Path

from telethon.sync import TelegramClient, events

import fileExplorer

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
    config.read('config.ini')
    API_ID = config.getint('authentication', 'api_id')
    API_HASH = config.get('authentication', 'api_hash')
    # reading channels from config.ini
    CHANNEL_ID = config.getint('channels', channelName)
    # base directory for current job
    DIR = baseDir

def progressBar(current, total, barLength = 50):
    percent = float(current) * 100 / total
    bar   = '█' * int(percent/100 * barLength - 1) + '█'
    spaces  = ' ' * (barLength - len(bar))
    print('Progress: [%s%s] %d %%' % (bar, spaces, percent), end='\r')

def deleteFile(file):
    try:
        os.remove(file.path)
    except Exception as err:
        print("Error on Delete: " , err.__class__)

def uploadFile(delete_on_complete = True):
    #recursively iter thru all the files in the base directory
    for file in fileExplorer.recursiveExplorer(DIR):
        if file != None:
            fileSize = os.path.getsize(file.path)
            if fileSize < MAX_FILE_SIZE:      #check if the file at hand is larger than 2GiB
                fileName = str(Path(file.path)).replace(DIR + '\\', '')     # cleaning file name by removing base directory and trailing '\'

                print('Uploading: ' + fileName)
                with TelegramClient('session', API_ID, API_HASH) as client:
                    client.send_file(entity=CHANNEL_ID, file=file.path, caption=fileName, force_document=False, progress_callback=progressBar, supports_streaming=True, fileSize=fileSize)

                    if delete_on_complete:
                        print('\nDeleting: ' + fileName)
                        deleteFile(file)
                    print('\n')
            else:
                print("FILE TOO BIG!:", fileName)

def main():
    configure(channelName= 'homework', baseDir='F:\\Homework folder\\new')
    uploadFile()


if __name__ == '__main__':
    main()
    exit()
