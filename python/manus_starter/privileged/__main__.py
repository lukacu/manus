#!/usr/bin/env python
import sys
import os
import hashlib
import echolib
from manus.privileged import PrivilegedCommand, PrivilegedCommandType, PrivilegedCommandSubscriber

from manus_starter.privileged import *

if __name__ == '__main__':
    testing = bool(os.getenv('MANUS_TESTING', False))
    loop = echolib.IOLoop()

    def control_callback(command):
        print "Running privileged command: %s" % PrivilegedCommandType.str(command.type)
        if testing:
            return
        try:
            if command.type == PrivilegedCommandType.SHUTDOWN:
                manus_privileged.run_shutdown()
            elif command.type == PrivilegedCommandType.RESTART:
                manus_privileged.run_restart()
            elif command.type == PrivilegedCommandType.UPGRADE:
                manus_privileged.run_upgrade()
        except Exception, e:
            print traceback.format_exc()

    def shutdown_handler(signum, frame):
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown_handler)

    client = echolib.Client()
    loop.add_handler(client)

    control = PrivilegedCommandSubscriber(client, "privileged", control_callback)

    try:
        while True:
            loop.wait(100)
    except KeyboardInterrupt:
        pass
    finally:
        pass

    shutdown_handler(0, None)