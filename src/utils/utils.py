from urllib.parse import urlparse, urlunparse

def clean_url(url):
    parsed = urlparse(url)
    clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
    return clean_url
