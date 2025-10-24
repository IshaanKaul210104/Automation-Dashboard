from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess, json, os, datetime

app = FastAPI(title="Automation Dashboard API")

# Enable CORS (for React frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config
with open("config/config.json", "r") as f:
    CONFIG = json.load(f)

# Simple test route
@app.get("/")
def read_root():
    return {"message": "Automation Dashboard Backend Running"}

@app.post("/run/{script_name}")
def run_script(script_name: str, body: dict = {}):  # <- changed 'params' to 'body'
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"logs/{script_name}_{timestamp}.log"

    # Create outputs/log folder if missing
    os.makedirs(f"outputs/{script_name}/{timestamp}", exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Dynamically import and run the script
    try:
        script_module = __import__(f"scripts.{script_name}", fromlist=["run"])
        # Use body directly as params
        params = body
        result = script_module.run(params, timestamp)
        log_file = f"logs/{script_name}_{timestamp}.log"
        with open(log_file, "w") as log:
            log.write(f"{script_name} ran successfully at {timestamp}\n{result}")
        return {"status": "success", "log": log_file, "output": result}
    except Exception as e:
        log_file = f"logs/{script_name}_{timestamp}.log"
        with open(log_file, "w") as log:
            log.write(f"{script_name} failed at {timestamp}\n{str(e)}")
        return {"status": "failed", "log": log_file, "error": str(e)}