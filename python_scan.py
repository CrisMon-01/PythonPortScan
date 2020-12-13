import socket # appartiene a standar lib

OPEN_PORTS = []

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
    print("[INFO] PORT SCAN ")
    target = input("[IN] INSET HOSTNAME: ")
    ip_addr = get_host_ip_addr(target)
    while True:
        try:
            port = int(input("[IN] INSERT PORT TO CHECK: "))
            scan_port(ip_addr, port)
            print(OPEN_PORTS)
        except KeyboardInterrupt:
            print("\n")
            print("[INFO] STOP BY INTERRUPT ")
            exit