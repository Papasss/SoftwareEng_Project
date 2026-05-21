from unittest.mock import Mock

import pytest

from participium.services.category_service import CategoryService
from participium.models.category import Category
from participium.core.exceptions import (
    ValidationError,
    NotFoundError,
)


# Create a test category
def make_category(
    id=1,
    name="Roads",
    is_active=True,
):
    category = Category(
        name=name,
        is_active=is_active,
    )

    category.id = id

    return category


# Build CategoryService with mocked dependencies
def build_service():
    return CategoryService(
        session=Mock(),
        category_repository=Mock(),
    )


# Categories should be returned from repository
def test_list_categories():
    service = build_service()

    categories = [
        make_category(id=1),
        make_category(id=2),
    ]

    service.category_repository.list_all.return_value = categories

    result = service.list_categories(active_only=True)

    assert result == categories

    service.category_repository.list_all.assert_called_once_with(
        active_only=True,
    )


# Existing category should be returned
def test_get_category_success():
    service = build_service()

    category = make_category()

    service.category_repository.get_by_id.return_value = category

    result = service.get_category(1)

    assert result == category


# Missing category should raise NotFoundError
def test_get_category_not_found():
    service = build_service()

    service.category_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        service.get_category(999)


# Empty category name should raise ValidationError
def test_create_category_empty_name():
    service = build_service()

    with pytest.raises(ValidationError):
        service.create_category("   ")


# Duplicate category name should raise ValidationError
def test_create_category_duplicate_name():
    service = build_service()

    service.category_repository.get_by_name.return_value = (
        make_category()
    )

    with pytest.raises(ValidationError):
        service.create_category("Roads")


# Category should be created successfully
def test_create_category_success():
    service = build_service()

    category = make_category()

    service.category_repository.get_by_name.return_value = None
    service.category_repository.add.return_value = category

    result = service.create_category("Roads")

    assert result == category

    service.category_repository.add.assert_called_once()
    service.session.commit.assert_called_once()


# Updating unknown category should raise NotFoundError
def test_update_category_not_found():
    service = build_service()

    service.category_repository.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        service.update_category(
            999,
            name="New Name",
        )


# Updating with duplicate name should fail
def test_update_category_duplicate_name():
    service = build_service()

    category = make_category(
        id=1,
        name="Roads",
    )

    duplicate = make_category(
        id=2,
        name="Waterworks",
    )

    service.category_repository.get_by_id.return_value = category
    service.category_repository.get_by_name.return_value = duplicate

    with pytest.raises(ValidationError):
        service.update_category(
            1,
            name="Waterworks",
        )


# Category name should be updated successfully
def test_update_category_change_name():
    service = build_service()

    category = make_category(
        id=1,
        name="Roads",
    )

    service.category_repository.get_by_id.return_value = category
    service.category_repository.get_by_name.return_value = None

    result = service.update_category(
        1,
        name="New Roads",
    )

    assert result == category
    assert category.name == "New Roads"

    service.session.commit.assert_called_once()


# Category active flag should be updated successfully
def test_update_category_change_active_flag():
    service = build_service()

    category = make_category(
        is_active=True,
    )

    service.category_repository.get_by_id.return_value = category

    result = service.update_category(
        1,
        is_active=False,
    )

    assert result == category
    assert category.is_active is False

    service.session.commit.assert_called_once()