from fastapi import APIRouter
router = APIRouter(prefix='/source', tags=['source'])
@router.get('')
def source():
    return {"repo":"prive/zip","note":"Contacte Basset pour l'accès Git."}
