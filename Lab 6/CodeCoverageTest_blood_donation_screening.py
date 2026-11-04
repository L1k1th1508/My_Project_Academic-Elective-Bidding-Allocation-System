import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge


# ============================================================================
# Code Coverage Test Suite (Line Coverage Analysis)
# ============================================================================
# This suite aims to execute every statement across all functions in
# blood_donation_screening.py, achieving 100% Line (Statement) Coverage.


def test_single_accepted_donor():
    """Initial baseline test: Standard cohort with an eligible donor."""
    cohorts = [
        {
            "clinic_registered": True,
            "type": "standard",
            "fast_track": False,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 450
    assert result["status"] == "ACCEPTED"


def test_invalid_cohorts_input_raises_error():
    """Executes line 3: raises ValueError when cohorts input is not a list."""
    with pytest.raises(ValueError, match="Invalid cohort list or volume"):
        process_donor_cohort("invalid_cohorts", 450)


def test_clinic_unregistered_skipped():
    """Executes line 10: skips cohort when clinic_registered is False."""
    cohorts = [
        {
            "clinic_registered": False,
            "type": "standard",
            "donors": [{"age": 30, "weight_kg": 70, "hb": 15.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"


def test_donor_underage_deferred():
    """Executes lines 21-22: donor with age < 17 is deferred."""
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [{"age": 16, "weight_kg": 60, "hb": 14.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"
    assert result["collected_ml"] == 0


def test_donor_low_hemoglobin_high_altitude_break():
    """Executes lines 25-28: low hemoglobin in high-altitude cohort resets yield and breaks."""
    cohorts = [
        {
            "clinic_registered": True,
            "type": "high_altitude",
            "donors": [
                {"age": 25, "weight_kg": 65, "hb": 14.0},
                {"age": 30, "weight_kg": 70, "hb": 11.0},
            ],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"


def test_donor_high_hemoglobin_deferred():
    """Executes lines 30-31: donor with hb > 18.0 is deferred."""
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [
                {"age": 25, "weight_kg": 65, "hb": 19.0},
                {"age": 28, "weight_kg": 70, "hb": 14.0},
            ],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 450
    assert result["status"] == "ACCEPTED"


def test_fast_track_bonus():
    """Executes line 36: adds 50 ml bonus for fast_track cohorts."""
    cohorts = [
        {
            "clinic_registered": True,
            "fast_track": True,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 500
    assert result["status"] == "ACCEPTED"


def test_high_deferral_status():
    """Executes line 39: deferred_count > 4 returns HIGH_DEFERRAL."""
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [
                {"age": 15, "weight_kg": 60, "hb": 14.0},
                {"age": 15, "weight_kg": 60, "hb": 14.0},
                {"age": 15, "weight_kg": 60, "hb": 14.0},
                {"age": 15, "weight_kg": 60, "hb": 14.0},
                {"age": 15, "weight_kg": 60, "hb": 14.0},
                {"age": 25, "weight_kg": 65, "hb": 14.0},
            ],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 450
    assert result["status"] == "HIGH_DEFERRAL"


def test_zero_yield_status():
    """Executes line 41: returns ZERO_YIELD when total collected is 0."""
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [{"age": 15, "weight_kg": 60, "hb": 14.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"


def test_centrifuge_no_data():
    """Executes line 47: returns NO_DATA when centrifuge_runs is empty."""
    assert verify_storage_centrifuge([]) == "NO_DATA"


def test_centrifuge_abort_spin():
    """Executes lines 53-55: aborts spin on two consecutive RPM drops below 3000."""
    runs = [[2500, 2600]]
    assert verify_storage_centrifuge(runs) == "ABORT_SPIN"


def test_centrifuge_stable():
    """Executes lines 57-58: completes stably with normal RPM."""
    runs = [[3200, 3100]]
    assert verify_storage_centrifuge(runs) == "STABLE"
