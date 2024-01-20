#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import sys
import subprocess
from bluepy import btle
from bluepy.btle import Scanner, BTLEDisconnectError, BTLEManagementError, DefaultDelegate
from datetime import datetime
import logging
import getopt


def print_help():
    print('Usage: {:s} [-hv] address'.format(os.path.basename(__file__)))


logger = logging.getLogger(__name__)
log_level = logging.ERROR

try:
    opts, args = getopt.getopt(sys.argv[1:], "hv")
except getopt.GetoptError:
    print_help()
    sys.exit(1)
for opt, arg in opts:
    if opt == '-h':
        print_help()
        sys.exit()
    elif opt == '-v':
        log_level = logging.DEBUG

if len(args) != 1:
    print_help()
    sys.exit(-1)

logging.basicConfig(level=log_level)
mac = args[0].lower()

class ScanProcessor():
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr == mac and isNewDev:
            for (sdid, desc, data) in dev.getScanData():
                logger.debug('Data received: sdid: {:d}; description: {:s}; data: {:s}'.format(sdid, str(desc), str(data)))
                ### Xiaomi V1 Scale ###
                if data.startswith('1d18') and sdid == 22:
                    measunit = data[4:6]
                    weight = int((data[8:10] + data[6:8]), 16) * 0.01
                    unit = None
                    if measunit.startswith(('03', 'a3')):
                        unit = 'lbs'
                        weight = weight * 0.4536
                    elif measunit.startswith(('12', 'b2')):
                        unit = 'jin'
                        weight = weight * 0.5
                    elif measunit.startswith(('22', 'a2')):
                        unit = 'kg'
                        weight = weight * 0.5

                    if unit:
                        weight = round(weight, 2)
                        new_measure = {
                            'weight': weight,
                            'unit': 'kg',
                            'timestamp': datetime.utcnow().replace(microsecond=0).isoformat()
                        }
                        print(new_measure)


def main():
    try:
        scanner = btle.Scanner(0).withDelegate(ScanProcessor())
        scanner.scan(3, passive=True)
    except Exception as error:
        logger.error(error)


if __name__ == "__main__":
    main()
