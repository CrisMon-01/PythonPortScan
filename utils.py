import json # app a starìndart lib 
from multiprocessing.pool import ThreadPool
import os
from rich.console import Console

console = Console()

def extract_json_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)  
    return data

def display_progress(iteration, total): 
    bar_max_width = 45 #num car
    bar_current_width = bar_max_width*iteration // total #divisione senza resto
    bar = "#" * bar_current_width + "-"*(bar_max_width-bar_current_width)
    progress = "%.1f" % (iteration / total * 100)
    console.print(f"| {bar}|{progress} %", end="\r", style="bold green") #end="\r" ritorna il terminale, permette di non printare + righe
    if(iteration == total): #spazio e esco
        print()

def threadpool_executer(function,iterable, iterable_length):
    number_of_workers = os.cpu_count()
    print(f"[INFO] RUNNING ON: {number_of_workers}\n")
    with ThreadPool(number_of_workers) as pool:
        for loop_index, _ in enumerate(pool.imap(function, iterable)): #il for è per avere l'avanzamento
            display_progress(loop_index, iterable_length)            
