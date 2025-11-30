CREATE TABLE IF NOT EXISTS endereco (
    cep        VARCHAR(8),
    rua        VARCHAR(150),
    numero     VARCHAR(10),
    cidade     VARCHAR(100),
    uf         CHAR(2),

    CONSTRAINT pk_endereco PRIMARY KEY (cep, rua, numero)
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

    CONSTRAINT pk_usuario PRIMARY KEY (cpf),
    CONSTRAINT fk_usuario_endereco
        FOREIGN KEY (cep, rua, numero) REFERENCES endereco (cep, rua, numero)
    CONSTRAINT chk_usuario_cargo CHECK (UPPER(cargo) IN ('GERENTE', 'CLIENTE', 'ADMINISTRADOR'))


);

CREATE TABLE IF NOT EXISTS provedora (
    cnpj VARCHAR(16),

    CONSTRAINT pk_provedora PRIMARY KEY (cnpj)
);

CREATE TABLE IF NOT EXISTS gerente (
    cpf       VARCHAR(11),
    provedora VARCHAR(16),

    CONSTRAINT pk_gerente PRIMARY KEY (cpf),
    CONSTRAINT fk_gerente_provedora FOREIGN KEY (provedora) REFERENCES provedora (cnpj),
    CONSTRAINT fk_gerente_usuario   FOREIGN KEY (cpf) REFERENCES usuario (cpf)
);

CREATE TABLE IF NOT EXISTS cliente (
    cpf        VARCHAR(11),
    pontuacao  NUMERIC SET DEFAULT 0,

    CONSTRAINT pk_cliente PRIMARY KEY (cpf),
    CONSTRAINT fk_cliente_usuario FOREIGN KEY (cpf) REFERENCES usuario (cpf)
);

CREATE TABLE IF NOT EXISTS administrador (
    cpf VARCHAR(11),

    CONSTRAINT pk_administrador PRIMARY KEY (cpf),
    CONSTRAINT fk_admin_usuario FOREIGN KEY (cpf) REFERENCES usuario (cpf)
);

CREATE TABLE IF NOT EXISTS infraestrutura (
    n_registro VARCHAR(26)  NOT NULL,
    provedora  VARCHAR(16)  NOT NULL,
    tipo       VARCHAR(100) NOT NULL,
    cep        VARCHAR(8)   NOT NULL,
    rua        VARCHAR(150) NOT NULL,
    numero     VARCHAR(10)  NOT NULL,

    CONSTRAINT pk_infraestrutura PRIMARY KEY (n_registro, provedora),
    CONSTRAINT fk_infra_provedora FOREIGN KEY (provedora) REFERENCES provedora (cnpj),
    CONSTRAINT fk_infra_endereco FOREIGN KEY (cep, rua, numero) REFERENCES endereco (cep, rua, numero),
    CONSTRAINT chk_usuario_cargo CHECK (UPPER(cargo) IN ('TOTENS_DE_RECARGA', 'PONTOS_DE_RETIRADA'))
    UNIQUE (cep, rua, numero)
);

CREATE TABLE IF NOT EXISTS reporte_de_problema (
    protocolo       UUID          NOT NULL DEFAULT gen_random_uuid(),
    usuario         VARCHAR(11)   NOT NULL,
    infraestrutura  VARCHAR(26)   NOT NULL,
    data            TIMESTAMP     NOT NULL DEFAULT current_timestamp,
    titulo          VARCHAR(100)  NOT NULL,
    descricao       TEXT,

    CONSTRAINT pk_reporte PRIMARY KEY (protocolo),
    CONSTRAINT fk_reporte_usuario FOREIGN KEY (usuario) REFERENCES usuario (cpf),
    CONSTRAINT fk_reporte_infra FOREIGN KEY (infraestrutura) REFERENCES infraestrutura (n_registro)
);

CREATE TABLE IF NOT EXISTS avaliacao (
    id             UUID          NOT NULL DEFAULT gen_random_uuid(),
    infraestrutura VARCHAR(26),
    cliente        VARCHAR(11)   NOT NULL,
    nota           INTEGER,
    descricao      TEXT,

    CONSTRAINT pk_avaliacao PRIMARY KEY (id),
    CONSTRAINT fk_avaliacao_infra FOREIGN KEY (infraestrutura) REFERENCES infraestrutura (n_registro),
    CONSTRAINT fk_avaliacao_cliente FOREIGN KEY (cliente) REFERENCES cliente (cpf)
);

CREATE TABLE IF NOT EXISTS bicicleta (
    codigo        VARCHAR(26),
    provedora     VARCHAR(16),
    modelo        VARCHAR(100),
    valor         NUMERIC(10,2),
    bateria       INTEGER NOT NULL,
    status        STATUS_BICICLETA,
    local_origem  VARCHAR(26),

    CONSTRAINT pk_bicicleta PRIMARY KEY (codigo),
    CONSTRAINT fk_bicicleta_provedora FOREIGN KEY (provedora) REFERENCES provedora (cnpj)
);

CREATE TABLE IF NOT EXISTS carro (
    placa                VARCHAR(20),
    cliente              VARCHAR(11)  NOT NULL,
    capacidade_bateria   INTEGER,
    autonomia            INTEGER,
    adaptador            VARCHAR(50)  NOT NULL,
    modelo               VARCHAR(100),

    CONSTRAINT pk_carro PRIMARY KEY (placa),
    CONSTRAINT fk_carro_cliente FOREIGN KEY (cliente) REFERENCES cliente (cpf),
    CONSTRAINT fk_ck_capacidade_bateria CHECK(capacidade_bateria > 0)
);

CREATE TABLE IF NOT EXISTS totens_de_recarga (
    n_registro  VARCHAR(26),
    provedora   VARCHAR(16) NOT NULL,
    capacidade  INTEGER,
    preco       NUMERIC(10,2),
    voltagem    INTEGER NOT NULL,
    conector    VARCHAR(50),
    potencia    INTEGER,
    status      STATUS_TOTEM,

    CONSTRAINT pk_toten PRIMARY KEY (n_registro, provedora),
    CONSTRAINT fk_toten_infra FOREIGN KEY (n_registro) REFERENCES infraestrutura (n_registro),
    CONSTRAINT fk_provedora FOREIGN KEY (provedora) REFERENCES provedora (cnpj),
    CONSTRAINT ck_to_capacidade CHECK(capacidade > 0),
    CONSTRAINT ck_to_potencia CHECK(potencia > 0)
);

CREATE TABLE IF NOT EXISTS horario_totens (
    totem   VARCHAR(26),
    horario TSRANGE,
    provedora VARCHAR(16) NOT NULL,

    CONSTRAINT pk_horario_totens PRIMARY KEY (totem, horario, provedora),
    CONSTRAINT fk_horario_toten FOREIGN KEY (totem) REFERENCES totens_de_recarga (n_registro),
    CONSTRAINT fk_provedora_horario FOREIGN KEY (provedora) REFERENCES provedora (cnpj)
);

CREATE TABLE IF NOT EXISTS manutencao_infraestrutura (
    protocolo       UUID NOT NULL DEFAULT gen_random_uuid(),
    horario         TSRANGE,
    status          VARCHAR(50),
    infraestrutura  VARCHAR(26) NOT NULL,
    gerente         VARCHAR(11) NOT NULL,

    CONSTRAINT pk_manutencao PRIMARY KEY (protocolo),
    CONSTRAINT fk_manutencao_infra FOREIGN KEY (infraestrutura) REFERENCES infraestrutura (n_registro),
    CONSTRAINT fk_manutencao_gerente FOREIGN KEY (gerente) REFERENCES gerente (cpf)
);

CREATE TABLE IF NOT EXISTS sessao_recarga (
    totem           VARCHAR(26),
    horario_inicio  TIMESTAMP,
    data            DATE,
    carro           VARCHAR(20),
    kwh_consumidos  NUMERIC(10,2),
    valor           NUMERIC(10,2),
    emissao_co2     NUMERIC(10,3),

    CONSTRAINT pk_sessao_recarga PRIMARY KEY (totem, horario_inicio, data, carro),
    CONSTRAINT fk_sessao_carro FOREIGN KEY (carro) REFERENCES carro (placa),
    CONSTRAINT fk_sessao_toten FOREIGN KEY (totem) REFERENCES totens_de_recarga (n_registro)
);

CREATE TABLE IF NOT EXISTS pontos_de_retirada (
    n_registro VARCHAR(26),
    capacidade INTEGER,
    status     STATUS_PONTO,
    voltagem   INTEGER NOT NULL,
    bicicletas_disponiveis INTEGER NOT NULL,
    provedora  VARCHAR(16) NOT NULL,

    CONSTRAINT pk_ponto_retirada PRIMARY KEY (n_registro, provedora),
    CONSTRAINT fk_provedora_retirada FOREIGN KEY (provedora) REFERENCES provedora (cnpj),
    CONSTRAINT fk_pontos_infra FOREIGN KEY (n_registro) REFERENCES infraestrutura (n_registro),
    CONSTRAINT ck_capacidade CHECK(capacidade > 0)
);

CREATE TABLE IF NOT EXISTS retirada_bicicleta (
    bicicleta      VARCHAR(26),
    ponto_retirada VARCHAR(26),

    CONSTRAINT pk_retirada_bicicleta PRIMARY KEY (bicicleta, ponto_retirada),
    CONSTRAINT fk_retirada_bicicleta_bike FOREIGN KEY (bicicleta) REFERENCES bicicleta (codigo),
    CONSTRAINT fk_retirada_ponto FOREIGN KEY (ponto_retirada) REFERENCES pontos_de_retirada (n_registro)
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

    CONSTRAINT pk_aluguel PRIMARY KEY (horario_inicio, data, bicicleta, cliente),
    CONSTRAINT fk_aluguel_bicicleta FOREIGN KEY (bicicleta) REFERENCES bicicleta (codigo),
    CONSTRAINT fk_aluguel_cliente FOREIGN KEY (cliente) REFERENCES cliente (cpf)
);
