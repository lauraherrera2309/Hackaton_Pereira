# TLS AKINATOR v1.0
### Cryptographic Intelligence & Web Defense Suite
**Universidad Nacional de Colombia - Tech Talent 2026**

TLS Akinator is a professional security auditing suite designed to automate the ingestion, analysis, and visualization of SSL/TLS configurations. It transforms raw network data into actionable intelligence, categorizing risks from **CRITICAL** to **INFO** based on modern cryptographic standards.

---

## 🏗️ System Architecture

The suite is composed of four high-performance modules:

1.  **Orchestrator (`main.py`)**: A robust CLI interface with built-in state validation. It manages the execution flow and prevents process conflicts (e.g., locking analysis while the dashboard is active).
2.  **Intelligence Engine (`engine.py`)**: An advanced wrapper for Nmap scripts that uses Regex to extract deep metadata, including Public Key specs, Certificate Expiration, and Protocol support.
3.  **Command Center (`app.py`)**: A Streamlit-based web dashboard providing visual analytics, relative exposure bars, and key distribution charts.
4.  **Executive Reporting (`report_gen.py`)**: A PDF generation engine that produces corporate-grade audit reports with automated remediation strategies.

---

## 🛠️ Installation & Environment Setup

Follow these steps to deploy the suite on a Linux-based system (Kali Linux recommended):

### 1. Repository Setup
Clone or move the project files to your workspace:
```bash
cd ~/Desktop/tls_akinator
