import os
import uuid
import argparse
import configparser

from stix2 import Indicator
from helpers import *

'''Checks the extension of a file to see if an automated import is possible'''
def extCheck(filename):
    #TODO: Add support for more filetypes to import IOCs from

    acceptable_extensions = ['md', 'txt']

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

def parseFiles(files):


    print("[+] Parsing files now...")
    for file in files:
        with open(file, 'r') as fileObj:
            for line in fileObj:
                print(line)


def testStix():
    indicator = Indicator(name="File hash for malware variant",
                          pattern="[file:hashes.md5 = 'd41d8cd98f00b204e9800998ecf8427e']",
                          pattern_type="stix")
    print(indicator)

