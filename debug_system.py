import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(name, url, params=None):
    print(f"\n--- Testing {name} ---")
    try:
        response = requests.get(url, params=params)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"Result Count: {len(data)}")
                if len(data) > 0:
                    print(f"Sample: {data[0]}")
                else:
                    print("Warning: Response list is empty")
            else:
                print(f"Result: {data}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

# 1. Test Key System Health
test_endpoint("Health Check", f"{BASE_URL}/")

# 2. Test Summary
test_endpoint("Summary Analytics", f"{BASE_URL}/analytics/summary")

# 3. Test Geo Stats (Aggregate)
test_endpoint("Geo Stats (All)", f"{BASE_URL}/analytics/geo")

# 4. Test Geo Stats (Specific State)
# We saw 'Uttar Pradesh' in previous outputs
test_endpoint("Geo Stats (Uttar Pradesh)", f"{BASE_URL}/analytics/geo", {"state": "Uttar Pradesh"})

# 5. Test Record Search
# Using a known pincode from the sample data logs
test_endpoint("Record Search (Pincode 273001)", f"{BASE_URL}/records", {"pincode": "273001"})
