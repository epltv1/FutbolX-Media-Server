from urllib.parse import urlparse


ALLOWED_ORIGINS = {
    "https://futbol-x.xyz",
    "https://www.futbol-x.xyz",
    "https://futbol-x.top",
    "https://www.futbol-x.top",
}


def is_allowed_origin(origin: str | None, referer: str | None):
    # Check Origin
    if origin:
        if origin.rstrip("/") in ALLOWED_ORIGINS:
            return True

    # Check Referer
    if referer:
        try:
            parsed = urlparse(referer)
            base = f"{parsed.scheme}://{parsed.netloc}"

            if base.rstrip("/") in ALLOWED_ORIGINS:
                return True

        except Exception:
            pass

    return False
