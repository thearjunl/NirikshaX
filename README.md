# NirikshaX - Digital Forensic Recovery & Investigation Tool

**NirikshaX** is a professional-grade command-line cybersecurity utility designed for Digital Forensics & Incident Response (DFIR). It provides a comprehensive suite of tools for filesystem analysis, file recovery, timeline generation, and artifact collection.

## Features

- **Filesystem Scanner**: Deep recursive scanning with magic byte validation (not just extensions).
- **Recovery Engine**: Automated identification and recovery of files.
- **Timeline Analysis**: Chronological reconstruction of file modifications and access.
- **Artifact Collection**: Extraction of browser history, recent files, and system metadata.
- **Suspicious File Detection**: Flags potential threats like double extensions and hidden executables.
- **Detailed Reporting**: Generates structured JSON reports for all activities.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/NirikshaX.git
   cd NirikshaX
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

NirikshaX helps investigators analyze a target directory or system.

### 1. Scan a Directory
Identify all files, including suspicious ones.
```bash
python nirikshax.py scan /path/to/target
```

### 2. Recover Files
Recover specific file types (e.g., images, documents) to the `output/recovered` directory.
```bash
python nirikshax.py recover /path/to/target --type jpg,png,pdf,docx
```

### 3. Generate Timeline
Create a temporal view of filesystem activity.
```bash
python nirikshax.py timeline /path/to/target
```

### 4. Collect Artifacts
Gather system artifacts, recent files, and browser history.
```bash
python nirikshax.py artifacts
```

## Authorized Use Only

> [!WARNING]
> **DISCLAIMER**: This tool is developed for educational and professional authorized digital forensic use only. The author is not responsible for any misuse or damage caused by this tool. Ensure you have proper authorization before scanning or recovering data from any system.

## License

MIT License
