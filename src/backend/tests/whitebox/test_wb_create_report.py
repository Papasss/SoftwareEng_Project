from __future__ import annotations

from unittest.mock import Mock

import pytest

from participium.core.exceptions import ValidationError
from participium.models.category import Category
from participium.models.enums import ReportStatus
from participium.models.report import Report, ReportPhoto, ReportStatusHistory
from participium.models.user import User
from participium.services.report_service import ReportService


pytestmark = pytest.mark.whitebox


def _photo(filename: str, content_type: str = "image/jpeg") -> Mock:
    photo = Mock(spec=["filename", "content_type"])
    photo.filename = filename
    photo.content_type = content_type
    return photo


@pytest.fixture
def report_service_bundle() -> dict[str, object]:
    session = Mock()
    report_repository = Mock()
    category_repository = Mock()
    storage_service = Mock()
    service = ReportService(
        session=session,
        report_repository=report_repository,
        category_repository=category_repository,
        storage_service=storage_service,
    )
    return {
        "service": service,
        "session": session,
        "report_repository": report_repository,
        "category_repository": category_repository,
        "storage_service": storage_service,
    }


@pytest.fixture
def active_category() -> Category:
    return Category(id=5, name="Road", is_active=True)


@pytest.fixture
def reporter() -> User:
    return User(id=100)


def test_create_report_raises_when_category_id_is_malformed(
    report_service_bundle: dict[str, object],
    reporter: User,
) -> None:
    service = report_service_bundle["service"]
    report_service_bundle["category_repository"].get_by_id.return_value = None

    with pytest.raises(ValidationError, match="A valid active category is required\."):
        service.create_report(
            reporter=reporter,
            category_id="invalid",
            title="Title",
            description="Description",
            latitude=10.0,
            longitude=20.0,
            photos=[_photo("photo.jpg")],
        )

    report_service_bundle["report_repository"].add.assert_not_called()
    report_service_bundle["session"].flush.assert_not_called()


def test_create_report_raises_when_category_is_missing(
    report_service_bundle: dict[str, object],
    reporter: User,
) -> None:
    service = report_service_bundle["service"]
    report_service_bundle["category_repository"].get_by_id.return_value = None

    with pytest.raises(ValidationError, match="A valid active category is required\."):
        service.create_report(
            reporter=reporter,
            category_id=999,
            title="Title",
            description="Description",
            latitude=10.0,
            longitude=20.0,
            photos=[_photo("photo.jpg")],
        )

    report_service_bundle["report_repository"].add.assert_not_called()
    report_service_bundle["session"].flush.assert_not_called()


def test_create_report_raises_when_category_is_inactive(
    report_service_bundle: dict[str, object],
    reporter: User,
    active_category: Category,
) -> None:
    service = report_service_bundle["service"]
    inactive_category = Category(id=5, name="Road", is_active=False)
    report_service_bundle["category_repository"].get_by_id.return_value = inactive_category

    with pytest.raises(ValidationError, match="A valid active category is required\."):
        service.create_report(
            reporter=reporter,
            category_id=5,
            title="Title",
            description="Description",
            latitude=10.0,
            longitude=20.0,
            photos=[_photo("photo.jpg")],
        )

    report_service_bundle["report_repository"].add.assert_not_called()
    report_service_bundle["session"].flush.assert_not_called()


@pytest.mark.parametrize(
    "title,description",
    [
        ("", "Description"),
        ("Title", ""),
        (None, "Description"),
        ("Title", None),
    ],
)
def test_create_report_raises_when_title_or_description_is_missing(
    report_service_bundle: dict[str, object],
    reporter: User,
    active_category: Category,
    title: str | None,
    description: str | None,
) -> None:
    service = report_service_bundle["service"]
    report_service_bundle["category_repository"].get_by_id.return_value = active_category

    with pytest.raises(ValidationError, match="Title and description are required\."):
        service.create_report(
            reporter=reporter,
            category_id=5,
            title=title,
            description=description,
            latitude=10.0,
            longitude=20.0,
            photos=[_photo("photo.jpg")],
        )

    report_service_bundle["report_repository"].add.assert_not_called()
    report_service_bundle["session"].flush.assert_not_called()


@pytest.mark.parametrize(
    "latitude,longitude",
    [
        (None, 20.0),
        (10.0, None),
        (None, None),
    ],
)
def test_create_report_raises_when_coordinates_are_missing(
    report_service_bundle: dict[str, object],
    reporter: User,
    active_category: Category,
    latitude: float | None,
    longitude: float | None,
) -> None:
    service = report_service_bundle["service"]
    report_service_bundle["category_repository"].get_by_id.return_value = active_category

    with pytest.raises(ValidationError, match="Latitude and longitude are required\."):
        service.create_report(
            reporter=reporter,
            category_id=5,
            title="Title",
            description="Description",
            latitude=latitude,
            longitude=longitude,
            photos=[_photo("photo.jpg")],
        )

    report_service_bundle["report_repository"].add.assert_not_called()
    report_service_bundle["session"].flush.assert_not_called()


def test_create_report_raises_when_coordinates_are_not_numeric(
    report_service_bundle: dict[str, object],
    reporter: User,
    active_category: Category,
) -> None:
    service = report_service_bundle["service"]
    report_service_bundle["category_repository"].get_by_id.return_value = active_category

    with pytest.raises(ValidationError, match="Latitude and longitude must be valid numbers\."):
        service.create_report(
            reporter=reporter,
            category_id=5,
            title="Title",
            description="Description",
            latitude="north",
            longitude="east",
            photos=[_photo("photo.jpg")],
        )

    report_service_bundle["report_repository"].add.assert_not_called()
    report_service_bundle["session"].flush.assert_not_called()


def test_create_report_raises_when_no_valid_photos_are_provided(
    report_service_bundle: dict[str, object],
    reporter: User,
    active_category: Category,
) -> None:
    service = report_service_bundle["service"]
    report_service_bundle["category_repository"].get_by_id.return_value = active_category

    with pytest.raises(ValidationError, match="At least one photo is required\."):
        service.create_report(
            reporter=reporter,
            category_id=5,
            title="Title",
            description="Description",
            latitude=10.0,
            longitude=20.0,
            photos=[_photo("")],
        )

    report_service_bundle["report_repository"].add.assert_not_called()
    report_service_bundle["session"].flush.assert_not_called()


def test_create_report_raises_when_more_than_three_photos_are_provided(
    report_service_bundle: dict[str, object],
    reporter: User,
    active_category: Category,
) -> None:
    service = report_service_bundle["service"]
    report_service_bundle["category_repository"].get_by_id.return_value = active_category

    photos = [_photo(f"photo_{index}.jpg") for index in range(4)]

    with pytest.raises(ValidationError, match="A report can contain at most 3 photos\."):
        service.create_report(
            reporter=reporter,
            category_id=5,
            title="Title",
            description="Description",
            latitude=10.0,
            longitude=20.0,
            photos=photos,
        )

    report_service_bundle["report_repository"].add.assert_not_called()
    report_service_bundle["session"].flush.assert_not_called()


def test_create_report_persists_report_photo_and_status_history(
    report_service_bundle: dict[str, object],
    reporter: User,
    active_category: Category,
) -> None:
    service = report_service_bundle["service"]
    session = report_service_bundle["session"]
    report_repository = report_service_bundle["report_repository"]
    category_repository = report_service_bundle["category_repository"]
    storage_service = report_service_bundle["storage_service"]

    category_repository.get_by_id.return_value = active_category

    added_reports: list[Report] = []

    def capture_add(report: Report) -> None:
        added_reports.append(report)

    report_repository.add.side_effect = capture_add
    session.flush.side_effect = lambda: setattr(added_reports[0], "id", 42)
    storage_service.save.side_effect = ["/photo1.jpg", "/photo2.jpg"]
    service.get_report = Mock(side_effect=lambda report_id: added_reports[0] if report_id == 42 and added_reports else None)

    photos = [_photo("first.jpg"), _photo("second.jpg"), _photo("")]

    result = service.create_report(
        reporter=reporter,
        category_id=5,
        title="  New title  ",
        description="  Detailed description  ",
        latitude=12.34,
        longitude=56.78,
        photos=photos,
        is_anonymous=True,
    )

    assert result is added_reports[0]
    assert len(added_reports) == 1

    created_report = added_reports[0]
    assert created_report.title == "New title"
    assert created_report.description == "Detailed description"
    assert created_report.latitude == 12.34
    assert created_report.longitude == 56.78
    assert created_report.is_anonymous is True
    assert created_report.status == ReportStatus.PENDING_APPROVAL
    assert created_report.reporter_id == reporter.id
    assert created_report.category_id == active_category.id

    assert storage_service.save.call_count == 2
    storage_service.save.assert_any_call(photos[0])
    storage_service.save.assert_any_call(photos[1])

    assert report_repository.add_photo.call_count == 2
    added_photo_args = [args[0] for args, _ in report_repository.add_photo.call_args_list]
    assert all(isinstance(photo, ReportPhoto) for photo in added_photo_args)
    assert [photo.report_id for photo in added_photo_args] == [42, 42]
    assert [photo.file_path for photo in added_photo_args] == ["/photo1.jpg", "/photo2.jpg"]
    assert [photo.original_filename for photo in added_photo_args] == ["first.jpg", "second.jpg"]

    assert report_repository.add_status_entry.call_count == 1
    status_entry = report_repository.add_status_entry.call_args.args[0]
    assert isinstance(status_entry, ReportStatusHistory)
    assert status_entry.report_id == 42
    assert status_entry.previous_status is None
    assert status_entry.new_status == ReportStatus.PENDING_APPROVAL
    assert status_entry.note == "Report submitted by citizen."
    assert status_entry.changed_by_id == reporter.id

    session.flush.assert_called_once_with()
    session.commit.assert_called_once_with()


