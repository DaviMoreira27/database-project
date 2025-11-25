-- ENDEREÇO
INSERT INTO endereco (cep, rua, numero, cidade, uf)
VALUES ('01001000', 'Praça da Sé', '100', 'São Paulo', 'SP');

-- USUÁRIO
INSERT INTO usuario (
    cpf, cargo, cep, rua, numero, nome, email, senha, data_nascimento
) VALUES (
    '12345678901', 'CLIENTE', '01001000', 'Praça da Sé', '100',
    'Marcos Silva', 'marcos.silva@example.com', '$2a$10$7yeGjNx5CGxcvs.gsKgiUuMA9CpMX5SqVtuZBI764yKyyeBUwbriq', '1990-04-12' -- Password: senha123
);


-- 1. Inserção na tabela ENDERECO
-- Necessário criar antes de Usuário e Infraestrutura
INSERT INTO endereco (cep, rua, numero, cidade, uf) VALUES
('01001000', 'Praça da Sé', '10', 'São Paulo', 'SP'),
('20040002', 'Rua Rio Branco', '15', 'Rio de Janeiro', 'RJ'),
('30140071', 'Rua da Bahia', '500', 'Belo Horizonte', 'MG'),
('70040010', 'Setor Bancário Sul', '1', 'Brasília', 'DF'),
('80020000', 'Rua das Flores', '100', 'Curitiba', 'PR');

-- 2. Inserção na tabela PROVEDORA
-- Necessário criar antes de Infraestrutura e Bicicleta
INSERT INTO provedora (cnpj) VALUES
('11111111000111'), -- EcoMove
('22222222000122'), -- PowerCharge
('33333333000133'), -- GreenCycle
('44444444000144'), -- UrbanFlow
('55555555000155'); -- ElectroCity

-- 3. Inserção na tabela USUARIO
-- Base para Cliente, Gerente e Administrador.
-- Note que repetimos os dados de endereço exatamente como cadastrados acima.
INSERT INTO usuario (cpf, cargo, cep, rua, numero, nome, email, senha, data_nascimento) VALUES
('11122233344', 'Cliente Standard', '01001000', 'Praça da Sé', '10', 'João Silva', 'joao@email.com', 'senha123', '1990-05-15'),
('22233344455', 'Cliente Premium', '20040002', 'Rua Rio Branco', '15', 'Maria Santos', 'maria@email.com', 'senha123', '1985-10-20'),
('33344455566', 'Gerente Regional', '30140071', 'Rua da Bahia', '500', 'Carlos Oliveira', 'carlos@email.com', 'senha123', '1978-03-12'),
('44455566677', 'Gerente Operacional', '70040010', 'Setor Bancário Sul', '1', 'Ana Souza', 'ana@email.com', 'senha123', '1992-07-30'),
('55566677788', 'Admin Sistema', '80020000', 'Rua das Flores', '100', 'Pedro Lima', 'pedro@email.com', 'senha123', '1988-12-01'),
-- Adicionando mais usuários para cobrir todos os papéis
('66677788899', 'Cliente', '01001000', 'Praça da Sé', '10', 'Lucas Mendes', 'lucas@email.com', 'senha123', '1995-01-10'),
('77788899900', 'Cliente', '20040002', 'Rua Rio Branco', '15', 'Julia Pereira', 'julia@email.com', 'senha123', '1993-06-25'),
('88899900011', 'Gerente', '30140071', 'Rua da Bahia', '500', 'Fernanda Costa', 'fernanda@email.com', 'senha123', '1982-09-14'),
('99900011122', 'Admin', '70040010', 'Setor Bancário Sul', '1', 'Roberto Alves', 'roberto@email.com', 'senha123', '1975-04-18'),
('00011122233', 'Cliente', '80020000', 'Rua das Flores', '100', 'Mariana Rocha', 'mariana@email.com', 'senha123', '2000-11-30');

-- 4. Inserção na tabela CLIENTE
-- CPFs devem existir em Usuario
INSERT INTO cliente (cpf, pontuacao) VALUES
('11122233344', 100),
('22233344455', 2500),
('66677788899', 50),
('77788899900', 300),
('00011122233', 0);

-- 5. Inserção na tabela GERENTE
-- CPFs devem existir em Usuario, CNPJs em Provedora
INSERT INTO gerente (cpf, provedora) VALUES
('33344455566', '11111111000111'),
('44455566677', '22222222000122'),
('88899900011', '33333333000133'),
('55566677788', '44444444000144'), -- Usando o CPF 555... (que era Admin no cargo, mas aqui atua como gerente para exemplo)
('99900011122', '55555555000155');

-- 6. Inserção na tabela ADMINISTRADOR
INSERT INTO administrador (cpf) VALUES
('55566677788'),
('99900011122'),
('11122233344'), -- Um usuário pode ter múltiplos papéis dependendo da regra de negócio, aqui assumimos que sim
('33344455566'),
('44455566677');

-- 7. Inserção na tabela INFRAESTRUTURA
-- Registros mistos que serão especializados em Totens ou Pontos de Retirada
INSERT INTO infraestrutura (n_registro, provedora, tipo, cep, rua, numero) VALUES
('INFRA-SP-001', '11111111000111', 'Estação de Recarga', '01001000', 'Praça da Sé', '10'),
('INFRA-RJ-002', '22222222000122', 'Estação de Recarga', '20040002', 'Rua Rio Branco', '15'),
('INFRA-MG-003', '33333333000133', 'Estação de Recarga', '30140071', 'Rua da Bahia', '500'),
('INFRA-DF-004', '44444444000144', 'Estação de Recarga', '70040010', 'Setor Bancário Sul', '1'),
('INFRA-PR-005', '55555555000155', 'Estação de Recarga', '80020000', 'Rua das Flores', '100'),
('INFRA-SP-006', '11111111000111', 'Ponto de Retirada', '01001000', 'Praça da Sé', '10'),
('INFRA-RJ-007', '22222222000122', 'Ponto de Retirada', '20040002', 'Rua Rio Branco', '15'),
('INFRA-MG-008', '33333333000133', 'Ponto de Retirada', '30140071', 'Rua da Bahia', '500'),
('INFRA-DF-009', '44444444000144', 'Ponto de Retirada', '70040010', 'Setor Bancário Sul', '1'),
('INFRA-PR-010', '55555555000155', 'Ponto de Retirada', '80020000', 'Rua das Flores', '100');

-- 8. Inserção na tabela TOTENS_DE_RECARGA
-- Herança de Infraestrutura (IDs 001 a 005)
INSERT INTO totens_de_recarga (n_registro, capacidade, preco, voltagem, conector, potencia, status) VALUES
('INFRA-SP-001', 2, 1.50, 220, 'Type 2', 22, 'ATIVO'),
('INFRA-RJ-002', 4, 1.80, 110, 'CCS2', 50, 'ATIVO'),
('INFRA-MG-003', 1, 1.20, 220, 'CHAdeMO', 50, 'MANUTENCAO'),
('INFRA-DF-004', 2, 2.00, 220, 'Type 2', 11, 'INATIVO'),
('INFRA-PR-005', 3, 1.60, 110, 'CCS2', 150, 'ATIVO');

-- 9. Inserção na tabela PONTOS_DE_RETIRADA
-- Herança de Infraestrutura (IDs 006 a 010)
INSERT INTO pontos_de_retirada (n_registro, capacidade, bicicletas_disponiveis, status, voltagem) VALUES
('INFRA-SP-006', 20, 15, 'ATIVO', 0),
('INFRA-RJ-007', 15, 5, 'ATIVO', 0),
('INFRA-MG-008', 10, 0, 'VAZIO', 0),
('INFRA-DF-009', 25, 25, 'ATIVO', 0),
('INFRA-PR-010', 12, 0, 'MANUTENCAO', 0);

-- 10. Inserção na tabela REPORTE_DE_PROBLEMA
-- Usa gen_random_uuid() implícito para protocolo se o banco suportar, caso contrário inserir string manual.
-- Assumindo suporte a DEFAULT gen_random_uuid() conforme schema.
INSERT INTO reporte_de_problema (usuario, infraestrutura, titulo, descricao) VALUES
('11122233344', 'INFRA-SP-001', 'Tela quebrada', 'A tela do totem está trincada e ilegível.'),
('22233344455', 'INFRA-RJ-002', 'Conector preso', 'Não consegui desconectar o cabo do meu carro.'),
('33344455566', 'INFRA-MG-008', 'Sem bicicletas', 'O aplicativo dizia que havia bicicletas, mas está vazio.'),
('66677788899', 'INFRA-DF-004', 'Desligado', 'O totem não dá sinal de vida.'),
('00011122233', 'INFRA-PR-010', 'Vandalismo', 'Picharam a lateral da estação.');

-- 11. Inserção na tabela AVALIACAO
INSERT INTO avaliacao (infraestrutura, cliente, nota, descricao) VALUES
('INFRA-SP-001', '11122233344', 5, 'Carregamento rápido e barato.'),
('INFRA-RJ-002', '22233344455', 4, 'Bom, mas a fila estava grande.'),
('INFRA-MG-003', '66677788899', 1, 'Estava em manutenção e o app não avisou.'),
('INFRA-DF-004', '77788899900', 3, 'Preço ok, mas potência baixa.'),
('INFRA-PR-005', '00011122233', 5, 'Excelente localização.');

-- 12. Inserção na tabela BICICLETA
INSERT INTO bicicleta (codigo, provedora, modelo, valor, bateria, status, local_origem) VALUES
('BIKE-001', '11111111000111', 'Mountain Bike Elétrica', 5.50, 100, 'ESTACIONADO', 'INFRA-SP-006'),
('BIKE-002', '22222222000122', 'City Cruiser', 4.00, 80, 'EM_USO', 'INFRA-RJ-007'),
('BIKE-003', '33333333000133', 'Speed Lite', 6.00, 15, 'MANUTENCAO', 'INFRA-MG-008'),
('BIKE-004', '44444444000144', 'Standard', 3.00, 95, 'ESTACIONADO', 'INFRA-DF-009'),
('BIKE-005', '55555555000155', 'Heavy Duty', 5.00, 0, 'FORA_DE_SERVICO', 'INFRA-PR-010');

-- 13. Inserção na tabela CARRO
INSERT INTO carro (placa, cliente, capacidade_bateria, autonomia, adaptador, modelo) VALUES
('ABC-1234', '11122233344', 50, 300, 'Type 2', 'Nissan Leaf'),
('XYZ-5678', '22233344455', 75, 450, 'CCS2', 'Tesla Model 3'),
('LMN-9012', '66677788899', 40, 250, 'Type 2', 'Renault Zoe'),
('DEF-3456', '77788899900', 90, 500, 'CCS2', 'Porsche Taycan'),
('GHI-7890', '00011122233', 60, 380, 'CHAdeMO', 'BYD Dolphin');

-- 14. Inserção na tabela HORARIO_TOTENS
-- Utilizando o formato de range do PostgreSQL [inicio, fim)
INSERT INTO horario_totens (totem, horario) VALUES
('INFRA-SP-001', '[2024-01-01 08:00, 2024-01-01 22:00)'),
('INFRA-RJ-002', '[2024-01-01 00:00, 2024-01-01 23:59)'),
('INFRA-MG-003', '[2024-01-01 06:00, 2024-01-01 20:00)'),
('INFRA-DF-004', '[2024-01-01 09:00, 2024-01-01 18:00)'),
('INFRA-PR-005', '[2024-01-01 05:00, 2024-01-01 23:00)');

-- 15. Inserção na tabela MANUTENCAO_INFRAESTRUTURA
INSERT INTO manutencao_infraestrutura (horario, status, infraestrutura, gerente) VALUES
('[2024-02-10 10:00, 2024-02-10 14:00)', 'Concluída', 'INFRA-SP-001', '33344455566'),
('[2024-02-11 08:00, 2024-02-11 12:00)', 'Agendada', 'INFRA-RJ-002', '44455566677'),
('[2024-02-12 09:00, 2024-02-12 11:00)', 'Em andamento', 'INFRA-MG-003', '88899900011'),
('[2024-02-13 13:00, 2024-02-13 17:00)', 'Cancelada', 'INFRA-DF-004', '55566677788'),
('[2024-02-14 14:00, 2024-02-14 16:00)', 'Concluída', 'INFRA-PR-005', '99900011122');

-- 16. Inserção na tabela SESSAO_RECARGA
INSERT INTO sessao_recarga (totem, horario_inicio, data, carro, kwh_consumidos, valor, emissao_co2) VALUES
('INFRA-SP-001', '2024-03-01 10:00:00', '2024-03-01', 'ABC-1234', 20.5, 30.75, 0.5),
('INFRA-RJ-002', '2024-03-02 14:30:00', '2024-03-02', 'XYZ-5678', 40.0, 72.00, 1.2),
('INFRA-SP-001', '2024-03-03 09:15:00', '2024-03-03', 'LMN-9012', 15.0, 22.50, 0.3),
('INFRA-PR-005', '2024-03-04 18:00:00', '2024-03-04', 'DEF-3456', 55.5, 88.80, 1.5),
('INFRA-RJ-002', '2024-03-05 11:45:00', '2024-03-05', 'GHI-7890', 30.0, 54.00, 0.8);

-- 17. Inserção na tabela RETIRADA_BICICLETA
-- Relaciona Bikes com Pontos de Retirada
INSERT INTO retirada_bicicleta (bicicleta, ponto_retirada) VALUES
('BIKE-001', 'INFRA-SP-006'),
('BIKE-002', 'INFRA-RJ-007'),
('BIKE-003', 'INFRA-MG-008'),
('BIKE-004', 'INFRA-DF-009'),
('BIKE-005', 'INFRA-PR-010');
