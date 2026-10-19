
#!/usr/bin/env python3

import subprocess
from datetime import datetime

ERROR_PATTERNS = [
    "failed password for",
    "authentication failure;",
    "login incorrect",
]


def main():
    print("=" * 50)
    print("       LINUX LOGIN MONITOR")
    print("=" * 50)
    print(f"Uruchomiono: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print("Źródło logów: systemd journal")
    print("Oczekiwanie na nowe wpisy... (Ctrl+C kończy pracę)")
    print()

    try:
        process = subprocess.Popen(
            ["journalctl", "-f", "-n", "0", "-o", "cat"],
            stdout=subprocess.PIPE,
            stderr=None,
            text=True,
            bufsize=1,
        )

        if process.stdout is None:
            print("Nie udało się odczytać dziennika systemowego.")
            return

        for line in process.stdout:
            lower_line = line.lower()

            if any(pattern in lower_line for pattern in ERROR_PATTERNS):
                print(f"[!] Podejrzany wpis — {datetime.now():%H:%M:%S}")
                print(line.strip())
                print()

    except FileNotFoundError:
        print("Nie znaleziono polecenia journalctl.")
    except KeyboardInterrupt:
        print("\nMonitor zatrzymany.")
    finally:
        if "process" in locals():
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()


if __name__ == "__main__":
    main()
