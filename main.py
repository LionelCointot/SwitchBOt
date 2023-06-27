#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 13:23:07 2022

@author: Travail
"""
import uuid
from SwitchbotClient.SwitchBotClient import SwitchBotClient
from Devices import Meter, HubMini
import sys
import os
from SwitchBotEnums import DeviceType
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


if __name__ == "__main__":

    token = "<Token>"  # copy and paste from the SwitchBot app V6.14 or later
    # secret key&<
    secret = "<secret>"  # copy and paste from the SwitchBot app V6.14 or later
    
    # To get the token and secret, please refer to https://github.com/OpenWonderLabs/SwitchBotAPI#getting-started

    switchbot_client = SwitchBotClient(token=token, secret=secret, nonce=str(uuid.uuid4()))
    devices = switchbot_client.devices()
    for device in devices:

        if device.DEVICE_TYPE == DeviceType.METER:
            meter : Meter = device
            meter.update()
            print(
                f"{meter.device_info.name} : {meter.temperature_info.temperature}{meter.temperature_info.UNIT} avec {meter.temperature_info.humidity}% d'humidité"
            )
            
        if isinstance(device, HubMini):
            print(device.device_info.name)