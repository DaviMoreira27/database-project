-- 1. Totens ativos com média de KWh consumidos e total de sessões
SELECT 
    t.n_registro,
    AVG(s.kwh_consumidos) AS media_kwh,
    COUNT(s.totem) AS total_sessoes
FROM totens_de_recarga t
LEFT JOIN sessao_recarga s 
    ON s.totem = t.n_registro
WHERE t.status = 'ATIVO'
GROUP BY t.n_registro;

-- 2. Clientes que já avaliaram todas as infraestruturas que usaram (DIVISÃO RELACIONAL)
SELECT c.cpf, c.pontuacao
FROM cliente c
WHERE NOT EXISTS (
    SELECT 1
    FROM sessao_recarga s
    WHERE s.carro IN (
        SELECT placa 
        FROM carro 
        WHERE cliente = c.cpf
    )
    AND NOT EXISTS (
        SELECT 1
        FROM avaliacao a
        WHERE a.infraestrutura = s.totem
          AND a.cliente = c.cpf
    )
);

-- 3. Infraestruturas com mais de uma manutenção concluída
SELECT 
    m.infraestrutura,
    COUNT(*) AS total_manutencoes
FROM manutencao_infraestrutura m
WHERE m.status = 'Concluída'
GROUP BY m.infraestrutura
HAVING COUNT(*) > 1;

-- 4. Lista de bicicletas com nome da provedora, status e indicação se precisam de recarga
SELECT 
    b.codigo,
    b.modelo,
    b.bateria,
    b.status,
    p.cnpj AS provedora,
    CASE 
        WHEN b.bateria < 20 THEN 'SIM'
        ELSE 'NAO'
    END AS precisa_recarga
FROM bicicleta b
JOIN provedora p 
    ON b.provedora = p.cnpj;

-- 5. Ranking de usuários por quantidade total de problemas reportados
SELECT 
    u.cpf,
    u.nome,
    COUNT(r.protocolo) AS total_reportes
FROM usuario u
LEFT JOIN reporte_de_problema r 
    ON u.cpf = r.usuario
GROUP BY u.cpf, u.nome
ORDER BY total_reportes DESC;
