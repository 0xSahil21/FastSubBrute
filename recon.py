import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import sys
import uuid
import time
from itertools import islice

# --- Logic: Handle Arguments vs Prompt ---
if len(sys.argv) > 1:
    TARGET_DOMAIN = sys.argv[1].strip()
else:
    TARGET_DOMAIN = input("Enter target (e.g., example.com): ").strip()

if not TARGET_DOMAIN:
    print("[!] Error: No domain provided."); sys.exit(1)

# Configuration
WORDLIST_PATH = "/home/kali/hacktify_ai/best-dns-wordlist.txt"
THREADS = 75       # Safe for 8GB RAM to prevent "zsh: killed".
CHUNK_SIZE = 10000 # Memory-safe chunking.
OUTPUT_FILE = f"found_{TARGET_DOMAIN}.txt"
MAX_DISPLAY = 25   # Updated to show top 25 results in terminal.

# Resolver Setup
custom_resolver = dns.resolver.Resolver()
custom_resolver.nameservers = ['1.1.1.1', '1.0.0.1'] # Using Cloudflare.
custom_resolver.timeout = 1.0 
custom_resolver.lifetime = 1.0

def get_wildcard_ip():
    """Checks for Wildcard DNS to avoid millions of false positives."""
    random_sub = f"{uuid.uuid4().hex}.{TARGET_DOMAIN}"
    try:
        answers = custom_resolver.resolve(random_sub, 'A')
        return set([str(rdata) for rdata in answers])
    except: return None

def check_subdomain(sub, wildcard_ips):
    full_domain = f"{sub.strip()}.{TARGET_DOMAIN}"
    try:
        answers = custom_resolver.resolve(full_domain, 'A')
        current_ips = [str(rdata) for rdata in answers]
        if wildcard_ips and set(current_ips).issubset(wildcard_ips):
            return None
        return full_domain
    except: return None

def main():
    print(f"[*] Target: {TARGET_DOMAIN}")
    wildcard_ips = get_wildcard_ip()
    if wildcard_ips: print(f"[!] Wildcard detected at {wildcard_ips}")
    
    start_time = time.time()
    try:
        with open(WORDLIST_PATH, 'rb') as f:
            total_lines = sum(1 for _ in f)
    except FileNotFoundError:
        print("[!] Wordlist not found."); return

    found_count = 0
    display_count = 0
    
    # Using 'a' (append) mode so you don't overwrite previous results.
    with open(WORDLIST_PATH, 'r', encoding='latin-1') as f, open(OUTPUT_FILE, 'a') as out:
        pbar = tqdm(total=total_lines, unit="sub", desc="Scanning")
        while True:
            # islice prevents the "killed" error by chunking the file.
            lines = list(islice(f, CHUNK_SIZE))
            if not lines: break
            with ThreadPoolExecutor(max_workers=THREADS) as executor:
                futures = {executor.submit(check_subdomain, l.strip(), wildcard_ips): l for l in lines}
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        out.write(result + "\n")
                        found_count += 1
                        if display_count < MAX_DISPLAY:
                            tqdm.write(f"[+] Found: {result}")
                            display_count += 1
                    pbar.update(1)
        pbar.close()

    total_time = time.time() - start_time
    print(f"\n[*] Complete! Found {found_count} subs in {int(total_time/60)}m {int(total_time%60)}s")

if __name__ == "__main__":
    main()
