# Academic Elective Bidding & Allocation System

A system for managing academic elective selection through student bidding, eligibility validation, timetable-conflict checking, automated allocation, and publication of allocation results.

> **Note:** This README is based on the project's Academic Elective Bidding & Allocation use-case documentation available in the conversation. The GitHub repository contents could not be fetched from this environment, so implementation-specific details such as the exact programming language, framework, database, folder structure, and installation commands have intentionally not been invented.

## Overview

The Academic Elective Bidding & Allocation System is designed to provide a structured workflow for students to submit elective bids and for the academic registrar to run the elective allocation process.

The system covers:

- Viewing available electives
- Submitting elective bids
- Validating bidding credits
- Validating prerequisites
- Checking timetable conflicts
- Viewing bid summaries
- Running elective allocation
- Resolving timetable conflicts
- Publishing allocation results
- Viewing allocation results

## Actors

### Student

Students interact with the system to:

- View available electives
- Submit elective bids
- View their bid summary
- View their final allocation results

During bid submission, the system validates bidding credits and prerequisites and checks for timetable conflicts.

### Academic Registrar

The academic registrar manages the allocation process by:

- Running elective allocation
- Resolving timetable conflicts
- Publishing allocation results

### Course / Timetable Database

The system uses course and timetable information while validating prerequisites, checking timetable conflicts, and supporting the allocation process.

## System Workflow

```text
Student
   |
   +--> View Available Electives
   |
   +--> Submit Elective Bids
          |
          +--> Validate Bidding Credits
          +--> Validate Prerequisites
          +--> Check Timetable Conflicts
   |
   +--> View Bid Summary
   |
   +--> View Allocation Results

Academic Registrar
   |
   +--> Run Elective Allocation
          |
          +--> Resolve Timetable Conflicts
   |
   +--> Publish Allocation Results
```

## Core Functional Modules

### 1. Elective Browsing

Students can view the electives available for bidding.

### 2. Bid Submission

Students can submit their elective bids through the system.

### 3. Bid Validation

The system performs validation during bidding, including:

- Bidding-credit validation
- Prerequisite validation
- Timetable-conflict checking

### 4. Bid Summary

Students can review a summary of their submitted bids.

### 5. Elective Allocation

The academic registrar can initiate the elective allocation process. Timetable conflicts can be resolved as part of the allocation workflow.

### 6. Allocation Publication

The allocation results can be published after the allocation process is completed.

### 7. Result Viewing

Students can view their allocation results after publication.

## Use-Case Summary

| Actor | Use Case | Purpose |
|---|---|---|
| Student | View Available Electives | Browse electives available for bidding |
| Student | Submit Elective Bids | Submit elective choices/bids |
| Student / System | Validate Bidding Credits | Check whether the student's bidding credits are valid |
| Student / System | Validate Prerequisites | Check prerequisite requirements |
| Student / System | Check Timetable Conflicts | Detect conflicts among selected electives |
| Student | View Bid Summary | Review submitted bids |
| Academic Registrar | Run Elective Allocation | Execute the allocation process |
| Academic Registrar | Resolve Timetable Conflicts | Handle conflicts during allocation |
| Academic Registrar | Publish Allocation Results | Make finalized results available |
| Student | View Allocation Results | View the student's allocated electives |
| Course / Timetable Database | Course & Timetable Information | Provide course and timetable data used by the system |

## Allocation Process

The documented workflow can be summarized as:

1. Students view the available electives.
2. Students submit their elective bids.
3. The system validates bidding credits and prerequisites.
4. The system checks timetable conflicts.
5. Students can review their bid summary.
6. The academic registrar runs the elective allocation.
7. Timetable conflicts are resolved as required.
8. The allocation results are published.
9. Students view their allocation results.

## Project Documentation

The project documentation includes a UML use-case representation of the Academic Elective Bidding & Allocation System, showing the interactions between students, the academic registrar, and the course/timetable database.

## Repository

GitHub repository:

`https://github.com/L1k1th1508/My_Project_Academic-Elective-Bidding-Allocation-System`

## Future README Sections

Once the repository implementation is available, the following can be added without guessing:

- Tech stack
- System requirements
- Project structure
- Installation steps
- Environment variables
- Database setup
- How to run the application
- Screenshots
- API documentation
- Testing instructions
- Contributors
- License
