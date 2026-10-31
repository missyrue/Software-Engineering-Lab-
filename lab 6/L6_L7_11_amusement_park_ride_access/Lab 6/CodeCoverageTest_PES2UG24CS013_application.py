"""Line coverage tests for the amusement park admission application."""

import pytest

from amusement_park_ride_access import (
    inspect_safety_restraints,
    process_ride_admissions,
)


def patron(height=150, *, child=False, warning=False):
    return {
        "height_cm": height,
        "is_child": child,
        "health_warning": warning,
    }


def group(*patrons, ride="family", open_=True, fast=False):
    return {
        "is_open": open_,
        "ride_type": ride,
        "has_fast_lane": fast,
        "patrons": list(patrons),
    }


@pytest.mark.parametrize("groups, fee", [(None, 2.0), ([], -1.0)])
def test_invalid_arguments_raise(groups, fee):
    with pytest.raises(ValueError, match="Invalid groups list or pass fee"):
        process_ride_admissions(groups, fee)


def test_closed_and_unknown_ride_groups_are_skipped_or_rejected():
    result = process_ride_admissions(
        [group(patron(), open_=False), group(patron(), ride="haunted")], 5.0
    )
    assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


def test_ticket_prices_child_admission_and_fast_lane():
    result = process_ride_admissions(
        [
            group(patron(), ride="roller_coaster"),
            group(patron(child=True), ride="water_ride"),
            group(patron(child=True), fast=True),
        ],
        5.0,
    )
    assert result == {"total_revenue": 46.8, "status": "COMPLETED"}


def test_invalid_short_and_health_warning_patrons_are_rejected():
    result = process_ride_admissions(
        [group(patron(0), patron(100), patron(warning=True))], 5.0
    )
    assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


def test_coaster_health_warning_cancels_group_and_stops_processing_it():
    result = process_ride_admissions(
        [group(patron(), patron(warning=True), patron(), ride="roller_coaster", fast=True)],
        5.0,
    )
    assert result == {"total_revenue": 5.0, "status": "COMPLETED"}


def test_rejection_threshold_triggers_safety_audit():
    result = process_ride_admissions(
        [group(*(patron(0) for _ in range(5))), group(patron())], 0.0
    )
    assert result == {"total_revenue": 10.0, "status": "SAFETY_AUDIT"}


def test_restraint_sensor_states():
    assert inspect_safety_restraints([]) == "NO_DATA"
    assert inspect_safety_restraints([[1, 0, 1, 0]]) == "SAFE"
    assert inspect_safety_restraints([[0, 1], [1, 0, 0]]) == "EMERGENCY_LOCK"
