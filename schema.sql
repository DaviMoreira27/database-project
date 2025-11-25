CREATE TABLE IF NOT EXISTS endereco (
    cep        VARCHAR(8)      NOT NULL,
    rua        VARCHAR(150) NOT NULL,
    numero     VARCHAR(10)  NOT NULL,
    cidade     VARCHAR(100) NOT NULL,
    uf         CHAR(2)      NOT NULL,

    PRIMARY KEY (cep, rua, numero)
);

CREATE TABLE IF NOT EXISTS usuario (
    cpf             VARCHAR(11)      NOT NULL,
    cargo           VARCHAR(100)  NOT NULL,
    cep             VARCHAR(10)       NOT NULL,
    rua             VARCHAR(150)  NOT NULL,
    numero          VARCHAR(10)   NOT NULL,
    nome            VARCHAR(150)  NOT NULL,
    email           VARCHAR(150)  NOT NULL UNIQUE,
    senha           VARCHAR(200)  NOT NULL,
    data_nascimento DATE          NULL,
    PRIMARY KEY (cpf),
    FOREIGN KEY (cep, rua, numero)
        REFERENCES endereco (cep, rua, numero)
);


CREATE TABLE IF NOT EXISTS provedora {
    cnpj VARCHAR(16) NOT NULL -- 2 a mais por que sim,

    PRIMARY KEY (CNPJ),
}

CREATE TABLE IF NOT EXISTS gerente {
    cpf VARCHAR(11) NOT NULL,
    provedora VARCHAR(16) NOT NULL,

    PRIMARY KEY (cpf),
    FOREIGN KEY (provedora)
        REFERENCES provedora (cnpj)
}

CREATE TABLE IF NOT EXISTS cliente {
    cpf VARCHAR(11) NOT NULL,
    pontuacao NUMBER NULL,

    PRIMARY KEY (cpf),
}

CREATE TABLE IF NOT EXISTS administrador {
    cpf VARCHAR(11) NOT NULL,

    PRIMARY KEY (cpf),
}

CREATE TABLE IF NOT EXISTS infraestrutura (
    n_registro VARCHAR(26)  NOT NULL -- Gerado pela aplicação,
    provedora  VARCHAR(14)     NOT NULL,
    tipo       VARCHAR(100) NOT NULL -- TODO: Ponto de retirada ou estação de recarga, talvez seja bom colocar um ENUM,
    cep        VARCHAR(8)      NOT NULL,
    rua        VARCHAR(150) NOT NULL,
    numero     VARCHAR(10)  NOT NULL,

    PRIMARY KEY (n_registro),

    FOREIGN KEY (provedora)
        REFERENCES provedora (cnpj),

    FOREIGN KEY (cep, rua, numero)
        REFERENCES endereco (cep, rua, numero)
);

CREATE TABLE IF NOT EXISTS reporte_de_problema (
    protocolo       UUID         NOT NULL DEFAULT gen_random_uuid(),
    usuario         VARCHAR(11)     NOT NULL,
    infraestrutura  VARCHAR(26)  NOT NULL,
    data            TIMESTAMP    NOT NULL DEFAULT current_timestamp(),
    titulo          VARCHAR(100) NOT NULL,
    descricao       TEXT         NOT NULL,

    PRIMARY KEY (protocolo),

    FOREIGN KEY (usuario)
        REFERENCES usuario (cpf),

    FOREIGN KEY (infraestrutura)
        REFERENCES infraestrutura (n_registro)
);

CREATE TABLE IF NOT EXISTS avaliacao (
    id             UUID         NOT NULL DEFAULT gen_random_uuid(),
    infraestrutura VARCHAR(26)         NOT NULL,
    cliente        VARCHAR(11)     NOT NULL,
    nota           INTEGER        NOT NULL,
    descricao      TEXT         NULL,

    PRIMARY KEY (id),

    FOREIGN KEY (infraestrutura)
        REFERENCES infraestrutura (n_registro),

    FOREIGN KEY (cliente)
        REFERENCES cliente (cpf)
);

CREATE TYPE STATUS_BICICLETA AS ENUM (
    'MANUTENCAO',
    'EM_USO',
    'FORA_DE_SERVICO',
    'ESTACIONADO'
);

CREATE TABLE IF NOT EXISTS bicicleta (
    codigo        VARCHAR(26)        NOT NULL -- Gerado pela aplicação,
    provedora     VARCHAR(16)        NOT NULL,
    modelo        VARCHAR(100)    NULL,
    valor         NUMERIC(10,2)   NOT NULL -- TODO: Tenho que verificar oq isso deveria significar,
    bateria       INTEGER         NOT NULL,
    status        STATUS_BICICLETA NOT NULL,
    local_origem  VARCHAR(150)    NOT NULL -- TODO: Talvez tenhamos que por esse local_origem como uma FK para ponto_retirada

    PRIMARY KEY (codigo),

    FOREIGN KEY (provedora)
        REFERENCES provedora (cnpj)
);

CREATE TABLE IF NOT EXISTS carro (
    placa                 VARCHAR(20)   NOT NULL,
    cliente               VARCHAR(11)      NOT NULL,
    capacidade_bateria    INTEGER       NULL,
    autonomia             INTEGER       NULL,
    adaptador             VARCHAR(50)   NULL,
    modelo                VARCHAR(100)  NULL,

    PRIMARY KEY (placa),

    FOREIGN KEY (cliente)
        REFERENCES cliente (cpf)
);

CREATE TYPE STATUS_TOTEM AS ENUM (
    'ATIVO',
    'INATIVO',
    'MANUTENCAO'
);

CREATE TABLE IF NOT EXISTS totens_de_recarga (
    n_registro  VARCHAR(26)  NOT NULL,
    capacidade  INTEGER      NOT NULL,
    preco       NUMERIC(10,2) NOT NULL,
    voltagem    INTEGER      NOT NULL,
    conector    VARCHAR(50)  NOT NULL,
    potencia    INTEGER      NOT NULL,
    status      STATUS_TOTEM NOT NULL,

    PRIMARY KEY (n_registro)

    FOREIGN KEY (n_registro)
        REFERENCES infraestrutura (n_registro)
);

CREATE TABLE IF NOT EXISTS horario_totens (
    totem    VARCHAR(26) NOT NULL,
    horario  TSRANGE   NOT NULL,

    PRIMARY KEY (totem, horario),

    FOREIGN KEY (totem)
        REFERENCES totens_de_recarga (n_registro)
);

CREATE TABLE IF NOT EXISTS manutencao_infraestrutura (
    protocolo       UUID       NOT NULL DEFAULT gen_random_uuid(),
    horario         TSRANGE    NOT NULL,
    status          VARCHAR(50) NOT NULL,
    infraestrutura  VARCHAR(26)       NOT NULL,
    gerente         VARCHAR(11)   NOT NULL,

    PRIMARY KEY (protocolo),

    FOREIGN KEY (infraestrutura)
        REFERENCES infraestrutura (n_registro),

    FOREIGN KEY (gerente)
        REFERENCES gerente (cpf)
);

CREATE TABLE IF NOT EXISTS sessao_recarga (
    totem            VARCHAR(26)    NOT NULL,
    horario_inicio   TIMESTAMP      NOT NULL,
    data             DATE           NOT NULL,
    carro            VARCHAR(20)        NOT NULL,
    kwh_consumidos   NUMERIC(10,2)  NOT NULL,
    valor            NUMERIC(10,2)  NOT NULL,
    emissao_co2      NUMERIC(10,3)  NULL,

    PRIMARY KEY (totem, horario_inicio, data, carro),

    FOREIGN KEY (carro)
        REFERENCES carro (placa)
);

CREATE TYPE STATUS_PONTO AS ENUM (
    'VAZIO',
    'MANUTENCAO',
    'ATIVO'
);

CREATE TABLE IF NOT EXISTS pontos_de_retirada ( -- Tabela que armazena os pontos de retirada de bicicletas
    n_registro              VARCHAR(26)   NOT NULL, -- Gerado pela aplicação
    capacidade              INTEGER       NOT NULL, -- Quantidade total de biciletas que o ponto pode comportar
    bicicletas_disponiveis  INTEGER       NOT NULL, -- Numero de bicicletas atualmente disponíveis no ponto
    status                  STATUS_PONTO  NOT NULL, -- Status operacional do ponto de retirada: VAZIO, MANUNTECAO ou ATIVO
    voltagem                INTEGER       NOT NULL, -- Voltagem disponível no ponto (quando aplicável)

    PRIMARY KEY (n_registro)

    FOREIGN KEY (n_registro)
        REFERENCES infraestrutura (n_registro)
);

CREATE TABLE IF NOT EXISTS retirada_bicicleta (
    bicicleta       VARCHAR(26)     NOT NULL,
    ponto_retirada  VARCHAR(26)  NOT NULL,

    PRIMARY KEY (bicicleta, ponto_retirada),

    FOREIGN KEY (bicicleta)
        REFERENCES bicicleta (codigo),

    FOREIGN KEY (ponto_retirada)
        REFERENCES pontos_de_retirada (n_registro)
);
