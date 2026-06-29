---
sidebar_position: 1
title: Glossário — Linguagem Ubíqua
description: 24 termos do domínio do CAR com definições precisas usadas em todo o projeto.
tags: [engenharia, ddd, glossário, domínio]
---

# Glossário — Linguagem Ubíqua

:::info Para quem é esta página
Engenheiros, PMs e designers. A linguagem ubíqua garante que todo o time fala a mesma coisa quando usa os mesmos termos. Não hesite em consultar esta página.
:::

> **Linguagem Ubíqua** é um termo do DDD (Domain-Driven Design). Significa que o código, os documentos, as conversas e a UI usam **exatamente os mesmos termos** para o mesmo conceito. Não "register" no código e "cadastro" na tela — sempre o mesmo.

---

| Termo | Definição no Domínio |
|---|---|
| **CAR** | Cadastro Ambiental Rural — registro eletrônico obrigatório de imóvel rural com dados geoespaciais e ambientais |
| **SICAR** | Sistema de Cadastro Ambiental Rural — sistema federal que centraliza todos os registros CAR do Brasil |
| **Processo CAR** | Fluxo de trabalho completo desde abertura até aprovação ou rejeição do registro |
| **Imóvel Rural** | Entidade geoespacial representando a propriedade a ser registrada, com geometria em SIRGAS 2000 |
| **Requerente** | Produtor rural ou possuidor do imóvel que solicita o registro CAR |
| **Proprietário** | Titular legal do imóvel, identificado pelo CPF/CNPJ na matrícula |
| **Analista** | Servidor público que avalia e decide sobre o processo |
| **Pendência** | Inconsistência ou documentação faltante que impede a aprovação |
| **Submissão** | Ato formal de enviar o processo para análise; gera o número de protocolo |
| **Protocolo** | Número gerado pelo SICAR no momento da submissão — é o identificador permanente do cadastro. Formato: `UF-NNNNNNN-NNNNNNNNNNNNNN`. Não é temporário: o número existe desde a submissão, independentemente do resultado da análise. |
| **Número CAR** | O mesmo número de protocolo gerado na submissão. Não é criado pelo analista na aprovação — já existe desde o momento em que o produtor envia o cadastro ao SICAR. |
| **Certificado CAR** | Documento oficial emitido pelo órgão ambiental estadual após análise concluída com resultado positivo. Comprova que o imóvel está regularmente cadastrado. Distinto do número de protocolo: o número existe desde a submissão; o Certificado só existe após a análise. |
| **Completude** | Score 0–100 indicando percentual de preenchimento do processo |
| **Score de Risco** | Pontuação 0–10 de risco ambiental baseada em dados externos (DETER, IBAMA) |
| **Geometria** | Representação geoespacial (polígono/multipolígono) do imóvel em SIRGAS 2000 (SRID 4674) |
| **Dossiê** | Documento PDF gerado automaticamente pelo CARla com todos os dados do processo |
| **Validação Documental** | Processo de OCR, extração e verificação de consistência dos documentos enviados |
| **APP** | Área de Preservação Permanente — faixa de vegetação obrigatoriamente preservada |
| **Reserva Legal** | Percentual mínimo de vegetação nativa que deve ser preservado por bioma |
| **Módulo Fiscal** | Unidade de medida agrária municipal — define a categoria do imóvel |
| **Bioma** | Região geográfica com características ecológicas que determina o percentual de RL |
| **Embargo** | Restrição legal ao uso do imóvel por infração ambiental (IBAMA) |
| **Recibo de Inscrição do Imóvel Rural no CAR** | Documento oficial gerado pelo SICAR após a análise do cadastro com resultado positivo. Comprova que o imóvel está regularmente inscrito no CAR. É o substituto do antigo "Certificado CAR" — o nome oficial é Recibo de Inscrição. |
| **Central do Proprietário/Possuidor** | Área do SICAR dedicada ao cidadão (proprietário ou possuidor do imóvel) para acompanhamento do status do cadastro, visualização de mensagens do analista e acesso ao Demonstrativo da Situação do CAR. |
| **Demonstrativo da Situação do CAR** | Documento gerado pelo SICAR que consolida a situação atual do cadastro do imóvel: status, pendências identificadas, situação de APP e Reserva Legal, e aba de Regularização Ambiental quando aplicável. |
| **Aba Regularização Ambiental** | Seção do Demonstrativo da Situação do CAR liberada quando o imóvel é identificado com passivo ambiental. É por esta aba que o proprietário formaliza a adesão ao PRA e acompanha o Termo de Compromisso. |
| **Termo de Compromisso** | Instrumento do PRA pelo qual o proprietário rural formaliza junto ao órgão ambiental o compromisso de regularizar o passivo ambiental dentro de um prazo estabelecido. Base legal: Decreto 7.830/2012. |
| **PRAD** | Projeto de Recuperação de Áreas Degradadas — plano técnico de recomposição de vegetação nativa, exigido em alguns casos como instrumento do PRA. |
| **CRA** | Cota de Reserva Ambiental — título representativo de vegetação nativa preservada além do mínimo exigido, que pode ser usado para compensação de déficit de Reserva Legal em outra propriedade. Base legal: art. 44 da Lei 12.651/2012. |
| **Responsável Técnico (RT)** | Profissional habilitado (engenheiro florestal, agrônomo ou técnico ambiental registrado no CREA/CONFEA/CFBio) que assina digitalmente o processo CAR e tem responsabilidade técnica e legal pelos dados prestados. Obrigatório para imóveis acima de 4 módulos fiscais na maioria dos estados. |
| **Status do cadastro (SICAR)** | Sequência oficial de status no SICAR: `Em Andamento` → `Cadastrado` → `Gravado/Enviado` → `Em Análise` → `Regular` ou `Pendente de Regularização`. Não usar termos genéricos como "aprovado" ou "rejeitado". |
| **PRA** | Programa de Regularização Ambiental — programa de recuperação de APP e Reserva Legal, exigido para imóveis com déficit ambiental após o cadastro. Base legal: art. 59 da Lei 12.651/2012 e arts. 6º e 7º do Decreto 7.830/2012. O CAR é pré-requisito para adesão ao PRA. |
| **Déficit Ambiental** | Situação em que a propriedade não atende os percentuais mínimos de APP ou Reserva Legal definidos pelo Código Florestal. Imóveis com déficit não são "rejeitados" — são aprovados com obrigação de aderir ao PRA. |
| **PSA** | Pagamento por Serviços Ambientais — programa que remunera proprietários rurais pela conservação de vegetação nativa. O CAR regularizado (`Regular`) é pré-requisito para participação. |
| **OEMA** | Órgão Estadual de Meio Ambiente — secretaria ou autarquia estadual responsável pela análise dos cadastros CAR no estado. É onde trabalham os analistas da Carla. Exemplos: SEMA-MT, SEMAD-GO, SEUC-AC, IPAAM-AM. |
| **Passivo Ambiental** | Situação de um imóvel com déficit de APP ou Reserva Legal identificado na análise do SICAR. Resulta no status `Pendente de Regularização` e obrigação de adesão ao PRA. Sinalizado com flag ⚠️ no painel do analista. |
| **Documento de Domínio** | Comprovante de propriedade ou posse apresentado na Etapa 3 (Domínio) do CAR. Tipos aceitos: Escritura, Contrato de Compra e Venda, Certidão de Registro, Autorização de Ocupação, Imissão de Posse, Termo de Autodeclaração. |
| **Conversa** | Sessão de chat com o assistente inteligente, com contexto preservado |
| **Base de Conhecimento** | Conjunto de documentos normativos indexados para o RAG do assistente IA |

---

## Percentuais de Reserva Legal por Bioma

:::tip Regra importante
O percentual mínimo de Reserva Legal varia por bioma conforme a Lei 12.651/2012:

| Bioma | Mínimo de RL |
|---|---|
| Amazônia Legal | 80% |
| Cerrado (Amazônia Legal) | 35% |
| Outros biomas | 20% |
:::

## Ver também

- [Bounded Contexts](./bounded-contexts.md) — como o domínio é organizado
- [Agregados e Entidades](./agregados.md) — modelos do domínio em código
- [Visão do Produto](../produto/visao.md) — contexto de negócio
