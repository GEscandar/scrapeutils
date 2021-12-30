import asyncio
from ..core.scrapers import BaseScraper
from .models import XenForoForumReferenceList, XenForoThreadList, XenForoSearchResultList



class XenForoScraper(BaseScraper):
    def __init__(self, base_url, creds=None) -> None:
        super().__init__(base_url, creds)
        

    def login(self, auth, redirect):
        """
        Login endpoint for scraping user data.
        """
        # return self.conn.post(f'/login/login/', data={
        #     'login': auth[0],
        #     'password': auth[1],
        #     'redirect': redirect,
        # })
        pass


    async def list_threads_from_page(self, forum_name: str, page = 1) -> XenForoThreadList:
        return await self.scrape_url(XenForoThreadList, f'forums/{forum_name}', params={'page': page})


    async def list_pages(self, forum_name, start_page, end_page):
        tasks = [asyncio.create_task(self.list_threads_from_page(forum_name, page)) for page in range(start_page, end_page)]
        return await asyncio.gather(*tasks)


    async def list_forums(self) -> XenForoForumReferenceList:
        return await self.scrape_url(XenForoForumReferenceList)


    async def search(self, query=None, order=None, title_only=None, users=None,
     container_only=None, min_words=None
     ) -> XenForoSearchResultList:
        params = {}
        params['q'] = query or '*'
        params['o'] = order or 'date'

        if min_words:
            params['c[word_count][lower]'] = min_words
        if users:
            params['c[users]'] = users
        if title_only:
            params['c[title_only]'] = '1'
        if container_only:
            params['c[container_only]'] = '1'


        return await self.scrape_url(XenForoSearchResultList, 'search/1', params=params)
