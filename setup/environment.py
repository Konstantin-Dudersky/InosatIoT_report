import os
import sys

config = '/etc/environment'
var_name = 'inosatiot_cfg'

path = os.getcwd().split('/')[:-1]
path.append('inosatiot_cfg.json')
path = '/'.join(path)

# check file exist
if not os.path.isfile(path):
    print("-----> ERROR: file inosatiot_cfg.json not exist")
    sys.exit(1)

# read file
with open(config, 'r') as reader:
    lines = reader.readlines()

# maybe variable exist - find line
for i in range(len(lines)):
    if lines[i].find(var_name) >= 0:
        del lines[i]
        with open(config, 'w') as reader:
            for line in lines:
                reader.write(line)
        break

# append new configuration
add = f'{var_name}="{path}"'

with open(config, 'a') as reader:
    reader.write(add)

print(f"Environment variable {var_name} set to {path}")
sys.exit(0)