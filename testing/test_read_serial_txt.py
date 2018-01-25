with open('test_serial.txt', 'r') as serial_file:
    serial = serial_file.read().rstrip()

print(serial)
