from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from migrate import run_migration
from shopify_importer import import_products_to_shopify
from redis_queue import q
from worker_jobs import run_scrape_job
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
def start_scrape(data: dict):

    url = data["url"]

    # Step 1: discover links
    from site_crawler import crawl_site
    from product_detector import is_product_page

    all_links = crawl_site(url)

    product_links = [l for l in all_links if is_product_page(l)]

    # Step 2: enqueue job
    job = q.enqueue(run_scrape_job, product_links)

    return {"job_id": job.get_id()}


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