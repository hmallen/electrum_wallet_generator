import os


def cleanup():
    os.chdir('wallet/')
    wallet_files = os.listdir()

    for file in wallet_files:
        if file != 'addr.png' and file != 'qr.png' and file != 'seed.png':
            os.remove(file)


if __name__ == '__main__':
    cleanup()
