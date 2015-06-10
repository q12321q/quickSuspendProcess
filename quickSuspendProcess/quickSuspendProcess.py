#!/usr/bin/env python
 
"""Quick Suspend Process

"""
 
import os
import sys
import argparse
import re
import psutil



class QuickSuspendProcess:
    def __init__(self, pattern):
        self.__pidList = None
        self.pattern = pattern

    def __refreshProcessList(self):
        self.__pidList = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'exe'])
            except psutil.NoSuchProcess:
                pass
            else:
                if pinfo["exe"] != None and self.__matchProcess(pinfo["exe"]):
                    self.__pidList.append(pinfo['pid'])

    def __matchProcess(self, name):
        return re.match(self.pattern, name, re.I) != None

    def resume(self):
        self.__refreshProcessList()
        for pid in self.__pidList:
            try:
                process = psutil.Process(pid)
                process.resume()
            except:
                print("Unable to resume pid %d" % pid)

    def suspend(self):
        self.__refreshProcessList()
        for pid in self.__pidList:
            try:
                process = psutil.Process(pid)
                process.suspend()
            except:
                print("Unable to suspend pid %d" % pid)

    def toggle(self):
        self.__refreshProcessList()
        firstStatus = None
        for pid in self.__pidList:
            try:
                process = psutil.Process(pid)
                if firstStatus == None:
                    firstStatus = process.status()

                if firstStatus == 'running':
                    process.suspend()
                else:
                    process.resume()
            except:
                print("Unable to toggle suspend/resume for pid %d" % pid)

    def display(self):
        self.__refreshProcessList()
        for pid in self.__pidList:
            try:
                process = psutil.Process(pid)
                print(process.name())
            except:
                print("Unable to suspend pid %d" % pid)




def main(arguments):

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--pattern', '-p', help="process name pattern", required=True)

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--suspend', '-s', action='store_const', const='suspend', dest='action')
    group.add_argument('--resume', '-r', action='store_const', const='resume', dest='action')
    group.add_argument('--toggle', '-t', action='store_const', const='toggle', dest='action')
    group.add_argument('--display', '-d', action='store_const', const='display', dest='action')

    args = parser.parse_args(arguments)

    qsp = QuickSuspendProcess(args.pattern)

    if args.action == 'suspend':
        qsp.suspend()
    elif args.action == 'resume':
        qsp.resume()
    elif args.action == 'toggle':
        qsp.toggle()
    else:
        qsp.display()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
