from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-15672.c61.us-east-1-3.ec2.redns.redis-cloud.com",
    port="15672",
    decode_responses=True,
    username="default",
    password="y4bQfR2CzuEufOXkStrznjjx9sSxLGuz",
)

class Product(HashModel):
    name: str
    price: float
    quantity: int
    
    class Meta:
        database = redis

@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)
    
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.post('/products')
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get(pk: str):
    product = Product.get(pk)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete('/products/{pk}')
def delete(pk: str):
    product = Product.get(pk)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.delete(pk) 