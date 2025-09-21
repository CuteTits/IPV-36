import socket
import requests
from pythonping import ping
import dns.resolver

# Replace with your IPHub API key or another VPN/proxy detection API key
IPHUB_API_KEY = "YOUR_IPHUB_API_KEY"

# Optional: basic subdomain wordlist for discovery
SUBDOMAIN_WORDLIST = ["www", "mail", "ftp", "api", "dev", "test"]

def get_ip_info(target):
    info = {}
    
    # Resolve IPs
    try:
        ipv4 = socket.gethostbyname(target)
        info['IPV4'] = ipv4
    except:
        info['IPV4'] = "N/A"

    try:
        ipv6 = socket.getaddrinfo(target, None, socket.AF_INET6)[0][4][0]
        info['IPV6'] = ipv6
    except:
        info['IPV6'] = "N/A"

    info['IP'] = info['IPV4'] if info['IPV4'] != "N/A" else info['IPV6']
    
    # IP type
    info['Ip type'] = 'Private' if info['IP'].startswith(('192.', '10.', '172.')) else 'Public'
    
    # Location & ISP
    try:
        res = requests.get(f'https://ipinfo.io/{info["IP"]}/json').json()
        info['Location'] = f"{res.get('continent','N/A')}/{res.get('country','N/A')}/{res.get('region','N/A')}/{res.get('city','N/A')}/{res.get('postal','N/A')}"
        info['ISP'] = res.get('org','N/A')
    except:
        info['Location'] = 'N/A'
        info['ISP'] = 'N/A'

    # Proxy/VPN detection
    try:
        headers = {"X-Key": IPHUB_API_KEY}
        res = requests.get(f'https://v2.api.iphub.info/ip/{info["IP"]}', headers=headers).json()
        info['Proxy'] = 'Yes' if res.get('block')==1 else 'No'
        info['VPN'] = 'Yes' if res.get('block')==1 else 'No'
        info['VPN/Proxy Provider'] = res.get('name','N/A')
    except:
        info['Proxy'] = 'N/A'
        info['VPN'] = 'N/A'
        info['VPN/Proxy Provider'] = 'N/A'

    # Ping
    try:
        response = ping(info['IP'], count=4, timeout=2)
        info['Uptime'] = f"{response.rtt_avg_ms} ms average"
        info['Is online?'] = 'Yes' if response.success() else 'No'
        info['Speeds (m/s)'] = f"{response.rtt_avg_ms/1000:.2f} m/s"
    except:
        info['Uptime'] = 'N/A'
        info['Is online?'] = 'No'
        info['Speeds (m/s)'] = 'N/A'

    # Connected URLs / Subdomains
    subdomains = []
    for sub in SUBDOMAIN_WORDLIST:
        full_domain = f"{sub}.{target}"
        try:
            socket.gethostbyname(full_domain)
            subdomains.append(full_domain)
        except:
            continue
    info['Connected URLs/Domains/Subdomains'] = ', '.join(subdomains) if subdomains else target

    return info

if __name__ == "__main__":
    target = input("Enter an IP address or domain to check: ").strip()
    data = get_ip_info(target)
    print("\n===== IP Lookup Result =====")
    for k, v in data.items():
        print(f"{k}: {v}")
