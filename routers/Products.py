from fastapi import APIRouter

#Create the router
router = APIRouter(prefix="/products",tags="Products", responses={404: {"message": "Not found"}})

products_list = ["1","2","3","4"]

@router.get("/")
async def get_products():
    return products_list