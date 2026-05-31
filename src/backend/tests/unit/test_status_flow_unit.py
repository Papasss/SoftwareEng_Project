from __future__ import annotations

import pytest

from participium.core.status_flow import ensure_transition_allowed
from participium.models.enums import ReportStatus
from participium.core.exceptions import ValidationError


def test_self_transition_allowed():
    assert ensure_transition_allowed(ReportStatus.PENDING_APPROVAL, ReportStatus.PENDING_APPROVAL) is True


def test_allowed_transition():
    assert ensure_transition_allowed(ReportStatus.PENDING_APPROVAL, ReportStatus.ASSIGNED) is True


def test_disallowed_transition_raises():
    with pytest.raises(ValidationError):
        ensure_transition_allowed(ReportStatus.REJECTED, ReportStatus.RESOLVED)
