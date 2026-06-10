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
| **Vinculação WhatsApp** | Associação entre um número de WhatsApp e um usuário autenticado via Gov.br |
| **Responsável Técnico (RT)** | Profissional habilitado (engenheiro florestal, agrônomo ou técnico ambiental registrado no CREA/CONFEA/CFBio) que assina digitalmente o processo CAR e tem responsabilidade técnica e legal pelos dados prestados. Obrigatório para imóveis acima de 4 módulos fiscais na maioria dos estados. |
| **PRA** | Programa de Regularização Ambiental — programa de recuperação de APP e Reserva Legal, exigido para imóveis com déficit ambiental após o cadastro. Base legal: art. 59 da Lei 12.651/2012. O CAR é pré-requisito para adesão ao PRA. |
| **Déficit Ambiental** | Situação em que a propriedade não atende os percentuais mínimos de APP ou Reserva Legal definidos pelo Código Florestal. Imóveis com déficit não são "rejeitados" — são aprovados com obrigação de aderir ao PRA. |
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
