from helpers import *
from stix_bundler import *

import logging

'''Parse command-line arguments for the user to enter'''
def parseArgs():
    # TODO Add files support for hash files
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", metavar="File to import", required=False, help="Input the file to use for an import")
    ap.add_argument("--dir", metavar="Directory to scan", required=False, help="Directory to scan for IOC files")
    args = vars(ap.parse_args())
    return args

'''Sanitize the command-line arguments after a basic check'''
def sanitizeArgs(args):

    if not args['dir'] and not args['file']:
        print("[INFO] Reverting to the current directory for a file search")
        args['dir'] = '.'
    elif args['dir'] and os.path.isdir(args['dir']):
        print('[ERROR] Specified path does not exist')
        exit()
    elif args['file'] and os.path.exists(args['file']):
        print('[ERROR] Specified file does not exist')
        exit()

def init():
    checkOS()

    args = parseArgs()
    sanitizeArgs(args)

    toParseFiles = getAllFiles(args['dir'])
    parseFiles(toParseFiles)

if __name__ == '__main__':
    logging.basicConfig(filename='errors.log', filemode='w', level=logging.DEBUG)
    init()