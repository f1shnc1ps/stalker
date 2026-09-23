# PHANTOM

**PHANTOM** is a command-line OSINT research helper for checking publicly available signals associated with usernames, email addresses, phone numbers, and IP addresses. It can print results in the terminal and export structured JSON for later review.

> **Use responsibly.** Only investigate yourself, people who have given you permission, or information you are otherwise authorized to access. Respect each service’s terms, robots rules, privacy laws, and rate limits. A match is a lead—not proof that two accounts belong to the same person.

## What it does

- **Username checks:** checks a username against the site patterns in `phantom/databases/sites.py`.
- **Email checks:** validates an email and runs the checks implemented by the email module.
- **Phone checks:** validates and normalizes a phone number and provides lookup links.
- **IP checks:** validates an IP and gathers the geolocation, DNS, reputation, Tor, and optional Shodan data supported by the project.
- **Combined sweeps:** runs several of the above checks and writes one JSON document.
- **JSON export:** every scan command supports `--export PATH`.

The project is a research utility, not a guarantee of identity, account ownership, breach status, geolocation accuracy, or current service availability. Public websites can change their URL formats and anti-bot behavior at any time.

## Requirements

- Python **3.11 or newer**
- Internet access for network-backed checks
- Optional API keys for providers that require them

## Download the repository

### Option 1: Git (recommended)

```bash
git clone https://github.com/f1shnc1ps/stalker.git
cd stalker
```

### Option 2: Download a ZIP

1. Open <https://github.com/f1shnc1ps/stalker>.
2. Select **Code** → **Download ZIP**.
3. Extract the ZIP file and open a terminal in the extracted `stalker` folder.

## Install

Using a virtual environment keeps PHANTOM’s dependencies separate from the rest of your system:

```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

Check that the CLI is installed:

```bash
phantom --help
phantom version
```

If your shell cannot find `phantom`, run it without installing the editable command entry point:

```bash
python -m phantom.cli --help
```

## Usage

### Username

```bash
phantom user USERNAME
phantom user USERNAME --threads 5 --export username-results.json
```

Use a modest thread count when researching services you do not control. The `--verbose` flag is also available for the username command.

### Email

```bash
phantom email person@example.com
phantom email person@example.com --export email-results.json
```

### Phone

```bash
phantom phone +14155552671
phantom phone +14155552671 --export phone-results.json
```

### IP address

```bash
phantom ipaddr 8.8.8.8
phantom ipaddr 8.8.8.8 --export ip-results.json
```

### Combined sweep

The `target` argument is used as the username input. Add the other identifiers only when you are authorized to check them:

```bash
phantom sweep USERNAME \\
  --email person@example.com \\
  --phone +14155552671 \\
  --ip 8.8.8.8 \\
  --threads 5 \\
  --export sweep-results.json
```

Run `phantom COMMAND --help` for the current options for any command.

## Optional API keys

Some providers may require credentials. Do not commit keys to this repository or place them in result files.

```bash
export SHODAN_API_KEY="your-key"
export ABUSEIPDB_API_KEY="your-key"
```

You can also pass the Shodan key for one command:

```bash
phantom ipaddr 8.8.8.8 --shodan-key "$SHODAN_API_KEY"
```

## Project layout

```text
phantom/
├── cli.py                     # Click command-line interface
├── config/config.yaml         # Runtime configuration
├── databases/sites.py         # Username site definitions
├── reconnaissance/            # Username, email, phone, and IP scanners
└── utils/                     # API, validation, and terminal helpers
setup.py                       # Package metadata and phantom entry point
requirements.txt               # Runtime dependencies
```

## Development checks

```bash
python -m compileall -q phantom
python setup.py --name --version
phantom --help
phantom version
```

## Limitations

Results depend on third-party services, network connectivity, public data quality, and the site definitions shipped with this repository. A site returning HTTP 200 does not always mean a username exists, and a failed request does not prove that it does not. Treat exported JSON as potentially sensitive and store it securely.

## License

This project is released under the [MIT License](LICENSE).
