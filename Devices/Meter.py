#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 13:23:07 2022

@author: Travail
"""

from __future__ import annotations
from pydantic import BaseModel, Field
from Devices.Device import Device
from typing import Optional
from dataclasses import dataclass
from SwitchBotEnums import DeviceType

class Meter(Device):
    DEVICE_TYPE : DeviceType = DeviceType.METER
    temperature_info : Optional[TemperatureInfo] = None

    def update(self):
        response = self.status()
        body = response.get("body")
        self.temperature_info = TemperatureInfo(**body)

class TemperatureInfo(BaseModel):
    #La température est toujours en °C
    UNIT: str = "°C"

    temperature : float = Field(alias="temperature")
    humidity : float = Field(alias="humidity")
