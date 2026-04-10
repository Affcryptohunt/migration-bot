from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from migrate import run_migration
from shopify_importer import import_products_to_shopify

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MigrationRequest(BaseModel):
    url: str


@app.post("/migrate")
def migrate_store(req: MigrationRequest):

    result = run_migration(req.url)

    return result


@app.post("/shopify-import")
def shopify_import(data: dict):

    products = data["products"]
    shop = data["shop"]
    token = data["token"]

    created = import_products_to_shopify(products, shop, token)

    return {"imported": created}