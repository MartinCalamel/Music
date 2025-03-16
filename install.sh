#!/bin/bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirement.txt
mv Code/install_need/startup.service ~/.config/systemd/user/startup.service
systemctl --user enable startup.service
systemctl --user start startup.service
