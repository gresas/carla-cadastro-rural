---
sidebar_position: 4
title: Sequência de Mensagens
description: Scripts completos das mensagens da Carla — abertura, criação do CAR (6 etapas), acompanhamento de status e dúvidas.
tags: [design, ux, carla, mensagens, roteiro]
---

# Sequência de Mensagens da Carla

:::info Para quem é esta página
Designers, redatores e engenheiros de IA. Este documento registra o roteiro oficial de conversas da Carla, alinhado à terminologia oficial do SICAR (manual do Módulo de Cadastro v3.2, Central do Proprietário/Possuidor), à Lei 12.651/2012 e ao Decreto 7.830/2012, e ao fluxo real de cadastro do Acre.

Para os fluxos visuais de abertura, veja [Abertura da Carla](./abertura-carla.md). Para os casos de uso formais, veja [Casos de Uso](../../produto/casos-de-uso.md).
:::

**Princípio de design:** a Carla nunca pede de novo um dado que já recebeu. Ela reaproveita, pré-preenche e pede apenas confirmação — e fecha cada etapa com um resumo único em bloco para revisão, em vez de confirmar campo a campo.

---

## 1. Mensagens de Abertura

### Cenário A — Primeiro acesso (sem login)

> Mensagem exibida ao cidadão que ainda não autenticou com Gov.br.

```
Olá! Eu sou a Carla, assistente virtual do Cadastro Ambiental Rural (CAR).

Posso te ajudar a:
🌱 Criar seu CAR do zero
💬 Tirar dúvidas sobre o CAR e seu processo
📬 Acompanhar mensagens e pendências do seu analista ambiental

Para começar, preciso confirmar sua identidade pelo Gov.br.
Pode clicar no botão abaixo para entrar com segurança.

[ 🔑 Entrar com Gov.br ]
```

### Cenário B — Logado, sem nenhum CAR iniciado

```
Olá, {nome}! Que bom te ver por aqui. 😊

Vi que você ainda não iniciou nenhum cadastro de imóvel rural.
Quer começar agora?
Eu te guio passo a passo, é mais simples do que parece.

[ 🌱 Iniciar meu CAR ] [ ❓ Tenho dúvidas antes ]
```

### Cenário C — Logado, com CAR em andamento, sem pendências novas

```
Olá de novo, {nome}! 🌿

Seu cadastro do imóvel "{nome_propriedade}" está na etapa {etapa_atual}.
Quer continuar de onde parou?

[ ▶️ Continuar cadastro ] [ 📊 Ver status completo ]
```

### Cenário D — Logado, com mensagens não lidas do analista

```
Olá, {nome}! Tenho uma novidade importante. 📬

Você tem {qtd} mensagem(ns) do analista ambiental sobre o seu CAR
"{nome_propriedade}", e pelo menos uma precisa de retorno seu.
Quer ver agora?

[ 📬 Ver mensagens ] [ 📊 Ver status do CAR ]
```

---

## 2. Mensagens de Criação do CAR

### Abertura do fluxo

```
Vamos criar seu Cadastro Ambiental Rural! Vai levar alguns minutos, mas pode parar e
voltar quando quiser — eu salvo seu progresso automaticamente.

Antes de começar: o imóvel que você vai cadastrar é um imóvel rural comum, certo?
(Imóveis de povos tradicionais ou assentamentos da reforma agrária seguem outro
fluxo, restrito a entidades específicas.)

[ ✅ Sim, é um imóvel rural comum ] [ ❓ Não tenho certeza ]
```

---

### Etapa 1 — Cadastrante

```
Vamos começar com seus dados como cadastrante.
Qual é o seu CPF?
```

```
Obrigada! Agora sua data de nascimento (dd/mm/aaaa):
```

```
Perfeito. Qual é o seu nome completo, exatamente como está no seu CPF?
```

```
E o nome da sua mãe?
```

```
Última pergunta dessa etapa: você tem um representante legal atuando neste cadastro?

[ Não possuo representante ] [ Possuo, e sou eu o cadastrante ] [ Possuo, mas não sou eu o cadastrante ]
```

**Confirmação em bloco:**

```
Confirma os dados do cadastrante?

👤 Nome: {nome}
🪪 CPF: {cpf}
📅 Nascimento: {data_nascimento}
👩 Nome da mãe: {nome_mae}
📋 Representante: {situacao_representante}

[ ✅ Está tudo certo, continuar ] [ ✏️ Quero corrigir algo ]
```

```
✅ Dados do cadastrante confirmados! Vamos para os dados do imóvel.
```

---

### Etapa 2 — Imóvel

```
Agora vamos identificar o imóvel. Qual é o nome do imóvel?
```

```
Em qual município ele está localizado? Se souber, me passa também o CEP.
```

```
Me descreva, em poucas palavras, como é o acesso ao imóvel (estradas, referências,
distância da sede do município etc.). Essa descrição ajuda o analista a localizar
fisicamente a propriedade.
```

```
A zona de localização do imóvel é Rural ou Urbana?

[ 🌱 Rural ] [ 🏙️ Urbana ]
```

**Reaproveitando dados já informados:**

```
O endereço de correspondência é o mesmo endereço/CEP do imóvel que você já me
passou ({municipio_imovel}, CEP {cep_imovel}), ou é outro endereço para receber
notificações?

[ ✅ É o mesmo endereço ] [ 📍 É um endereço diferente ]
```

*(Se endereço diferente:)*
```
Sem problemas. Me passa então: endereço/logradouro, número, complemento, bairro, CEP, UF e município.
```

```
Por fim (opcional), você quer informar um e-mail e/ou telefone de contato adicionais para esse imóvel?
```

**Confirmação em bloco:**

```
Confirma os dados do imóvel?

🏡 Nome: {nome_imovel}
📍 Município: {municipio_imovel} — CEP {cep_imovel}
🌱 Zona: {zona}
✉️ Correspondência: {endereco_correspondencia}

[ ✅ Está tudo certo, continuar ] [ ✏️ Quero corrigir algo ]
```

```
✅ Dados do imóvel confirmados! Vamos para a etapa de Domínio.
```

---

### Etapa 3 — Domínio (proprietário/possuidor)

```
Agora preciso saber quem é o(s) proprietário(s) ou possuidor(es) do imóvel.
Pode ter mais de um — vamos adicionar um de cada vez.
```

**Reaproveitando os dados do cadastrante:**

```
Você (cadastrante) é também um dos proprietários ou possuidores desse imóvel?
Se sim, já tenho seus dados: {nome}, CPF {cpf} — só preciso de uma foto do seu CPF para confirmar.

[ ✅ Sim, sou eu mesmo ] [ ✏️ Não, é outra pessoa ]
```

*(Se outra pessoa — pessoa física:)*

```
Entendido. O proprietário é pessoa física ou pessoa jurídica?

[ 👤 Pessoa Física ] [ 🏢 Pessoa Jurídica ]
```

```
Certo! Preciso de: CPF, data de nascimento, nome completo e nome da mãe do proprietário.
Pode me passar o CPF?
```

*(...segue coletando nome, data de nascimento, nome da mãe...)*

```
Por fim, preciso de uma foto do CPF dele(a). Pode enviar a imagem aqui mesmo na conversa. 📷
```

*(Se pessoa jurídica:)*

```
Entendido. Preciso do CNPJ da empresa, nome da empresa e, se tiver, nome fantasia.
```

*(...segue coletando CNPJ, nome, nome fantasia...)*

```
Agora os dados do representante legal: CPF, data de nascimento, nome, nome da mãe, e-mail e telefone.
```

```
O endereço do representante legal é o mesmo que você já me passou para o imóvel, ou é outro?

[ ✅ É o mesmo endereço ] [ 📍 É um endereço diferente ]
```

```
Por último, me envie uma imagem que comprove o CNPJ. 📷
```

> 💡 *Dica: se você já tem esses dados organizados em uma planilha, posso importar tudo de uma vez via CSV — só anexar o arquivo aqui que eu confiro pra você.*

**Confirmação em bloco a cada proprietário:**

```
Confirma os dados desse proprietário/possuidor?

👤 {tipo_pessoa}: {nome_proprietario}
🪪 {documento_label}: {documento_numero}
📷 Comprovante: recebido

[ ✅ Está certo, adicionar ] [ ✏️ Quero corrigir algo ]
```

```
✅ Proprietário adicionado! Tem mais algum proprietário ou possuidor para incluir?

[ ➕ Adicionar outro ] [ ▶️ Seguir para documentação ]
```

---

### Etapa 4 — Documentação

```
Agora vamos à parte de documentação.
O imóvel é uma Propriedade (você tem o título/matrícula) ou uma Posse (você ocupa, mas ainda não tem o domínio formal)?

[ 📄 Propriedade ] [ 🌱 Posse ]
```

*(Se Propriedade:)*

```
Já uso o nome e a localização que você me passou na etapa do imóvel ({nome_imovel}, {municipio_imovel}).
Só preciso confirmar a área total em hectares e o tipo de documento (contrato de compra e venda, escritura,
certidão de registro, em regularização ou imissão de posse).
```

```
Você tem o número da matrícula ou documento? Se sim, vou pedir também a data, livro, folha, UF e município
do cartório. Se não tiver, podemos seguir sem isso.
```

```
Você também tem (se aplicável): código no SNCR, certificação no INCRA, ou NIRF?
Pode informar o que tiver — nenhum é obrigatório.
```

```
Agora uma pergunta importante: o imóvel possui Reserva Legal averbada e/ou aprovada e não averbada?

[ Sim ] [ Não ]
```

*(Se Sim:)*

```
Beleza, preciso de mais alguns dados: número da averbação/documento, data da averbação e área (ha).
```

```
E essa Reserva Legal está dentro do imóvel que você está cadastrando?

[ Sim, está dentro ] [ Não, está em outro imóvel ]
```

*(Se em outro imóvel:)*

```
Sem problemas. Me passa o número de registro no CAR do imóvel onde essa Reserva Legal está localizada.
```

```
Já tenho o endereço do imóvel das etapas anteriores. A localização do documento de propriedade é a mesma, ou é diferente?

[ ✅ É a mesma ] [ 📍 É diferente ]
```

```
Por fim, preciso que você anexe imagens que comprovem a propriedade e os dados que você informou.
Pode mandar aqui mesmo. 📷
```

*(Se Posse:)*

```
Entendido, vamos pelo caminho de Posse. Já uso o nome e a localização que você já me passou ({nome_imovel}, {municipio_imovel}).
Só preciso confirmar a área (ha) e qual o tipo de documento que você tem:
Autorização de Ocupação, Carta de Anuência, Contratos diversos, Declarações, Licença de ocupação,
Termo de autodeclaração, Termo de doação, Títulos diversos, etc.
```

> 💡 *Os campos seguintes mudam um pouco dependendo do tipo de documento escolhido — eu já ajusto as perguntas automaticamente para combinar com o seu caso.*

*(...coleta campos específicos: emissor, data, ou dados do vendedor, conforme o tipo...)*

```
E para fechar, anexe a imagem do documento que você preencheu/possui. 📷
```

**Confirmação em bloco:**

```
Confirma os dados do documento?

📄 Tipo: {tipo_documento}
🌱 Área: {area_ha} ha
🌿 Reserva Legal averbada: {tem_reserva_legal}
📍 Localização: {localizacao_documento}
📷 Imagens: recebidas

[ ✅ Está tudo certo, continuar ] [ ✏️ Quero corrigir algo ]
```

```
✅ Documentação registrada! Próxima etapa: a parte do mapa.
```

---

### Etapa 5 — Geo

```
Agora vem a parte do mapa! Esta é a etapa que mais costuma gerar dúvida — então vou com calma aqui.

Como você já me informou a área aproximada ({area_ha} ha) e o município ({municipio_imovel}),
já consigo te mostrar uma demarcação de polígonos sugerida para essa região.
Você confere e ajusta o que achar necessário — não precisa desenhar do zero.

[ 🗺️ Ver demarcação sugerida ]
```

```
Aqui está a sugestão com base nos seus dados. Se houver Reserva Legal ou área de preservação dentro
do imóvel, eu já destaco onde normalmente ficam, mas você pode mover, redesenhar ou ajustar qualquer parte.

[ ✅ Está correto, confirmar ] [ ✏️ Quero ajustar o desenho ]
```

> **Nota de produto:** aqui entra a funcionalidade de mapa visual — pré-carregar a região com base nos dados já informados (nome do imóvel, município, área declarada) e sugerir uma demarcação inicial, sempre editável pelo usuário.

```
✅ Área do imóvel definida! Última etapa: algumas perguntas sobre a situação ambiental do imóvel.
```

---

### Etapa 6 — Informações (PRA e situação ambiental)

```
Essa última parte é só um questionário de sim/não sobre a situação ambiental do imóvel.
Pode parecer extensa, mas a maioria das perguntas só pede mais detalhes se você responder "Sim"
— então vai ser rápido se a resposta for "Não" na maioria.
Como você já me disse que {tem_reserva_legal_resumo}, algumas dessas perguntas eu já posso
pré-marcar para você só confirmar.

Vamos lá:
```

**Pergunta 1 — Adesão ao PRA:**

```
1. Deseja aderir ao Programa de Regularização Ambiental (PRA), caso o imóvel se enquadre em
alguma situação ocorrida até 22/07/2008 (déficit de Reserva Legal, necessidade de recomposição
de APP, etc.)?

[ Sim ] [ Não ]
```

*(Se Sim — modal de confirmação):*
```
⚠️ Essa opção assegura o cumprimento do prazo de requerimento de adesão ao PRA,
previsto na Lei 12.651/12. Deseja confirmar?

[ Cancelar ] [ Confirmar ]
```

*(Se Não — modal de confirmação):*
```
⚠️ Ao final do prazo de requerimento de adesão ao PRA, você não poderá mais requerer
os benefícios previstos no programa. Deseja confirmar mesmo assim?

[ Cancelar ] [ Confirmar ]
```

**Perguntas 2 a 12** (resumo — a Carla exibe uma de cada vez):

```
2. O imóvel possui área com déficit de vegetação nativa para fins de cumprimento da Reserva Legal?
   [ Sim ] → Qual alternativa para regularizar: Compensar / Regeneração natural / Recompor
   [ Não ]

3. Existe Termo de Ajuste de Conduta (TAC) aprovado referente à regularização de APP, Reserva Legal
   ou área de uso restrito?
   [ Sim ] → Órgão emitente, data de assinatura e data de encerramento
   [ Não ]

4. Existe Projeto de Recuperação de Áreas Degradadas (PRAD) ou outro documento aprovado?
   [ Sim ] → Órgão emitente, data de assinatura e data de encerramento
   [ Não ]

5. Existem infrações cometidas até 22/07/2008, relativas à supressão irregular de vegetação?
   [ Sim ] [ Não ] — não pede mais nada além da resposta

6. O imóvel possui área remanescente de vegetação nativa excedente ao mínimo exigido para Reserva Legal?
   [ Sim ] → O que deseja fazer: Servidão ambiental / Arrendamento / CRA / Outro imóvel / Outros fins
   [ Não ]

7. Existe Reserva Particular do Patrimônio Natural (RPPN) no interior do imóvel?
   [ Sim ] → Área (ha), data de publicação, número do decreto/portaria
   [ Não ]

8. Possui Cota de Reserva Florestal (CRF)?
   [ Sim ] [ Não ]

9. A Reserva Legal está submetida à legislação de qual período?
   → Lista de períodos de 1934 até 2012 (pode marcar mais de uma)

10. Ocorreu alteração no tamanho da área do imóvel após 22/07/2008?
    [ Sim ] → Qual era a área (ha) em 22/07/2008?
    [ Não ]

11. Possui Licenciamento Ambiental?
    [ Sim ] → Número do licenciamento (pode adicionar mais de um)
    [ Não ]

12. Possui Multa Ambiental?
    [ Sim ] → Órgão emissor e número da multa (pode adicionar mais de uma)
    [ Não ]
```

**Resumo final antes de enviar:**

```
Antes de finalizar, aqui está um resumo geral do seu CAR:

🏡 Imóvel: {nome_imovel} — {municipio_imovel}, {area_ha} ha
👤 Cadastrante: {nome}
👥 Proprietários/possuidores: {qtd_proprietarios}
📄 Documentação: {tipo_documento}
🗺️ Geo: demarcado e confirmado
🌿 PRA: {situacao_pra}

[ ✅ Tudo certo, finalizar cadastro ] [ ✏️ Quero revisar alguma etapa ]
```

```
🎉 Pronto, {nome}! Você concluiu todas as etapas do seu CAR. Agora seu cadastro vai para análise
de um analista ambiental. Eu te aviso assim que houver qualquer atualização ou mensagem sobre ele.

[ 📊 Ver resumo do meu cadastro ]
```

---

## 3. Mensagens de Acompanhamento do CAR

> Os status abaixo seguem a terminologia oficial do SICAR (módulo de cadastro + Central do Proprietário/Possuidor): **Em Andamento → Cadastrado → Gravado/Enviado → Em Análise → Regular ou Pendente de Regularização**.

```
Seu cadastro "{nome_propriedade}" está na etapa: {etapa_atual}.

📅 Última atualização: {data}
📋 Status: {status}
```

### Se Em Andamento (cadastro incompleto)

```
Você ainda não finalizou seu cadastro — está parado na etapa {etapa_atual} desde {data}.
Quer continuar agora?

[ ▶️ Continuar de onde parei ]
```

### Se Cadastrado, mas ainda não enviado

```
Você já preencheu todas as etapas do seu CAR, mas ele ainda não foi enviado para análise.
Falta só confirmar o envio.

[ 📤 Enviar meu CAR agora ]
```

### Se Em Análise

```
Seu CAR foi enviado e está em análise pelo órgão ambiental responsável.
Recibo de Inscrição: {numero_recibo}

Assim que houver qualquer retorno do analista, eu te aviso por aqui.
```

### Se Pendente de Regularização (com retorno do analista)

```
⚠️ Seu CAR foi analisado e está Pendente de Regularização — o analista identificou
um ponto que precisa da sua atenção:

"{trecho_da_mensagem}"

Isso precisa da sua resposta para o processo continuar. Você também pode aderir ao
Programa de Regularização Ambiental (PRA) para regularizar essa pendência.

[ 📬 Ver mensagem completa ] [ ✍️ Responder agora ] [ 🌿 Saber mais sobre o PRA ]
```

### Se Regular

```
✅ Boas notícias! Seu CAR está Regular desde {data}.

Recibo de Inscrição do Imóvel Rural no CAR: {numero_recibo}

[ 📄 Baixar Recibo de Inscrição ]
```

---

## 4. Mensagens de Dúvidas sobre o CAR

### Dúvidas gerais (conceito)

> *Exemplo de pergunta: "O que é o CAR?"*

```
Claro, posso te explicar! 😊

O CAR — Cadastro Ambiental Rural — é um registro público eletrônico obrigatório para
todos os imóveis rurais do Brasil. Ele reúne informações ambientais da propriedade,
como Áreas de Preservação Permanente, Reserva Legal e remanescentes de vegetação nativa.

Tem mais alguma dúvida sobre isso, ou posso te ajudar a iniciar seu cadastro?

[ ❓ Tenho outra dúvida ] [ 🌱 Quero iniciar meu CAR ]
```

### Dúvidas sobre o processo (etapas)

> *Exemplo de pergunta: "Por que estão me pedindo a Reserva Legal averbada?"*

```
Boa pergunta! Você está perguntando sobre uma etapa específica do seu cadastro,
ou é uma dúvida geral sobre como o processo funciona?

Essa pergunta aparece porque, se você marcou que possui Reserva Legal já averbada
(registrada em cartório) ou aprovada, o sistema precisa registrar onde e como ela está
formalizada — isso evita que seu cadastro seja questionado depois por falta de comprovação.

Quer que eu te ajude a responder essa parte agora, com base no seu caso?

[ ✅ Sim, me ajuda a preencher ] [ 👍 Só queria entender, obrigado ]
```

### Dúvida sobre PRA (Programa de Regularização Ambiental)

> *Exemplo de pergunta: "O que acontece depois que meu CAR é analisado?"*

```
Depois que seu CAR é analisado pelo órgão ambiental, duas coisas podem acontecer:

✅ Se está tudo certo, seu cadastro fica com status Regular.
⚠️ Se for identificado algum passivo ambiental (por exemplo, déficit de Reserva Legal
ou necessidade de recompor APP), o cadastro fica Pendente de Regularização e a aba
Regularização Ambiental é liberada para você.

Nesse caso, você pode aderir ao PRA (Programa de Regularização Ambiental). Ao aderir,
você formaliza um Termo de Compromisso com o órgão ambiental, se comprometendo a
regularizar a pendência dentro do prazo combinado.

[ 🌿 Quero aderir ao PRA ] [ ❓ Tenho outra dúvida ]
```

### Dúvida técnica — encaminhamento ao analista

```
Essa é uma pergunta mais específica, e quero te dar uma resposta certa, não um chute.
Vou encaminhar para o seu analista ambiental, que pode esclarecer com mais segurança.

Posso registrar essa pergunta para ele?

[ ✅ Sim, encaminhar ] [ ❌ Não, deixa pra lá ]
```

---

## Ver também

- [Abertura da Carla](./abertura-carla.md) — fluxo de entrada pelo car.gov.br e os 4 cenários
- [Fluxo do Cidadão](./cidadao.md) — diagrama visual das 6 etapas
- [Fundamentação Legal](../../dominio/fundamentacao-legal.md) — Lei 12.651/2012 e Decreto 7.830/2012
- [Glossário](../../dominio/glossario.md) — terminologia oficial do SICAR
