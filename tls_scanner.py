import subprocess
import json
import sys
import re
import os

# PHASE 1: TARGET INPUT AND VALIDATION [cite: 309]
def validate_target(target):
    """Checks if the input is a valid IP or domain format."""
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    domain_pattern = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")
    return ip_pattern.match(target) or domain_pattern.match(target)

# PHASE 2: TLS ANALYSIS ENGINE [cite: 314]
def analyze_tls(target):
    """Performs the technical audit using Nmap[cite: 189, 315]."""
    print(f"[+] Analyzing: {target}...")
    nmap_cmd = ["nmap", "-sV", "-p", "443", "--script", "ssl-enum-ciphers,ssl-cert", target]
    
    try:
        # Manages timeouts and connection errors [cite: 312]
        result = subprocess.run(nmap_cmd, capture_output=True, text=True, timeout=300)
        output = result.stdout
        if "0 hosts up" in output or "filtered" in output:
            return {"target": target, "error": "Unreachable/Port 443 closed"}
        return {"target": target, "raw": output}
    except Exception as e:
        return {"target": target, "error": str(e)}

# PHASE 3: EVALUATION AND RECOMMENDATIONS ENGINE [cite: 329, 330]
def evaluate_risk(data):
    """Interprets findings and translates them into actionable intel."""
    if "error" in data: return data
    
    raw = data['raw']
    report = {
        "server": data['target'],
        "tls_versions": [],
        "findings": [],
        "severity": "LOW",
        "recommendations": []
    }

    # Identify enabled versions [cite: 316]
    for v in ["TLSv1.0", "TLSv1.1", "TLSv1.2", "TLSv1.3"]:
        if v in raw: report["tls_versions"].append(v)

    # Rule: Obsolete Protocols [cite: 317, 332]
    if any(v in report["tls_versions"] for v in ["TLSv1.0", "TLSv1.1"]):
        report["findings"].append("Obsolete protocols (TLS 1.0/1.1) enabled")
        report["recommendations"].append("Disable TLS 1.0/1.1 and restrict to TLS 1.2+ [cite: 333]")
        report["severity"] = "HIGH"

    # Rule: Insecure Configurations [cite: 318]
    if "WITH_NULL" in raw or "anon_WITH" in raw or "MD5" in raw:
        report["findings"].append("Insecure ciphers detected (NULL/Anonymous/MD5)")
        report["recommendations"].append("Enforce modern cipher suites (AES-GCM/CHACHA20)")
        report["severity"] = "HIGH"

    # Rule: Weak RSA [cite: 318]
    if "rsa 1024" in raw:
        report["findings"].append("Weak 1024-bit RSA Key")
        report["recommendations"].append("Upgrade to 2048-bit RSA or ECDSA certificate")
        if report["severity"] != "HIGH": report["severity"] = "MEDIUM"

    return report

# PHASE 4: RESULTS VISUALIZATION AND CONSOLIDATION [cite: 336]
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 tls_scanner.py <target_or_file.txt>")
        sys.exit(1)

    input_val = sys.argv[1]
    targets = []

    # Individual or Bulk Analysis [cite: 313]
    if os.path.isfile(input_val):
        with open(input_val, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
    else:
        targets = [input_val]

    all_results = []
    for t in targets:
        if validate_target(t):
            raw_data = analyze_tls(t)
            all_results.append(evaluate_risk(raw_data))
        else:
            print(f"[!] Invalid format: {t}")

    # Output: Structured File and Console [cite: 337, 353]
    with open("final_report.json", "w") as f:
        json.dump(all_results, f, indent=4)

    # Consolidated View [cite: 343]
    print("\n" + "="*60)
    print(f"{'SERVER':<25} | {'SEVERITY':<10} | {'TLS VERSIONS'}")
    print("-" * 60)
    for r in all_results:
        if "error" in r:
            print(f"{r['target']:<25} | ERROR: {r['error']}")
        else:
            versions = ", ".join(r['tls_versions'])
            print(f"{r['server']:<25} | {r['severity']:<10} | {versions}")
    print("="*60 + "\nReport saved to: final_report.json")

if __name__ == "__main__":
    main()