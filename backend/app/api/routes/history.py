from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.db.models import ChatLog
router = APIRouter(prefix='/history', tags=['history'])
@router.get('')
def history(visitor_id: str = Query(...), limit: int = Query(50, ge=1, le=500), db: Session = Depends(get_db)):
    rows = (db.query(ChatLog).filter(ChatLog.visitor_id==visitor_id).order_by(ChatLog.created_at.asc()).limit(limit).all())
    return [{"role":r.role,"text":r.text,"at":str(r.created_at)} for r in rows]
@router.delete('')
def clear(visitor_id: str, db: Session = Depends(get_db)):
    db.query(ChatLog).filter(ChatLog.visitor_id==visitor_id).delete(); db.commit(); return {"status":"ok"}
