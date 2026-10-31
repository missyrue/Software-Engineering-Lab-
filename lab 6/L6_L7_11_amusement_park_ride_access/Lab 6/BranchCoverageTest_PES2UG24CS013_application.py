"""Branch coverage tests for the amusement park admission application."""

import pytest

from amusement_park_ride_access import (
    inspect_safety_restraints,
    process_ride_admissions,
)


def patron(height=150, *, child=False, warning=False):
    return {"height_cm": height, "is_child": child, "health_warning": warning}


def group(*patrons, ride="family", open_=True, fast=False):
    return {
        "is_open": open_,
        "ride_type": ride,
        "has_fast_lane": fast,
        "patrons": list(patrons),
    }


@pytest.mark.parametrize("groups, fee", [(None, 1.0), ([], -1.0)])
def test_each_invalid_argument_branch(groups, fee):
    with pytest.raises(ValueError):
        process_ride_admissions(groups, fee)


@pytest.mark.parametrize(
    "ride, expected",
    [("roller_coaster", 25.0), ("water_ride", 18.0), ("family", 10.0)],
)
def test_each_supported_ride_type(ride, expected):
    result = process_ride_admissions([group(patron(), ride=ride)], 5.0)
    assert result == {"total_revenue": expected, "status": "COMPLETED"}


def test_default_values_and_skipped_closed_group():
    groups = [
        {"is_open": False},
        {"is_open": True, "patrons": [{}]},
    ]
    assert process_ride_admissions(groups, 0.0) == {
        "total_revenue": 0.0,
        "status": "ZERO_ADMISSIONS",
    }


def test_patron_rejection_and_admission_paths():
    result = process_ride_admissions(
        [
            group(patron(0), patron(119), patron(120, child=True)),
            group(patron(warning=True), ride="water_ride"),
            group(patron(121), patron(122, child=True), ride="family"),
        ],
        0.0,
    )
    assert result == {"total_revenue": 22.0, "status": "COMPLETED"}


def test_unknown_ride_is_counted_as_rejected():
    result = process_ride_admissions([group(patron(), ride="unknown")], 0.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


def test_coaster_warning_breaks_and_fast_lane_is_still_charged():
    result = process_ride_admissions(
        [group(patron(), patron(warning=True), patron(), ride="roller_coaster", fast=True)],
        5.0,
    )
    assert result == {"total_revenue": 5.0, "status": "COMPLETED"}


@pytest.mark.parametrize(
    "groups, expected",
    [
        ([group()], "ZERO_ADMISSIONS"),
        ([group(patron(0), patron(0), patron(0), patron(0))], "ZERO_ADMISSIONS"),
        ([group(patron(0), patron(0), patron(0), patron(0), patron(0))], "SAFETY_AUDIT"),
    ],
)
def test_audit_boundary_and_zero_revenue(groups, expected):
    assert process_ride_admissions(groups, 0.0)["status"] == expected


def test_restraint_no_data_safe_reset_and_emergency():
    assert inspect_safety_restraints([]) == "NO_DATA"
    assert inspect_safety_restraints([[0], [1, 0, 1]]) == "SAFE"
    assert inspect_safety_restraints([[1, 0, 0]]) == "EMERGENCY_LOCK"
