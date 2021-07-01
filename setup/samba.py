import json
import os

share_name = '[inosatiot-report]'

with open(os.getenv('inosatiot_cfg')) as f:
    cfg = json.loads(f.read())

# read file
with open('/etc/samba/smb.conf', 'r') as reader:
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
    with open('/etc/samba/smb.conf', 'w') as reader:
        for line in lines:
            reader.write(line)

# append new configuration
config = f"""{share_name}
    comment = Report folder for InosatIoT
    path = {cfg['report']['output_path']}
    read only = no
    browsable = yes
#{share_name}"""

with open('/etc/samba/smb.conf', 'a') as reader:
    reader.write(config)
