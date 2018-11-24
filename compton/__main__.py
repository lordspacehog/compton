import signal
import sys
import logging
import compton

logging.basicConfig(level=logging.DEBUG)


def handle_kbint(signum, frame):
    print("Exiting")
    sys.exit(0)


if __name__ == '__main__':
    print("Listening for events...")
    signal.signal(signal.SIGINT, handle_kbint)
    compton.run_server()
