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
