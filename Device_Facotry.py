from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional
from Devices.Meter import Device, Meter


class DeviceFactory(object):
    def Create(type) -> Device:
        match type:
            case "Meter":
                return Meter()
