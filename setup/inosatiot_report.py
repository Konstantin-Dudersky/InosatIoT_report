import os

os.chdir('..')
path = os.getcwd()
os.chdir('setup')

service = f"""
[Unit]
Description=Reporting for InosatIoT
StartLimitIntervalSec=500
StartLimitBurst=5

[Service]
Restart=on-failure
RestartSec=5s
Type=simple
User=inosat
Group=inosat
EnvironmentFile=/etc/environment
ExecStart={path}/venv/bin/python3 {path}/main.py

[Install]
WantedBy=multi-user.target
"""

f = open("inosatiot_report.service", "w")
f.write(service)
f.close()
