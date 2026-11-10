import pytest
from hypothesis import given, strategies as st
from processor import validate_blood_type, calculate_pulse_pressure, parse_donor_registry

# Strategy generating arbitrary types to thoroughly stress-test input validation
any_type = st.one_of(
    st.text(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.booleans(),
    st.none(),
    st.lists(st.text()),
)


@given(val=any_type)
def test_validate_blood_type_no_crash(val):
    """
    Ensures validate_blood_type handles valid blood types (A+, O-, etc.), invalid strings,
    empty strings, None, and improper types safely without unhandled crashes.
    """
    try:
        result = validate_blood_type(val)
        # If it returns without raising an exception, it should be a boolean or normalized string
        assert isinstance(result, (bool, str))
    except (ValueError, TypeError):
        pass  # Handled validation exceptions are expected for invalid inputs


@given(val=any_type)
def test_calculate_pulse_pressure_safe(val):
    """
    Ensures calculate_pulse_pressure handles valid inputs, invalid numeric strings,
    malformed tuples/lists, None, and non-string inputs without crashing.
    """
    try:
        result = calculate_pulse_pressure(val)
        assert isinstance(result, (int, float))
    except (ValueError, TypeError, ZeroDivisionError, AttributeError):
        pass  # Handled validation exceptions are expected for invalid inputs


@given(val=any_type)
def test_parse_donor_registry_safe(val):
    """
    Ensures parse_donor_registry handles formatted strings, empty strings, None,
    malformed records, and arbitrary data types safely.
    """
    try:
        result = parse_donor_registry(val)
        assert isinstance(result, (list, dict))
    except (ValueError, TypeError, AttributeError):
        pass  # Handled validation exceptions are expected for invalid inputs