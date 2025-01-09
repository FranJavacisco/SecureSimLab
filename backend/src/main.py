from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .ransomware_simulator import RansomwareSimulator
from .system_monitor import SystemMonitor

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL del frontend (Vite)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instanciar las clases
simulator = RansomwareSimulator("./data/test_files", "./data/backup_files")
monitor = SystemMonitor()

@app.post("/api/simulation/start")
async def start_simulation():
    simulator.start_simulation()
    monitor.start_monitoring()
    return {"status": "started"}

@app.post("/api/simulation/stop")
async def stop_simulation():
    simulator.stop_simulation()
    monitor.stop_monitoring()
    return {"status": "stopped"}

@app.get("/api/metrics")
async def get_metrics():
    metrics = monitor.collect_metrics()
    return metrics

@app.post("/api/report/generate")
async def generate_report():
    report = monitor.generate_report()
    return report

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)