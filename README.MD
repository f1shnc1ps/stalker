# PHANTOM — Unified OSINT Intelligence Gatherer

![PHANTOM](https://img.shields.io/badge/PHANTOM-OSINT-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11+-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-black?style=flat-square)

Fast, parallel reconnaissance tool for comprehensive OSINT. Search 600+ platforms simultaneously. Gather intelligence on usernames, emails, phone numbers, and IP addresses from the command line.

## Features

✨ **Username Reconnaissance**
- Search 600+ social media, code, gaming, and community platforms
- Parallel scanning with configurable thread count
- Direct URL access or API data retrieval
- ~30 seconds for full 600+ platform sweep

🔍 **Email Intelligence**
- Have I Been Pwned (HIBP) breach history
- EmailRep reputation and fraud scoring
- SMTP validation and MX record checking
- Identify compromised accounts instantly

📱 **Phone Lookup**
- Format validation (US/International)
- Truecaller reverse lookup URLs
- Numverify integration
- Region detection

🌐 **IP Reconnaissance**
- Geolocation (ipinfo.io)
- Reputation scoring (AbuseIPDB)
- Tor exit node detection
- Reverse DNS lookup
- Shodan service discovery (with API key)

⚡ **Performance**
- Multi-threaded parallel scanning
- Configurable concurrency (1-50 threads)
- Built-in rate limiting
- Timeout handling and retries

📊 **Output**
- Colorized terminal output
- JSON export for all results
- Detailed reporting
- Structured data for automation

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/phantom.git
cd phantom

# Install dependencies
pip install -r requirements.txt

# Install as command-line tool
pip install -e .
```

### Quick Install

```bash
pip install phantom-osint
```

## Usage

### Username Search

```bash
# Search single username
phantom user targetuser

# With more threads for faster scan
phantom user targetuser --threads 20

# Export results
phantom user targetuser --export results.json

# Verbose output
phantom user targetuser --verbose
```

### Email Reconnaissance

```bash
# Check email in breaches
phantom email target@example.com

# Export results
phantom email target@example.com --export email_results.json
```

### Phone Lookup

```bash
# Validate and lookup phone
phantom phone +14155552671

# Export results
phantom phone +14155552671 --export phone_results.json
```

### IP Intelligence

```bash
# Full IP reconnaissance
phantom ipaddr 8.8.8.8

# With Shodan integration (requires API key)
phantom ipaddr 1.1.1.1 --shodan-key YOUR_KEY

# Export results
phantom ipaddr 8.8.8.8 --export ip_results.json
```

### Full Sweep

```bash
# Comprehensive OSINT on all fronts
phantom sweep targetuser --email target@example.com --phone +14155552671 --ip 1.1.1.1

# Export everything
phantom sweep targetuser --email target@example.com --export full_results.json

# With API keys
phantom sweep targetuser --shodan-key YOUR_KEY --export results.json
```

## Configuration

### Environment Variables

```bash
# Shodan API key (optional)
export SHODAN_API_KEY="your_key_here"

# AbuseIPDB API key (optional)
export ABUSEIPDB_API_KEY="your_key_here"
```

### Threads

Adjust concurrency for speed vs. rate-limit avoidance:

```bash
# Fast (more aggressive, may trigger rate limits)
phantom user target --threads 30

# Moderate (recommended)
phantom user target --threads 10

# Slow (respectful crawling)
phantom user target --threads 5
```

## Examples

### Reconnaissance on a Username

```bash
$ phantom user github_user --export scan.json

[*] =========================
[*] USERNAME RECONNAISSANCE
[*] =========================

[+] github: https://github.com/github_user
[+] twitter: https://twitter.com/github_user
[+] reddit: https://reddit.com/user/github_user
...
[*] Found on 45/600 platforms

[*] Exported to scan.json
```

### Email Breach Check

```bash
$ phantom email user@example.com

[*] =========================
[*] EMAIL RECONNAISSANCE
[*] =========================

[+] Email format valid
[-] Found in 2 breaches:
    • LinkedIn (2021)
    • MyFitnessPal (2018)

[*] EmailRep reputation: excellent
```

### IP Geolocation & Reputation

```bash
$ phantom ipaddr 1.1.1.1

[*] =========================
[*] IP RECONNAISSANCE
[*] =========================

[+] Valid IP address
[*] Location: Los Angeles, California, United States
[*] ISP: Cloudflare
[*] Timezone: America/Los_Angeles
[*] Coordinates: 34.0522,-118.2437
[*] Open ports: 53, 80, 443
```

## Performance Metrics

| Operation | Time | Details |
|-----------|------|---------|
| Username (10 threads) | ~30s | 600+ platforms |
| Username (20 threads) | ~15s | 600+ platforms |
| Email check | ~5s | HIBP + EmailRep |
| Phone validation | <1s | Format + URLs |
| IP reconnaissance | ~3s | Geo + reputation |
| Full sweep | ~45s | All checks combined |

## API Integrations

- **ipinfo.io** - Free geolocation (no key required)
- **Have I Been Pwned** - Breach history (free API)
- **EmailRep** - Email reputation (free)
- **AbuseIPDB** - IP reputation (requires key for full data)
- **Shodan** - Service discovery (requires paid key)
- **Tor Project** - Tor exit node list (public)
- **DNS** - Reverse lookups (local)

## Project Structure