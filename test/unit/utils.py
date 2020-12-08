import os
import socket
import time

import pytest


def public_dir(path):
    os.chmod(path, 0o777)

    for root, dirs, files in os.walk(path):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o777)
        for f in files:
            os.chmod(os.path.join(root, f), 0o777)


def waitforfiles(*files):
    for i in range(50):
        wait = False

        for f in files:
            if not os.path.exists(f):
                wait = True
                break

        if not wait:
            return True

        time.sleep(0.1)

    return False


def waitforsocket(port):
    for i in range(50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.settimeout(5)
                sock.connect(('127.0.0.1', port))
                return

            except ConnectionRefusedError:
                time.sleep(0.1)

            except KeyboardInterrupt:
                raise

    pytest.fail('Can\'t connect to the 127.0.0.1:' + port)
