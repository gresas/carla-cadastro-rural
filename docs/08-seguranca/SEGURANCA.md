# CARla — Segurança e Conformidade

**Versão:** 1.0.0  
**Data:** 2026-06-01  
**Classificação:** Documento Interno — Restrito

---

## 1. LGPD — Lei Geral de Proteção de Dados (Lei 13.709/2018)

### 1.1 Dados Pessoais Tratados

| Dado | Categoria | Finalidade | Base Legal (Art. 7) | Retenção | Compartilhamento | Proteção Técnica |
|---|---|---|---|---|---|---|
| CPF | Pessoal (identificador único) | Autenticação, vinculação ao imóvel | II — Obrigação legal (Lei 12.651/2012) | 5 anos pós-inatividade | SICAR (obrigatório por lei) | pgcrypto + hash SHA-256 |
| Email | Pessoal | Notificações sobre o processo | IX — Interesse legítimo | 5 anos pós-inatividade | Não compartilhado | pgcrypto |
| Nome completo | Pessoal | Identificação nos documentos oficiais | II — Obrigação legal | 10 anos (prazo legal CAR) | SICAR | Armazenado em claro |
| Geometria do imóvel | Pessoal (localização) | Registro CAR — dado geoespacial do imóvel | II — Obrigação legal | Indefinida (registro público) | SICAR, SIGEF | RBAC — sem acesso público individual |
| Documentos pessoais | Pessoal (dados sensíveis indiretos) | Comprovação de propriedade e área | II — Obrigação legal | 10 anos pós-conclusão | SICAR | AES-256 no object storage (MinIO) |
| Histórico de acesso (IP, UA) | Pessoal | Segurança, prevenção fraude, auditoria | IX — Interesse legítimo | 6 meses | Não | Logs seguros, IP truncado em analytics |
| Conversas com IA | Pessoal (conteúdo conversacional) | Atendimento ao cidadão | I — Consentimento (explícito no onboarding) | 90 dias → anonimização | Não (mascaramento PII para LLM externo) | PII masking antes do LLM |
| Fotos de documentos | Pessoal | OCR para extração de dados | II — Obrigação legal | 10 anos pós-conclusão | Não (processamento interno) | AES-256, acesso por role |

### 1.2 Direitos dos Titulares (Art. 18)

| Direito | Como Implementado | Prazo | Canal |
|---|---|---|---|
| Acesso | Portal → Minha Conta → Exportar Meus Dados (JSON/PDF) | 15 dias úteis | Portal ou email dpo@ |
| Retificação | Portal → Minha Conta → Editar Dados Pessoais | 15 dias úteis | Portal |
| Eliminação | Portal → Solicitar Exclusão da Conta (soft delete + anonimização de dados não obrigatórios) | 15 dias úteis | Portal + confirmação por email |
| Portabilidade | Export JSON estruturado de todos os dados do usuário | 15 dias úteis | Portal |
| Revogação de consentimento | Para conversas IA: Portal → Privacidade → Revogar consentimento | Imediato | Portal |
| Oposição | Para tratamentos baseados em interesse legítimo | 15 dias úteis | Email dpo@ |
| Informação sobre compartilhamento | Seção "Compartilhamento de dados" no Aviso de Privacidade | — | Portal (link no footer) |

### 1.3 DPO — Encarregado de Proteção de Dados
**Canal de contato obrigatório (Art. 41):** dpo@carcopilot.gov.br  
**Prazo de resposta:** 15 dias úteis para todos os direitos dos titulares  
**Registro de solicitações:** Tabela interna de controle de solicitações LGPD

### 1.4 Notificação de Incidentes (Art. 48)
**Prazo:** 72 horas para comunicar à ANPD  
**Critério:** Incidentes que possam causar risco ou dano relevante aos titulares  
**Conteúdo da comunicação:** Natureza dos dados, titulares afetados, medidas de proteção adotadas, riscos relacionados, motivo da demora se > 72h  
**Canal ANPD:** https://www.gov.br/anpd/pt-br/canais_atendimento

---

## 2. Autenticação

### 2.1 JWT — JSON Web Tokens

```python
# Configuração de segurança dos tokens
JWT_CONFIG = {
    "algorithm": "RS256",              # RSA 2048-bit; nunca HS256 (simétrico)
    "access_token_expire_hours": 1,
    "refresh_token_expire_days": 30,
    "refresh_rotation": True,         # Refresh token rotacionado a cada uso
    "key_rotation_hours": 24,         # Chaves RS256 rotacionadas via Vault
    "issuer": "https://api.carcopilot.gov.br",
    "audience": "carla-api",
}

# Blacklist de tokens revogados (Redis)
# SET "jwt:blacklist:{jti}" "1" EX {ttl_seconds}
# Verificado em cada requisição autenticada
```

### 2.2 Política de Lockout

- **5 tentativas falhas** em 15 minutos por IP → lockout 15 minutos
- **5 tentativas falhas** em 15 minutos por CPF → lockout 15 minutos + notificação por email
- **Delay progressivo:** 1s → 2s → 5s → 10s → lockout
- **Notificação:** Email para o titular após lockout

### 2.3 Armazenamento de Tokens no Browser

```javascript
// Access token: apenas em memória (nunca localStorage — vulnerável a XSS)
// Refresh token: httpOnly cookie com atributos de segurança
document.cookie = `refresh_token=${token}; HttpOnly; Secure; SameSite=Strict; Path=/api/v1/auth/refresh; Max-Age=2592000`;
```

---

## 3. Autorização — RBAC Detalhado

### 3.1 Roles do Sistema

| Role | Descrição | Restrições de Acesso |
|---|---|---|
| `produtor_rural` | Cidadão dono do imóvel | Acessa apenas seus próprios processos/imóveis |
| `consultor_ambiental` | Profissional que representa proprietários | Acessa processos com autorização explícita do proprietário |
| `analista_ambiental` | Servidor que analisa processos | Vê todos os processos; não pode ver dados pessoais de outros analistas |
| `supervisor_ambiental` | Supervisiona analistas e decide recursos | Tudo do analista + recursos + relatórios de analistas |
| `admin` | TI — gerencia a plataforma | Acesso completo + audit logs + configurações de sistema |

### 3.2 Matriz de Permissões

| Recurso | Ação | Produtor | Consultor | Analista | Supervisor | Admin |
|---|---|:---:|:---:|:---:|:---:|:---:|
| Próprio processo | Criar | ✓ | ✓* | - | - | ✓ |
| Próprio processo | Ler | ✓ | ✓* | ✓ | ✓ | ✓ |
| Processo de terceiro | Ler | - | - | ✓ | ✓ | ✓ |
| Processo | Submeter | ✓ | ✓* | - | - | ✓ |
| Processo | Aprovar | - | - | ✓ | ✓ | ✓ |
| Processo | Rejeitar | - | - | ✓ | ✓ | ✓ |
| Processo | Criar pendência | - | - | ✓ | ✓ | ✓ |
| Documento | Upload | ✓ | ✓* | - | - | ✓ |
| Documento | Baixar | ✓ (próprio) | ✓* | ✓ | ✓ | ✓ |
| Dossiê | Gerar/Baixar | - | - | ✓ | ✓ | ✓ |
| Usuário | Listar | - | - | - | - | ✓ |
| Usuário | Desativar | - | - | - | - | ✓ |
| Audit logs | Consultar | - | - | - | ✓ | ✓ |
| Configurações LLM | Alterar | - | - | - | - | ✓ |
| Dashboard analista | Acessar | - | - | ✓ | ✓ | ✓ |
| Relatórios gerenciais | Acessar | - | - | - | ✓ | ✓ |

(*) Apenas processos com autorização explícita do proprietário (tabela `autorizacoes_consultor`)

### 3.3 Ownership Check

```python
# Implementação do ownership check no middleware
async def verificar_acesso_ao_processo(
    processo_id: UUID,
    current_user: UsuárioAutenticado,
    db: AsyncSession,
) -> ProcessoCAR:
    processo = await db.get(ProcessoCARModel, processo_id)

    if processo is None or processo.deleted_at is not None:
        raise HTTPException(status_code=404)  # 404, não 403 — evita enumeração

    if current_user.tipo in (TipoUsuário.ANALISTA_AMBIENTAL, TipoUsuário.SUPERVISOR_AMBIENTAL, TipoUsuário.ADMIN):
        return processo  # Analistas e acima podem ver qualquer processo

    if processo.requerente_id == current_user.id:
        return processo  # Produtor/consultor acessa o próprio processo

    raise HTTPException(status_code=404)  # Retorna 404, não 403
```

---

## 4. Criptografia

### 4.1 Em Repouso

| Dado | Algoritmo | Gerenciamento de Chave | Rotação |
|---|---|---|---|
| CPF no banco | pgp_sym_encrypt (AES-256) | HashiCorp Vault — chave mestra | 90 dias |
| Email no banco | pgp_sym_encrypt (AES-256) | HashiCorp Vault | 90 dias |
| Documentos no MinIO | AES-256-GCM (server-side) | MinIO KMS + Vault | 90 dias |
| Backup do banco | AES-256 + GPG | Chaves offline em HSM | Anual |
| Segredos de aplicação | Vault KV v2 | Auto-unseal com cloud KMS | Automático |

```sql
-- Exemplo de uso pgcrypto para CPF
INSERT INTO users (cpf_hash, cpf_encrypted, nome_completo)
VALUES (
    encode(digest('12345678901' || current_setting('app.cpf_salt'), 'sha256'), 'hex'),
    pgp_sym_encrypt('12345678901', current_setting('app.encryption_key')),
    'João Silva'
);

-- Recuperar CPF (apenas quando necessário, ex: exibição no portal)
SELECT pgp_sym_decrypt(cpf_encrypted, current_setting('app.encryption_key')) AS cpf
FROM users WHERE id = $1;
```

### 4.2 Em Trânsito

```nginx
# Configuração TLS 1.3 no Nginx
ssl_protocols TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 1d;
ssl_session_tickets off;

# HSTS
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

# Certificate Transparency
ssl_stapling on;
ssl_stapling_verify on;
```

---

## 5. Headers de Segurança HTTP

```nginx
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self' https://api.carcopilot.gov.br;" always;
add_header X-XSS-Protection "1; mode=block" always;
```

---

## 6. OWASP Top 10 (2021) — Mitigações

| OWASP | Risco | Mitigação Implementada |
|---|---|---|
| A01 — Broken Access Control | Acesso a dados de terceiros | RBAC + ownership check + retorno 404 (não 403) + testes de autorização |
| A02 — Cryptographic Failures | Dados pessoais expostos | TLS 1.3, AES-256, RS256 JWT, pgcrypto, sem MD5/SHA-1 |
| A03 — Injection | SQL injection, XSS | Pydantic v2 valida todos os inputs; SQLAlchemy ORM parametrizado; sem raw SQL com input do usuário |
| A04 — Insecure Design | Falhas arquiteturais | Threat modeling por feature; DDD boundaries; security review em ADRs |
| A05 — Security Misconfiguration | Configs padrão inseguras | Hardened Docker images (non-root, read-only FS); Vault para segredos; CORS allowlist |
| A06 — Vulnerable Components | Dependências com CVE | Dependabot + Renovate; Safety (pip); Trivy (Docker); SBOM por release |
| A07 — Auth Failures | Credential stuffing, brute force | Gov.br cuida da senha; JWT RS256; lockout + delay; blacklist de tokens |
| A08 — Data Integrity Failures | Uploads maliciosos | SHA-256 de todos os uploads; assinatura de imagens Docker (Cosign); pinagem de dependências |
| A09 — Security Logging Failures | Falta de rastreabilidade | Audit log imutável; logs estruturados; SIEM integration; sem PII em logs |
| A10 — SSRF | Requisições forjadas ao servidor | Whitelist de URLs externas; sem URLs fornecidas pelo usuário; egress network policy K8s |

---

## 7. Segurança de Uploads

```python
# Validação multicamada de arquivos enviados
class ValidadorUpload:
    TIPOS_PERMITIDOS = {
        "application/pdf",
        "image/jpeg",
        "image/png",
        "image/tiff",
    }
    TAMANHO_MAXIMO_BYTES = 50 * 1024 * 1024  # 50MB

    async def validar(self, arquivo: UploadFile) -> None:
        # 1. Verificar Content-Type header
        if arquivo.content_type not in self.TIPOS_PERMITIDOS:
            raise HTTPException(415, detail={"code": "CAR-006"})

        # 2. Verificar tamanho
        conteudo = await arquivo.read()
        if len(conteudo) > self.TAMANHO_MAXIMO_BYTES:
            raise HTTPException(413, detail={"code": "CAR-005"})

        # 3. Verificar magic bytes (tipo real do arquivo, não apenas header)
        import magic
        tipo_real = magic.from_buffer(conteudo[:2048], mime=True)
        if tipo_real not in self.TIPOS_PERMITIDOS:
            raise HTTPException(415, detail={"code": "CAR-006", "message": "Tipo real do arquivo não corresponde"})

        # 4. Calcular hash para deduplicação e integridade
        import hashlib
        hash_sha256 = hashlib.sha256(conteudo).hexdigest()

        # 5. ClamAV scan assíncrono (não bloqueia resposta)
        await self._enfileirar_scan_antivirus(hash_sha256, conteudo)

        await arquivo.seek(0)
```

---

## 8. Kubernetes Security

### Pod Security Standards
```yaml
# Namespace com restricted profile
apiVersion: v1
kind: Namespace
metadata:
  name: carla-prod
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
```

### Network Policies
```yaml
# Deny-all por padrão, whitelist explícita
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: carla-prod
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-process-to-postgres
spec:
  podSelector:
    matchLabels:
      app: process-service
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgresql
    ports:
    - port: 5432
```

---

## 9. Gestão de Segredos

```yaml
# External Secrets Operator — sincroniza Vault → K8s Secrets
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: carla-secrets
spec:
  refreshInterval: 15m
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: carla-secrets
  data:
  - secretKey: DB_PASSWORD
    remoteRef:
      key: carla/database
      property: password
  - secretKey: ANTHROPIC_API_KEY
    remoteRef:
      key: carla/llm
      property: anthropic_key
```

---

## 10. Auditoria e Rastreabilidade

### Eventos de Segurança Auditados

| Evento | Tabela | Campos Registrados |
|---|---|---|
| Login bem-sucedido | audit_logs | user_id, ip, user_agent, timestamp |
| Falha de login | audit_logs | ip, user_agent, cpf_hash (sem CPF), motivo, timestamp |
| Logout | audit_logs | user_id, session_id, timestamp |
| Acesso negado (403/404 de segurança) | audit_logs | user_id, recurso tentado, timestamp |
| Download de documento | audit_logs | user_id, documento_id, processo_id, timestamp |
| Download de dossiê | audit_logs | user_id, processo_id, timestamp |
| Aprovação de processo | historico_processos | analista_id, processo_id, status_anterior, motivo |
| Rejeição de processo | historico_processos | analista_id, processo_id, motivo, código |
| Mudança de role de usuário | audit_logs | admin_id, user_id, role_anterior, role_nova |
| Acesso ao painel admin | audit_logs | user_id, ação, timestamp |
| Tentativa de acesso Gov.br fraudulenta | audit_logs | ip, state_tentado, timestamp |

---

## 11. Plano de Resposta a Incidentes

### Classificação de Severidade

| Nível | Exemplos | SLA Resposta | Comunicação |
|---|---|---|---|
| P0 — Crítico | Vazamento de dados pessoais, acesso não autorizado em massa | < 15 min | CISO + CTO + equipe segurança |
| P1 — Alto | Sistema indisponível, falha de autenticação generalizada | < 1 hora | Equipe técnica + gestor |
| P2 — Médio | Degradação de performance, falha de integração isolada | < 4 horas | Equipe técnica |
| P3 — Baixo | Bug menor, alerta não crítico | < 24 horas | Ticket de suporte |

### Processo P0 — Vazamento de Dados

1. **Detecção** (automática via SIEM ou manual)
2. **Contenção** (< 1h): Isolamento do sistema afetado; revogação de tokens comprometidos
3. **Avaliação** (< 2h): Quais dados foram expostos? Quantos titulares afetados?
4. **Comunicação ANPD** (< 72h): Formulário no portal da ANPD
5. **Comunicação aos titulares**: Prazo razoável + canal adequado
6. **Remediação**: Corrigir vulnerabilidade, atualizar sistemas
7. **Post-mortem** (< 7 dias): Causa raiz, lições aprendidas, ações preventivas

---

## 12. Testes de Segurança

```bash
# Pipeline CI — executar em cada PR
bandit -r src/ -ll -i --exit-zero  # SAST Python
safety check --json                 # CVEs em dependências
gitleaks detect --source .          # Segredos no código

# Pipeline CD — executar em staging
trivy image carla:latest      # Vulnerabilidades na imagem Docker
docker run -t owasp/zap-baseline-scan -t https://staging-api.carcopilot.gov.br
```

### Testes de Autorização (pytest)
```python
class TestAutorizacao:
    async def test_produtor_nao_acessa_processo_de_outro(self, client, token_produtor_a, processo_produtor_b):
        response = await client.get(
            f"/api/v1/processos/{processo_produtor_b.id}",
            headers={"Authorization": f"Bearer {token_produtor_a}"}
        )
        # 404, não 403 — segurança por obscuridade
        assert response.status_code == 404

    async def test_produtor_nao_acessa_rota_analista(self, client, token_produtor):
        response = await client.get(
            "/api/v1/analista/processos",
            headers={"Authorization": f"Bearer {token_produtor}"}
        )
        assert response.status_code == 403
```
