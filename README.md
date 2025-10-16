# NoBrokerage Property Search Chatbot

Chat-based property search using natural language instead of filters.

## What it does

Type "2BHK in Mumbai" and get matching properties with summary and cards.

## Tech Stack

- **Streamlit** - Chat UI (faster than React for prototype)
- **Pandas** - Data processing
- **Regex** - Query parsing (task suggested regex/rule-based instead of LLM APIs)

## Files

```
├── app.py                   # Main app
├── query_parser.py          # Extracts filters
├── search_engine.py         # Searches data
├── summary_generator.py     # Creates summaries
└── 4 CSV files             # Property data
```

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Try these

- 2BHK in Mumbai
- 3BHK in Pune under 2 Cr
- Properties in Chembur

## How it works

1. Parse query using regex to extract city, BHK, budget, status
2. Filter CSV data based on extracted parameters
3. Generate summary from actual results (no hallucinations)
4. Display property cards

## Design Choices

**Streamlit over React:** Faster development, Python-based, good for prototype

**Regex over LLM:** Task recommended regex/rule-based parsing. Works well for structured queries, no API costs

**CSV over Database:** Simple for prototype, easy to switch to PostgreSQL later

## What can be improved

**For production:**
- Add semantic search using embeddings for better query understanding
- Implement fuzzy matching for typos
- Add more cities and localities
- Include property images
- Add filters for amenities (gym, pool, parking)
- Implement user authentication and saved searches
- Add comparison feature
- Include EMI calculator

**Technical improvements:**
- Move to PostgreSQL for better performance
- Add caching layer (Redis)
- Implement API rate limiting
- Add analytics tracking

---

Built by Mahesh Vyas for NoBrokerage.com
