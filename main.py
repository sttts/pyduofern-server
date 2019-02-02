import argparse
import logging
import os
import sys

import time

import tempfile
from pyduofern.duofern_stick import DuofernStickThreaded, duoACK, duoSetPairs
from flask import Flask
from pyduofern.exceptions import DuofernTimeoutException

app = Flask(__name__)
logger = logging.getLogger(__file__)

def setPair(device):
    hex_to_write = duoSetPairs.replace('nn', '{:02X}'.format(0)).replace('yyyyyy', device)
    stick.send(hex_to_write)

@app.route('/')
def index():
    return "pyduofern-server"

@app.route('/devices/<device>/up')
def up(device):
    setPair(device)
    stick.command(device, "up")
    time.sleep(0.5)
    stick.command(device, "up")
    time.sleep(0.5)
    stick.command(device, "up")
    time.sleep(2)
    return "OK\n"

@app.route('/devices/<device>/down')
def down(device):
    setPair(device)
    stick.command(device, "down")
    time.sleep(0.5)
    stick.command(device, "down")
    time.sleep(0.5)
    stick.command(device, "down")
    time.sleep(2)
    return "OK\n"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web service for a duofern USB stick.')
    parser.add_argument('--code', help='the pairing code')
    parser.add_argument('--debug', '-d', help='debug mode', action='store_true')
    parser.add_argument('--listen', '-l', help='to address to listen on', default='127.0.0.1')
    parser.add_argument('--port', '-p', help='to port to listen on', default='8080')
    parser.add_argument('--device', help='the USB stick device', default=None)
    args = parser.parse_args(sys.argv[1:])

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    config_file = tempfile.NamedTemporaryFile(delete=False)
    config_file.write(b'{}')
    config_file.close()

    try:
        stick = DuofernStickThreaded(serial_port=args.device, system_code=args.code, config_file_json=config_file.name)
        stick._initialize()
        stick.start()

        app.run(debug=args.debug is True, host=args.listen, port=args.port)
    except:
        raise
    finally:
        os.unlink(config_file.name)
