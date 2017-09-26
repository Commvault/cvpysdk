from enum import Enum

class hypervisor_type(Enum):
		VIRTUAL_CENTER = "VMware"
		MS_VIRTUAL_SERVER = "hyper-v"
		AZURE = "Azure"
		AZURE_V2  = "Azure Resource Manager"