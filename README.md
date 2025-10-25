# bs4-token-ext
Add token counting capabilities to BeautifulSoup tags for LLM applications.
---
LLM（大規模言語モデル）向けに、BeautifulSoup のタグにトークン数をカウントする機能を追加する。
## Usage
```python
from bs4_token_ext import TokenAwareBeautifulSoup

html = "<div><p>Hello, world!</p></div>"
soup = TokenAwareBeautifulSoup(html, 'html.parser')
div = soup.find('div')
p = soup.find('p')

print(p.token_count) 
print(p.token_count_with_html)  
print(div.token_count)  
print(div.token_count_with_html)  
```