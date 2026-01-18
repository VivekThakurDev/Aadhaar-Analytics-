import os
import glob
import pandas as pd
import hashlib

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_ROOT = os.path.dirname(BASE_DIR)

# Paths to data folders (adjusting based on observed structure)
PATH_ENROLMENT = os.path.join(DATA_ROOT, 'api_data_aadhar_enrolment', 'api_data_aadhar_enrolment')
PATH_DEMOGRAPHIC = os.path.join(DATA_ROOT, 'api_data_aadhar_demographic', 'api_data_aadhar_demographic')
PATH_BIOMETRIC = os.path.join(DATA_ROOT, 'api_data_aadhar_biometric', 'api_data_aadhar_biometric')

OUTPUT_FILE = os.path.join(BASE_DIR, 'processed_records.csv')

def load_data(folder_path, tag):
    """
    Load all CSV files from a folder into a single DataFrame.
    Prefix value columns with the tag (e.g., 'enrol_', 'demo_').
    """
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    if not all_files:
        print(f"Warning: No files found in {folder_path}")
        return pd.DataFrame()
    
    df_list = []
    for filename in all_files:
        print(f"Loading {filename}...")
        try:
            df = pd.read_csv(filename)
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            
    if not df_list:
        return pd.DataFrame()
        
    final_df = pd.concat(df_list, ignore_index=True)
    
    # Standardize column names (lowercase, strip)
    final_df.columns = [c.strip().lower() for c in final_df.columns]
    
    return final_df

def generate_record_id(row):
    """
    Generate a unique ID based on Date, Pincode, and District.
    Format: ADHR-YYYYMMDD-PINCODE-HASH
    """
    # Create a unique string signature
    raw_str = f"{row['date']}-{row['pincode']}-{row['district']}-{row['state']}"
    # Simple hash suffix
    hash_suffix = hashlib.sha256(raw_str.encode()).hexdigest()[:6].upper()
    
    # Format date for readability if possible, else keep original
    # Assuming date is DD-MM-YYYY
    try:
        parts = row['date'].split('-')
        date_str = f"{parts[2]}{parts[1]}{parts[0]}"
    except:
        date_str = "00000000"
        
    return f"ADHR-{date_str}-{row['pincode']}-{hash_suffix}"

def process_data():
    print("Starting Data Processing...")
    
    # 1. Load Datasets
    print("\n--- Loading Enrolment Data ---")
    df_enrol = load_data(PATH_ENROLMENT, "enrol")
    
    print("\n--- Loading Demographic Data ---")
    df_demo = load_data(PATH_DEMOGRAPHIC, "demo")
    
    print("\n--- Loading Biometric Data ---")
    df_bio = load_data(PATH_BIOMETRIC, "bio")
    
    # 2. Merge Data
    # Keys for merging
    merge_keys = ['date', 'state', 'district', 'pincode']
    
    # Start with Enrolment as base (assuming it has the most comprehensive coverage)
    if df_enrol.empty:
        print("Critical Error: Enrolment data is empty. Cannot proceed.")
        return

    # Merge Enrolment + Demo
    if not df_demo.empty:
        df_merged = pd.merge(df_enrol, df_demo, on=merge_keys, how='outer', suffixes=('', '_demo'))
    else:
        df_merged = df_enrol

    # Merge + Bio
    if not df_bio.empty:
        df_merged = pd.merge(df_merged, df_bio, on=merge_keys, how='outer', suffixes=('', '_bio'))
        
    # Fill NaNs with 0 for numerical columns
    num_cols = df_merged.select_dtypes(include=['number']).columns
    df_merged[num_cols] = df_merged[num_cols].fillna(0)
    
    # 3. Standardization
    # Ensure text columns are strings
    for col in merge_keys:
        df_merged[col] = df_merged[col].astype(str)

    # 4. Generate Unique Record IDs
    print("\nGenerating Unique Record IDs...")
    # We apply this to every row in the aggregated table
    df_merged['record_id'] = df_merged.apply(generate_record_id, axis=1)
    
    # 5. Save Processed Data
    print(f"\nSaving processed data to {OUTPUT_FILE}...")
    df_merged.to_csv(OUTPUT_FILE, index=False)
    print(f"Success! Saved {len(df_merged)} records.")
    
    # Print sample
    print("\nSample Record:")
    print(df_merged.iloc[0].to_dict())

if __name__ == "__main__":
    process_data()
