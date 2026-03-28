import subprocess
import re
import json

def evaluate_findings(raw_output, target):
    """
    Advanced Engine: Extracts protocols, key specs, and certificate metadata.
    """
    report = {
        "server": target,
        "tls_versions": [],
        "key_info": "Unknown",
        "cert_expiry": "Unknown",
        "severity": "LOW",
        "findings": [],
        "recommendations": []
    }

    if "0 hosts up" in raw_output or "filtered" in raw_output:
        return {"server": target, "severity": "UNKNOWN", "findings": ["Host unreachable"], "tls_versions": []}

    # Protocol Detection
    for v in ["TLSv1.0", "TLSv1.1", "TLSv1.2", "TLSv1.3"]:
        if v in raw_output: report["tls_versions"].append(v)
    
    # Advanced Metadata Extraction
    key_type = re.search(r"Public Key type: (\w+)", raw_output)
    key_bits = re.search(r"Public Key bits: (\d+)", raw_output)
    expiry = re.search(r"Not valid after:\s+(.*)", raw_output)
    
    if key_type and key_bits:
        report["key_info"] = f"{key_type.group(1)} {key_bits.group(1)}-bit"
    if expiry:
        report["cert_expiry"] = expiry.group(1).strip()

    # --- CRITICAL: NO ENCRYPTION ---
    if "WITH_NULL" in raw_output or "anon_WITH" in raw_output:
        report["severity"] = "CRITICAL"
        report["findings"].append("CRITICAL: NULL/Anonymous Ciphers enabled")
        report["recommendations"].append("Disable NULL and Anonymous suites to prevent plaintext exposure.")

    # --- HIGH: BROKEN PROTOCOLS & HASHING ---
    if any(v in report["tls_versions"] for v in ["TLSv1.0", "TLSv1.1"]):
        if report["severity"] != "CRITICAL": report["severity"] = "HIGH"
        report["findings"].append("HIGH: Deprecated TLS (1.0/1.1) in use")
        report["recommendations"].append("Upgrade to TLS 1.2+ and implement HSTS.")

    if "MD5" in raw_output:
        if report["severity"] not in ["CRITICAL"]: report["severity"] = "HIGH"
        report["findings"].append("HIGH: MD5 Hashing detected in suites")
        report["recommendations"].append("Migrate to SHA-256 for integrity checks.")

    # --- MEDIUM: WEAK INFRASTRUCTURE ---
    if key_bits and int(key_bits.group(1)) <= 1024:
        if report["severity"] not in ["CRITICAL", "HIGH"]: report["severity"] = "MEDIUM"
        report["findings"].append("MEDIUM: Weak RSA Key Strength (1024-bit)")
        report["recommendations"].append("Generate a new 2048-bit RSA or 256-bit ECDSA certificate.")

    if "TLSv1.3" not in report["tls_versions"]:
        report["findings"].append("INFO: TLS 1.3 Best Practice missing")
        report["recommendations"].append("Deploy TLS 1.3 to optimize security and handshake speed.")

    return report

def full_extraction_pipeline(target):
    cmd = ["nmap", "-sV", "-p", "443", "--script", "ssl-enum-ciphers,ssl-cert", target]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return evaluate_findings(result.stdout, target)
    except Exception as e:
        return {"server": target, "severity": "ERROR", "findings": [f"Execution error: {str(e)}"]}
