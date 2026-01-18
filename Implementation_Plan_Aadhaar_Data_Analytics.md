# Implementation Plan - Aadhaar Data Analytics

## Goal Description
Develop an **Age-Based Unique Identification System Prototype** and an **Analytics Dashboard** using the provided Aadhaar datasets. The system will process demographic, biometric, and enrolment data to visualize citizen distribution across life stages (0-5, 5-17, 18+) and generate unique Record IDs for tracking purposes.

## User Review Required
> [!IMPORTANT]
> **Data Aggregation vs. Individual Records**: The provided datasets are **aggregated** by Day/State/District/Pincode. They do not contain individual citizen records.
> - **Decision Point**: The "Unique Record ID" will be generated for each **Data Entry Row** (representing a Pincode-Date-AgeGroup block) unless we strictly need to simulate individual citizens (which would require expanding the counts into millions of dummy rows).
> - **Assumption**: We will proceed with generating IDs for the *aggregated blocks* to track trends and demand.

## Proposed Changes

### 1. Data Processing Engine (Python)
We will build a Python-based processing engine to ingest and normalize the data from the `api_data_aadhar_*` directories.

#### [NEW] `backend/data_processor.py`
- **Responsibilities**:
    - Scan `d:/gov/api_data_aadhar_*` directories for CSV files.
    - specialized readers for:
        - `Biometric`: (Columns: `biometric_captured`, etc.)
        - `Demographic`: (Columns: `demo_age_5_17`, `demo_age_17_`)
        - `Enrolment`: (Columns: `age_0_5`, `age_5_17`, `age_18_greater`)
    - **Data Merging**: Join datasets on `[date, state, district, pincode]` to create a unified view.
    - **ID Generation**: simple hash generation (e.g., `SHA256(pincode + date + suffix)`) to create a stable `Record_ID` for each data row.
    - **Normalization**: Standardize State/District names to handle inconsistencies.

### 2. Analytics API (FastAPI)
Expose the processed data via a lightweight REST API for the dashboard.

#### [NEW] `backend/main.py`
- **Endpoints**:
    - `GET /analytics/summary`: Returns total counts by Life Stage (0-5, 5-17, 18+).
    - `GET /analytics/geo`: Returns data grouped by State/District for map visualization.
    - `GET /records`: Searchable list of records with their generated Unique IDs.

### 3. Analytics Dashboard (Frontend)
A React-based dashboard to visualize the insights.

#### [NEW] `frontend/src/App.jsx`
- **Features**:
    - **Demand Heatmap**: Visual map showing high-demand areas for child services (0-5 age group).
    - **Age Distribution Charts**: Bar/Pie charts showing the 3 life stages.
    - **Record Explorer**: Table view to search/filter by Pincode or Record ID.
- **Tech Stack**: React, Recharts (for viz), TailwindCSS (for styling).

## Verification Plan

### Automated Tests
- **Data Integrity**: Verify that `Sum(age_groups) == Total_Enrolment`.
- **ID Uniqueness**: Ensure generated `Record_ID`s are unique across the dataset.
- **API Tests**:
    ```bash
    # Test Summary Endpoint
    curl http://localhost:8000/analytics/summary
    ```

### Manual Verification
- **Dashboard Check**:
    1. Open Dashboard.
    2. Filter by "Uttar Pradesh".
    3. Verify that the "0-5 Years" count matches the sum of the enrolment CSVs for that state.
    4. Search for a specific Pincode (e.g., `221001`) and verify the Record ID is displayed.
