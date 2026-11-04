import pytest
from blood_donation_screening import process_donor_cohort, verify_storage_centrifuge


# ============================================================================
# Branch Coverage Test Suite (Branch & Decision Coverage Analysis)
# ============================================================================
# This suite is designed to ensure 100% branch and decision coverage by
# evaluating every boolean predicate, compound condition, edge case, and
# control structure (if/elif/else, loops) to both True and False outcomes.


# --- Tests for process_donor_cohort ---

def test_single_accepted_donor():
    """Baseline test: Standard cohort with an eligible donor."""
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


def test_invalid_cohorts_not_a_list():
    """Branch line 2: not isinstance(cohorts, list) evaluates to True."""
    with pytest.raises(ValueError, match="Invalid cohort list or volume"):
        process_donor_cohort("invalid_type", 450)


def test_invalid_volume_zero_or_negative():
    """Branch line 2: isinstance(cohorts, list) is True, standard_volume_ml <= 0 is True."""
    with pytest.raises(ValueError, match="Invalid cohort list or volume"):
        process_donor_cohort([], 0)

    with pytest.raises(ValueError, match="Invalid cohort list or volume"):
        process_donor_cohort([], -100)


def test_empty_cohorts_list():
    """Branch line 8: cohorts list is empty (for-loop executes 0 times)."""
    result = process_donor_cohort([], 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"


def test_clinic_unregistered_branch():
    """Branch line 9: not cohort.get('clinic_registered', False) is True -> continue."""
    cohorts = [
        {
            "clinic_registered": False,
            "type": "standard",
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"


def test_cohort_empty_donors():
    """Branch line 15: cohort with empty donors list (for-loop executes 0 times)."""
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"


def test_donor_underage_branch():
    """Branch line 20: age < 17 is True (weight >= 50)."""
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [{"age": 16, "weight_kg": 60, "hb": 14.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"


def test_donor_underweight_branch():
    """Branch line 20: age >= 17 is True, but weight < 50 is True."""
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [{"age": 25, "weight_kg": 49, "hb": 14.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"


def test_donor_boundary_age_and_weight_accepted():
    """Branch line 20: boundary values age == 17 and weight == 50 evaluate to False."""
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [{"age": 17, "weight_kg": 50, "hb": 14.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 450
    assert result["status"] == "ACCEPTED"


def test_donor_low_hemoglobin_standard_cohort_branch():
    """Branch line 26: hemoglobin < 12.5 and cohort_type != 'high_altitude' (False branch)."""
    cohorts = [
        {
            "clinic_registered": True,
            "type": "standard",
            "donors": [
                {"age": 25, "weight_kg": 65, "hb": 12.4},
                {"age": 30, "weight_kg": 70, "hb": 14.0},
            ],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 450
    assert result["status"] == "ACCEPTED"


def test_donor_low_hemoglobin_high_altitude_branch():
    """Branch line 26: hemoglobin < 12.5 and cohort_type == 'high_altitude' (True branch)."""
    cohorts = [
        {
            "clinic_registered": True,
            "type": "high_altitude",
            "donors": [
                {"age": 25, "weight_kg": 65, "hb": 14.0},
                {"age": 30, "weight_kg": 70, "hb": 11.0},
                {"age": 35, "weight_kg": 80, "hb": 14.5},
            ],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 0
    assert result["status"] == "ZERO_YIELD"


def test_donor_high_hemoglobin_branch():
    """Branch line 29: hemoglobin > 18.0 is True."""
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [
                {"age": 25, "weight_kg": 65, "hb": 18.1},
                {"age": 28, "weight_kg": 70, "hb": 14.0},
            ],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 450
    assert result["status"] == "ACCEPTED"


def test_donor_hemoglobin_boundaries_accepted():
    """Branch lines 24 & 29: exact boundaries hb == 12.5 and hb == 18.0 accepted."""
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [
                {"age": 25, "weight_kg": 65, "hb": 12.5},
                {"age": 28, "weight_kg": 70, "hb": 18.0},
            ],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["collected_ml"] == 900
    assert result["status"] == "ACCEPTED"


def test_fast_track_true_and_false_branches():
    """Branch line 35: fast_track is True vs fast_track is False/omitted."""
    # fast_track True branch
    cohort_fast = [
        {
            "clinic_registered": True,
            "fast_track": True,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}],
        }
    ]
    assert process_donor_cohort(cohort_fast, 450)["collected_ml"] == 500

    # fast_track False branch
    cohort_normal = [
        {
            "clinic_registered": True,
            "fast_track": False,
            "donors": [{"age": 25, "weight_kg": 65, "hb": 14.0}],
        }
    ]
    assert process_donor_cohort(cohort_normal, 450)["collected_ml"] == 450


def test_high_deferral_branch():
    """Branch line 38: deferred_count > 4 is True."""
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
    assert result["status"] == "HIGH_DEFERRAL"
    assert result["collected_ml"] == 450


def test_zero_yield_branch():
    """Branch line 40: total_collected_ml == 0 is True."""
    cohorts = [
        {
            "clinic_registered": True,
            "donors": [{"age": 15, "weight_kg": 60, "hb": 14.0}],
        }
    ]
    result = process_donor_cohort(cohorts, 450)
    assert result["status"] == "ZERO_YIELD"
    assert result["collected_ml"] == 0


# --- Tests for verify_storage_centrifuge ---

def test_centrifuge_no_data_branch():
    """Branch line 46: not centrifuge_runs evaluates to True."""
    assert verify_storage_centrifuge([]) == "NO_DATA"
    assert verify_storage_centrifuge(None) == "NO_DATA"


def test_centrifuge_abort_spin_branch():
    """Branch line 54: rpm_drop_streak >= 2 is True -> returns ABORT_SPIN."""
    runs = [[2500, 2600]]
    assert verify_storage_centrifuge(runs) == "ABORT_SPIN"


def test_centrifuge_single_drop_then_recovery_streak_reset():
    """Branch lines 52, 54, 57: single drop (<3000) followed by recovery (>=3000)."""
    # 2800 (streak 1) -> 3200 (resets to 0) -> 2900 (streak 1) -> finishes stably
    runs = [[2800, 3200, 2900]]
    assert verify_storage_centrifuge(runs) == "STABLE"


def test_centrifuge_multiple_stable_runs():
    """Branch line 49 & 51: multiple runs and empty sub-runs completing stably."""
    runs = [
        [3100, 3200, 3000],
        [],
        [3500, 3400],
    ]
    assert verify_storage_centrifuge(runs) == "STABLE"
