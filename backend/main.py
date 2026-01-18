from fastapi import FastAPI, HTTPException, Query
import pandas as pd
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Aadhaar Analytics API")

# Enable CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "processed_records.csv")
DF = None

@app.on_event("startup")
def load_data():
    global DF
    if os.path.exists(DATA_PATH):
        print("Loading data...")
        try:
            DF = pd.read_csv(DATA_PATH)
            # Ensure pincode is string for searching
            if 'pincode' in DF.columns:
                DF['pincode'] = DF['pincode'].astype(str)
            
            # Fill NaNs
            DF = DF.fillna(0)
            print(f"Data loaded! {len(DF)} records.")
        except Exception as e:
            print(f"Error loading data: {e}")
            DF = pd.DataFrame()
    else:
        print("Warning: Processed data file not found. Run data_processor.py.")
        DF = pd.DataFrame()

@app.get("/")
def health_check():
    return {"status": "ok", "records_count": len(DF) if DF is not None else 0}

@app.get("/analytics/summary")
def get_summary():
    if DF is None or DF.empty:
        return {"error": "No data available"}
    
    # Use Enrolment columns for the primary age distribution
    # 0-5
    s05 = int(DF['age_0_5'].sum()) if 'age_0_5' in DF.columns else 0
    # 5-17
    s517 = int(DF['age_5_17'].sum()) if 'age_5_17' in DF.columns else 0
    # 18+
    s18 = int(DF['age_18_greater'].sum()) if 'age_18_greater' in DF.columns else 0
    
    return {
        "age_0_5": s05,
        "age_5_17": s517,
        "age_18_plus": s18,
        "total": s05 + s517 + s18
    }

@app.get("/analytics/geo")
def get_geo_stats(state: str = None):
    if DF is None or DF.empty:
        return []
    
    data = DF
    if state:
        # Case insensitive match might be nicer, but exact for now
        data = data[data['state'] == state]
        
    cols_to_sum = []
    if 'age_0_5' in DF.columns: cols_to_sum.append('age_0_5')
    if 'age_5_17' in DF.columns: cols_to_sum.append('age_5_17')
    if 'age_18_greater' in DF.columns: cols_to_sum.append('age_18_greater')
    
    if not cols_to_sum:
        return []

    # Group by State and District
    grouped = data.groupby(['state', 'district'])[cols_to_sum].sum().reset_index()
    
    return grouped.to_dict(orient='records')

@app.get("/records")
def search_records(pincode: str = Query(..., min_length=3), limit: int = 50):
    if DF is None or DF.empty:
        return []
    
    if 'pincode' not in DF.columns:
        return []

    # Filter by pincode substring matches for better UX
    results = DF[DF['pincode'].str.contains(pincode, na=False)]
    
    # Replace NaN with clean values for JSON
    results = results.fillna("")
    
    return results.head(limit).to_dict(orient='records')
