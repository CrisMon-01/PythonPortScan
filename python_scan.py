import socket # appartiene a standar lib
import sys
# venv
import pyfiglet
from rich.console import Console
from rich.table import Table

from utils import extract_json_data, threadpool_executer

console = Console() 

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
            sys.exit()
        print("\n [INFO] IP ADDRESS ACQUIRES: {ip_addr}")
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

    @staticmethod
    def show_startup_msg():
        ascii_art = pyfiglet.figlet_format("!PyPORTSCAN!")
        console.print(f"[bold green]{ascii_art}[/bold green]") 

    def show_completion_msg(self):
        if self.open_ports:
            console.print("[INFO] OPEN PORTS:", style="bold blue")
            table = Table(show_header=True, header_style="bold blue")
            table.add_column("PORT", style="blue")
            table.add_column("STATE", style="blue", justify="center")
            table.add_column("SERVICE", style="blue")
            for port in self.open_ports:
                table.add_row(str(port), "OPEN", self.ports_info[port])
            console.print(table)  #uso portsinfo e prendo val
        else:
            console.print("[INFO] NO PORTS FOUND", style="bold grey")

    def initialize(self):
        # self x trovare metodo
        self.show_startup_msg()
        self.get_ports_info()
        # stati metod posso usare anche solo show_startup_msg
        try:
            target = input("[IN] INSET HOSTNAME: ")
        except KeyboardInterrupt:
            console.print("\n[INFO] EXIT...", style="bold red")
            sys.exit()
        self.remote_host = self.get_host_ip_addr(target)
        try:
            input("\n [INFO] PYSCAN IS READY - PRESS ENTER TO SCAN")
            self.run()
        except KeyboardInterrupt:
            console.print("\n[INFO] EXIT...", style="bold red")
            sys.exit()

    def run(self):
        threadpool_executer(self.scan_port, self.ports_info.keys(), len(self.ports_info ))
        self.show_completion_msg()

# p.to ingresso allo script a se stante  
# sto eseguendo questo script python 
if __name__ == "__main__": 
    #richiamo classe
    pscan = PScan()
    pscan.initialize()
