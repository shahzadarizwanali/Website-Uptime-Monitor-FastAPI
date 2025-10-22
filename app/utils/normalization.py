from urllib.parse import urlparse, urlunparse


def normalize_url(url: str) -> str:
    url = url.strip()
    if "://" not in url:
        url = "https://" + url
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError("Unsupported URL scheme")
        if not parsed.netloc:
            raise ValueError("Malformed URL")

        normalized = urlunparse((parsed.scheme, parsed.netloc.lower(), "", "", "", ""))
        return normalized.rstrip("/")

    return url.rstrip("/")
