# tuya_iot

for set_countdown.py to get executed before shutdown use the below settings

[Unit]
Description=Run my custom task at shutdown
DefaultDependencies=no
Before=shutdown.target

[Service]
Type=simple
WorkingDirectory=/home/ucp/tuya_iot/
ExecStart=/usr/bin/python set_countdown.py
TimeoutStartSec=0

[Install]
WantedBy=shutdown.target


systemctl daemon-reload
systemctl enable before-shutdown.service
systemctl start before-shutdown.service
