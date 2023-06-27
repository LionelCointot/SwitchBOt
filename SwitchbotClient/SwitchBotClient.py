import base64
import hashlib
import hmac
import time
from typing import List

from Devices import DeviceInfo, Device, MAP

__version__ = "2.2.3"
from SwitchbotClient.RESTClient import RESTClient
HOST = "https://api.switch-bot.com/v1.1"


class SwitchBotClient:
    def __init__(self, token: str, secret: str, nonce: str = ""):
        self.client = RESTClient(HOST)

        timestamp = int(round(time.time() * 1000))
        string_to_sign = f"{token}{timestamp}{nonce}"
        string_to_sign = bytes(string_to_sign, "utf-8")
        secret = bytes(secret, "utf-8")
        sign = base64.b64encode(
            hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest()
        )


        
        self.client.add_header("Authorization", token)
        self.client.add_header("t", str(timestamp))
        self.client.add_header("sign", str(sign, 'utf-8'))
        self.client.add_header("nonce",  nonce)


    def devices(self) -> List[Device]:
        response = self.client.get("devices")

        devices_info = [
            DeviceInfo(**device)
            for device in response["body"]["deviceList"]
        ]
        instances = []
        for device_info in devices_info:
            cls = MAP.get(device_info.type, Device)
            instances.append(cls(self.client, device_info))
        return instances

    def device(self, id: str) -> Device:
        # Currently, SwitchBot API does not support to retrieve device_name,
        # enable_cloud_service and hub_device_id without getting all device list
        # Therefore, for backward compatibility reason,
        # we query all devices first, then return the matching device
        for device in self.devices():
            if device.id == id:
                return device
        raise ValueError(f"Unknown device {id}")

    def remotes(self) -> List[Device]:
        response = self.client.get("devices")
        return [
            Device.create(client=self.client, id=remote["deviceId"], **remote)
            for remote in response["body"]["infraredRemoteList"]
        ]

    def remote(self, id: str) -> Device:
        for remote in self.remotes():
            if remote.id == id:
                return remote
        raise ValueError(f"Unknown remote {id}")
