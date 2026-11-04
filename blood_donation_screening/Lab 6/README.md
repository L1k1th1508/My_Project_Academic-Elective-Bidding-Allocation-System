# L6_L7_05 — Blood Donation Screening

Lab 6: Code and Branch Coverage Analysis

## About

A Python module that screens prospective blood donor cohorts based on age, weight, and hemoglobin levels, and monitors centrifuge spin cycles for rotation speed failures.

## Files & Deliverables

| File | Description |
|------|-------------|
| `blood_donation_screening.py` | The module under test |
| `test_blood_donation.py` | Full test suite covering all line and branch paths |
| `CodeCoverageTest_blood_donation_screening.py` | Deliverable test suite achieving 100% Code (Line) Coverage |
| `BranchCoverageTest_blood_donation_screening.py` | Deliverable test suite achieving 100% Branch Coverage |
| `code_coverage_analysis.png` | Terminal output screenshot for Code Coverage analysis |
| `branch_coverage_analysis.png` | Terminal output screenshot for Branch Coverage analysis |

## Running Tests & Coverage

### 1. Code Coverage (Line Coverage)

Run tests and measure line coverage:
```bash
coverage run -m pytest CodeCoverageTest_blood_donation_screening.py
coverage report -m
```

**Result:**
- **Line Coverage:** 100% (45 / 45 statements executed)
- **Status:** Passed (12/12 test cases)

### 2. Branch Coverage

Run tests and measure branch coverage:
```bash
coverage run --branch -m pytest BranchCoverageTest_blood_donation_screening.py
coverage report -m
```

**Result:**
- **Branch Coverage:** 100% (32 / 32 branches evaluated to both True & False)
- **Line Coverage:** 100% (45 / 45 statements executed)
- **Status:** Passed (20/20 test cases)

## Commit History

This repository maintains systematic commits according to the lab specification:
1. `feat(lab6): add code coverage test cases and analysis report screenshot` (Commit 1)
2. `feat(lab6): add branch coverage test cases and analysis report screenshot` (Commit 2)
