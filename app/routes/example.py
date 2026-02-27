from fastapi import APIRouter,Depends

router=APIRouter(prefix='/example')

@router.get('/testdata',status_code=200)
def test():
    return ("Fastapi running successfully!")
