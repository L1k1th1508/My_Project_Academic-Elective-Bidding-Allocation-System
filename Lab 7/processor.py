"""
processor.py - Hardened Blood Donation Screening Module (Interactive UI)
"""

def validate_blood_type(blood_code):
    """
    Validates and formats blood group string (e.g., 'A+', 'O-', 'AB+').
    Raises ValueError or TypeError for invalid, missing, or malformed inputs.
    """
    if blood_code is None:
        raise TypeError("Blood code cannot be None.")
    if not isinstance(blood_code, str):
        raise TypeError(f"Expected string input, got {type(blood_code).__name__}.")

    cleaned = blood_code.strip().upper()
    if not cleaned:
        raise ValueError("Blood code cannot be empty.")

    rh_map = {'+': 'Positive', '-': 'Negative'}
    rh_char = cleaned[-1]

    if rh_char not in rh_map:
        raise ValueError(f"Invalid Rh factor symbol in code: '{rh_char}'")

    antigen = cleaned[:-1]
    valid_antigens = {'A', 'B', 'AB', 'O'}
    if antigen not in valid_antigens:
        raise ValueError(f"Invalid antigen group: '{antigen}'")

    return f"{antigen} {rh_map[rh_char]}"


def calculate_pulse_pressure(sys_dia_pair):
    """
    Calculates pulse pressure given (systolic, diastolic) values or 'sys/dia' string.
    Raises ValueError or TypeError for missing, malformed, or invalid inputs.
    """
    if sys_dia_pair is None:
        raise TypeError("Input cannot be None.")

    # Handle string formatted as "120/80"
    if isinstance(sys_dia_pair, str):
        cleaned = sys_dia_pair.strip()
        if not cleaned or '/' not in cleaned:
            raise ValueError("String input must be formatted as 'systolic/diastolic'.")
        parts = cleaned.split('/')
        if len(parts) != 2:
            raise ValueError("Invalid format for systolic/diastolic pair.")
        try:
            sys_val = float(parts[0].strip())
            dia_val = float(parts[1].strip())
        except ValueError:
            raise ValueError("Systolic and diastolic values must be numeric.")
    # Handle tuple/list input like (120, 80)
    elif isinstance(sys_dia_pair, (list, tuple)):
        if len(sys_dia_pair) != 2:
            raise ValueError("Expected exactly 2 elements (systolic, diastolic).")
        try:
            sys_val = float(sys_dia_pair[0])
            dia_val = float(sys_dia_pair[1])
        except (ValueError, TypeError):
            raise ValueError("Systolic and diastolic values must be numeric.")
    else:
        raise TypeError(f"Unsupported type: {type(sys_dia_pair).__name__}")

    if sys_val < dia_val:
        raise ValueError("Systolic pressure cannot be less than diastolic pressure.")

    return sys_val - dia_val


def parse_donor_registry(donor_entry):
    """
    Parses pipe-delimited record: 'DonorID|WeightKg|Hemoglobin'.
    Handles missing fields, malformed numbers, None, and empty inputs cleanly.
    """
    if donor_entry is None:
        raise TypeError("Donor entry cannot be None.")
    if not isinstance(donor_entry, str):
        raise TypeError(f"Expected string input, got {type(donor_entry).__name__}.")

    cleaned = donor_entry.strip()
    if not cleaned:
        raise ValueError("Donor entry cannot be empty.")

    fields = cleaned.split('|')
    if len(fields) != 3:
        raise ValueError("Donor record must contain exactly 3 pipe-separated fields (DonorID|WeightKg|Hemoglobin).")

    donor_id = fields[0].strip()
    if not donor_id:
        raise ValueError("Donor ID cannot be empty.")

    try:
        weight = float(fields[1].strip())
        hemoglobin = float(fields[2].strip())
    except ValueError:
        raise ValueError("Weight and Hemoglobin must be valid numerical values.")

    if weight <= 0 or hemoglobin <= 0:
        raise ValueError("Weight and Hemoglobin values must be positive.")

    return {
        "donor_id": donor_id,
        "weight_kg": weight,
        "hemoglobin": hemoglobin
    }


def main_menu():
    """Interactive User Interface"""
    while True:
        print("\n==============================================")
        print("  BLOOD DONATION SCREENING SYSTEM - MENU")
        print("==============================================")
        print("1. Validate Blood Type (e.g., O+, AB-)")
        print("2. Calculate Pulse Pressure (e.g., 120/80)")
        print("3. Parse Donor Registry Record (e.g., D101|70.5|14.2)")
        print("4. Exit")
        print("----------------------------------------------")
        
        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            user_input = input("\nEnter blood type code: ")
            try:
                result = validate_blood_type(user_input)
                print(f"[SUCCESS] Validated Blood Type: {result}")
            except (ValueError, TypeError) as e:
                print(f"[ERROR] Invalid Input: {e}")

        elif choice == '2':
            user_input = input("\nEnter blood pressure (Systolic/Diastolic, e.g., 120/80): ")
            try:
                result = calculate_pulse_pressure(user_input)
                print(f"[SUCCESS] Pulse Pressure: {result} mmHg")
            except (ValueError, TypeError) as e:
                print(f"[ERROR] Invalid Input: {e}")

        elif choice == '3':
            user_input = input("\nEnter donor record (DonorID|WeightKg|Hemoglobin): ")
            try:
                result = parse_donor_registry(user_input)
                print(f"[SUCCESS] Parsed Record:")
                print(f"  - Donor ID   : {result['donor_id']}")
                print(f"  - Weight (kg): {result['weight_kg']}")
                print(f"  - Hemoglobin : {result['hemoglobin']}")
            except (ValueError, TypeError) as e:
                print(f"[ERROR] Invalid Input: {e}")

        elif choice == '4':
            print("\nExiting program. Goodbye!")
            break
        else:
            print("[ERROR] Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main_menu()