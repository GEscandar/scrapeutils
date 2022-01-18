import asyncio
import random

from .connection import Connection
from .serialization import Deserializer
from .rotator_config import ProxyRotatorConfiguration, UserAgentRotatorConfiguration
from typing import Coroutine, List



class ResourceRotator:
    """
    Get a random resource from a list of valid resources
    """

    def __init__(self, config, resources = None) -> None:
        self.resources = resources
        if not self.resources:
            # This will only run once, so do it synchronously
            scraper = BaseScraper(config.RESOURCE_URL)
            response = scraper.run_sync(scraper.scrape_url(config.RESOURCE_MODEL))
            self.resources = getattr(response, config.RESOURCE_ATTRIBUTE_NAME)


    def get_random(self):
        randindex = random.randint(0, len(self.resources) - 1)
        return self.resources[randindex]



class BaseScraper:
    """
    Async web scraper base class.
    """
    def __init__(self, base_url, creds=None) -> None:
        self.conn = Connection(base_url, creds)
        self.loop = asyncio.get_event_loop()
        

    def login(self, auth, redirect):
        """
        Login endpoint for scraping user data.
        """
        pass
        

    def run_sync(self, coro: Coroutine):
        """
        Run Coroutine synchronously.
        """
        return self.loop.run_until_complete(coro)


    async def scrape_url(self, model, path='', **kwargs):
        html_resp = await self.conn.get(path, **kwargs)
        return Deserializer(model).deserialize(html_resp)



class RotatingScraper(BaseScraper):
    """
    Async web scraper with a rotating configuration for each request.
    """
    def __init__(self, base_url, creds=None) -> None:
        super().__init__(base_url, creds)
        self.proxy_rotator = ResourceRotator(ProxyRotatorConfiguration)
        self.user_agent_rotator = ResourceRotator(UserAgentRotatorConfiguration)


    async def scrape_url(self, model, path='', **kwargs):
        proxy = self.proxy_rotator.get_random()
        user_agent = self.user_agent_rotator.get_random()

        proxies = {
            'https' if proxy.https else 'http': f'{proxy.ip}:{proxy.port}'
        }

        headers = kwargs.get('headers', {})
        headers['User-Agent'] = user_agent

        return await super().scrape_url(model, path, proxies=proxies, headers=headers, **kwargs)
    


