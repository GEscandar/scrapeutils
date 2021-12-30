from urllib.parse import urljoin
from aiohttp import ClientSession

class Connection:

    def __init__(self, base_url, creds=None) -> None:
        self.base_url = base_url
        self.creds = creds


    async def request(self, method, path, **kwargs):
        url = urljoin(self.base_url, path)

        async with ClientSession() as session:
            async with session.request(method, url, **kwargs) as response:
                return await response.text()


    async def get(self, path, **kwargs):
        return await self.request('GET', path, **kwargs)


    async def post(self, path, **kwargs):
        return await self.request('POST', path, **kwargs)