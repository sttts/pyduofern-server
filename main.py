import argparse
import sys

from pyduofern.duofern_stick import DuofernStickThreaded
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/devices/<device>/up')
def up(device):
    stick.command(device, "up")


@app.route('/devices/<device>/down')
def down(device):
    stick.command(device, "down")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web service for a duofern USB stick.')
    parser.add_argument('--code', help='the pairing code')
    parser.add_argument('--debug', '-d', help='debug mode', action='store_true')
    parser.add_argument('--listen', '-l', help='to address to listen on', default='127.0.0.1')
    parser.add_argument('--port', '-p', help='to port to listen on', default='8080')
    parser.add_argument('--device', help='the USB stick device', default=None)
    args = parser.parse_args(sys.argv[1:])

    stick = DuofernStickThreaded(serial_port=args.device, system_code=args.code)
    stick._initialize()
    stick.start()

    app.run(debug=args.debug is True, host=args.listen, port=args.port)
