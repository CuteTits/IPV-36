import requests
import socket

def get_ip(url):
    try:
        ip = socket.gethostbyname(url)
        return ip
    except socket.gaierror:
        return "error"

def get_geolocation(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        isp = data.get('org', 'Unknown')
        location = data.get('loc', '').split(',')
        city = data.get('city', 'Unknown')
        region = data.get('region', 'Unknown')
        country = data.get('country', 'Unknown')
        continent = data.get('continent', 'Unknown')
        coordinates = tuple(map(float, location))
        return isp, continent, country, region, city, coordinates
    except Exception as e:
        print(e)
        return "error"

def main():
    url = input("Enter URL or IP: ")
    ip = get_ip(url)
    if ip == "error":
        print("Unable to resolve IP from URL.")
        return

    isp, continent, country, state, city, coordinates = get_geolocation(ip)
    if isp == "error":
        print("Error fetching geolocation information.")
        return

    print(f"IP: {ip}")
    print(f"ISP: {isp}")
    print(f"Continent: {continent}")
    print(f"Country: {country}")
    print(f"State: {state}")
    print(f"City: {city}")
    print(f"Coordinates: {coordinates}")

if __name__ == "__main__":
    main()
