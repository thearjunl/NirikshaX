# Common file signatures (Magic Bytes)
FILE_SIGNATURES = {
    "jpg": [b"\xFF\xD8\xFF"],
    "png": [b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"],
    "pdf": [b"\x25\x50\x44\x46"],
    "zip": [b"\x50\x4B\x03\x04"],
    "gif": [b"\x47\x49\x46\x38"],
    "exe": [b"\x4D\x5A"],
    "rar": [b"\x52\x61\x72\x21\x1A\x07\x00"],
    "mp3": [b"\x49\x44\x33"],
    "mp4": [b"\x00\x00\x00\x18\x66\x74\x79\x70", b"\x00\x00\x00\x20\x66\x74\x79\x70"],
    "docx": [b"\x50\x4B\x03\x04\x14\x00\x06\x00"], # ZIP-based (Office Open XML)
}

def get_file_type(header_bytes):
    """Detects file type based on magic bytes."""
    for ext, signatures in FILE_SIGNATURES.items():
        for sig in signatures:
            if header_bytes.startswith(sig):
                return ext
    return None
