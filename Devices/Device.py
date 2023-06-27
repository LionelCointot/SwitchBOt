

from pydantic import Field, BaseModel
from dataclasses import dataclass
from typing import ClassVar, Optional, Dict, Any
from SwitchbotClient.RESTClient import RESTClient
from typing import Any, ClassVar, Dict, List, Optional, TYPE_CHECKING

MAP={}


class DeviceInfo(BaseModel):

    id: str = Field(alias="deviceId")
    name: str = Field(alias="deviceName")
    type: str = Field(alias="deviceType")
    cloud_enabled: Optional[bool] = Field(alias="enableCloudService")
    hub_id: str = Field(alias="hubDeviceId")

@dataclass
class Device:

    DEVICE_TYPE: ClassVar[Optional[str]] = None

    client : RESTClient 
    device_info : DeviceInfo 
    
    def __init_subclass__(cls):
        if cls.DEVICE_TYPE is not None:
            MAP[cls.DEVICE_TYPE] = cls

    def status(self) -> Dict[str, Any]:
        
        response = self.client.get(f"devices/{self.device_info.id}/status")
        return response

    def from_json(JsonString :  str):
        pass

    def __repr__(self):
        name = "Device" if self.type is None else self.type
        name = name.replace(" ", "")
        return f"{name}(id={self.id})"
