from bs4 import BeautifulSoup, Tag
import tiktoken


class TokenCountTag(Tag):
    """Custom Tag with token counting capabilities"""
    
    def __init__(self, *args, encoding="cl100k_base", **kwargs):
        super().__init__(*args, **kwargs)
        self._encoding_name = encoding
        self._encoding = None
    
    @property
    def encoding(self):
        """Lazy initialization of encoding object"""
        if self._encoding is None:
            self._encoding = tiktoken.get_encoding(self._encoding_name)
        return self._encoding
    
    @property
    def token_count(self):
        """
        Calculate token count for text content only (HTML tags excluded)
        
        Returns:
            int: Number of tokens
        """
        text = self.get_text()
        return len(self.encoding.encode(text))
    
    @property
    def token_count_with_html(self):
        """
        Calculate token count including HTML tags
        
        Returns:
            int: Number of tokens
        """
        html = str(self)
        return len(self.encoding.encode(html))


class TokenAwareBeautifulSoup(BeautifulSoup):
    """
    BeautifulSoup wrapper with token counting capabilities
    
    Examples:
        >>> soup = TokenAwareBeautifulSoup(html, 'html.parser')
        >>> div = soup.find('div')
        >>> print(div.token_count)  # Text only
        >>> print(div.token_count_with_html)  # With HTML tags
        
        >>> # Custom encoding
        >>> soup = TokenAwareBeautifulSoup(html, 'html.parser', encoding='o200k_base')
    """
    
    def __init__(self, markup="", features=None, encoding="cl100k_base", **kwargs):
        """
        Initialize TokenAwareBeautifulSoup
        
        Args:
            markup: HTML/XML markup to parse
            features: Parser specification (e.g., 'html.parser', 'lxml')
            encoding: tiktoken encoding name
                - "cl100k_base": GPT-4, GPT-3.5-turbo (default)
                - "o200k_base": GPT-4o, GPT-4o-mini
                - "p50k_base": Codex, text-davinci-002/003
            **kwargs: Additional arguments to pass to BeautifulSoup
        """
        self._encoding = encoding
        
        # Get user-specified element_classes
        user_element_classes = kwargs.get('element_classes', {})
        
        # Factory function to pass encoding to TokenCountTag
        def create_token_tag(*args, **tag_kwargs):
            return TokenCountTag(*args, encoding=self._encoding, **tag_kwargs)
        
        # Default class mapping
        default_classes = {Tag: create_token_tag}
        
        # Merge with user-specified classes (user takes priority)
        merged_classes = {**default_classes, **user_element_classes}
        
        kwargs['element_classes'] = merged_classes
        super().__init__(markup, features, **kwargs)

if __name__ == "__main__":
    # Example usage
    html = "<div><p>Hello, world!</p></div>"
    _soup = BeautifulSoup(html, 'html.parser')
    _div = _soup.find('div')
    soup = TokenAwareBeautifulSoup(html, 'html.parser',encoding='o200k_base')
    div = soup.find('div')
    p = soup.find('p')
    print("Paragraph text:",p.get_text())
    print("Paragraph token count (text only):", p.token_count)
    print("Paragraph token count (with HTML):", p.token_count_with_html)
    print("Div text:", div.get_text())
    print("Div token count (text only):", div.token_count)
    print("Div token count (with HTML):", div.token_count_with_html)