class UnsupportedSystem(Exception):
    def __init__(self, message="This system is not supported"):
        self.message = message
        super().__init__(self.message)

class UserNotFound(Exception):
    def __init__(self, username: str, message="Specified user is nowhere to be found"):
        self.username = username
        self.message = message
        super().__init__(self.message)

try:
    import pwd
except ModuleNotFoundError:
    raise UnsupportedSystem(
        message="A pwd module is required; nowhere to be found(are you even UNIX-compatible?)")

import argparse, pyDHE, pickle, socket, sys
from math import ceil

parser = argparse.ArgumentParser(
    description='Passwordless authentication server')
parser.add_argument("--username", metavar="username",
                    type=str, help="Generate authentication QR-code")
args = parser.parse_args()


def main(args):
    HOST = socket.gethostname()
    PORT = 40001
    hostname = socket.gethostname()
    username = args.username

    import qrcode
    try:
        pwd.getpwnam(username)
    except KeyError:
        raise UserNotFound(username)
    qr = qrcode.QRCode()
    data = f"{username};{hostname}".format()
    print(data)
    qr.add_data(data)
    qr.print_tty()

    print(f"Scan this QR-code to begin negotiations for {username} authorization")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('', PORT))
        sock.listen()
        conn, addr = sock.accept()
        with conn:
            print("Connected by", addr)
            server_key = pyDHE.new(14)
            client_pubkey = int.from_bytes(conn.recv(2048),sys.byteorder,signed=False)
            shared_key = server_key.update(client_pubkey)
            server_pubkey = server_key.getPublicKey()
            conn.sendall(server_pubkey.to_bytes(ceil(server_pubkey.bit_length()/8),sys.byteorder,signed=False))
            print(shared_key)


if __name__ == "__main__":
    main(args)

