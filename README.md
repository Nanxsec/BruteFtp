# Sobre:
O script contém 3 módulos! Scanner de portas, Brute Force e Shell

# Funcionalidade:
Ao passar o alvo e setar a wordlist, ele irá escanear as portas do alvo em busca da porta do FTP<br>
Caso ele encontre a porta, irá iniciar o segundo módulo que é o módulo de Brute Force<br>
Caso ele retorne sucesso no brute force, irá mostrar a senha e também irá iniciar o terceiro módulo que é te dando uma shell!

# Como usar:

    git clone https://github.com/Nanxsec/BruteFtp
    cd BruteFtp
    python3 ftp.py -h

# Wordlist:

A wordlist padrão que deixei com o script contém algumas credênciais default e também senhas que coletei
durante algumas explorações! Fique a vontade se quiser colocar mais senhas nela respeitando o formado username:password
