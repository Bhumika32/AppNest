from fastapi import APIRouter

main_router = APIRouter()

@main_router.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
