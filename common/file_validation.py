import magic
import os

ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/webp",
    "text/plain",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

BLOCKED_EXTENSIONS = {
    ".exe", ".sh", ".bat", ".cmd", ".msi",
    ".js", ".jar", ".php", ".py",
    ".ps1", ".vbs", ".dll", ".so",
}

MAX_FILE_SIZE_MB = 10


def validate_uploaded_file(file):
    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValueError("File size exceeds the maximum limit")

    ext = os.path.splitext(file.name)[1].lower()
    if ext in BLOCKED_EXTENSIONS:
        raise ValueError("filer extension is not allowed")

    file.seek(0)
    mime = magic.from_buffer(file.read(2048), mime=True)
    file.seek(0)

    if mime not in ALLOWED_MIME_TYPES:
        raise ValueError(f"MIME type not allowed: {mime}")

    return mime

