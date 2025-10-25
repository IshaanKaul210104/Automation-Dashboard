from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json, os, datetime, importlib

app = FastAPI(title="Automation Dashboard API")

# Enable CORS (for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config (optional)
if os.path.exists("config/config.json"):
    with open("config/config.json", "r") as f:
        CONFIG = json.load(f)
else:
    CONFIG = {}

@app.get("/")
def read_root():
    return {"message": "Automation Dashboard Backend Running"}

@app.post("/run/{script_name}")
async def run_script(script_name: str, request: Request):
    """
    Dynamically runs scripts like 'webscraper.py' under /scripts folder.
    Accepts optional JSON body (e.g., {'url': 'https://example.com'}).
    """
    body = await request.json()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs("logs", exist_ok=True)

    try:
        try:
            script_module = importlib.import_module(f"scripts.{script_name}")
        except ModuleNotFoundError:
            # fallback alias: if 'scraper' was sent, try 'webscraper'
            if script_name == "scraper":
                script_module = importlib.import_module("scripts.webscraper")
            else:
                raise

        # ✅ Ensure URL is valid or fallback to default
        url = body.get("url", "").strip() or "https://www.theverge.com"
        params = body if isinstance(body, dict) else {}

        # Run script (with both URL and timestamp for flexibility)
        if hasattr(script_module, "run"):
            result = script_module.run(params, timestamp)
        elif hasattr(script_module, "run_web_scraper"):
            result = script_module.run_web_scraper(url)
        else:
            raise Exception(f"No valid entry point found in {script_name}.py")

        # Write logs
        log_file = f"logs/{script_name}_{timestamp}.log"
        with open(log_file, "w") as log:
            log.write(f"{script_name} ran successfully at {timestamp}\n{json.dumps(result, indent=2)}")

        return {"status": "success", "log": log_file, "output": result}

    except Exception as e:
        log_file = f"logs/{script_name}_{timestamp}.log"
        with open(log_file, "w") as log:
            log.write(f"{script_name} failed at {timestamp}\n{str(e)}")
        return {"status": "failed", "log": log_file, "error": str(e)}