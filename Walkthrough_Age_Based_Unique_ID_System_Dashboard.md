# Walkthrough - Age-Based Unique ID System Dashboard

## Overview
This document provides a comprehensive guide to navigating, using, and verifying the **Age-Based Unique Identification System Prototype** and **Analytics Dashboard**. It details the steps to validate that the data processing engine correctly aggregates Aadhaar data and that the dashboard accurately visualizes citizen distribution and generated Unique IDs.

## Prerequisites
Before starting the walkthrough, ensure the following components are running:
1.  **Backend API**: Fast API server running (default: `http://localhost:8000`).
2.  **Frontend Dashboard**: React application running (default: `http://localhost:3000`).
3.  **Data**: Source CSV files placed in `d:/gov/api_data_aadhar_*`.

## 1. Data Ingestion & Processing Verification
**Objective**: Confirm that the system correctly ingests disparate CSV files and generates unique IDs.

### Steps:
1.  **Run the Processor**:
    - Execute the data processing script (e.g., `python backend/data_processor.py`).
    - **Observe**: Console output should list the number of files processed for Biometric, Demographic, and Enrolment categories.
2.  **Verify Integrity**:
    - Check the logs for the "Total Records" count.
    - **Validation**: Ensure `Sum(0-5) + Sum(5-17) + Sum(18+)` matches the total enrolment figures from the raw CSVs.

## 2. Dashboard Navigation

### A. Home / Summary View
**Objective**: Visualize the high-level citizen distribution.
- **Action**: Open the dashboard landing page.
- **Expected Visualization**:
    - **Total Citizens Card**: Displays the grand total of all age groups.
    - **Age Distribution Chart**: A Pie/Bar chart split into:
        - **0-5 Years** (Early Childhood)
        - **5-17 Years** (School Age)
        - **18+ Years** (Adults)

### B. Demand Heatmap (0-5 Years)
**Objective**: Identify regions with high demand for age-specific services (e.g., vaccination, kindergarten).
- **Action**: Navigate to the "Heatmap" or "Geographic View" tab.
- **Action**: Select "0-5 Years" from the filter dropdown.
- **Expected Result**:
    - The map highlights States/Districts.
    - **Darker Red/Blue**: Indicates higher population density for the 0-5 age group (e.g., a district with >50k children).
    - **Tooltip**: Hovering over a region shows the exact count (e.g., "Gorakhpur: 49,000").

### C. Unique Record Explorer
**Objective**: Verify the generation and retrieval of Unique Record IDs.
- **Action**: Go to the "Search Records" tab.
- **Action**: Enter a specific **Pincode** (e.g., `221001` or `560001`) in the search bar.
- **Expected Result**:
    - A table appears listing aggregated data rows for that pincode.
    - **Column `Record_ID`**: Displays a unique hash string for each row (e.g., `ADHR-20250301-273001-05`).
    - This ID is consistent and reproducible for the same data block.

## 3. Scenarios & Testing

### Scenario 1: Planning for a New School
- **Goal**: Find a district with a high number of school-age children (5-17).
- **Steps**:
    1.  Filter the dashboard by "5-17 Years".
    2.  Sort the data table by "Count" (Descending).
    3.  **Result**: The dashboard identifies the top 5 districts (e.g., "Allahabad", "Bangalore Urban") requiring new educational infrastructure.

### Scenario 2: Data Audit
- **Goal**: Trace a summary figure back to the source.
- **Steps**:
    1.  Note the "Total 18+" count for a specific Date and District on the dashboard.
    2.  Open the corresponding raw CSV file in `d:/gov/api_data_aadhar_enrolment/...`.
    3.  **Result**: The sum of the `age_18_greater` column in the CSV exactly matches the dashboard figure.

## Conclusion
This walkthrough confirms that the system successfully transforms raw, fragmented Aadhaar data into actionable insights, providing unique identification tracking and clear demographic visualization.
