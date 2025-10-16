import pandas as pd

def search_properties(df, filters):
    # filter data based on what user asked
    result = df.copy()
    
    # filter by city
    if 'city' in filters:
        city = filters['city']
        # Check in fullAddress or cityId
        result = result[
            result['fullAddress'].str.lower().str.contains(city, na=False) |
            result['cityId'].astype(str).str.lower().str.contains(city, na=False)
        ]
    
    # filter by BHK
    if 'bhk' in filters:
        bhk = filters['bhk']
        result = result[result['type'].str.contains(bhk, na=False, case=False)]
    
    # filter by budget
    if 'max_budget' in filters:
        max_budget = filters['max_budget']
        budget_filtered = result[pd.to_numeric(result['price'], errors='coerce') <= max_budget]
        if len(budget_filtered) > 0:
            result = budget_filtered
        else:
            result = result.sort_values('price', ascending=True)
    
    # filter by status
    if 'status' in filters:
        status = filters['status']
        status_filtered = result[result['status'] == status]
        if len(status_filtered) > 0:
            result = status_filtered
        # else show all statuses
    
    # filter by locality
    if 'locality' in filters:
        locality = filters['locality']
        result = result[
            result['fullAddress'].str.lower().str.contains(locality, na=False) |
            result['landmark'].str.lower().str.contains(locality, na=False)
        ]
    
    # remove duplicates
    result = result.drop_duplicates(subset=['projectName', 'type'])
    result = result.head(10)
    
    return result
