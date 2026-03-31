"""
guardrails/validators.py
Reusable validation helpers used by input and output guardrails.
"""

from app.guardrails.policy import VALID_MODES, MAX_MESSAGE_LENGTH, BLOCKED_CONTENT_PATTERNS

# Image file signatures (magic bytes) for common math-incompatible formats
# We allow: JPEG, PNG, WebP, HEIC (photos of math work)
# We check: if an image was sent, it should be a photo format, not a meme/gif/video


def is_within_length(message: str, max_length: int = MAX_MESSAGE_LENGTH) -> bool:
    """Check if a message is within the allowed length."""
    return len(message) <= max_length


def contains_blocked_content(message: str) -> bool:
    """Check if a message contains any blocked content patterns."""
    lower = message.lower()
    return any(pattern in lower for pattern in BLOCKED_CONTENT_PATTERNS)


def is_valid_mode(mode: str) -> bool:
    """Check if a mode string is one of the allowed modes."""
    return mode in VALID_MODES


def is_valid_image(image_base64: str | None) -> dict:
    """
    Check if an uploaded image is likely math-related (a photo, not a meme/GIF).

    We can't know for sure without vision analysis, but we can check:
      - Is it a valid image format (JPEG/PNG based on base64 header)?
      - Is it suspiciously small (likely an icon/emoji, not a photo)?

    Returns:
        {"valid": bool, "reason": str}
    """
    if not image_base64:
        return {"valid": True, "reason": "no_image"}

    # Check minimum size — a real photo of math work is at least a few KB
    # Base64 is ~33% larger than binary, so 1KB binary ≈ 1400 base64 chars
    if len(image_base64) < 1000:
        return {
            "valid": False,
            "reason": "image_too_small",
        }

    # Check for common image format headers in base64
    valid_headers = [
        "/9j/",     # JPEG
        "iVBOR",    # PNG
        "UklGR",    # WebP
        "AAAA",     # HEIC (partial)
    ]

    has_valid_header = any(image_base64.startswith(h) for h in valid_headers)
    if not has_valid_header:
        # Could be a data URL prefix — check after stripping it
        if "base64," in image_base64:
            data_part = image_base64.split("base64,", 1)[1]
            has_valid_header = any(data_part.startswith(h) for h in valid_headers)

    if not has_valid_header:
        return {
            "valid": False,
            "reason": "unrecognized_format",
        }

    return {"valid": True, "reason": "valid_image"}


# Pre-built rejection messages (no LLM call needed — saves tokens)
REJECTION_MESSAGES = {
    "off_topic": (
        "I'm your math tutor — I'm best at helping with math problems, "
        "equations, and concepts! What math topic are you working on?"
    ),
    "empty_message": (
        "It looks like you sent an empty message. "
        "What math problem can I help you with?"
    ),
    "invalid_image": (
        "I can help best with photos of math work — handwritten problems, "
        "textbook pages, or equations. Could you send a photo of what "
        "you're working on?"
    ),
    "image_too_small": (
        "That image seems too small to read. Could you send a clearer "
        "photo of your math work?"
    ),
    "too_long": (
        "That's a lot of text! Could you break your question into a "
        "smaller piece? What's the first part you need help with?"
    ),
}
