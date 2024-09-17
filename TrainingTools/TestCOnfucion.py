import os


def ping_ip(ip):
    response = os.system(f"ping -n 1 {ip} >nul 2>&1")
    return response == 0


def read_ips_from_file(file_path):
    with open(file_path, 'r') as file:
        ips = file.readlines()
    return [ip.strip() for ip in ips]


def main():
    file_path = r'C:\Users\y80txk\Downloads\ips.txt'  # Ruta del archivo en Windows
    ips = read_ips_from_file(file_path)

    reachable_ips = []
    unreachable_ips = []

    for ip in ips:
        if ping_ip(ip):
            reachable_ips.append(ip)
        else:
            unreachable_ips.append(ip)

    print("IPs que respondieron:")
    for ip in reachable_ips:
        print(ip)

    print("\nIPs que no respondieron:")
    for ip in unreachable_ips:
        print(ip)


if __name__ == "__main__":
    main()
