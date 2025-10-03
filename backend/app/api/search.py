from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

class SearchResult(BaseModel):
    title: str
    content: str
    url: str
    source_type: str
    relevance_score: float

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_results: int

@router.get("/", response_model=SearchResponse)
async def search_documents(
    q: str = Query(..., description="Search query"),
    source_type: Optional[str] = Query(None, description="Filter by source: 'vidal' or 'meddispar'"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results")
):
    """
    Search in the knowledge base (Vidal + Meddispar)
    """
    # Validate empty query first
    if not q or not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        results = await rag_service.search_documents(
            query=q,
            source_type=source_type,
            limit=limit
        )
        
        return SearchResponse(
            query=q,
            results=results,
            total_results=len(results)
        )
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}") from e

@router.get("/stats")
async def get_database_stats():
    """Get statistics about the indexed documents"""
    try:
        stats = await rag_service.get_stats()
        return stats
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}") from e
