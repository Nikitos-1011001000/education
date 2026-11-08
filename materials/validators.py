from urllib.parse import urlparse

from django.core.exceptions import ValidationError

ALLOWED_DOMAINS = {'youtube.com', 'www.youtube.com', 'youtu.be'}


def validate_youtube_link(value):
    if not value:
        return

    parsed_url = urlparse(value)
    domain = parsed_url.netloc.lower()

    if domain not in ALLOWED_DOMAINS:
        raise ValidationError(
            'Разрешены только ссылки на YouTube.'
        )