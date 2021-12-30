import re
from ..core.models import Model, ReferenceLink


class XenForoThreadReference(Model):

    _html_map = {
        'title': {
            'container': {'name': 'div', 'class': 'structItem-title'},
            'type': ReferenceLink
        },
        'parts': {
            'container': {'name': 'ul', 'class': 'structItem-parts'},
            'elements': {'name': 'li'},
            'identifiers': ['author', 'last_reply_date'],
            'type': ReferenceLink
        },
        'stats': {
            'container': {'name': 'div', 'class':'structItem-cell--meta'},
            'elements': {'name': 'dd'},
            'attr': 'text',
            'identifiers': ['replies', 'views']
        }
    }


class XenForoThreadList(Model):
    _html_map = {
        'threads': {
            'container': {'name': 'div', 'class': 'js-threadList'},
            'elements': {'name': 'div', 'class': re.compile('js-threadListItem[0-9]*')},
            'type': XenForoThreadReference,
        },
    }


class XenForoForumExtra(Model):
    _html_map = {
        'title': {
            'container': {'name': 'div', 'class': 'node-extra-row'},
            'type': ReferenceLink
        },
        'date': {
            'container': {'name': 'time', 'class': 'node-extra-date'},
            'attr': 'datetime'
        },
        'user': {
            'container': {'name': 'li', 'class': 'node-extra-user'},
            'type': ReferenceLink
        }
        
    }


class XenForoForumReference(Model):
    _html_map = {
        'title': {
            'container': {'name': 'h3', 'class': 'node-title'},
            'type': ReferenceLink
        },
        'description': {
            'container': {'name': 'div', 'class': 'node-description node-description--tooltip js-nodeDescTooltip'},
            'attr': 'text'
        },
        'stats': {
            'container': {'name': 'div', 'class': 'node-statsMeta'},
            'elements': {'name': 'dd'},
            'attr': 'text',
            'identifiers': ['threads', 'messages']
        },
        'extra': {
            'container': {'name': 'div', 'class': re.compile('^node-extra$')},
            'type': XenForoForumExtra
        }
    }


class XenForoForumReferenceList(Model):
    _html_map = {
        'forums': {
            'elements': {'name': 'div', 'class': 'node--forum'},
            'type': XenForoForumReference,
        },
    }


class XenForoForumBlock(XenForoForumReferenceList):
    _html_map = {
        'header': {
            'container': {'class': ['block-header', 'block-header--left']},
            'attr': 'text',
        }
    }

    def __init__(self) -> None:
        self._html_map.update(super()._html_map)



class XenForoSearchResult(Model):
    _html_map = {
        'title': {
            'container': {'name': 'h3', 'class': 'contentRow-title'},
            'type': ReferenceLink
        },
        # 'threadmark_label': {
        #     'container': {'name': 'div', 'class': 'threadmarkLabel'},
        #     'attr': 'text'
        # },
        'snippet': {
            'container': {'name': 'div', 'class': 'contentRow-snippet'},
            'attr': 'text'
        },
    }


class XenForoSearchResultList(Model):
    _html_map = {
        'results': {
            'elements': {'name': 'div', 'class': 'contentRow-main'},
            'type': XenForoSearchResult,
        },
    }