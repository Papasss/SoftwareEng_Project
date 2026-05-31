from pathlib import Path
from io import BytesIO

from werkzeug.datastructures import FileStorage

from participium.services.storage_service import (
    StorageService,
    LocalFileStorageService,
)


# Base StorageService should return simulated file name
def test_storage_service_save():
    service = StorageService()

    file = FileStorage(
        stream=BytesIO(b"data"),
        filename="test.txt",
    )

    result = service.save(file)

    assert result == "simulated-file"


# Local storage should create media directory automatically
def test_local_storage_creates_directory(tmp_path):
    media_root = tmp_path / "uploads"

    LocalFileStorageService(media_root)

    assert media_root.exists()
    assert media_root.is_dir()


# Uploaded file should be saved on disk
def test_local_storage_save_file(tmp_path):
    service = LocalFileStorageService(tmp_path)

    uploaded_file = FileStorage(
        stream=BytesIO(b"hello world"),
        filename="photo.jpg",
    )

    relative_name = service.save(uploaded_file)

    saved_file = tmp_path / relative_name

    assert saved_file.exists()
    assert saved_file.read_bytes() == b"hello world"


# Missing filename should use attachment.bin fallback
def test_local_storage_default_filename(tmp_path):
    service = LocalFileStorageService(tmp_path)

    uploaded_file = FileStorage(
        stream=BytesIO(b"content"),
        filename="",
    )

    relative_name = service.save(uploaded_file)

    assert relative_name.endswith("attachment.bin")


# Filename should be sanitized using secure_filename
def test_local_storage_secure_filename(tmp_path):
    service = LocalFileStorageService(tmp_path)

    uploaded_file = FileStorage(
        stream=BytesIO(b"content"),
        filename="../../evil file.txt",
    )

    relative_name = service.save(uploaded_file)

    assert ".." not in relative_name
    assert "evil_file.txt" in relative_name