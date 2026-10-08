"""Request and response models for LegalEase API routes."""

import base64
import binascii
from io import BytesIO
from typing import Literal

from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel, ConfigDict, Field, field_validator


class DocumentRequest(BaseModel):
    """
    Input required to generate a legal document.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True
    )

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=120,
    )

    parties: str = Field(
        ...,
        min_length=3,
        max_length=4000,
    )

    terms: str = Field(
        ...,
        min_length=3,
        max_length=10000,
    )

    effective_date: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    jurisdiction: str = Field(
        default="Not specified",
        max_length=200,
    )

    purpose: str = Field(
        default="",
        max_length=2000,
    )

    branding_name: str = Field(
        default="LegalEase",
        max_length=120,
    )

    branding_font: Literal[
        "Times New Roman",
        "Arial",
        "Courier New",
    ] = "Times New Roman"

    additional_instructions: str = Field(
        default="",
        max_length=5000,
    )

    @field_validator(
        "document_type",
        "parties",
        "terms",
        "effective_date",
    )
    @classmethod
    def reject_blank_values(cls, value: str) -> str:
        """Reject required strings that contain only whitespace."""
        if not value.strip():
            raise ValueError(
                "This field cannot be blank."
            )

        return value.strip()


class GenerateResponse(BaseModel):
    """
    Response returned after AI generation.
    """

    document_type: str
    content: str
    demo_mode: bool = False


class ExportRequest(DocumentRequest):
    """
    Input used by all document export endpoints.
    """

    content: str = Field(
        ...,
        min_length=20,
        max_length=100000,
    )

    logo_base64: str = Field(
        default="",
        max_length=7_000_000,
    )

    @field_validator("content")
    @classmethod
    def content_not_blank(cls, value: str) -> str:
        """Reject document content that contains only whitespace."""
        if not value.strip():
            raise ValueError(
                "Document content cannot be blank."
            )

        return value.strip()

    @field_validator("logo_base64")
    @classmethod
    def validate_logo(cls, value: str) -> str:
        """Validate the encoded logo's size, format, and dimensions."""
        if not value:
            return value

        try:
            image_bytes = base64.b64decode(
                value,
                validate=True,
            )
        except (binascii.Error, ValueError) as exc:
            raise ValueError("Logo must be a valid PNG or JPEG image.") from exc

        if len(image_bytes) > 5 * 1024 * 1024:
            raise ValueError("Logo image must be 5 MB or smaller.")

        try:
            with Image.open(BytesIO(image_bytes)) as image:
                if image.format not in {"PNG", "JPEG"}:
                    raise ValueError("Logo must be a PNG or JPEG image.")
                if image.width * image.height > 16_000_000:
                    raise ValueError("Logo image dimensions are too large.")
                image.verify()
        except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
            raise ValueError("Logo must be a valid PNG or JPEG image.") from exc

        return value
