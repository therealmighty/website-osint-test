from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="OSINT Backend API")

# --- CORS Configuration ---
# Allows your frontend HTML file (running locally) to connect to this server
origins = [
    "*", 
    # For security, later change "*" to the specific URL where your app is hosted
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------

@app.post("/search")
async def search_endpoint(payload: dict):
    """
    Handles the search query from the frontend.
    For now, this returns dummy data to test the UI formatting.
    """
    
    query = payload.get("query", "N/A")
    search_type = payload.get("type", "N/A")
    
    # Simulate a small delay for realistic searching (3 seconds)
    time.sleep(3) 
    
    # --- DUMMY RESPONSE DATA ---
    # This data will show up formatted beautifully in your new UI!
    if search_type == "username":
        return {
            "target": query,
            "scan_status": "COMPLETED",
            "hits": [
                {"platform": "Twitter", "status": "FOUND", "link": f"https://twitter.com/{query}"},
                {"platform": "Instagram", "status": "NOT FOUND", "link": None},
                {"platform": "GitHub", "status": "FOUND", "link": f"https://github.com/{query}"},
                {"platform": "EmailLeak", "status": "CONFIRMED BREACH", "source": "2018 leak"}
            ],
            "summary": f"Search for username '{query}' completed across 8 sources."
        }
    
    # You can add more complex logic here later, e.g., calling OSINT APIs
    return {"status": "SUCCESS", "type": search_type, "query_received": query}

# Helper endpoint (optional)
@app.get("/")
def home():
    return {"message": "OSINT Backend is running successfully!"}
