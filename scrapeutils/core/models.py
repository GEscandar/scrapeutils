
class Model:
    _html_map = {}
    

    def __repr__(self) -> str:
        return str(self.__dict__)


class ReferenceLink(Model):
    _html_map = {
        'text': {
            'container': {'name': 'a'},
            'attr': 'text'
        },
        'url': {
            'container': {'name': 'a'},
            'attr': 'href'
        },
    }


class UserAgentList(Model):
    _html_map = {
        'user_agents': {
            'container': {'name': 'ol'},
            'elements': {'name': 'li'},
            'attr': 'text'
        }
    }


class FreeProxy(Model):
    _html_map = {
        'data': {
            'elements': {'name': 'td'},
            'attr': 'text',
            'identifiers': {
                'ip': 'str',
                'port': 'int',
                'country': 'str',
                'anonimity': 'str',
                'is_google_supported': lambda x: x == 'yes',
                'https': lambda x: x == 'yes',
                'last_checked': 'str'},
        }
    }


class FreeProxyList(Model):
    _html_map = {
        'proxies': {
            'container': {'name': 'tbody'},
            'elements': {'name': 'tr'},
            'type': FreeProxy,
        }
    }