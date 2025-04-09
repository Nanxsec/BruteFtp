import socket
import ftplib
import os
import sys
import readline
from datetime import datetime

# Auto complete
comandos_disponiveis = [
    "ls --> Lista Diretórios", "cd --> Entra em um diretório", "dw --> Baixa um arquivo", "up --> Upload de um arquivo", "rn --> Renomear um arquivo", "mk --> Criar diretórios", "rm --> Remover", "ex --> alias para rm", "pw --> Mostra o diretorio atual", "cl --> limpa a tela",
    "qt --> Fecha a shell", "pa --> Ativa o modo passivo (ativado por padrão)", "ld --> Listagem detalhada", "c  --> Mostra essa mensagem"
]

def completer(text, state):
    matches = [cmd for cmd in comandos_disponiveis if cmd.startswith(text)]
    return matches[state] if state < len(matches) else None

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")


class FTPShell:
    def __init__(self, rhost, usern, paswd, rport=21, use_ftps=False):
        self.rhost = rhost
        self.usern = usern
        self.paswd = paswd
        self.rport = rport
        self.use_ftps = use_ftps
        self.ftp = None
        self.sock = None
        self.log_file = f"ftp_commands_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    def banner(self):
       os.system("clear")
       print("""\033[1;31m
     _       _ _ 
 ___| |_ ___| | |
|_ -|   | -_| | |
|___|_|_|___|_|_|
\033[m\033[32mInstagram:\033[m @nanoxsec
""")

    def comandos(self):
        print("\n\033[1;36mComandos disponíveis:\033[m")
        for cmd in comandos_disponiveis:
            print(f"  {cmd}")

    def log(self, linha):
        with open(self.log_file, "a") as f:
            f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {linha}\n")

    def conectar(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.use_ftps:
                self.ftp = ftplib.FTP_TLS()
                self.ftp.connect(self.rhost, self.rport)
                self.ftp.login(user=self.usern, passwd=self.paswd)
                self.ftp.prot_p()
            else:
                self.ftp = ftplib.FTP()
                self.ftp.connect(self.rhost, self.rport)
                self.ftp.login(user=self.usern, passwd=self.paswd)

            print(f"\n\033[1m[\033[m\033[1;32m OK! \033[m\033[1m]\033[m Conectado em: \033[1;36m{self.rhost}:{self.rport}\033[m")
            print("\033[1m[\033[m\033[1;32m OK! \033[m\033[1m]\033[m Digite \033[1;33mC\033[m para ver os comandos disponíveis.")
            self.banner()
            self.loop()
        except Exception as e:
            print(f"[!] Falha ao conectar: {e}")

    def loop(self):
        while True:
            try:
                prompt_path = self.ftp.pwd()
            except:
                prompt_path = "ftpbrute"
            cmd_line = input(f"\n\033[1;31mftp@{prompt_path}>\033[m ").strip()
            if not cmd_line:
                continue

            self.log(cmd_line)

            cmd_parts = cmd_line.split()
            cmd = cmd_parts[0].lower()
            args = cmd_parts[1:] if len(cmd_parts) > 1 else []

            try:
                if cmd == "c":
                    self.comandos()
                elif cmd == "ls":
                    self.ftp.dir()
                elif cmd == "cd":
                    path = args[0] if args else input("Diretório: ").strip()
                    self.ftp.cwd(path)
                elif cmd == "dw":
                    filename = args[0] if args else input("Arquivo a baixar: ").strip()
                    with open(filename, "wb") as f:
                        self.ftp.retrbinary(f"RETR {filename}", f.write)
                    print("Download concluído!")
                elif cmd == "up":
                    filename = args[0] if args else input("Arquivo para upload: ").strip()
                    with open(filename, "rb") as f:
                        self.ftp.storbinary(f"STOR {filename}", f)
                    print("Upload concluído!")
                elif cmd == "rn":
                    old = args[0] if len(args) > 0 else input("Nome do arquivo: ").strip()
                    new = args[1] if len(args) > 1 else input("Novo nome: ").strip()
                    self.ftp.rename(old, new)
                elif cmd in ["rm", "ex"]:
                    alvo = args[0] if args else input("Arquivo ou diretório: ").strip()
                    try:
                        self.ftp.rmd(alvo)
                    except:
                        self.ftp.delete(alvo)
                elif cmd == "mk":
                    nome = args[0] if args else input("Nome do diretório: ").strip()
                    self.ftp.mkd(nome)
                elif cmd == "pw":
                    print("Diretório atual:", self.ftp.pwd())
                elif cmd == "pa":
                    try:
                        self.sock.connect((self.rhost, self.rport))
                        self.sock.recv(1024)
                        self.sock.send(b"USER " + self.usern.encode() + b"\r\n")
                        self.sock.recv(1048)
                        self.sock.send(b"PASS " + self.paswd.encode() + b"\r\n")
                        self.sock.recv(1048)
                        self.sock.send(b"PASV \r\n")
                        resposta = self.sock.recv(2048).decode("utf-8")
                        if "227" in resposta:
                            print("Modo passivo ativado!")
                    except:
                        print("Erro ao ativar modo passivo.")
                elif cmd == "ld":
                    print(list(self.ftp.mlsd()))
                elif cmd == "cl":
                    os.system("cls" if sys.platform == "win32" else "clear")
                    self.banner()
                elif cmd == "qt":
                    print("Saindo...")
                    try:
                        self.ftp.quit()
                    except:
                        pass
                    finally:
                        self.sock.close()
                        break
                else:
                    print("Comando não reconhecido.")
            except Exception as e:
                print(f"Erro: {e}")
