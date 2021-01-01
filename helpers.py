
import datetime
import time
import platform
import os
import json
import magic

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

def saveJsonData(data):
    type(data)
    try:
        os.mkdir('DATA')
    except FileExistsError:
        pass
    with open(f'STIX_{currDate()}.json', 'w', encoding="utf-8") as opFile:
        # for obj in data:
        # try:
        #     json.dump(data, opFile, ensure_ascii=False, indent=4)
        #     print('[INFO] Successfully wrote a JSON file in the same directory.ffds')
        # except:
        #     jsonStr = json.dumps(data, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        #     # opFile.write(jsonStr)
        #     print('[INFO] Successfully wrote a JSON file in the same directory.')
        # finally:

        # Since the data is already serialized by STIX2, we don't need another go.
        opFile.write(data)

'''Checks the extension of a file to see if an automated import is possible'''
def extCheck(filename):
    #TODO: Add support for more filetypes to import IOCs from

    acceptable_extensions = ['txt', 'csv']

    ext = filename.split('.')
    try:
        if ext[1] not in acceptable_extensions:
            return False
    except IndexError:
        # It's a file without an extension
        if ext not in acceptable_extensions:
            return False
    except:
        return False

'''Return the files in the current directory and all its child directories'''
def getAllFiles(dir):

    targetFiles = []
    fileCount = 0

    for root, dirs, files in os.walk(dir):
        for file in files:
            # Failure to match the extension will be neglected for now...
            if extCheck(file) == False:
                continue
            fileName = os.path.abspath(os.path.join(root, file))
            fileCount += 1
            try:
                print(f'[+] IOC file found: {fileName}')
                targetFiles.append(fileName)
            except:
                print(f"[-] An error occured while processing file: {fileName}")

    print(f"[+] Located all files. Final Count: {fileCount}")
    return targetFiles

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