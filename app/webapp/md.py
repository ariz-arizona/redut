from markdownfield.validators import MARKDOWN_ATTRS, MARKDOWN_TAGS, Validator

VALIDATOR_MY = Validator(
    allowed_tags=MARKDOWN_TAGS,
    allowed_attrs={
        **MARKDOWN_ATTRS,
        'img': ['src', 'alt', 'title', 'class'],
        'a': ['href', 'alt', 'title', 'name', 'class'],
        'div': ['class'],
    },
) 