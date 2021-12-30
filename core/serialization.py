from typing import Callable, Any, Union

from bs4 import BeautifulSoup
from bs4.element import Tag
from .models import Model


class Deserializer:
    def __init__(self, model: Callable):
        self.model_cls = model


    def __call__(self, text, model=None) -> Any:
        if model:
            self.model_cls = model
        return self.deserialize(text)


    def deserialize(self, text: str, **kwargs) -> Model:
        """
        Deserialize the response text into a model object.
        """
        soup = BeautifulSoup(markup=text, features='lxml', **kwargs)
        return self._deserialize(soup)

    def _deserialize(self, soup: Union[BeautifulSoup, Tag]) -> Model:
        """
        Deserialize a BeautifulSoup object into a model object.

        :param soup: BeautifulSoup object
        :return: Model object
        """ 

        model = self.model_cls()

        if not hasattr(model, '_html_map'):
            raise AttributeError('Model must have an _html_map attribute')

        html_map = model._html_map

        for attr_name, mapconfig in html_map.items():
            html_attr = mapconfig.get('attr')

            if 'container' in mapconfig:
                container = self.find_tags('container', soup, mapconfig['container'], _all=False)
            else:
                container = soup

            inner_model = mapconfig.get('type')

            if 'elements' in mapconfig:
                elements = self.find_tags('elements', container, mapconfig['elements'])
                identifiers = mapconfig.get('identifiers')

                if identifiers:
                    if isinstance(identifiers, list):
                        identifiers = dict.fromkeys(identifiers, inner_model)
                    for name, _type, tag in zip(identifiers.keys(), identifiers.values(), elements):
                        value = self.get_content(_type, tag, html_attr)
                        setattr(model, name, value)
                else:
                    attrs = [self.get_content(inner_model, tag, html_attr) for tag in elements]
                    setattr(model, attr_name, attrs)
            else:
                attr_value = self.get_content(inner_model, container, html_attr)
                setattr(model, attr_name, attr_value)

        return model

    
    def get_content(self, model: Union[Model, str], tag: Tag, html_attr: str = None):
        """
        Helper function to get the content of a tag, and if it's a model, deserialize it.

        If the tag's content is not a model, check if said tag has the mapped html attribute, and return that instead. Otherwise, return None.
        """

        try:
            attr = tag.attrs.get(html_attr, getattr(tag, html_attr)).strip()
        except:
            attr = None

        if tag:
            if model:
                if isinstance(model, type) and issubclass(model, Model):
                    # If the tag's content is a model, deserialize it
                    return Deserializer(model)._deserialize(tag)
                else:
                    attr = attr or tag.text
                    if callable(model):
                        # model is a custom callable (be it a function or a class), so call it
                        return model(attr)
                    elif isinstance(model, str):
                        # model is a base type string
                        return self._deserialize_base(model, attr)   
        return attr


    def _deserialize_base(self, type_string, html_attr):
        """
        Deserialize the tag's content into the given base type.
        """
        _type = __builtins__.get(type_string)
        return _type(html_attr) if _type else html_attr


    def find_tags(self, key, soup, find_kwds, _all=True):
        if soup:
            return soup.find_all(**find_kwds) if _all else soup.find(**find_kwds)
        return []

        # if not tags:
        #     print('Found', soup.text)
        #     raise ValueError(f'Could not find {key} {find_kwds} for model {self.model_cls.__name__}')
