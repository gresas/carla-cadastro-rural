---
sidebar_position: 4
title: Documentos
description: Upload multipart, OCR assíncrono e consulta de status de validação.
tags: [engenharia, api, documentos, ocr]
---

# API — Documentos

:::info Para quem é esta página
Engenheiros back-end e front-end. Para fluxo UX de upload, veja [Fluxo do Cidadão](../design/fluxos/cidadao.md).
:::

## Upload de Documento

```
POST /api/v1/documentos/upload
Content-Type: multipart/form-data
Authorization: Bearer {JWT}

Fields:
  processo_id: UUID
  tipo_documento: matricula_imovel | ccir | planta_georeferenciada | ...
  arquivo: File (max 50MB)
```

**Response 202** (aceito para processamento assíncrono):
```json
{
  "data": {
    "id": "uuid",
    "status": "aguardando",
    "hash_sha256": "abc123..."
  }
}
```

:::tip 202 Accepted, não 201 Created
O upload retorna 202 porque o processamento (OCR, validação) é assíncrono. O documento existe no storage, mas ainda não foi validado.
:::

## Tipos de Documento Aceitos

| Tipo | Descrição |
|---|---|
| `matricula_imovel` | Certidão de matrícula — **obrigatório** |
| `ccir` | Certificado de Cadastro de Imóvel Rural — **obrigatório** |
| `planta_georeferenciada` | Planta com coordenadas georreferenciadas |
| `memorial_descritivo` | Memorial descritivo do levantamento |
| `car_anterior` | Número de CAR anterior (para retificações) |
| `declaracao_area` | Declaração de área assinada |
| `outros` | Qualquer outro documento relevante |

## Consultar Status

```
GET /api/v1/documentos/{id}/status
→ { "status": "valido" | "invalido" | "aguardando" | "processando" }

GET /api/v1/documentos/{id}/dados-extraidos
→ { "numero_matricula": "...", "area_ha": 150.0, "proprietario_nome": "..." }
```

## Formatos e Limites

| Parâmetro | Valor |
|---|---|
| Tamanho máximo | 50MB por arquivo |
| Tipos aceitos | `application/pdf`, `image/jpeg`, `image/png`, `image/tiff` |
| Hash de integridade | SHA-256 calculado no servidor |
| Deduplicação | Hash duplicado retorna `CAR-007` |

:::warning Qualidade da imagem
OCR requer boa qualidade. Documentos fotografados com baixa iluminação ou desfocados terão confiança abaixo de 70% e o sistema solicitará reenvio com instruções.
:::
