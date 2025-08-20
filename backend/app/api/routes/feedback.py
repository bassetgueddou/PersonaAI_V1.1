from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.db.models import Feedback
router = APIRouter(prefix='/feedback', tags=['feedback'])
class FeedbackIn(BaseModel):
    comment: str
@router.post('')
def feedback(body: FeedbackIn, db: Session = Depends(get_db)):
    db.add(Feedback(comment=body.comment)); db.commit()
    return {"status":"ok","message":"Merci pour votre retour 🙏"}
