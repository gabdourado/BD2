# Sistema de Reserva de Assentos em Cinema 

## Proposição do Problema

O objetivo desta documentação é apresentar o desenvolvimento do backend de um sistema de reserva de assentos para sessões de cinema. Além de abordar a modelagem de dados e a implementação da API, este documento discute os principais desafios de concorrência enfrentados durante o desenvolvimento e as estratégias adotadas para garantir transações seguras em banco de dados relacionais.

## Cenário

Em cinemas tradicionais, a venda de ingressos era feita presencialmente, o que frequentemente resultava em confusões, especialmente em horários de pico. Problemas como dupla reserva de assentos eram comuns.  
Para solucionar isso, foi proposto o desenvolvimento de um sistema online de reserva de assentos, com controle rigoroso de disponibilidade em tempo real. 

## Especificação Técnica

A seguir, detalhamos o banco de dados relacional utilizado (MariaDB), sua modelagem de tabelas e a estrutura da API desenvolvida com FastAPI. Por fim, abordamos os desafios relacionados à concorrência e as soluções implementadas.

### Banco de Dados e Modelagem

Escolhemos o Mariadb como Banco de Dados pois é open-source e possui uma comunidade robusta, o que torna mais acessível para o projeto e contribui para sua evolução contínua.

Feita a Modelagem, o Banco possui seguintes tabelas:

| Tabela          | Colunas                                                          |
|-----------------|------------------------------------------------------------------|
| Filmes          | ID (PK), Titulo, Duracao, Formato                                |
| Salas           | ID (PK), Nome                                                    |
| Sessoes         | ID (PK), Filme_ID (FK), Sala_ID (FK), Horario, Preco             |
| Agenda_Sessao   | ID (PK), Sessao_ID (FK), Data_Sessao                             |
| Usuarios        | ID (PK), Nome, Email                                             |
| Assentos        | ID (PK), Numero, Sala_ID (FK)                                    |
| Reservas        | ID (PK), Usuario_ID (FK), Agenda_Sessao_ID (FK), Assento_ID (FK) |

Descrição de cada tabela do Banco de Dados:

- **Filmes**: Tabela que contém os filmes que estão em cartaz no cinema.  
- **Salas**: Tabela com os nomes de cada sala, funciona como uma tabela auxiliar.  
- **Sessoes**: Tabela que contém as sessões que cada filme pode passar.  
- **Agenda_Sessao**: São as datas de cada sessão.  
- **Usuarios**: Tabela que contém os clientes que fazem a compra dos ingressos.  
- **Assentos**: Tabela com os assentos de cada sala.  
- **Reservas**: Tabela que guarda a reserva que um determinado usuário fez de um assento para uma determinada sessão.

---

## API Backend: FastAPI

A API foi desenvolvida em FastAPI devido à sua performance, suporte a validação automática com Pydantic, e facilidade de integração com Swagger. 

**Os principais endpoints criados incluem:**

- `/sessoes`: Lista as sessões com seus respectivos filmes. (GET) ✅  
- `/fazer-reserva`: Reserva um assento para uma sessão específica. (POST) 🔄  
- `/mostrar-reservas`: Mostra todas as reservas de uma determinada sessão (GET)  
- `/alterar-reserva`: Altera uma reserva feita por um usuário específico. (POST) ✅  
- `/deletar-reserva`: Deleta um assento para uma sessão específica. (GET)  
- `/assentos`: Exibe assentos disponíveis para uma sessão específica. (GET) 🔄  
- `/adicionar-assento`: Adiciona um novo assento em uma sala específica. (POST)  
- `/remover-reserva`: Remover uma reserva realizada. (POST)  
- `/cadastrar-filme`: Adicionar um novo filme no banco de dados. (POST) ✅  
- `/iarley`:  

---

### Como funciona uma API?

### O que é Pydantic?

O Pydantic é uma biblioteca Python para validação de dados baseados em tipagem. Ele permite garantir que os dados que estão sendo manipulados atendem a certos tipos e regras de validação, facilitando a construção de APIs e sistemas que lidam com dados.

Por exemplo, o modelo `ReservaRequest` é uma classe que herda de `BaseModel` do Pydantic, e nela definimos os campos que a requisição de reserva deve ter:

```python
from pydantic import BaseModel

class ReservaRequest(BaseModel):
    usuario_id: int
    agenda_sessao_id: int
    assento_numero: str
```

Assim, se ao realizar uma requisição, algum desses campos contiver algo diferente do esperado, o Pydantic lança um erro informando qual campo está inválido e qual é o tipo esperado.

Isso torna o código mais seguro, pois a validação de tipos é realizada automaticamente, sem que o desenvolvedor precise escrever manualmente a lógica de validação.

### O que é Swagger?

Já o Swagger consiste em uma ferramenta para documentar API’s, gerando automaticamente a interface de testes.

Por exemplo, ao utilizar FastAPI para criar uma API com este modelo, o Swagger UI é gerado automaticamente, incluindo todos os campos do modelo `ReservaRequest` na documentação interativa.

Assim, ao acessar `http://localhost:8000/docs`, o Swagger UI mostrará algo como:

```json
{
    "usuario_id": 123,
    "agenda_sessao_id": 456,
    "assento_numero": "A10"
}
```

Com isso, o Swagger ajuda os desenvolvedores e usuários da API a entender rapidamente como a API funciona, quais dados são esperados, e quais são os possíveis códigos de resposta.

### Problemas de Concorrência

Em situações com múltiplos usuários tentando reservar o mesmo assento, é possível que ocorra uma condição de corrida. Em situações de alta concorrência, duas transações podiam ler o mesmo estado do assento (disponível) e tentar reservá-lo ao mesmo tempo, resultando em duplicidade.

Para resolver isso, implementamos transações explícitas e uso de locks pessimistas como veremos a seguir, garantindo atomicidade e isolamento nas operações no Banco.
Solução Proposta

Transações em Banco de Dados devem obedecer aos princípios ACID, para garantir a integridade e a consistência dos dados.

    Atomicidade: A transação é “tudo ou nada”. Ou todas as operações são concluídas com sucesso, ou nenhuma é.

    Consistência: Após a transação, o banco deve permanecer em um estado consistente, respeitando todas as regras e restrições definidas.

    Isolamento: Transações simultâneas não devem interferir entre si. Cada uma deve parecer ser executada isoladamente.

    Durabilidade: Uma vez confirmadas, as alterações da transação persistem no banco mesmo em caso de falha do sistema.

Para garantir que esses princípios sejam atendidos, implementamos transações explícitas e uso de locks pessimistas.

    (Trecho do Código)

No trecho de código mostrado acima, a transação é iniciada com conn.begin() e é encerrada com conn.commit() se tudo correr bem ou conn.rollback() em caso de erro.

O uso explícito de FOR UPDATE nas consultas impede que outras transações leiam ou escrevam os mesmos registros simultaneamente, aplicando um lock pessimista durante a leitura dos dados críticos.

Isso evita condições de corrida, garantindo que duas pessoas não reservem o mesmo assento ao mesmo tempo.