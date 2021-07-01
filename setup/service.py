import getpass
import os

path = os.getcwd()

service = f"""[Unit]
Description=Reporting for InosatIoT
StartLimitIntervalSec=500
StartLimitBurst=5

[Service]
Restart=on-failure
RestartSec=5s
Type=simple
User={getpass.getuser()}
Group={getpass.getuser()}
EnvironmentFile=/etc/environment
ExecStart={path}/venv/bin/python3 {path}/main.py

[Install]
WantedBy=multi-user.target"""

f = open("setup/inosatiot_report.service", "w")
f.write(service)
f.close()

print(f'Created service file: \n{service}')
