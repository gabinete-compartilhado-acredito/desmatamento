SELECT 
    data, id_servidor, desc_cargo, sigla_funcao, nivel_funcao, atividade, cod_uorg_lotacao, uorg_lotacao, cod_org_lotacao, org_lotacao, cod_orgsup_lotacao, orgsup_lotacao, 
    cod_uorg_exercicio, uorg_exercicio, cod_org_exercicio, org_exercicio, cod_orgsup_exercicio, orgsup_exercicio, situacao_vinculo, regime_juridico 
FROM `gabinete-compartilhado.executivo_federal_servidores.cadastro_civis_completo`
WHERE cod_org_exercicio = '40701'
ORDER BY data
