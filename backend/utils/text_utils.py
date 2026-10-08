import html
import re
import unicodedata


def sanitize_text(text: str) -> str:
    """
    Normalize text before exporting it.
    """

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u2026": "...",
        "\u00a0": " ",
        "\ufeff": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = unicodedata.normalize(
        "NFKC",
        text,
    )

    text = re.sub(
        r"[ \t]+\n",
        "\n",
        text,
    )

    text = re.sub(
        r"\n{4,}",
        "\n\n\n",
        text,
    )

    return text.strip()


def terms_to_list(terms: str) -> list[str]:
    """
    Convert semicolon-separated terms into a list.
    """

    return [
        item.strip()
        for item in terms.split(";")
        if item.strip()
    ]


def escape_html(text: str) -> str:
    """
    Safely escape text for HTML rendering.
    """

    return html.escape(
        text,
        quote=True,
    )


def safe_filename(document_type: str) -> str:
    """
    Convert a document type into a safe filename.
    """

    cleaned = re.sub(
        r"[^A-Za-z0-9]+",
        "-",
        document_type.strip(),
    )

    cleaned = cleaned.strip("-")

    if not cleaned:
        cleaned = "legal-document"

    return cleaned[:80].lower()