# Esboço do que pode ser o trabalho de Banco de Dados II

    - Objetivos:

        O objetivo deste trabalho é propor e implementar um cenário realista que exija o uso de transações explícitas em um banco de dados relacional para garantir a atomicidade, consistência e controle de concorrência em operações críticas.

        O foco está em situações onde múltiplos usuários ou processos podem acessar e modificar os mesmos dados simultaneamente, exigindo mecanismos como:

        - Transações ACID: Para garantir que operações múltiplas sejam tratadas como uma única unidade atômica.

        - Controle de concorrência: Evitando condições de corrida, como vendas duplicadas de um mesmo produto ou reservas conflitantes.

    - Possível implementação:

        Uma possível implementação para o trabalho seria a criação de um sistema de reservas de assentos em um cinema, onde:

        - Vários usuários podem tentar reservar o mesmo assento ao mesmo tempo.

        - O sistema deve garantir que um assento não seja reservado por mais de um usuário.

        - Se uma reserva falhar, todas as alterações no banco de dados devem ser revertidas (rollback).

    - Banco de Dados, ferramentas e API:

        Para fins de simplecidade e otimização de tempo, podemos usar o como banco de Dados o MariaDB, Python + mysqlclient e FastAPI.

# Instruções para execução na sua máquina

    - Passos no Linux (Ubuntu)

        1. Com o MariaDB instalado, execute no seu terminal os comandos do arquivo: ./cinema.sdb

        2. Crie um ambiente virtual python executando os comandos do arquivo: ./script.sh
        
        3. Execute o arquivo main.py usando o comando 'uvicorn main:app --reload'

        4. Ao executar o código, copiar a URL e acessar a interface iterativa /docs, ou melhor, http://127.0.0.1:8000/docs

        5. Para fazer uma reserva, selecione o endpoint POST /reservar, clique em "Try it out" e preencha os campos necessários, depois clique em "Execute" para fazer a requisição.

        6. O status da transação será mostrado em seguida.