from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Contractors API",
    description="API for accessing contractor insights and information",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Contractors API"}

@app.get("/contractors/insights")
async def get_contractors_insights(min_rating: Optional[float] = None, limit: Optional[int] = 10):
    """
    Get insights for contractors.
    Optional filters:
    - min_rating: Minimum rating threshold (e.g., 4.5)
    - limit: Maximum number of contractors to return
    """
    try:
        # Start building the query
        query = supabase.table('contractors').select('name, rating, insight')
        
        # Apply rating filter if provided
        if min_rating is not None:
            query = query.gte('rating', min_rating)
        
        # Execute query with limit
        result = query.limit(limit).execute()
        
        if not result.data:
            return {"message": "No contractors found", "insights": []}
            
        return {
            "message": "Successfully retrieved contractor insights",
            "insights": result.data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @app.get("/contractors/top-rated")
# async def get_top_rated_contractors(limit: Optional[int] = 5):
#     """
#     Get insights for top-rated contractors.
#     """
#     try:
#         result = supabase.table('contractors')\
#             .select('name, rating, insight')\
#             .order('rating', desc=True)\
#             .limit(limit)\
#             .execute()
            
#         if not result.data:
#             return {"message": "No contractors found", "contractors": []}
            
#         return {
#             "message": "Successfully retrieved top-rated contractors",
#             "contractors": result.data
#         }
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/contractors/search")
# async def search_contractors(
#     name: Optional[str] = None,
#     min_rating: Optional[float] = None,
#     service: Optional[str] = None,
#     limit: Optional[int] = 10
# ):
#     """
#     Search contractors with various filters.
#     """
#     try:
#         query = supabase.table('contractors').select('name, rating, services, insight')
        
#         if name:
#             query = query.ilike('name', f'%{name}%')
        
#         if min_rating is not None:
#             query = query.gte('rating', min_rating)
            
#         if service:
#             # Filter for contractors that have the specified service
#             query = query.contains('services', [service])
            
#         result = query.limit(limit).execute()
        
#         if not result.data:
#             return {"message": "No contractors found", "contractors": []}
            
#         return {
#             "message": "Successfully retrieved contractors",
#             "contractors": result.data
#         }
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 