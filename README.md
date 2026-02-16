# fastSubBrute 🛡️

A high-performance, memory-efficient subdomain brute-forcer written in Python. Designed to handle massive wordlists (9M+ entries) on resource-constrained systems like virtual machines.

## 🚀 Overview
`fastSubBrute` was developed to overcome the limitations of standard shell-based loops. By utilizing Python's `ThreadPoolExecutor` and optimized DNS resolution via Cloudflare (1.1.1.1), it provides professional-grade speed without crashing your system.

## ✨ Key Features
* **Multi-Threaded Execution**: Leverages concurrency to process hundreds of subdomains per second.
* **Memory-Safe Chunking**: Uses `itertools.islice` to process large wordlists in chunks, preventing OOM (Out of Memory) "Killed" errors on systems with limited RAM.
* **Direct DNS Resolution**: Uses the `dnspython` library to communicate directly with resolvers, reducing system process overhead.
* **Wildcard Detection**: Automatically identifies wildcard DNS records to prevent false positives.
* **Real-time Progress**: Integrated `tqdm` progress bar with Estimated Time of Completion (ETC).

## 🛠️ Installation

1. **Clone the repository**:
   git clone https://github.com/<your-username>/fastSubBrute.git
   cd fastSubBrute

2. **Install dependencies**:
   sudo apt update
   sudo apt install python3-dnspython python3-tqdm

## 📖 Usage

**Option A: Command Line Argument**
Run the script by providing the target domain as an argument:
python3 recon.py mitacsc.ac.in

**Option B: Interactive Prompt**
Alternatively, run the script and enter the domain when prompted:
python3 recon.py

## 📊 Performance
On an 8GB RAM Kali VM, the tool comfortably handles:
* **Thread Count**: 75 threads
* **Wordlist Size**: 9.5 million entries
* **Average Speed**: ~150+ resolutions per second

## 📝 License
This project is for educational and ethical security testing purposes only.
