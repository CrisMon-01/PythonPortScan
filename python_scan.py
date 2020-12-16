import socket # appartiene a standar lib
import json # app a starìndart lib

OPEN_PORTS = []
PORTS_DATA_FILE = "./common_ports.json"

def extract_json_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)  
    return data

def get_ports_info():
    data = extract_json_data(PORTS_DATA_FILE)
    #metodo items di python su diz. rit. tuple <k,v>
    ports_info = {int(k): v for (k, v) in data.items()}
    return ports_info

def get_host_ip_addr(targername):
    try:
        ip_addr = socket.gethostbyname(targername)
    except socket.gaierror as namerr: #gai = get addr info
        print(f"[ERR] {e}")
    else:
        return ip_addr

def scan_port(ip, port):
    #init socker, astrazione sw per comunicare
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #fam (ipv4, ) tipo (tcp)
    sock.settimeout(1.0)
    conn_status = sock.connect_ex((ip, port)) #passo tupla conn_ex = esegui connessione
    if conn_status == 0:
        OPEN_PORTS.append(port)
    sock.close()   #chiudi sempre conn

# p.to ingresso allo script a se stante  
# sto eseguendo questo script python 
if __name__ == "__main__": 
    # extract_json_data(PORTS_DATA_FILE)
    print("[INFO] PORT SCAN ")
    target = input("[IN] INSET HOSTNAME: ")
    ip_addr = get_host_ip_addr(target)
    ports_info = get_ports_info()
    #ciclo sulle key
    for port in ports_info.keys():
        try:
            print(f"[INFO] SCANNING: {ip_addr}:{port}")
            scan_port(ip_addr, port)
        except KeyboardInterrupt:
            print("\n")
            print("[INFO] STOP BY INTERRUPT ")
            break
    print("[INFO] OPEN PORTS: ")
    for port in OPEN_PORTS:
        print(str(port), ports_info[port])  #uso portsinfo e prendo val