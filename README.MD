# 📡 NetScan — Network Discovery Scanner

![Version](https://img.shields.io/badge/version-1.0-00ffe5?style=flat-square)
![Python](https://img.shields.io/badge/python-3.7+-00aaff?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-ff3c6e?style=flat-square)

NetScan is a fast, parallel network scanner that discovers online hosts on a local or remote network using ICMP ping. It comes with both a **CLI tool** (`netscan.py`) and a **dark-themed web frontend** (`netscan.html`).

---

## 🗂 Project Structure

```
netscan/
├── netscan.py        ← Core scanner (CLI)
├── api.py            ← Flask API backend (you create this — see below)
└── netscan.html      ← Web frontend (dark theme UI)
```

---

## ⚙️ Features

| Feature | CLI | Web UI |
|---|---|---|
| Auto-detect local network | ✅ | ✅ |
| Custom CIDR input | ✅ | ✅ |
| Parallel scanning (100 threads) | ✅ | ✅ (via backend) |
| Live terminal log | — | ✅ |
| Online host count + stats | ✅ | ✅ |
| Export results to TXT | — | ✅ |
| Copy IPs to clipboard | — | ✅ |
| Windows & Linux/macOS support | ✅ | ✅ |

---

## 🖥️ CLI Usage

```bash
# Scan your local network (auto-detect)
python netscan.py

# Scan a specific /24 network
python netscan.py 192.168.1.0/24

# Short form (expands to /24 automatically)
python netscan.py 192.168.1

# Show help
python netscan.py --help
```

### Accepted Input Formats

| Input | Interpreted As |
|---|---|
| *(none)* | Auto-detected local subnet |
| `192.168.1.0/24` | Exact CIDR |
| `192.168.1` | 192.168.1.0/24 |
| `192.168.1.5` | 192.168.1.5/24 |
| `10.0.0.0/8` | Full /8 block |

---

## 🌐 Web Frontend Setup

The web UI (`netscan.html`) runs entirely in the browser. In **demo mode**, it simulates a scan with random IPs so you can preview the interface without running any backend.

To connect it to your real `netscan.py` backend, follow the steps below.

---

## 🔌 Backend Integration — Step by Step

### Step 1 — Install dependencies

```bash
pip install flask flask-cors
```

### Step 2 — Create `api.py` (place next to `netscan.py`)

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from netscan import scan_network, parse_network

app = Flask(__name__)
CORS(app)  # Required so the browser can call this API

@app.route('/scan', methods=['POST'])
def scan():
    data   = request.get_json()
    target = data.get('network', '')
    try:
        network = parse_network(target if target else None)
        online  = scan_network(network)
        online.sort(key=lambda x: tuple(map(int, x.split('.'))))
        return jsonify({
            'network': str(network),
            'total':   network.num_addresses - 2,
            'online':  online,
            'count':   len(online)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### Step 3 — Start the backend

```bash
python api.py
# Output: * Running on http://0.0.0.0:5000
```

### Step 4 — Update `netscan.html` to use the real backend

Open `netscan.html` and find the `startScan()` function. Replace the simulation block with:

```javascript
const res = await fetch('http://localhost:5000/scan', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ network: target })
});
const data = await res.json();
if (data.error) throw new Error(data.error);
const { online: hosts, total, network: net } = data;
```

Comment out or delete the simulation block above it (`simulateScan(...)`).

### Step 5 — Open the frontend

Open `netscan.html` directly in your browser (double-click or `File → Open`).  
Make sure `api.py` is still running. Hit **Scan** and you're live. ✅

---

## 📁 Folder Layout (after setup)

```
netscan/
├── netscan.py       ← Original scanner
├── api.py           ← Flask server (you created)
└── netscan.html     ← Open this in your browser
```

---

## 🔒 Permissions & Notes

- **Linux/macOS**: `ping` may require root for some configurations.  
  Run as: `sudo python api.py`
- **Windows**: Run Command Prompt as Administrator if scan fails.
- **Firewall**: Hosts behind firewalls that block ICMP will appear offline even if they are online.
- **Large networks**: Scanning `/16` or `/8` ranges will take significantly longer. Use with care.

> ⚠️ **Legal notice:** Only scan networks you own or have explicit permission to scan. Unauthorized network scanning may be illegal in your jurisdiction.

