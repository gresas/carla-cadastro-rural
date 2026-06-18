---
sidebar_position: 4
title: Criar um Novo ADR
description: Quando e como criar um Architecture Decision Record no projeto CARla.
tags: [contribuindo, adr, arquitetura, decisões]
---

# Criar um Novo ADR

:::info Para quem é esta página
Engenheiros e arquitetos. Para ver os ADRs existentes, veja [Decisões Arquiteturais](../arquitetura/decisoes/index.md).
:::

## Quando criar um ADR?

Crie um ADR quando a decisão:

- Afeta múltiplos serviços ou camadas do sistema
- Tem implicações de segurança ou conformidade legal
- Envolve rejeitar uma alternativa popular e o "porquê" precisa estar documentado
- Pode ser questionada no futuro por novos membros do time

**Não** crie ADR para decisões triviais (ex: qual biblioteca de logging usar internamente em um serviço).

## Template

```markdown
---
sidebar_position: N
title: "ADR-00X: Título Descritivo"
description: Uma frase explicando a decisão tomada.
tags: [adr, área-afetada]
---

# ADR-00X: Título

**Status:** Aceito | **Data:** YYYY-MM-DD

## Contexto

[Descreva o problema, forças em conflito, requisitos e restrições que levaram à necessidade desta decisão]

## Decisão

[Descreva a decisão tomada, com exemplos de código quando relevante]

## Consequências

✅ [Benefício 1]
✅ [Benefício 2]
❌ [Desvantagem/limitação]

## Alternativas Rejeitadas

| Alternativa | Motivo da rejeição |
|---|---|
| Opção A | Por quê não |
| Opção B | Por quê não |
```

## Processo

1. **Criar o arquivo** em `website/docs/arquitetura/decisoes/adr-00X-titulo.md`
2. **Adicionar ao sidebar** em `website/sidebars.ts` (na lista de ADRs)
3. **Atualizar o índice** em `website/docs/arquitetura/decisoes/index.md`
4. **Abrir PR** para revisão do time
5. **Após aprovação:** status muda para "Aceito"

## Revisando uma Decisão Existente

Se uma decisão anterior ficou desatualizada:

1. Crie um **novo ADR** com a nova decisão
2. No novo ADR, mencione qual ADR anterior está sendo substituído
3. No ADR antigo, mude o status para `"Substituído por ADR-00X"`

> O ADR antigo **nunca é deletado** — faz parte da história de decisões do projeto.
