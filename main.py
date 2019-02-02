import argparse
import logging
import os
import sys
import time
import tempfile
import flask
import threading

from pyduofern.duofern_stick import DuofernStickThreaded, duoACK, duoSetPairs
from flask import Flask

app = Flask(__name__)
logger = logging.getLogger(__file__)
lock = threading.Lock()


def setPair(device):
    hex_to_write = duoSetPairs.replace('nn', '{:02X}'.format(0)).replace('yyyyyy', device)
    stick.send(hex_to_write)


def sendAndWait(device, cmd):
    stick.command(device, cmd)
    while len(stick.write_queue) > 0:
        time.sleep(0.1)


@app.route('/')
def index():
    return "pyduofern-server"


@app.route('/devices/<device>/up')
def up(device):
    if len(device) != 6:
        flask.abort(404)
        return
    try:
        with lock:
            setPair(device)
            sendAndWait(device, "up")
            time.sleep(0.5)
            sendAndWait(device, "up")
            time.sleep(0.5)
            sendAndWait(device, "up")
            time.sleep(2)
        return "OK\n"
    except KeyError:
        flask.abort(404)


@app.route('/devices/<device>/down')
def down(device):
    if len(device) != 6:
        flask.abort(404)
        return
    try:
        with lock:
            setPair(device)
            sendAndWait(device, "down")
            time.sleep(0.5)
            sendAndWait(device, "down")
            time.sleep(0.5)
            sendAndWait(device, "down")
            time.sleep(2)
        return "OK\n"
    except KeyError:
        flask.abort(404)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web service for a duofern USB stick.')
    parser.add_argument('--code', help='the pairing code')
    parser.add_argument('--debug', '-d', help='debug mode', action='store_true')
    parser.add_argument('--listen', '-l', help='to address to listen on', default='127.0.0.1')
    parser.add_argument('--port', '-p', help='to port to listen on', default='8080')
    parser.add_argument('--device', help='the USB stick device', default=None)
    parser.add_argument('--pair', help='start up for pairing and terminate after the pairing time', action='store_true')
    parser.add_argument('--pair-time', help='time to wait for pairing requests in seconds', metavar="seconds", default=60, type=int)
    args = parser.parse_args(sys.argv[1:])

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    config_file = tempfile.NamedTemporaryFile(delete=False)
    config_file.write(b'{}')
    config_file.close()

    try:
        stick = DuofernStickThreaded(serial_port=args.device, system_code=args.code, config_file_json=config_file.name)
        stick._initialize()
        stick.daemon = False
        stick.start()

        if args.pair:
            stick.pair(timeout=args.pair_time)
            time.sleep(args.pairtime + 0.5)
        else:
            app.run(debug=args.debug is True, host=args.listen, port=args.port)
    except KeyboardInterrupt:
        pass
    except Exception as error:
        print(error)
    finally:
        os.unlink(config_file.name)
