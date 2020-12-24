
import datetime
import time
import platform
import os
import json

'''

Datetime Functions

'''

def currDate():
    return datetime.date.fromtimestamp(time.time())

def currEpoch():
    return str(time.time()).split('.')[0]

def retPrevDate():
    return currDate()-datetime.timedelta(days=1)

def convertEpochToDatetime(epochTime):
    return datetime.datetime.fromtimestamp(epochTime/1000).strftime('%Y-%m-%d %H:%M:%S')

'''

Filesystem Functions


'''

def saveJsonData(self, data):
    try:
        os.mkdir('data')
    except FileExistsError:
        pass
    with open(f'STIX_{currDate()}.json', 'w', encoding="utf-8") as opFile:
        # for obj in data:
        json.dump(data, opFile, ensure_ascii=False, indent=4, )


'''

General Functions


'''

def checkOS():
    ''' Return screen clearing command as per OS '''

    o_sys = platform.system()
    if o_sys == "Windows":
        os.system('cls')
    elif o_sys == "Linux":
        os.system('clear')
    else:
        return

    print('''
    ------------------------------
    STIXA

    Version: 0.1
    Author: Syed Hasan
    -------------------------------

    ''')