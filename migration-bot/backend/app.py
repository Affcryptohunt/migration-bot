from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.migrate import run_migration
from backend.shopify_importer import import_products_to_shopify
from backend.redis_queue import q
from backend.worker_jobs import run_scrape_job
from rq.job import Job
import redis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_conn = redis.Redis()

class MigrationRequest(BaseModel):
    url: str


@app.post("/migrate")
def migrate_store(req: MigrationRequest):

    result = run_migration(req.url)

    return result


@app.post("/scrape")
def scrape(data: dict):

    url = data["url"]

    from backend.site_crawler import crawl_site
    from backend.product_detector import is_product_page
    from backend.migrate import scrape_product
    from concurrent.futures import ThreadPoolExecutor, as_completed

    all_links = crawl_site(url)

    product_links = [l for l in all_links if is_product_page(l)]

    products = []

    with ThreadPoolExecutor(max_workers=5) as executor:

        futures = [executor.submit(scrape_product, link) for link in product_links]

        for future in as_completed(futures):
            p = future.result()
            if p:
                products.append(p)

    return {
        "products": products[:20],
        "count": len(products)
    }


@app.get("/status/{job_id}")
def get_status(job_id: str):

    job = Job.fetch(job_id, connection=redis_conn)

    if job.is_finished:
        return {
            "status": "finished",
            "result": job.result
        }

    return {"status": "processing"}


@app.post("/shopify-import")
def shopify_import(data: dict):

    products = data["products"]
    shop = data["shop"]
    token = data["token"]

    created = import_products_to_shopify(products, shop, token)

    return {"imported": created}