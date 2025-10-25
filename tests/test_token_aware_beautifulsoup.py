from src.bs4_token_ext.main import TokenAwareBeautifulSoup, TokenCountTag
import pytest


def test_token_count():
    """Test basic token counting"""
    html = "<div>Hello world</div>"
    soup = TokenAwareBeautifulSoup(html, 'html.parser')
    div = soup.find('div')
    
    assert div is not None
    assert div.token_count > 0
    assert isinstance(div.token_count, int)


def test_token_count_with_html():
    """Test token counting with HTML tags"""
    html = "<div>Hello world</div>"
    soup = TokenAwareBeautifulSoup(html, 'html.parser')
    div = soup.find('div')
    
    assert div is not None
    assert div.token_count_with_html > div.token_count


def test_custom_encoding():
    """Test custom encoding"""
    html = "<div>Test</div>"
    soup = TokenAwareBeautifulSoup(html, 'html.parser', encoding='o200k_base')
    div = soup.find('div')
    
    assert div is not None
    assert div._encoding_name == "o200k_base"
    assert div.token_count > 0


def test_nested_tags_text_only():
    """Test token counting for nested tags (text only)"""
    html = "<div><p>Hello</p><span>World</span></div>"
    soup = TokenAwareBeautifulSoup(html, 'html.parser')
    
    div = soup.find('div')
    p = soup.find('p')
    span = soup.find('span')
    
    assert div is not None
    assert p is not None
    assert span is not None
    
    # Parent should count all nested text
    assert "HelloWorld" in div.get_text()
    assert div.token_count > 0
    
    # Child elements should count their own text
    assert p.token_count > 0
    assert span.token_count > 0


def test_nested_tags_with_html():
    """Test token counting for nested tags (with HTML)"""
    html = "<div><p>Hello</p><span>World</span></div>"
    soup = TokenAwareBeautifulSoup(html, 'html.parser')
    
    div = soup.find('div')
    p = soup.find('p')
    
    assert div is not None
    assert p is not None
    
    # Parent HTML should include nested tags
    assert "<p>" in str(div)
    assert div.token_count_with_html > div.token_count
    
    # Child HTML should only include its own tags
    assert "<p>Hello</p>" == str(p)
    assert p.token_count_with_html > p.token_count