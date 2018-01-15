import os
import subprocess
import time

print('Hello, world!')

p = subprocess.Popen(['echo', 'hello world'], stdout=subprocess.PIPE)
com = p.communicate()

print(com)

print('Sleeping 3 seconds...')
time.sleep(3)
print('Coninuing.')

#p = subprocess.Popen(['electrum', '-D env3/bin/', 'create', '-w 4'], stdout=subprocess.PIPE)
p = subprocess.Popen(['electrum', 'create', '-w 4'], stdout=subprocess.PIPE)

com = p.communicate('\n')

print(com)
