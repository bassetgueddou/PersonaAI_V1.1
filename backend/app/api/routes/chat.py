from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.db.models import ChatLog
from app.core.config import settings
from fastapi.responses import StreamingResponse
from openai import OpenAI
from pathlib import Path
router = APIRouter(prefix='/chat', tags=['chat'])
client = OpenAI(api_key=settings.openai_api_key)
class ChatIn(BaseModel):
    message: str
    visitor_id: str | None = None

def load_system_prompt() -> str:
    prompt = Path(__file__).resolve().parents[2] / 'prompts' / 'system.md'
    data = Path(__file__).resolve().parents[2] / 'data' / 'bassetData.json'
    return prompt.read_text(encoding='utf-8') + '\n' + data.read_text(encoding='utf-8')

@router.post('')
def chat(body: ChatIn, db: Session = Depends(get_db)):
    ctx = load_system_prompt()
    vid = body.visitor_id or 'anon'
    db.add(ChatLog(visitor_id=vid, role='user', text=body.message)); db.commit()
    try:
        resp = client.chat.completions.create(model=settings.model_name, messages=[{"role":"system","content":ctx},{"role":"user","content":body.message}], temperature=0.6)
        reply = resp.choices[0].message.content
    except Exception as e:
        raise HTTPException(502, f'OpenAI error: {e}')
    db.add(ChatLog(visitor_id=vid, role='assistant', text=reply)); db.commit()
    return {"reply": reply}

@router.post('/stream')
def chat_stream(body: ChatIn, db: Session = Depends(get_db)):
    ctx = load_system_prompt()
    vid = body.visitor_id or 'anon'
    db.add(ChatLog(visitor_id=vid, role='user', text=body.message)); db.commit()
    def gen():
        try:
            with client.chat.completions.stream(model=settings.model_name, messages=[{"role":"system","content":ctx},{"role":"user","content":body.message}], temperature=0.6) as stream:
                full = ''
                for event in stream:
                    if event.type == 'chunk':
                        delta = event.choices[0].delta.content or ''
                        full += delta
                        yield delta
                db.add(ChatLog(visitor_id=vid, role='assistant', text=full)); db.commit()
        except Exception as e:
            yield f'[ERROR] {e}'
    return StreamingResponse(gen(), media_type='text/plain')
