import re

def parse_query(query):
    # extract filters from query using regex
    query_lower = query.lower()
    filters = {}
    
    # TODO: add more cities (bangalore, delhi, etc)
    # get city
    cities = ['pune', 'mumbai', 'chembur', 'kharadi', 'wakad', 'baner', 'ravet']
    for city in cities:
        if city in query_lower:
            filters['city'] = city
            break
    
    # get BHK
    bhk_patterns = [
        r'(\d+)\s*bhk',
        r'(\d+)\s*bedroom',
        r'(\d+)bhk',
        r'(\d+\.?\d*)\s*bhk'
    ]
    for pattern in bhk_patterns:
        match = re.search(pattern, query_lower)
        if match:
            filters['bhk'] = match.group(1)
            break
    
    # get budget - handles Cr and Lakhs
    # tried using NLP but regex works fine for now
    cr_patterns = [
        r'under\s*₹?\s*(\d+\.?\d*)\s*cr',
        r'below\s*₹?\s*(\d+\.?\d*)\s*cr',
        r'less than\s*₹?\s*(\d+\.?\d*)\s*cr',
        r'₹?\s*(\d+\.?\d*)\s*cr',
        r'(\d+\.?\d*)\s*crore'
    ]
    
    for pattern in cr_patterns:
        match = re.search(pattern, query_lower)
        if match:
            filters['max_budget'] = float(match.group(1)) * 10000000  # Convert to actual value
            break
    
    # Pattern for Lakhs
    if 'max_budget' not in filters:
        lakh_patterns = [
            r'under\s*₹?\s*(\d+\.?\d*)\s*l',
            r'below\s*₹?\s*(\d+\.?\d*)\s*l',
            r'₹?\s*(\d+\.?\d*)\s*lakh',
            r'(\d+\.?\d*)\s*lakh'
        ]
        for pattern in lakh_patterns:
            match = re.search(pattern, query_lower)
            if match:
                filters['max_budget'] = float(match.group(1)) * 100000
                break
    
    # get status
    if any(word in query_lower for word in ['ready', 'ready to move', 'ready-to-move']):
        filters['status'] = 'READY_TO_MOVE'
    elif any(word in query_lower for word in ['under construction', 'upcoming']):
        filters['status'] = 'UNDER_CONSTRUCTION'
    
    # TODO: add fuzzy matching for typos
    # get locality
    localities = ['wakad', 'baner', 'kharadi', 'ravet', 'chembur', 'mulund', 'thane', 
                  'andheri', 'ghatkopar', 'shivajinagar', 'camp', 'mundhwa']
    for locality in localities:
        if locality in query_lower:
            filters['locality'] = locality
            break
    
    return filters
