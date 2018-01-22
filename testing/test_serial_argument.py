import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--serial', type=str, default='', help='Serial number to print on overlays for reference.')
args = parser.parse_args()

serial_number = args.serial
print(serial_number)

if serial_number != '':
    print('Has a value.')
else:
    print('Doesn\'t have a value.')
