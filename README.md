# Age-Based Unique ID System & Analytics Dashboard

## 1. Project Overview
This project is an **Age-Based Unique Identification System Prototype** designed to analyze and visualize Aadhaar enrolment data. It addresses the need to quantify demand for age-specific services (0-5, 5-17, 18+ years) and provides a mechanism to generate and track Unique Record IDs for aggregated data blocks.

### Key Features
-   **Data Ingestion Engine**: Consolidates fragmented CSV datasets (Enrolment, Demographic, Biometric) into a unified record set.
-   **Unique ID Generation**: algorithmically generates stable, unique IDs for every data row key (Date + Pincode).
-   **Analytics API**: A fast, lightweight REST API serving demographic summaries and geographic distributions.
-   **Interactive Dashboard**: A React-based UI featuring:
    -   **Demand Heatmaps**: Identify high-density areas for child services.
    -   **Age Distribution Visualization**: Interactive charts for demographic analysis.
    -   **Record Explorer**: Search and verification tool for Unique IDs.

---

## 2. System Architecture

### A. Data Layer (`processed_records.csv`)
-   **Source**: Raw CSVs in `api_data_aadhar_*` directories.
-   **Processing**: `backend/data_processor.py` merges these files and adds:
    -   `record_id`: `ADHR-YYYYMMDD-PINCODE-HASH`
    -   Normalized age columns: `age_0_5`, `age_5_17`, `age_18_greater`

### B. Backend API (`backend/main.py`)
-   **Tech Stack**: Python, FastAPI, Pandas.
-   **Port**: `8000`.
-   **Endpoints**:
    -   `GET /analytics/summary`: Aggregate counts for the entire dataset.
    -   `GET /analytics/geo`: State/District-wise breakdown.
    -   `GET /records?pincode=...`: Searchable interface for individual records.

### C. Frontend Dashboard (`frontend/`)
-   **Tech Stack**: React (Vite), Tailwind CSS, Recharts, Axios.
-   **Port**: `5173`.
-   **Components**: Summary Cards, Bar/Pie Charts, Data Table.

---

## 3. Installation & Setup

### Prerequisites
-   Python 3.10+
-   Node.js 18+
-   Git (optional)

### Step 1: Data Processing
Before running the app, you must generate the unified dataset.
```bash
cd d:/gov
python backend/data_processor.py
# This creates 'processed_records.csv' in the project root.
```

### Step 2: Backend Setup
```bash
cd d:/gov
# Install dependencies
pip install -r backend/requirements.txt

# Start the API Server
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
> The API will be available at `http://localhost:8000`.

### Step 3: Frontend Setup
```bash
cd d:/gov/frontend
# Install dependencies (ensure Tailwind v3 is used for stability)
npm install
# Start the Dashboard
npm run dev
```
> The Dashboard will be available at `http://localhost:5173`.

---

## 4. Usage Guide

### verifying the Data
1.  Navigate to the **Dashboard Home**.
2.  Check the **Total Enrolments** card. It should match the sum of your raw CSV data (~6.6 Million in sample data).
3.  Use the **Record Explorer** to search for Pincode `273001` (Gorakhpur).
4.  Verify that a unique `Record ID` (e.g., `ADHR-20250301-273001-XXXX`) matches the data row.

### Analyzing Demand
1.  Look at the **Top 5 Districts** bar chart.
2.  Identify districts with high `0-5 Years` bars (Blue). These are priority areas for early childhood services (vaccination, preschools).

---

## 5. Troubleshooting

### Issue: "React/Tailwind styles are missing"
-   **Fix**: Ensure you are using a compatible Tailwind version. We recommend `tailwindcss@3.4.17`.
    ```bash
    npm install -D tailwindcss@3.4.17 postcss autoprefixer
    ```

### Issue: "No Data Available" in Dashboard
-   **Fix**: Ensure `processed_records.csv` exists in `d:/gov/`.
-   **Fix**: Check if the backend is running. Open `http://localhost:8000/` in your browser to see the health check.

### Issue: "Port already in use"
-   **Fix**: Kill existing terminal processes or change the port flags (`--port 8001`) in the run commands.

---

## 6. Developer Notes
-   **Extensibility**: The `data_processor.py` can be easily modified to include new columns (e.g., specific biometric failure rates) by adding them to the merge logic.
-   **Production**: For production deployment, build the React app (`npm run build`) and serve static files using Nginx or FastAPI's `StaticFiles`.
