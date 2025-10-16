import pandas as pd

def generate_summary(results, filters):
    if len(results) == 0:
        return "No properties found."
    
    count = len(results)
    bhk = filters.get('bhk', '')
    city = filters.get('city', '').title()
    
    # get price range
    min_price = results['price'].astype(float).min()
    max_price = results['price'].astype(float).max()
    
    min_cr = min_price / 10000000
    max_cr = max_price / 10000000
    
    # simple summary
    if bhk and city:
        summary = f"Found {count} {bhk}BHK in {city}. "
    else:
        summary = f"Found {count} properties. "
    
    # add price range
    if max_cr >= 1:
        summary += f"Prices: Rs {min_cr:.1f} Cr - Rs {max_cr:.1f} Cr"
    else:
        min_l = min_price / 100000
        max_l = max_price / 100000
        summary += f"Prices: Rs {min_l:.0f}L - Rs {max_l:.0f}L"
    
    return summary
