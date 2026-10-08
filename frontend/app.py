import base64
import html
import os
from datetime import date

import requests
import streamlit as st

from dotenv import load_dotenv


# =====================================================
# Configuration
# =====================================================

load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000",
).rstrip("/")


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


LOGO_PATH = os.path.join(
    PROJECT_ROOT,
    "assets",
    "logo.svg",
)


# =====================================================
# Streamlit configuration
# =====================================================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================
# Custom CSS
# =====================================================

st.markdown(
    """
    <style>

    .hero {
        padding: 1.5rem;
        border-radius: 18px;
        background:
            linear-gradient(
                135deg,
                #111827,
                #1f2937
            );
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        margin: 0;
        font-size: 2.5rem;
    }

    .hero p {
        margin-top: 0.5rem;
        color: #d1d5db;
        font-size: 1.05rem;
    }

    .preview {
        background: #111827;
        color: #f9fafb;
        border: 1px solid #374151;
        border-radius: 14px;
        padding: 1.25rem;
        max-height: 650px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-family: Georgia, serif;
        line-height: 1.7;
    }

    .notice {
        padding: 1rem;
        border-left: 4px solid #6b7280;
        background: #f3f4f6;
        border-radius: 8px;
        margin-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# Session state
# =====================================================

if "content" not in st.session_state:
    st.session_state.content = ""

if "generated" not in st.session_state:
    st.session_state.generated = False

if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False


# =====================================================
# Helper functions
# =====================================================

def call_backend(
    endpoint: str,
    payload: dict,
    timeout: int = 120,
):
    """
    Send a POST request to FastAPI.
    """

    return requests.post(
        f"{BACKEND_URL}{endpoint}",
        json=payload,
        timeout=timeout,
    )


def get_error_message(
    response: requests.Response,
) -> str:
    """
    Extract a useful error message from FastAPI.
    """

    try:
        data = response.json()

        return str(
            data.get(
                "detail",
                response.text,
            )
        )

    except Exception:
        return response.text


def create_export_payload(
    document_type: str,
    parties: str,
    terms: str,
    effective_date: date,
    jurisdiction: str,
    purpose: str,
    branding_name: str,
    branding_font: str,
    additional_instructions: str,
    logo_base64: str,
) -> dict:
    """
    Build payload for export endpoints.
    """

    return {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "effective_date": (
            effective_date.isoformat()
        ),
        "jurisdiction": jurisdiction,
        "purpose": purpose,
        "branding_name": branding_name,
        "branding_font": branding_font,
        "logo_base64": logo_base64,
        "additional_instructions": (
            additional_instructions
        ),
        "content": st.session_state.content,
    }


# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    # Skip missing or empty logo files. Streamlit/Pillow cannot decode an
    # empty SVG and may report it as FileNotFoundError for an empty path.
    if os.path.isfile(LOGO_PATH) and os.path.getsize(LOGO_PATH) > 0:
        st.image(
            LOGO_PATH,
            width=90,
        )

    st.markdown(
        "## LegalEase"
    )

    st.caption(
        "AI-assisted legal document drafting"
    )

    st.divider()

    st.markdown(
        "**Backend URL**"
    )

    st.code(
        BACKEND_URL,
        language="text",
    )

    st.divider()

    st.info(
        "LegalEase creates AI-assisted drafts. "
        "Generated documents should be reviewed "
        "by a qualified legal professional before "
        "being used for an actual legal matter."
    )


# =====================================================
# Hero section
# =====================================================

st.markdown(
    """
    <div class="hero">

        <h1>⚖️ LegalEase</h1>

        <p>
            Create, review, edit and export
            AI-assisted legal document drafts.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# Main columns
# =====================================================

left_column, right_column = st.columns(
    [0.9, 1.1],
    gap="large",
)


# =====================================================
# LEFT SIDE - INPUT FORM
# =====================================================

with left_column:

    st.subheader(
        "Document Details"
    )

    # Document type
    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement (NDA)",
            "Lease Agreement",
            "Freelance Work Contract",
            "Service Agreement",
            "General Agreement",
            "Custom",
        ],
    )

    if document_type == "Custom":

        document_type = st.text_input(
            "Custom Document Type",
            placeholder=(
                "Example: Partnership Agreement"
            ),
        )

    # Parties
    parties = st.text_area(
        "Parties Involved",
        placeholder=(
            "Jane Doe (Service Provider); "
            "TechNova Inc. (Client)"
        ),
        height=110,
    )

    # Terms
    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Payment within 30 days of invoice; "
            "Confidentiality; "
            "Either party may terminate with "
            "15 days notice"
        ),
        help=(
            "Separate individual terms using "
            "semicolons."
        ),
        height=150,
    )

    # Effective date
    effective_date = st.date_input(
        "Effective Date",
        value=date.today(),
    )

    # Jurisdiction
    jurisdiction = st.text_input(
        "Jurisdiction",
        value="Not specified",
        placeholder=(
            "Example: Tamil Nadu, India"
        ),
    )

    # Purpose
    purpose = st.text_area(
        "Purpose / Background",
        placeholder=(
            "Briefly explain why this document "
            "is being created."
        ),
        height=90,
    )

    # Branding
    branding_name = st.text_input(
        "Branding Name",
        value="LegalEase",
    )

    branding_font = st.selectbox(
        "Document Font",
        ["Times New Roman", "Arial", "Courier New"],
    )

    logo_upload = st.file_uploader(
        "Company Logo (optional)",
        type=["png", "jpg", "jpeg"],
        max_upload_size=5,
        help="PNG or JPEG, up to 5 MB. Added to DOCX and PDF exports.",
    )

    logo_base64 = (
        base64.b64encode(logo_upload.getvalue()).decode("ascii")
        if logo_upload is not None
        else ""
    )

    # Additional instructions
    additional_instructions = st.text_area(
        "Additional Instructions",
        placeholder=(
            "Optional drafting instructions, "
            "clauses, formatting preferences, etc."
        ),
        height=110,
    )

    # Generate button
    generate_button = st.button(
        "✨ Generate Document",
        type="primary",
        use_container_width=True,
    )


    # =================================================
    # Generation
    # =================================================

    if generate_button:

        if not document_type.strip():

            st.error(
                "Please enter a document type."
            )

        elif not parties.strip():

            st.error(
                "Please enter the parties involved."
            )

        elif not terms.strip():

            st.error(
                "Please enter the terms and conditions."
            )

        else:

            request_payload = {
                "document_type": document_type,
                "parties": parties,
                "terms": terms,
                "effective_date": (
                    effective_date.isoformat()
                ),
                "jurisdiction": jurisdiction,
                "purpose": purpose,
                "branding_name": branding_name,
                "branding_font": branding_font,
                "additional_instructions": (
                    additional_instructions
                ),
            }

            with st.spinner(
                "Generating your document..."
            ):

                try:

                    response = call_backend(
                        "/generate",
                        request_payload,
                        timeout=180,
                    )

                    if response.ok:

                        data = response.json()

                        st.session_state.content = (
                            data["content"]
                        )

                        st.session_state.generated = (
                            True
                        )

                        st.session_state.demo_mode = (
                            data.get(
                                "demo_mode",
                                False,
                            )
                        )

                        st.success(
                            "Document generated successfully!"
                        )

                    else:

                        error = (
                            get_error_message(
                                response
                            )
                        )

                        st.error(
                            f"Generation failed: {error}"
                        )

                except requests.RequestException as exc:

                    st.error(
                        "Could not connect to the "
                        f"FastAPI backend at "
                        f"{BACKEND_URL}.\n\n"
                        "Make sure the backend is running.\n\n"
                        f"Technical details: {exc}"
                    )


# =====================================================
# RIGHT SIDE - DOCUMENT PREVIEW
# =====================================================

with right_column:

    st.subheader(
        "Document Preview"
    )

    if st.session_state.generated:

        if st.session_state.demo_mode:

            st.warning(
                "DEMO MODE is active. "
                "This is sample output and was "
                "not generated by Gemini."
            )

        # Editable document
        edited_content = st.text_area(
            "Editable Document",
            value=st.session_state.content,
            height=520,
            label_visibility="collapsed",
        )

        st.session_state.content = (
            edited_content
        )

        # Preview
        st.markdown(
            "**Formatted Preview**"
        )

        safe_preview = html.escape(
            st.session_state.content
        )

        st.markdown(
            f"""
            <div class="preview">
                {safe_preview}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Export data
        export_payload = (
            create_export_payload(
                document_type=document_type,
                parties=parties or "Not provided",
                terms=terms or "Not provided",
                effective_date=effective_date,
                jurisdiction=(
                    jurisdiction
                    or "Not specified"
                ),
                purpose=purpose,
                branding_name=(
                    branding_name
                    or "LegalEase"
                ),
                branding_font=branding_font,
                additional_instructions=(
                    additional_instructions
                ),
                logo_base64=logo_base64,
            )
        )

        # Download section
        st.markdown(
            "### Download"
        )

        txt_col, docx_col, pdf_col = (
            st.columns(3)
        )

        # TXT
        with txt_col:

            try:

                response = call_backend(
                    "/export/txt",
                    export_payload,
                    timeout=60,
                )

                if response.ok:

                    st.download_button(
                        "⬇️ TXT",
                        data=response.content,
                        file_name=(
                            "legal-document.txt"
                        ),
                        mime="text/plain",
                        use_container_width=True,
                    )

                else:

                    st.error(
                        "TXT export failed."
                    )

            except requests.RequestException:

                st.error(
                    "Backend unavailable."
                )

        # DOCX
        with docx_col:

            try:

                response = call_backend(
                    "/export/docx",
                    export_payload,
                    timeout=60,
                )

                if response.ok:

                    st.download_button(
                        "⬇️ DOCX",
                        data=response.content,
                        file_name=(
                            "legal-document.docx"
                        ),
                        mime=(
                            "application/"
                            "vnd.openxmlformats-officedocument."
                            "wordprocessingml.document"
                        ),
                        use_container_width=True,
                    )

                else:

                    st.error(
                        "DOCX export failed."
                    )

            except requests.RequestException:

                st.error(
                    "Backend unavailable."
                )

        # PDF
        with pdf_col:

            try:

                response = call_backend(
                    "/export/pdf",
                    export_payload,
                    timeout=60,
                )

                if response.ok:

                    st.download_button(
                        "⬇️ PDF",
                        data=response.content,
                        file_name=(
                            "legal-document.pdf"
                        ),
                        mime="application/pdf",
                        use_container_width=True,
                    )

                else:

                    st.error(
                        "PDF export failed."
                    )

            except requests.RequestException:

                st.error(
                    "Backend unavailable."
                )

    else:

        st.info(
            "Your generated document will appear "
            "here.\n\n"
            "Fill in the document information on "
            "the left and click "
            "**Generate Document**."
        )


# =====================================================
# Footer
# =====================================================

st.divider()

st.markdown(
    """
    <div class="notice">

        <strong>Review Notice</strong>

        <br><br>

        AI-generated legal documents can contain
        omissions, inaccurate assumptions, or
        jurisdiction-specific issues.

        <br><br>

        Review the completed document with a
        qualified legal professional before using
        it for a real transaction or legal matter.

    </div>
    """,
    unsafe_allow_html=True,
)
