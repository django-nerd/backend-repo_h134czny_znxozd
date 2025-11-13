import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CineCards API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "CineCards Backend is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/api/movies")
def get_movies():
    """Return a curated set of movie cards.
    This is static showcase data for the demo UI.
    """
    base = "https://image.tmdb.org/t/p/w780"
    # Curated popular/movie-like posters (public TMDB paths for demo purposes)
    movies = [
        {
            "id": 1,
            "title": "Dune: Part Two",
            "thumbnail": f"{base}/cDB2k7s4O5GNi2cwr6j2kacrTP2.jpg",
            "rating": 8.7,
            "description": "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.",
            "url": "https://www.youtube.com/watch?v=Way9Dexny3w"
        },
        {
            "id": 2,
            "title": "Spider‑Man: Across the Spider‑Verse",
            "thumbnail": f"{base}/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg",
            "rating": 8.4,
            "description": "Miles Morales catapults across the Multiverse, where he encounters a team of Spider‑People charged with protecting its very existence.",
            "url": "https://www.youtube.com/watch?v=cqGjhVJWtEg"
        },
        {
            "id": 3,
            "title": "The Batman",
            "thumbnail": f"{base}/74xTEgt7R36Fpooo50r9T25onhq.jpg",
            "rating": 7.8,
            "description": "Batman ventures into Gotham City's underworld when a sadistic killer leaves behind a trail of cryptic clues.",
            "url": "https://www.youtube.com/watch?v=mqqft2x_Aa4"
        },
        {
            "id": 4,
            "title": "Interstellar",
            "thumbnail": f"{base}/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
            "rating": 8.6,
            "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
            "url": "https://www.youtube.com/watch?v=zSWdZVtXT7E"
        },
        {
            "id": 5,
            "title": "Blade Runner 2049",
            "thumbnail": f"{base}/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg",
            "rating": 8.0,
            "description": "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard.",
            "url": "https://www.youtube.com/watch?v=gCcx85zbxz4"
        },
        {
            "id": 6,
            "title": "Inception",
            "thumbnail": f"{base}/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
            "rating": 8.8,
            "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.",
            "url": "https://www.youtube.com/watch?v=YoHD9XEInc0"
        },
    ]
    return {"results": movies}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
