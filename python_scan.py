import socket # appartiene a standar lib
from utils import extract_json_data

class PScan:

    #var di classe
    PORTS_DATA_FILE = "./common_ports.json"

    #init ha biogno di self, rif all'istanza della classe
    def __init__(self):
        self.open_ports = []
        self.ports_info = {}
        self.remote_host = ""

    #passo self operando su un campo
    def get_ports_info(self):   
        data = extract_json_data(PScan.PORTS_DATA_FILE)
        #metodo items di python su diz. rit. tuple <k,v>
        self.ports_info = {int(k): v for (k, v) in data.items()}
        # return ports_info

    # x metodi a cui non passo self
    @staticmethod
    def get_host_ip_addr(targername):
        try:
            ip_addr = socket.gethostbyname(targername)
        except socket.gaierror as namerr: #gai = get addr info
            print(f"[ERR] {e}")
        else:
            return ip_addr

    #self x aggiungere porte a open port
    def scan_port(self, port):
        #init socker, astrazione sw per comunicare
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #fam (ipv4, ) tipo (tcp)
        sock.settimeout(1.0)
        conn_status = sock.connect_ex((self.remote_host, port)) #passo tupla conn_ex = esegui connessione
        if conn_status == 0:
            self.open_ports.append(port)
        sock.close()   #chiudi sempre conn

    def run(self):
        print("[INFO] PORT SCAN ")
        target = input("[IN] INSET HOSTNAME: ")
        self.remote_host = self.get_host_ip_addr(target)
        self.get_ports_info()
        
        #ciclo sulle key
        for port in self.ports_info.keys():
            try:
                print(f"[INFO] SCANNING: {self.remote_host}:{port}")
                self.scan_port(port)
                #scan_port(ip_addr, port)
            except KeyboardInterrupt:
                print("\n")
                print("[INFO] STOP BY INTERRUPT ")
                break
        print("[INFO] OPEN PORTS: ")
        for port in self.open_ports:
            print(str(port), self.ports_info[port])  #uso portsinfo e prendo val

# p.to ingresso allo script a se stante  
# sto eseguendo questo script python 
if __name__ == "__main__": 
    #richiamo classe
    pscan = PScan()
    pscan.run()
