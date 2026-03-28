# TLS AKINATOR v1.0
### Cryptographic Intelligence & Web Defense Suite  
**Universidad Nacional de Colombia - Tech Talent 2026**

TLS Akinator is a professional security auditing suite designed to automate the ingestion, analysis, and visualization of SSL/TLS configurations. It transforms raw network data into actionable intelligence, categorizing risks from **CRITICAL** to **INFO** based on modern cryptographic standards.

---

## 🏗️ System Architecture

The suite is composed of four high-performance modules:

1. **Orchestrator (`main.py`)**  
   A robust CLI interface with built-in state validation. It manages the execution flow and prevents process conflicts (e.g., locking analysis while the dashboard is active).

2. **Intelligence Engine (`engine.py`)**  
   An advanced wrapper for Nmap scripts that uses Regex to extract deep metadata, including Public Key specs, Certificate Expiration, and Protocol support.

3. **Command Center (`app.py`)**  
   A Streamlit-based web dashboard providing visual analytics, relative exposure bars, and key distribution charts.

4. **Executive Reporting (`report_gen.py`)**  
   A PDF generation engine that produces corporate-grade audit reports with automated remediation strategies.

---

## 🛠️ Installation & Environment Setup

Follow these steps to deploy the suite on a Linux-based system (Kali Linux recommended):

### 1. Repository Setup

Clone or move the project files to your workspace:

```bash
cd ~/Desktop/tls_akinator
```

### 2. Virtual Environment Configuration

It is highly recommended to use a virtual environment to manage dependencies and avoid system conflicts.

Create the environment:

```bash
python3 -m venv venv
```

Activate the environment:

```bash
source venv/bin/activate
```

### 3. Dependency Installation

Install the required Python libraries using the provided requirements file:

```bash
pip install -r requirements.txt
```

### 4. System Dependencies

Ensure your OS has the necessary binary tools and GUI support for the file explorer:

```bash
sudo apt update
```

```bash
sudo apt install nmap python3-tk -y
```

---

## 🚀 Operational Workflow

### Step 1: Data Ingestion (Analysis)

Launch the main orchestrator from your terminal:

```bash
python3 main.py
```

- **Option `[1]`: Individual Analysis** — Enter a single IP or domain for an immediate deep scan.
- **Option `[2]`: Batch Analysis** — Populate `targets.txt` (one host per line) to scan entire infrastructures automatically.

### Step 2: Visualizing Telemetry

Once the scan is complete, the `final_report.json` cache is generated, unlocking reporting options.

- **Option `[3]`: Launch the Web Dashboard** — Opens a browser tab with real-time analytics.

> ⚠️ **IMPORTANT:**  
> The terminal will enter **Server Mode**. All other options will be **BLOCKED**.  
> You must press `s` to stop the server before performing new scans or exiting the program.

### Step 3: Executive Export

- **Option `[4]`: Generate the Executive PDF** — A native file explorer will appear; select your desired destination and filename (e.g., `~/Desktop/Report.pdf`).

---

## 🛡️ Risk Assessment Logic

The engine evaluates findings based on the following security scale:

| Severity | Technical Finding | Security Impact |
|---|---|---|
| **CRITICAL** | NULL / Anonymous Ciphers | No Encryption: Data is transmitted in plaintext. High risk of total exposure. |
| **HIGH** | TLS 1.0/1.1 or MD5 Hashing | Broken Protocols: Vulnerable to modern Man-in-the-Middle (MitM) attacks. |
| **MEDIUM** | RSA 1024-bit or less | Weak Infrastructure: Prone to brute-force factorization by modern hardware. |
| **INFO** | Missing TLS 1.3 | Best Practice: Lacks the latest security enhancements and faster handshakes. |

---

## 🧹 Session Cleanup & Exit

- **Option `[q]`: Exit the system safely**

Before exiting, ensure the dashboard server is stopped.

Upon choosing `[q]`, the program performs an automatic cleanup of the `final_report.json` cache to ensure data privacy and a clean workspace for future audits.
