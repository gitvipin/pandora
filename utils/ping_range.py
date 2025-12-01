'''
Network IP Reachability Scanner

This module provides a simple utility for scanning a range of IP addresses on a
local network to determine which hosts are reachable. This is useful in cases
where devices may obtain new IP addresses (e.g., via DHCP) and you need to
locate a machine before initiating a remote connection.

Features:
- Accepts optional --start and --end IP range parameters via the command line.
- Defaults to scanning 10.0.0.1 through 10.0.0.50.
- Prints only the reachable IP addresses.
- Saves all reachable IPs to 'reachable_ips.txt'.

USAGE : 

python3 ping_range.py

python3 ping_range.py --start 10.0.0.5 --end 10.0.0.20

python3 ping_range.py --start 192.168.1.1 --end 192.168.1.100
'''
import argparse
import subprocess
import ipaddress

def ping(ip: str) -> bool:
    """Ping an IP once and return True if reachable."""
    result = subprocess.run(
        ["ping", "-c", "1", "-W", "1", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description="Check reachable IP addresses in a range.")
    parser.add_argument("--start", default="10.0.0.1", help="Start IP address")
    parser.add_argument("--end", default="10.0.0.50", help="End IP address")

    args = parser.parse_args()

    start_ip = ipaddress.IPv4Address(args.start)
    end_ip = ipaddress.IPv4Address(args.end)

    if start_ip > end_ip:
        print("Error: Start IP must be less than or equal to end IP.")
        return

    output_file = "reachable_ips.txt"
    reachable = []

    for ip_int in range(int(start_ip), int(end_ip) + 1):
        ip = str(ipaddress.IPv4Address(ip_int))
        if ping(ip):
            print(f"{ip} is reachable")
            reachable.append(ip)

    with open(output_file, "w") as f:
        for ip in reachable:
            f.write(ip + "\n")

    print(f"\nReachable IPs saved to {output_file}")

if __name__ == "__main__":
    main()
