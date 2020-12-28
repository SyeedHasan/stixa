import os
import uuid
import argparse
import configparser
import logging
import re

from stix2 import Indicator, Bundle
from helpers import *

log = logging.getLogger(__name__)

'''Checks the extension of a file to see if an automated import is possible'''
def extCheck(filename):
    #TODO: Add support for more filetypes to import IOCs from

    acceptable_extensions = ['txt']

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


def sanitizeIOC(ioc):

    if re.match("(^|[^a-fA-F0-9])[a-fA-F0-9]{32}([^a-fA-F0-9]|$)", ioc) is not None:
        return "file:hashes.md5"
    elif re.match(r"\b[0-9a-f]{40}\b", ioc) is not None:
        return "file:hashes.sha1"
    elif re.match(r"^[A-Fa-f0-9]{64}$", ioc) is not None:
        return "file:hashes.sha256"
    elif re.match(r"\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b", ioc) is not None:
        return "ipv4-addr:value"
    elif re.match(r"^((?!-))(xn--)?[a-z0-9][a-z0-9-_]{0,61}[a-z0-9]{0,1}\.(xn--)?([a-z0-9\-]{1,61}|[a-z0-9-]{1,30}\.[a-z]{2,})$", ioc) is not None:
        return "domain-name:value"
    else:
        return False

def createIndicators(IOC, name, iocType):

    pattern = f"[{iocType} = '{IOC}']"

    indicator = Indicator(name=name, pattern=pattern, pattern_type="stix")
    return indicator

def bundleIndicators(indicators):

    bundle = Bundle(*indicators).serialize()

    return bundle

''' Parse the IOC files for extraction, sanitization, and STIX bundling '''
def parseFiles(files):

    print("[+] Parsing files now...")
    allIndicators = []

    for file in files:
        with open(file, 'r') as fileObj:
            for line in fileObj:

                #Skip empty lines
                if line.rstrip('\n') == "":
                    continue

                line.rstrip('\n').split(';')
                # Try to separate a comment from the actual indicator
                try:
                    cleanedData = line.rstrip('\n').split(';')
                    ioc = cleanedData[0]
                    name = cleanedData[1]

                except ValueError:
                    log.debug(f"Reverting to using the indicator as identifier for: {line}")
                    ioc = line.rstrip('\n').split(';')
                    name = ioc[0]

                except:
                    log.debug(f"Unknown issue detected for the indicator: {line}")
                    continue

                finally:
                    iocType = sanitizeIOC(ioc)

                    # Invalid IOC or something I don't wish to cover right now!
                    if type is False:
                        log.debug(f"IOC type is either incorrect or currently not covered by Stixa. Kindly re-try manual ingestion for {ioc}")

                    allIndicators.append(createIndicators(ioc, name, iocType))


    print("[+] Completed Parsing. Total Number of Indicators:", len(allIndicators))


    finalBundle = bundleIndicators(allIndicators)
    print("[+] Completed forming a bundle")
    saveJsonData(finalBundle)


def testStix():
    indicator = Indicator(name="File hash for malware variant",
                          pattern="[file:hashes.md5 = 'd41d8cd98f00b204e9800998ecf8427e']",
                          pattern_type="stix")
    print(indicator)

