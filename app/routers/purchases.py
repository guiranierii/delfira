from fastapi import HTTPException, HTTPException, Query, Request, APIRouter
from datetime import date
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.services.dremio_connection import dremio_query


router=APIRouter()
limiter = Limiter(key_func=get_remote_address)

def purchases_query(order_id: int = None,
                 limit: int = 10,
                 offset: int = 0,
                 purchased_at: date = None,
                 id: int = None,
                 product_id: str = None,
                 user_id: int = None
):
    base_query = "SELECT * FROM lakehouse.faker WHERE 1=1"

    filters = []

    if order_id:
       filters.append(f"order_id = {order_id}")
    if purchased_at:
       filters.append(f"cast(purchased_at as date) = '{purchased_at}'")
    if id:
       filters.append(f"id = {id}")
    if product_id:
       filters.append(f"product_id = '{product_id}'")
    if user_id:
       filters.append(f"user_id = {user_id}")

    if filters:
        base_query += " AND " + " AND ".join(filters)

    base_query += f" LIMIT {limit} OFFSET {offset}"

    return base_query

# Fazer o get no dremio
@router.get("/purchases")
@limiter.limit("100/minute")
async def get_purchases(
    request: Request,
    order_id: int = Query(None),
    purchased_at: date = Query(None),
    id: int = Query(None),
    product_id: str = Query(None),
    user_id: int = Query(None),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    try:
        query = purchases_query(order_id, limit, offset, purchased_at, id, product_id, user_id)

        df = dremio_query(query)
        if df.is_empty():
            raise HTTPException(status_code=404, detail="Erroou")
        
        # Criar Json
        result = df.to_pandas().to_dict(orient="records")
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    