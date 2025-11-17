CREATE TABLE IF NOT EXISTS endereco (
    cep        CHAR(8)      NOT NULL,
    rua        VARCHAR(150) NOT NULL,
    numero     VARCHAR(10)  NOT NULL,
    cidade     VARCHAR(100) NOT NULL,
    uf         CHAR(2)      NOT NULL,
    PRIMARY KEY (cep, rua, numero)
);

CREATE TABLE IF NOT EXISTS usuario (
    cpf             CHAR(11)      NOT NULL,
    cargo           VARCHAR(100)  NOT NULL,
    cep             CHAR(8)       NOT NULL,
    rua             VARCHAR(150)  NOT NULL,
    numero          VARCHAR(10)   NOT NULL,
    nome            VARCHAR(150)  NOT NULL,
    email           VARCHAR(150)  NOT NULL UNIQUE,
    senha           VARCHAR(200)  NOT NULL,
    data_nascimento DATE          NOT NULL,
    PRIMARY KEY (cpf),
    FOREIGN KEY (cep, rua, numero)
        REFERENCES endereco (cep, rua, numero)
);
