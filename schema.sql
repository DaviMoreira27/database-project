CREATE TABLE IF NOT EXISTS endereco (
    cep        VARCHAR(8),
    rua        VARCHAR(150),
    numero     VARCHAR(10),
    cidade     VARCHAR(100),
    uf         CHAR(2),
    PRIMARY KEY (cep, rua, numero)
);

CREATE TABLE IF NOT EXISTS usuario (
    cpf             VARCHAR(11),
    cargo           VARCHAR(100)  NOT NULL,
    cep             VARCHAR(8)    NOT NULL,
    rua             VARCHAR(150)  NOT NULL,
    numero          VARCHAR(10)   NOT NULL,
    nome            VARCHAR(150),
    email           VARCHAR(150) UNIQUE,
    senha           VARCHAR(200),
    data_nascimento DATE,
    PRIMARY KEY (cpf),
    FOREIGN KEY (cep, rua, numero) REFERENCES endereco (cep, rua, numero)
);

CREATE TABLE IF NOT EXISTS provedora (
    cnpj VARCHAR(16),
    PRIMARY KEY (cnpj)
);

CREATE TABLE IF NOT EXISTS gerente (
    cpf       VARCHAR(11),
    provedora VARCHAR(16),
    PRIMARY KEY (cpf),
    FOREIGN KEY (provedora) REFERENCES provedora (cnpj)
    FOREIGN KEY (cpf) REFERENCES Usuário (cpf)
);

CREATE TABLE IF NOT EXISTS cliente (
    cpf        VARCHAR(11),
    pontuacao  NUMERIC,
    PRIMARY KEY (cpf)
    FOREIGN KEY (cpf) REFERENCES Usuário (cpf)
);

CREATE TABLE IF NOT EXISTS administrador (
    cpf VARCHAR(11),
    PRIMARY KEY (cpf),
    FOREIGN KEY (cpf) REFERENCES Usuário (cpf)
);

CREATE TABLE IF NOT EXISTS infraestrutura (
    n_registro VARCHAR(26)  NOT NULL,
    provedora  VARCHAR(16)  NOT NULL,
    tipo       VARCHAR(100) NOT NULL,
    cep        VARCHAR(8)   NOT NULL,
    rua        VARCHAR(150) NOT NULL,
    numero     VARCHAR(10)  NOT NULL,
    PRIMARY KEY (n_registro, provedora),
    FOREIGN KEY (provedora) REFERENCES provedora (cnpj),
    FOREIGN KEY (cep, rua, numero) REFERENCES endereco (cep, rua, numero),
    UNIQUE (cep, rua, numero)
);

CREATE TABLE IF NOT EXISTS reporte_de_problema (
    protocolo       UUID          NOT NULL DEFAULT gen_random_uuid(),
    usuario         VARCHAR(11)   NOT NULL,
    infraestrutura  VARCHAR(26)   NOT NULL,
    data            TIMESTAMP     NOT NULL DEFAULT current_timestamp,
    titulo          VARCHAR(100)  NOT NULL,
    descricao       TEXT,
    PRIMARY KEY (protocolo),
    FOREIGN KEY (usuario) REFERENCES usuario (cpf),
    FOREIGN KEY (infraestrutura) REFERENCES infraestrutura (n_registro)
);

CREATE TABLE IF NOT EXISTS avaliacao (
    id             UUID          NOT NULL DEFAULT gen_random_uuid(),
    infraestrutura VARCHAR(26),
    cliente        VARCHAR(11)   NOT NULL,
    nota           INTEGER,
    descricao      TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (infraestrutura) REFERENCES infraestrutura (n_registro),
    FOREIGN KEY (cliente) REFERENCES cliente (cpf)
);

CREATE TABLE IF NOT EXISTS bicicleta (
    codigo        VARCHAR(26),
    provedora     VARCHAR(16),
    modelo        VARCHAR(100),
    valor         NUMERIC(10,2),
    bateria       INTEGER            NOT NULL,
    status        STATUS_BICICLETA ,
    local_origem  VARCHAR(26),
    PRIMARY KEY (codigo),
    FOREIGN KEY (provedora) REFERENCES provedora (CNPJ)
);

CREATE TABLE IF NOT EXISTS carro (
    placa                VARCHAR(20),
    cliente              VARCHAR(11)  NOT NULL,
    capacidade_bateria   INTEGER,
    autonomia            INTEGER,
    adaptador            VARCHAR(50)  NOT NULL,
    modelo               VARCHAR(100),
    PRIMARY KEY (placa),
    FOREIGN KEY (cliente) REFERENCES cliente (cpf)
);

CREATE TABLE IF NOT EXISTS totens_de_recarga (
    n_registro  VARCHAR(26),
    capacidade  INTEGER,
    preco       NUMERIC(10,2),
    voltagem    INTEGER     NOT NULL,
    conector    VARCHAR(50),
    potencia    INTEGER,
    status      STATUS_TOTEM,
    PRIMARY KEY (n_registro),
    FOREIGN KEY (n_registro) REFERENCES infraestrutura (n_registro)
);

CREATE TABLE IF NOT EXISTS horario_totens (
    totem   VARCHAR(26),
    horario TSRANGE,
    PRIMARY KEY (totem, horario),
    FOREIGN KEY (totem) REFERENCES totens_de_recarga (n_registro)
);

CREATE TABLE IF NOT EXISTS manutencao_infraestrutura (
    protocolo       UUID        NOT NULL DEFAULT gen_random_uuid(),
    horario         TSRANGE,
    status          VARCHAR(50),
    infraestrutura  VARCHAR(26) NOT NULL,
    gerente         VARCHAR(11) NOT NULL,
    PRIMARY KEY (protocolo),
    FOREIGN KEY (infraestrutura) REFERENCES infraestrutura (n_registro),
    FOREIGN KEY (gerente) REFERENCES gerente (cpf)
);

CREATE TABLE IF NOT EXISTS sessao_recarga (
    totem           VARCHAR(26),
    horario_inicio  TIMESTAMP,
    data            DATE,
    carro           VARCHAR(20),
    kwh_consumidos  NUMERIC(10,2),
    valor           NUMERIC(10,2),
    emissao_co2     NUMERIC(10,3),
    PRIMARY KEY (totem, horario_inicio, data, carro),
    FOREIGN KEY (carro) REFERENCES carro (placa),
    FOREIGN KEY (totem) REFERENCES totens_de_recarga (n_registro)
);

CREATE TABLE IF NOT EXISTS pontos_de_retirada (
    n_registro VARCHAR(26),
    capacidade INTEGER,
    status     STATUS_PONTO,
    voltagem   INTEGER       NOT NULL,
    bicicletas_disponiveis  INTEGER       NOT NULL,
    PRIMARY KEY (n_registro),
    FOREIGN KEY (n_registro) REFERENCES infraestrutura (n_registro)
);

CREATE TABLE IF NOT EXISTS retirada_bicicleta (
    bicicleta      VARCHAR(26),
    ponto_retirada VARCHAR(26),
    PRIMARY KEY (bicicleta, ponto_retirada),
    FOREIGN KEY (bicicleta) REFERENCES bicicleta (codigo),
    FOREIGN KEY (ponto_retirada) REFERENCES pontos_de_retirada (n_registro)
);

CREATE TABLE IF NOT EXISTS aluguel (
    horario_inicio     TIMESTAMP,
    data               DATE,
    bicicleta          VARCHAR(26),
    cliente            VARCHAR(11),
    origem             VARCHAR(150),
    destino            VARCHAR(150),
    horario_devolucao  TIMESTAMP,
    distancia          NUMERIC(10,2),
    valor              NUMERIC(10,2),
    PRIMARY KEY (horario_inicio, data, bicicleta, cliente),
    FOREIGN KEY (bicicleta) REFERENCES bicicleta (codigo),
    FOREIGN KEY (cliente) REFERENCES cliente (cpf)
);
