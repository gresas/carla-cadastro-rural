---
sidebar_position: 1
title: Princípios de UX
description: Diretrizes de design, acessibilidade e linguagem do CARla.
tags: [design, ux, acessibilidade, wcag]
---

# Princípios de UX

:::info Para quem é esta página
Designers, front-end engineers e redatores UX. Para contexto de negócio, veja [Visão do Produto](../produto/visao.md).
:::

## Princípios Fundamentais

### 1. Linguagem do cidadão, não do servidor

O CARla fala com produtores rurais que podem ter baixo letramento digital. Toda instrução deve ser compreensível sem formação técnica ou jurídica.

:::tip Como aplicar
- Use frases curtas e ativas: "Envie a matrícula do imóvel" em vez de "Proceda com o upload do documento comprobatório de propriedade"
- Explique o *porquê* antes do *como*: "Precisamos da matrícula para confirmar que o imóvel é seu"
- Evite siglas sem explicação: escreva "CAR (Cadastro Ambiental Rural)" na primeira menção
:::

### 2. Feedback imediato em cada etapa

O usuário nunca deve ficar sem saber o que está acontecendo. Cada ação deve ter resposta visual em < 200ms e texto de confirmação em < 3s.

| Estado | Resposta esperada |
|---|---|
| Upload iniciado | Barra de progresso + "Enviando..." |
| Upload concluído | "Recebido! Estamos verificando o documento." |
| Validação concluída | ✓ "Documento válido" ou ✗ "Problema encontrado — veja o que fazer" |
| Pendência criada | Notificação in-app + e-mail/WhatsApp com link direto |

### 3. Erros são oportunidades de orientação

Quando algo dá errado, o sistema não diz "Erro". Explica o que aconteceu e o que fazer.

:::warning Exemplo ruim
`"Documento inválido. Código de erro: VAL-422"`
:::

:::tip Exemplo bom
`"A matrícula enviada está ilegível — o texto não pôde ser lido. Tire uma nova foto com boa iluminação e sem reflexos. Veja como → [Dicas de digitalização]"`
:::

### 4. Progressão visível no processo

O cidadão precisa saber onde está e quanto falta. Use stepper com etapas nomeadas e porcentagem de completude.

### 5. Mobilidade em primeiro lugar

João Silva usa um smartphone Android básico em uma zona rural com conexão instável. O CARla deve funcionar bem em telas de 360px e com 3G.

---

## Acessibilidade — WCAG 2.1 AA

O CARla deve atingir o nível AA da WCAG 2.1 (Diretrizes de Acessibilidade para Conteúdo Web).

| Critério | Implementação |
|---|---|
| Contraste mínimo 4,5:1 | Verde `#1B5E20` sobre branco: 9,7:1 ✓ |
| Navegação por teclado | Todos os elementos interativos focáveis com Tab |
| Textos alternativos | Toda imagem com `alt` descritivo |
| Labels em formulários | Nenhum campo sem `<label>` associado |
| Mensagens de erro | Não usar apenas cor — incluir texto e ícone |
| Tamanho mínimo de toque | 44×44px para elementos clicáveis (mobile) |

:::caution Obrigação legal
A Lei Brasileira de Inclusão (Lei 13.146/2015) exige acessibilidade em serviços públicos digitais. Portais governamentais devem seguir o eMAG (Modelo de Acessibilidade em Governo Eletrônico).
:::

---

## Linguagem e Tom

| Contexto | Tom |
|---|---|
| Mensagens do assistente IA | Amigável, direto, sem juridiquês |
| Erros de validação | Explicativo, nunca culpado |
| Notificações de pendência | Claro e urgente, com próximo passo |
| Confirmações de ação | Positivo, conciso |
| Instruções do analista | Profissional, técnico quando necessário |

---

## Paleta de Cores

| Cor | Hex | Uso |
|---|---|---|
| Verde Escuro | `#1B5E20` | Primário — headers, CTAs principais |
| Verde Médio | `#2E7D32` | Botões, links, badges de sucesso |
| Verde Claro | `#66BB6A` | Hover states, highlights |
| Fundo Verde | `#E8F5E9` | Backgrounds de seção, cards |
| Vermelho Alerta | `#C62828` | Erros, rejeições |
| Laranja Atenção | `#E65100` | Pendências, avisos |
| Azul Info | `#1565C0` | Links, informações |

## Ver também

- [Personas UX](./personas.md) — quem usa e como pensa
- [Fluxo do Cidadão](./fluxos/cidadao.md) — jornada visual completa
- [Fluxo do Analista](./fluxos/analista.md) — jornada do analista
