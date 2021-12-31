# Web Scraping utilities for Python   
This contains some simple python modules to simplify web scraping. It's purpose is to decouple IO logic (making requests for the html content) from deserialization logic 
(parsing said html into objects), so that you only have to worry about defining which tags you want to scrape, and then do that using the scraping classes.

## How to use
This uses BeautifulSoup to find tags when scraping, so the idea is to define whatever you'd need to pass to its finding methods. Whatever is in the 'container' key gets 
passed first to the `find` method, and whatever is in the 'elements' key gets passed right after to the `find_all` method.
```
from scraputils.core.models import Model

class UserAgentList(Model):
    _html_map = {
        'user_agents': {
            'container': {'name': 'ol'},
            'elements': {'name': 'li'},
            'attr': 'text'
        }
    }
```

Then, once you've defined your model, you can just get right to scraping.
```
from scraputils.core.scrapers import BaseScraper

url = 'https://user-agents.net/random'
scraper = BaseScraper(url)
resp = await scraper.scrape_url(UserAgentList, '/')
```
You can check out the other models for more detailed examples.
