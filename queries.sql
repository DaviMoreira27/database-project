-- Qual porcentagem das bicicletas estacionadas da provedora cada ponto possui
SELECT
    pr.n_registro AS ponto_retirada,

    -- Quantas bicicletas estacionadas existem na provedora (conjunto divisor)
    (
        SELECT COUNT(*)
        FROM bicicleta b2
        WHERE b2.provedora = :cnpj_provedora
          AND b2.status = 'ESTACIONADO'
    ) AS total_estacionadas,

    -- Quantas dessas bicicletas o ponto contém
    (
        SELECT COUNT(DISTINCT b.codigo)
        FROM retirada_bicicleta rb
        JOIN bicicleta b ON b.codigo = rb.bicicleta
        WHERE rb.ponto_retirada = pr.n_registro
          AND b.provedora = :cnpj_provedora
          AND b.status = 'ESTACIONADO'
    ) AS estacionadas_no_ponto,

    -- Razão: (quantidade possuída / conjunto divisor)
    CASE
        WHEN (
            SELECT COUNT(*)
            FROM bicicleta b2
            WHERE b2.provedora = :cnpj_provedora
              AND b2.status = 'ESTACIONADO'
        ) = 0
        THEN 0
        ELSE
            (
                (
                    SELECT COUNT(DISTINCT b.codigo)
                    FROM retirada_bicicleta rb
                    JOIN bicicleta b ON b.codigo = rb.bicicleta
                    WHERE rb.ponto_retirada = pr.n_registro
                      AND b.provedora = :cnpj_provedora
                      AND b.status = 'ESTACIONADO'
                )::NUMERIC
                /
                (
                    SELECT COUNT(*)
                    FROM bicicleta b2
                    WHERE b2.provedora = :cnpj_provedora
                      AND b2.status = 'ESTACIONADO'
                )
            )
    END AS percentual_relacional

FROM pontos_de_retirada pr
JOIN infraestrutura i ON i.n_registro = pr.n_registro
WHERE i.provedora = :cnpj_provedora
ORDER BY percentual_relacional DESC;
-- RETORNO:
-- | ponto_retirada | total_estacionadas | estacionadas_no_ponto | percentual_relacional |
-- | -------------- | ------------------ | --------------------- | --------------------- |
-- | P10            | 3                  | 2                     | 0.6667                |
-- | P20            | 3                  | 1                     | 0.3333                |
-- | P30            | 3                  | 0                     | 0.0000                |

----------------------------------------------------------------------------------------------------------------------------

-- Para cada infraestrutura da provedora: conta quantos problemas foram reportados,
-- conta quantas avaliações ela recebeu, calcula a razão problemas/avaliações. e ordena da pior para melhor (dificil)
SELECT
    i.n_registro,

    COALESCE(
        (
            SELECT COUNT(*)
            FROM reporte_de_problema r
            WHERE r.infraestrutura = i.n_registro
        ),
        0
    ) AS problemas,

    COALESCE(
        (
            SELECT COUNT(*)
            FROM avaliacao a
            WHERE a.infraestrutura = i.n_registro
        ),
        0
    ) AS avaliacoes,

    CASE
        WHEN COALESCE(
                (SELECT COUNT(*) FROM avaliacao a WHERE a.infraestrutura = i.n_registro),
                0
             ) = 0
        THEN NULL
        ELSE
            COALESCE(
                (SELECT COUNT(*) FROM reporte_de_problema r WHERE r.infraestrutura = i.n_registro),
                0
            )::NUMERIC
            /
            (SELECT COUNT(*) FROM avaliacao a WHERE a.infraestrutura = i.n_registro)
    END AS razao_problema_por_avaliacao

FROM infraestrutura i
WHERE i.provedora = :cnpj_provedora
ORDER BY razao_problema_por_avaliacao DESC NULLS LAST;
-- RETORNO:
-- | n_registro | problemas | avaliacoes | razao_problema_por_avaliacao |
-- | ---------- | --------- | ---------- | ---------------------------- |
-- | INF1       | 2         | 2          | 1.0                          |
-- | INF2       | 0         | 1          | 0.0                          |
-- | INF3       | 1         | 0          |                              |

----------------------------------------------------------------------------------------------------------------------------

-- Taxa de ocupação de cada ponto (bicicletas disponíveis / capacidade) (media) ??????
SELECT
    pr.n_registro,
    pr.capacidade,
    pr.bicicletas_disponiveis,
    (pr.bicicletas_disponiveis::NUMERIC / pr.capacidade) AS taxa_ocupacao
FROM pontos_de_retirada pr
JOIN infraestrutura i ON i.n_registro = pr.n_registro
WHERE i.provedora = :cnpj_provedora;
-- RETORNO:
-- | n_registro | capacidade | bicicletas_disponiveis | taxa_ocupacao |
-- | ---------- | ---------- | ---------------------- | ------------- |
-- | P1         | 10         | 4                      | 0.32000000000 |
-- | P2         | 6          | 6                      | 0.32000000000 |

----------------------------------------------------------------------------------------------------------------------------

-- Soma total do valor das sessões de recarga por mês. (media)
SELECT
    DATE_TRUNC('month', sr.data) AS mes,
    SUM(sr.valor) AS receita
FROM sessao_recarga sr
JOIN totens_de_recarga td     ON td.n_registro = sr.totem
JOIN infraestrutura i         ON i.n_registro = td.n_registro
WHERE i.provedora = :cnpj_provedora
GROUP BY DATE_TRUNC('month', sr.data)
ORDER BY mes;
-- RETORNO:
-- | mes                     | receita  |
-- | ----------------------- | -----   |
-- | 2025-01-01 00:00:00+00 | 3000.00 |
-- | 2025-02-01 00:00:00+00 | 6423.00 |

----------------------------------------------------------------------------------------------------------------------------

-- Quantidade de sessões de recarga por dia. (media)
SELECT
    sr.data,
    COUNT(*) AS total_sessoes
FROM sessao_recarga sr
JOIN totens_de_recarga td ON td.n_registro = sr.totem
JOIN infraestrutura i ON i.n_registro = td.n_registro
WHERE i.provedora = :cnpj_provedora
GROUP BY sr.data
ORDER BY sr.data;
-- RETORNO:
-- | data       | total_sessoes |
-- | ---------- | ------------- |
-- | 2025-01-05 | 2             |
-- | 2025-01-06 | 3             |
