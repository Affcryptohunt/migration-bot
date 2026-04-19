import os
import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response, HTMLResponse
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor, as_completed
from rq.job import Job

# ✅ Internal imports (safe)
from backend.migrate import run_migration, scrape_product
from backend.shopify_importer import import_products_to_shopify
from backend.site_crawler import crawl_site
from backend.product_detector import is_product_page
from backend.redis_queue import q, redis_conn
from backend.worker_jobs import run_scrape_job

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Absolute path handling (VERY IMPORTANT)
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "../frontend")

# ✅ Static files
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.middleware("http")
async def add_headers(request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Frame-Options"] = "ALLOWALL"
    return response

# =========================
# Models
# =========================
class MigrationRequest(BaseModel):
    url: str


# =========================
# Routes
# =========================
@app.get("/")
def home():
    return {"status": "NEW VERSION"}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    file_path = os.path.join(os.path.dirname(__file__), "../frontend/dashboard.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# =========================
# Core Features
# =========================
@app.post("/migrate")
def migrate_store(req: MigrationRequest):
    return run_migration(req.url)


@app.post("/scrape")
def scrape(data: dict):

    url = data["url"]

    job = q.enqueue(run_scrape_job, url)

    return {
        "job_id": job.id
    }


# =========================
# Async Job Queue (RQ)
# =========================
@app.post("/start-job")
def start_job(data: dict):
    url = data["url"]

    job = q.enqueue("backend.worker_jobs.run_scrape_job", url)

    return {"job_id": job.id}


@app.get("/status/{job_id}")
def get_status(job_id: str):

    job = Job.fetch(job_id, connection=redis_conn)

    if job.is_finished:
        return {
            "status": "finished",
            "result": job.result
        }

    if job.is_failed:
        return {"status": "failed"}

    return {"status": "processing"}


# =========================
# Shopify Import
# =========================
@app.post("/shopify-import")
def shopify_import(data: dict):
    products = data["products"]
    shop = data["shop"]
    token = data["token"]

    created = import_products_to_shopify(products, shop, token)

    return {"imported": created}