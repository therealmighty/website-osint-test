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

    elif search_type == "discord_id":
        # Simulate resolving a Discord User ID to public information
        return {
            "target": query,
            "scan_status": "DISCORD_ID_RESOLVED",
            "resolution": {
                "user_tag": f"User_{query[:4]}#0000",
                "creation_date": "2018-05-15",
                "verified_email": "YES" if len(query) % 2 == 0 else "NO"
            },
            "hits": [
                {"source": "UsernameDB", "link": f"https://usernamedb.com/id/{query}", "status": "Indexed"},
                {"source": "PublicServers", "count": 12, "note": "12 shared public server groups found"}
            ],
            "note": f"Discord IDs are unique and often yield quick resolution of related public data."
        }

    elif search_type == "discord_name":
        # Simulate enumerating accounts tied to a non-unique display name
        return {
            "target": query,
            "scan_status": "DISCORD_NAME_ENUMERATION",
            "potential_matches": [
                {"id": "19401945", "tag": f"{query}#1940", "activity": "High"},
                {"id": "78320194", "tag": f"{query}#7832", "activity": "Low"}
            ],
            "warning": "Discord names are not unique. Multiple results are common. Requires further filtering."
        }

    elif search_type == "email":
        # Simulate an email breach search
        return {
            "target": query,
            "scan_status": "CONFIRMED_BREACHES",
            "breach_hits": [
                {"source": "Collection #1", "date": "2019-01-16", "data_types": ["Passwords (Hashed)", "Usernames"]},
                {"source": "Private Leak", "date": "2020-05-01", "data_types": ["Names", "Phone Numbers"]}
            ],
            "summary": f"Email address '{query}' found in 2 public data breaches."
        }
    
    elif search_type == "ip":
        # Simulate a network reconnaissance search
        return {
            "target": query,
            "scan_status": "NET_RECON_COMPLETE",
            "geolocation": {"country": "US", "city": "Ashburn", "isp": "Cloudflare"},
            "open_ports": [80, 443, 22],
            "domains_hosted": ["example.com", "testsite.net"],
            "note": "IP data may be obfuscated by VPNs or proxy services."
        }

    # Fallback if module type is unknown
    return {"status": "ERROR", "message": f"Unknown module type received: {search_type}. Please select a valid module."}

# Helper endpoint (optional)
@app.get("/")
def home():
    return {"message": "OSINT Backend is running successfully!"}
