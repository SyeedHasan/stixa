import os
import uuid
import argparse
import configparser
import logging
import re

from stix2 import Indicator, MarkingDefinition, Bundle
from helpers import *

log = logging.getLogger(__name__)

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
    # TODO: Add support for URLs
    # TODO: Add support for Yara rules
    # TODO: Add support for email
    # TODO: Add support for CVEs or vulnerability -- a type
    else:
        return False

def createIndicators(IOC, name, iocType):

    pattern = f"[{iocType} = '{IOC}']"
    indicator = Indicator(name=name, pattern=pattern, pattern_type="stix")
    return indicator

def bundleIndicators(indicators):

    bundle = Bundle(*indicators).serialize()
    return bundle

def textFileParser(file):
    print(f'[INFO] Parsing the text file {file}')

    indicators = []

    with open(file, 'r') as fileObj:
        for line in fileObj:
            #Skip empty lines
            if line.rstrip('\n') == "":
                continue

            # Try to separate a comment from the actual indicator
            try:
                cleanedData = line.rstrip('\n').split(';')
                ioc = cleanedData[0]
                name = cleanedData[1]

            except IndexError:
                log.debug(f"Reverting to using the indicator as identifier for: {line}")
                ioc = line.rstrip('\n')
                name = ioc

            except:
                log.debug(f"Unknown issue detected for the indicator: {line}")

            finally:
                if ioc:
                    iocType = sanitizeIOC(ioc)

                    # Invalid IOC or something I don't wish to cover right now!
                    if type is False:
                        log.debug(f"IOC type is either incorrect or currently not covered by Stixa. Kindly re-try manual ingestion for {ioc}")

                    indicators.append(createIndicators(ioc, name, iocType))


    print("[+] Completed Parsing. Total Number of Indicators:", len(indicators))
    return indicators

def csvFileParser(file):
    print(f'[INFO] Parsing the CSV file {file}')
    return []

''' Parse the IOC files for extraction, sanitization, and STIX bundling '''
def parseFiles(files):

    print("[+] Parsing files now...")

    allIndicators = []

    for file in files:
        ext = file.split('.')
        if ext[1] == "txt":
            allIndicators.extend(textFileParser(file))
        elif ext[1] == "csv":
            allIndicators.extend(csvFileParser(file))
        else:
            print('[ERROR] File format is not currently accepted for parsing.')
            pass

    finalBundle = bundleIndicators(allIndicators)
    print(f"[+] Completed forming a bundle of {len(allIndicators)} items")
    saveJsonData(finalBundle)
