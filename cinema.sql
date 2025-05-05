-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS cinema;
USE cinema;
-- Tabela de filmes
CREATE TABLE IF NOT EXISTS Filmes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    genero VARCHAR(50),
    duracao TIME,
    formato VARCHAR(20)
);
-- Tabela de salas de exibição
CREATE TABLE IF NOT EXISTS Salas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);
-- Tabela de sessões fixas
CREATE TABLE IF NOT EXISTS Sessoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filme_id INT NOT NULL,
    sala_id INT NOT NULL,
    horario_padrao TIME NOT NULL,
    preco DECIMAL(6,2) NOT NULL DEFAULT 24.00, -- Preço da Inteira :/

    FOREIGN KEY (filme_id) REFERENCES Filmes(id),
    FOREIGN KEY (sala_id) REFERENCES Salas(id)
);
-- Tabela de agenda (datas específicas em que a sessão será exibida)
CREATE TABLE IF NOT EXISTS Agenda_Sessao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sessao_id INT NOT NULL,
    data_sessao DATE NOT NULL,

    FOREIGN KEY (sessao_id) REFERENCES Sessoes(id),
    UNIQUE(sessao_id, data_sessao) -- Evita datas repetidas para a mesma sessão --
);
-- Tabela de assentos (relacionado à sala)
CREATE TABLE IF NOT EXISTS Assentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sala_id INT NOT NULL,
    numero VARCHAR(10) NOT NULL,
    reservado BOOLEAN DEFAULT FALSE, 

    FOREIGN KEY (sala_id) REFERENCES Salas(id),
    UNIQUE (sala_id, numero) -- Evita assentos duplicados para uma mesma sala
);
-- Tabela de usuários
CREATE TABLE IF NOT EXISTS Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
-- Tabela de reservas (ligadas a um agendamento de sessão e assento específico)
CREATE TABLE IF NOT EXISTS Reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    agenda_sessao_id INT NOT NULL,
    assento_id INT NOT NULL,

    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id),
    FOREIGN KEY (agenda_sessao_id) REFERENCES Agenda_Sessao(id),
    FOREIGN KEY (assento_id) REFERENCES Assentos(id),
    
    UNIQUE (agenda_sessao_id, assento_id) -- Impede reservar mesmo assento duas vezes para a mesma sessão --
);
-- Inserindo filmes
INSERT INTO Filmes (titulo, genero, duracao, formato) VALUES
('Superman: Legacy', 'Ação', '02:10:00', '2D'),
('Thunderbolts', 'Ação', '01:55:00', '3D'),
('Quarteto Fantástico', 'Ficção', '02:05:00', '2D'),
('Deadpool 3', 'Comédia/Ação', '02:00:00', 'IMAX');
-- Inserindo salas
INSERT INTO Salas (nome) VALUES
('Sala 1'),
('Sala 2'),
('Sala IMAX');
-- Inserindo sessões
INSERT INTO Sessoes (filme_id, sala_id, horario_padrao, preco) VALUES
(1, 1, '18:00:00', 24.00), -- Superman na Sala 1
(2, 2, '20:00:00', 26.00), -- Thunderbolts na Sala 2
(3, 1, '16:00:00', 22.00), -- Quarteto Fantástico na Sala 1
(4, 3, '21:00:00', 30.00); -- Deadpool 3 na IMAX
-- Inserindo agenda de sessões
INSERT INTO Agenda_Sessao (sessao_id, data_sessao) VALUES
(1, '2025-05-01'),
(1, '2025-05-02'),
(2, '2025-05-01'),
(3, '2025-05-03'),
(4, '2025-05-01'),
(4, '2025-05-02');
-- Inserido assentos de cada sala
INSERT INTO Assentos (sala_id, numero) VALUES
(1, 'A1'), (1, 'A2'), (1, 'A3'), (1, 'A4'), (1, 'A5'), -- Assentos da Sala 1
(2, 'B1'), (2, 'B2'), (2, 'B3'), (2, 'B4'), (2, 'B5'), -- Assentos da Sala 2
(3, 'C1'), (3, 'C2'), (3, 'C3'), (3, 'C4'), (3, 'C5'); -- Assentos da Sala IMAX
-- Inserindo usuários
INSERT INTO Usuarios (nome, email) VALUES
('Leonardo Uchoa', 'leo@gmail.com'),
('Ednilson Silverio', 'ednilson@gmail.com'),
('Iarley Freitas', 'iarley@gmail.com'),
('Gabriel Dourado', 'gabriel@gmail.com');