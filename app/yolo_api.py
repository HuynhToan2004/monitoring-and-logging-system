from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import numpy as np, cv2, io, time, torch, logging, contextlib
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator
from pathlib import Path
import random
# ────────────────────────────────────────────
app = FastAPI()
Instrumentator().instrument(app).expose(app)        # /metrics

# ────────────────────────────────────────────

REQUEST_TOTAL   = Counter("api_requests_total",      "Tổng request")
REQUEST_ERRORS  = Counter("api_request_errors_total","Tổng lỗi")
INFER_SEC       = Histogram("inference_seconds",     "CPU inference time")
GPU_INFER_SEC   = Histogram("inference_gpu_seconds", "GPU inference time",
                            buckets=(.001,.005,.01,.05,.1,.5,1,2))
CONFIDENCE_HIST = Histogram("predict_confidence",    "Độ tin cậy model")

# ────────────────────────────────────────────

model = YOLO("best_model.pt")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()        
    ],
)
log = logging.getLogger(__name__)
log.info("App started")

# ────────────────────────────────────────────

def draw_boxes(img: np.ndarray, res) -> np.ndarray:
    for box in res.boxes:
        x1,y1,x2,y2 = map(int, box.xyxy[0].tolist())
        conf        = float(box.conf[0]); cls = int(box.cls[0])
        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.putText(img, f"{model.names[cls]} {conf:.2f}", (x1,y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
    return img

# ────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def home():
    return (Path("static/index.html").read_text(encoding="utf-8"))
# docker-compose logs -f fluent-bit | grep error
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    REQUEST_TOTAL.inc()

    # if random.random() < 0.5:
    #     log.error("Fake error triggered!")
    #     raise Exception("Simulated prediction failure")
    try:
        contents = await file.read()
        image    = cv2.imdecode(np.frombuffer(contents,np.uint8), cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("File không phải ảnh hợp lệ")

      
        cpu_start = time.perf_counter()
        if torch.cuda.is_available():
            torch.cuda.synchronize(); gpu_start = time.perf_counter()

        results = model.predict(image, save=False)[0]

        if torch.cuda.is_available():
            torch.cuda.synchronize()
            GPU_INFER_SEC.observe(time.perf_counter() - gpu_start)

        INFER_SEC.observe(time.perf_counter() - cpu_start)
        # ---------------------------------------

        # metric confidence
        if results.boxes.conf.numel():
            CONFIDENCE_HIST.observe(float(results.boxes.conf[0]))

        # vẽ & trả ảnh
        out = draw_boxes(image, results)
        _, buf = cv2.imencode(".jpg", out)
        return StreamingResponse(io.BytesIO(buf.tobytes()), media_type="image/jpeg")

    except Exception as e:
        REQUEST_ERRORS.inc()
        log.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=str(e)) from e

