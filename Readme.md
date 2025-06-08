# Monitoring and Logging API

This project includes a real-time License Plate Detection API built using FastAPI and YOLOv8. The API allows users to upload images and receive detection results with bounding boxes of license plates.
This repository contains instructions and scripts to set up monitoring and logging for a machine learning API, using Prometheus, Grafana, and Fluent Bit.

This project is a part of MLOps cource (CS317.P22), with members:
- Huynh La Viet Toan: 22521486
- Nguyen Truong Minh Khoa: 22520680
- Nguyen Thanh Luan: 22520826
- Luong Truong Thinh: 22521412
- Phan Phuoc Loc Ngoc: 22520960

## How It Works

- Upload an image via web interface or POST request
- Automatically detects license plates using YOLOv8 model
- Returns annotated image and detection details
- Lightweight UI for image testing
- Ready to deploy via Docker and Docker Compose

## Requirements

- Python 3.10+
- Dependencies: ultralytics (for YOLOv8)
- Docker
- FastAPI
- Prometheus
- Grafana
- Node Exporter
- Fluent Bit
- Alertmanager
- 
## Setup & Usage

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/HuynhToan2004/monitoring-and-logging-system.git
    cd monitoring-and-logging-system
    ```

2.  **Install Docker and Docker Compose:**

    Make sure Docker and Docker Compose are installed on your machine.

    - **Ubuntu:**
      ```bash
      sudo apt update
      sudo apt install docker.io docker-compose -y
      sudo systemctl enable docker
      sudo systemctl start docker
      ```

    - **macOS / Windows:**
      Download and install **Docker Desktop** from: https://www.docker.com/products/docker-desktop

    - Verify installations:
      ```bash
      docker --version
      docker compose version
      ```

3.  **Prepare Configuration Files:**

    Ensure the following files and directories are present in the project:
    
    - `monitoring/prometheus.yml`: Prometheus configuration with targets for your services.
    - `monitoring/grafana/provisioning/`: Configuration for dashboards and data sources.
    - `monitoring/fluent-bit.conf`: Log processing pipeline for Fluent Bit.
    - `monitoring/alert.rules.yml`: (optional) Alert rules for Prometheus + Alertmanager.
    
    You may modify them according to your needs.

4.  **Open Required Ports:**

    These services will run on the following default ports:

    | Service        | Port  |
    |----------------|-------|
    | Prometheus     | 9090  |
    | Node Exporter  | 9100  |
    | Grafana        | 3000  |
    | Fluent Bit     | 2020  |
    | Alertmanager   | 9093  |
    | FastAPI (app)  | 8070  |

    Make sure these ports are not in use.

5.  **Start All Services:**

    Run the following command in the root directory of the project:

    ```bash
    docker compose up -d
    ```

    This will start:
    
    - Prometheus (metrics collection)
    - Node Exporter (host metrics)
    - Grafana (dashboard visualization)
    - Fluent Bit (logs collector)
    - Alertmanager (optional alerts)
    - FastAPI service (monitored API)

6.  **Access the Services:**

    | Service       | URL                           |
    |---------------|-------------------------------|
    | FastAPI App   | http://localhost:8070         |
    | Prometheus    | http://localhost:9090         |
    | Grafana       | http://localhost:3000         |
    | Fluent Bit    | http://localhost:2020         |
    | Alertmanager  | http://localhost:9093         |

    - **Grafana login credentials** (default):
        - Username: `admin`
        - Password: `admin` (you should change this)

7.  **Import Grafana Dashboard (Optional):**

    Go to Grafana → Dashboards → Import and upload the provided JSON file (if available), or use the preconfigured provisioning if included.

---

Once everything is running, you can proceed to simulate traffic and test logging, metrics, and alerting functionality.
## 📺 Demo

### ✅ Normal Operation Monitoring
> This demo shows:
> - The fully configured dashboard (Prometheus + Grafana)
> - Simulated traffic requests sent to the FastAPI endpoint
> - Live dashboard updates (e.g., request rate, latency, resource usage)
> - Logs captured from both API and system level via Fluent Bit

![Normal Operation Demo](video_demo/failure_cases.gif)

---

### ⚠️ API Failure Simulation
> This demo illustrates:
> - Injected API errors (simulated using random failure in code)
> - Error logs captured and sent via Fluent Bit
> - Error rate reflected in the Grafana dashboard

![API Error Simulation](video_demo/failure_cases.gif)

## Collaborators
<a href="https://github.com/luanntd">
  <img src="https://github.com/luanntd.png?size=50" width="50" style="border-radius: 50%;" />
</a>
<a href="https://github.com/Khoa-Nguyen-Truong">
  <img src="https://github.com/Khoa-Nguyen-Truong.png?size=50" width="50" style="border-radius: 50%;" />
</a>
<a href="https://github.com/HuynhToan2004">
  <img src="https://github.com/HuynhToan2004.png?size=50" width="50" style="border-radius: 50%;" />
</a>
<a href="https://github.com/locngocphan12">
  <img src="https://github.com/locngocphan12.png?size=50" width="50" style="border-radius: 50%;" />
</a>
<a href="https://github.com/thinhlt04">
  <img src="https://github.com/thinhlt04.png?size=50" width="50" style="border-radius: 50%;" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>
