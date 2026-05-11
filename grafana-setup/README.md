# Grafana Automation Monitoring Setup

This project provides a local environment to track and monitor automation test results (like `jbehave-surefire.xml`) using Grafana and InfluxDB.

## Architecture
- **Grafana**: Visualization platform (Port 3000).
- **InfluxDB 2.x**: Time-series database to store test outcomes (Port 8086).
- **Python Ingestor**: A script to parse JUnit-style XML results and push them to InfluxDB.

---

## 🚀 Quick Start

### 1. Start the Environment
Run the deployment script to pull and start the containers:
```bash
./grafana-setup/deploy.sh
```

### 2. Setup Python Ingestor
Ensure you have Python installed, then install the required library:
```bash
pip install -r grafana-setup/requirements.txt
```

### 3. Push Test Results
After your automation run finishes, push the results to the database:
```bash
python grafana-setup/push_results.py path/to/your/jbehave-surefire.xml

ython3 push_results.py /Users/sergio.gonzalez/workspace/messaging-integration-tests/integrationtests-robots/target/jbehave/view/jbehave-surefire.xml
```

---

## 📊 Grafana Configuration

The InfluxDB data source and the **Automation Results Dashboard** are **automatically configured** via provisioning.

1. Open **[http://localhost:3000](http://localhost:3000)** (User: `admin` | Pass: `admin`).
2. Navigate to **Dashboards**.
3. You will see the **"Automation Results Dashboard"** under the **Automation** folder.
4. (Optional) To verify the data source, check **Connections > Data Sources**. You will see `InfluxDB` already listed.

---

## 🛠 Management

### Stop and Clean Up
To stop the services and **delete all stored data**:
```bash
./grafana-setup/destroy.sh
```

### Credentials & Config
- **Grafana**: `admin` / `admin`
- **InfluxDB UI**: `admin` / `password123` (at http://localhost:8086)
- **InfluxDB Org**: `my-org`
- **InfluxDB Bucket**: `automation_results`

## Data Persistence
Data is stored in Docker volumes (`grafana-storage` and `influxdb-storage`). This means your data remains safe even if the containers are stopped or your computer restarts.
