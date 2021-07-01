import json
import os

share_name = '[inosatiot-report]'
config_file = '/etc/samba/smb.conf'

with open(os.getenv('inosatiot_cfg')) as f:
    cfg = json.loads(f.read())

# read file
with open(config_file, 'r') as reader:
    lines = reader.readlines()

# maybe config exist - find lines
begin = -1
end = -1
for i in range(len(lines)):
    if lines[i].find('#' + share_name) >= 0:
        end = i
    elif lines[i].find(share_name) >= 0:
        begin = i

# write file if config found
if begin >= 0 and end >= 0:
    del lines[begin:end + 1]
    with open(config_file, 'w') as reader:
        for line in lines:
            reader.write(line)

# append new configuration
config = f"""{share_name}
    comment = Report folder for InosatIoT
    path = {cfg['report']['output_path']}
    read only = no
    browsable = yes
#{share_name}"""

with open(config_file, 'a') as reader:
    reader.write(config)

print(f'Added configuration to file {config_file}: \n{config}')