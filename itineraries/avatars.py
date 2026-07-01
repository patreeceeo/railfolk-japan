from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen


DICEBEAR_AVATAR_URL = "https://api.dicebear.com/10.x/lorelei/svg"
AVATAR_FETCH_TIMEOUT_SECONDS = 2
SUCCESS_CACHE_CONTROL = "public, max-age=31536000, immutable"
FALLBACK_CACHE_CONTROL = "public, max-age=300"
SVG_CONTENT_TYPE = "image/svg+xml"

DEFAULT_AVATAR_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96">
<rect width="96" height="96" fill="#f2f2f2"/>
<circle cx="48" cy="36" r="18" fill="#9a9a9a"/>
<path d="M18 86c4-20 16-30 30-30s26 10 30 30" fill="#9a9a9a"/>
</svg>
"""


class AvatarFetchError(Exception):
    pass


def fetch_avatar_svg(avatar_key):
    url = f"{DICEBEAR_AVATAR_URL}?{urlencode({'seed': avatar_key})}"

    try:
        with urlopen(url, timeout=AVATAR_FETCH_TIMEOUT_SECONDS) as response:
            status = getattr(response, "status", 200)
            content_type = response.headers.get("Content-Type", "")

            if status != 200:
                raise AvatarFetchError(f"avatar provider returned HTTP {status}")
            if not content_type.startswith(SVG_CONTENT_TYPE):
                raise AvatarFetchError("avatar provider returned non-SVG content")

            return response.read()
    except (OSError, URLError) as exc:
        raise AvatarFetchError("avatar provider request failed") from exc
