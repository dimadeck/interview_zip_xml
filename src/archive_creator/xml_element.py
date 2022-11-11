from typing import Optional


class XMLElement:
    """
    Generating element like:
        <element_name />
    or
        <element_name param='value'>...</element_name>
    """
    def __init__(self, element_name: str, params: Optional[dict] = None):
        self._element_name = element_name
        self._params = params
        self._child = []

    @property
    def document(self) -> str:
        params = self._prepare_params(self._params)
        tag = ' '.join([self._element_name, params]).strip()
        if self._child:
            content = self._prepare_content()
            return f'<{tag}>{content}</{self._element_name}>'
        return f'<{tag}/>'

    @staticmethod
    def _prepare_params(params: Optional[dict] = None) -> str:
        if params:
            return ' '.join([f"{name}='{value}'" for name, value in params.items()])
        return ''

    def _prepare_content(self):
        return " ".join([element.document for element in self._child])

    def add_child(self, content: 'XMLElement') -> 'XMLElement':
        self._child.append(content)
        return self
