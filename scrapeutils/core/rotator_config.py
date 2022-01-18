from enum import Enum
from .models import FreeProxyList, UserAgentList


class ProxyRotatorConfiguration(Enum):
    """
    Configuration for the proxy rotator.
    """
    RESOURCE_URL = 'https://free-proxy-list.net/'
    RESOURCE_MODEL = FreeProxyList
    RESOURCE_ATTRIBUTE_NAME = 'proxies'


class UserAgentRotatorConfiguration(Enum):
    """
    Configuration for the user agent rotator.
    """
    RESOURCE_URL = 'https://user-agents.net/random'
    RESOURCE_MODEL = UserAgentList
    RESOURCE_ATTRIBUTE_NAME = 'user_agents'