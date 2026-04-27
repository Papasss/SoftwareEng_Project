from __future__ import annotations

from participium.core.status_flow import ensure_transition_allowed
from participium.core.exceptions import ValidationError
from participium.models.enums import ReportStatus

import pytest


# PENDING APPROVAL
@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize("next_state", [
    ReportStatus.PENDING_APPROVAL,
    ReportStatus.ASSIGNED,
    ReportStatus.REJECTED
])
def test_verify_pending_status_success(next_state) -> None:
    current_state = ReportStatus.PENDING_APPROVAL

    status = ensure_transition_allowed(current_state, next_state)

    assert isinstance(status, bool)
    assert status == True


@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize("next_state", [
    ReportStatus.RESOLVED,
    ReportStatus.IN_PROGRESS,
    ReportStatus.SUSPENDED
])
def test_verify_pending_status_error(next_state) -> None:
    current_state = ReportStatus.PENDING_APPROVAL

    with pytest.raises(ValidationError):
        ensure_transition_allowed(current_state, next_state)


# ASSIGNED
@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize("next_state", [
    ReportStatus.IN_PROGRESS,
    ReportStatus.ASSIGNED,
    ReportStatus.SUSPENDED,
    ReportStatus.RESOLVED
])
def test_verify_assigned_status_success(next_state) -> None:
    current_state = ReportStatus.ASSIGNED

    status = ensure_transition_allowed(current_state, next_state)

    assert isinstance(status, bool)
    assert status == True


@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize("next_state", [
    ReportStatus.REJECTED,
    ReportStatus.PENDING_APPROVAL
])
def test_verify_assigned_status_error(next_state) -> None:
    current_state = ReportStatus.ASSIGNED

    with pytest.raises(ValidationError):
        ensure_transition_allowed(current_state, next_state)


# IN PROGRESS
@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize("next_state", [
    ReportStatus.IN_PROGRESS,
    ReportStatus.SUSPENDED,
    ReportStatus.RESOLVED
])
def test_verify_in_progress_status_success(next_state) -> None:
    current_state = ReportStatus.IN_PROGRESS

    status = ensure_transition_allowed(current_state, next_state)

    assert isinstance(status, bool)
    assert status == True


@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize("next_state", [
    ReportStatus.REJECTED,
    ReportStatus.PENDING_APPROVAL,
    ReportStatus.ASSIGNED
])
def test_verify_in_progress_status_error(next_state) -> None:
    current_state = ReportStatus.IN_PROGRESS

    with pytest.raises(ValidationError):
        ensure_transition_allowed(current_state, next_state)


# SUSPENDED
@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize("next_state", [
    ReportStatus.IN_PROGRESS,
    ReportStatus.SUSPENDED,
    ReportStatus.RESOLVED
])
def test_verify_suspended_status_success(next_state) -> None:
    current_state = ReportStatus.SUSPENDED

    status = ensure_transition_allowed(current_state, next_state)

    assert isinstance(status, bool)
    assert status == True


@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize("next_state", [
    ReportStatus.REJECTED,
    ReportStatus.PENDING_APPROVAL,
    ReportStatus.ASSIGNED
])
def test_verify_suspended_status_error(next_state) -> None:
    current_state = ReportStatus.SUSPENDED

    with pytest.raises(ValidationError):
        ensure_transition_allowed(current_state, next_state)


# REJECTED
@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize("next_state", [
    ReportStatus.REJECTED
])
def test_verify_rejected_status_success(next_state) -> None:
    current_state = ReportStatus.REJECTED

    status = ensure_transition_allowed(current_state, next_state)

    assert isinstance(status, bool)
    assert status == True


@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize("next_state", [
    ReportStatus.PENDING_APPROVAL,
    ReportStatus.ASSIGNED,
    ReportStatus.IN_PROGRESS,
    ReportStatus.SUSPENDED,
    ReportStatus.RESOLVED
])
def test_verify_rejected_status_error(next_state) -> None:
    current_state = ReportStatus.REJECTED

    with pytest.raises(ValidationError):
        ensure_transition_allowed(current_state, next_state)


# RESOLVED
@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize("next_state", [
    ReportStatus.REJECTED
])
def test_verify_resolved_status_success(next_state) -> None:
    current_state = ReportStatus.RESOLVED

    status = ensure_transition_allowed(current_state, next_state)

    assert isinstance(status, bool)
    assert status == True


@pytest.mark.skip(reason="Disabled.")
@pytest.mark.parametrize("next_state", [
    ReportStatus.PENDING_APPROVAL,
    ReportStatus.ASSIGNED,
    ReportStatus.IN_PROGRESS,
    ReportStatus.SUSPENDED,
    ReportStatus.REJECTED
])
def test_verify_resolved_status_error(next_state) -> None:
    current_state = ReportStatus.RESOLVED

    with pytest.raises(ValidationError):
        ensure_transition_allowed(current_state, next_state)
