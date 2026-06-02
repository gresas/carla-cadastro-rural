# ADR-005: Autenticação via Gov.br com OAuth2/OIDC

**Status:** Aceito  
**Data:** 2026-06-01  
**Contexto:** Autenticação e Identidade de todos os usuários cidadãos

---

## Contexto

O CARla é uma plataforma pública do governo brasileiro. Os cidadãos que acessam o sistema precisam de autenticação com as seguintes características:

- **CPF verificado:** O processo CAR é vinculado ao CPF do proprietário — precisamos garantir que o CPF informado é legítimo
- **Sem nova senha:** Criar mais uma senha para o cidadão aumenta abandono e risco de segurança
- **Base de usuários existente:** Gov.br tem 150M+ contas cadastradas — cidadãos já estão lá
- **Níveis de confiabilidade:** O Gov.br oferece bronze/prata/ouro — diferente nível de verificação
  - Bronze: e-mail verificado
  - Prata: validação biométrica ou bancária
  - Ouro: reconhecimento facial com biometria
- **Conformidade:** Decreto 10.900/2021 recomenda Gov.br para autenticação em serviços digitais federais

O risco principal é a dependência de um sistema externo que pode ficar indisponível.

---

## Decisão

**Integrar Gov.br como Identity Provider via OAuth2 Authorization Code Flow + PKCE.**

### Requisitos de Nível por Operação

| Operação | Nível Mínimo | Justificativa |
|---|---|---|
| Consultar informações públicas CAR | Sem autenticação | Dados públicos |
| Consultar próprio processo | Bronze | Visualização, baixo risco |
| Criar rascunho de processo | Bronze | Sem impacto legal ainda |
| Submeter processo CAR | Prata | Ato jurídico — precisa de identificação confiável |
| Corrigir pendências | Prata | Ato jurídico |
| Interpor recurso | Prata | Ato jurídico |
| Operações administrativas | Ouro | Máxima segurança para servidores |

### Fluxo de Autenticação

```python
# auth/infrastructure/govbr_adapter.py
import hashlib, secrets, base64
from urllib.parse import urlencode
import httpx

class GovBrAdapter:
    """Anti-Corruption Layer: isola o domínio do protocolo Gov.br."""

    AUTHORIZATION_URL = "https://sso.acesso.gov.br/authorize"
    TOKEN_URL = "https://sso.acesso.gov.br/token"
    USERINFO_URL = "https://sso.acesso.gov.br/userinfo"
    JWKS_URL = "https://sso.acesso.gov.br/jwk"

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def gerar_authorization_url(self, state: str) -> tuple[str, str]:
        """Gera URL de autorização com PKCE."""
        code_verifier = secrets.token_urlsafe(64)
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).rstrip(b'=').decode()

        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "openid email profile govbr_confiabilidades",
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
            "nonce": secrets.token_urlsafe(16),
        }
        url = f"{self.AUTHORIZATION_URL}?{urlencode(params)}"
        return url, code_verifier

    async def trocar_code_por_tokens(
        self, code: str, code_verifier: str
    ) -> 'TokensGovBr':
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": self.redirect_uri,
                    "code_verifier": code_verifier,
                },
                auth=(self.client_id, self.client_secret),
                timeout=10.0,
            )
            response.raise_for_status()
            return TokensGovBr(**response.json())

    def extrair_nivel_confiabilidade(self, id_token_claims: dict) -> NivelConfiabilidade:
        """Mapeia confiabilidades Gov.br para o enum do domínio."""
        confiabilidades = id_token_claims.get("govbr_confiabilidades", [])
        if any("3" in c for c in confiabilidades):  # nível ouro
            return NivelConfiabilidade.OURO
        if any("2" in c for c in confiabilidades):  # nível prata
            return NivelConfiabilidade.PRATA
        return NivelConfiabilidade.BRONZE
```

### JWT Interno

```python
# Após autenticação Gov.br, emitimos nosso próprio JWT RS256
import jwt
from cryptography.hazmat.primitives import serialization

class JWTService:
    def emitir(self, usuario: Usuário) -> tuple[str, str]:
        payload = {
            "sub": str(usuario.id),
            "nome": usuario.nome_completo,
            "tipo_usuario": usuario.tipo.value,
            "nivel_confiabilidade": usuario.nivel_confiabilidade.value,
            "jti": str(uuid4()),
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=1),
        }
        access_token = jwt.encode(payload, self._private_key, algorithm="RS256")
        refresh_token = secrets.token_urlsafe(64)
        return access_token, refresh_token
```

### Fallback de Emergência

```python
# Para servidores em caso de indisponibilidade Gov.br
# Apenas para usuários tipo ADMIN com MFA separado
# Ativado por flag de configuração — NUNCA padrão
FALLBACK_AUTH_ENABLED = os.getenv("GOVBR_FALLBACK_ENABLED", "false") == "true"
```

---

## Consequências

### Positivas
- **UX superior:** Cidadão não cria nova senha — usa conta Gov.br que já tem
- **CPF verificado de graça:** Gov.br já verificou o CPF — eliminamos fraude de identidade
- **Conformidade legal:** Alinhado com Decreto 10.900/2021 e E-PING (Padrões de Interoperabilidade do Governo Eletrônico)
- **Sem responsabilidade de senha:** Não armazenamos senha — reduz superfície de ataque e responsabilidade LGPD
- **Nível de confiabilidade:** Podemos exigir nível adequado por operação de risco

### Negativas
- **Dependência externa crítica:** Se Gov.br cair, cidadãos não conseguem logar
- **Latência adicional:** Cada autenticação envolve redirect para Gov.br (~500ms extra)
- **Complexidade PKCE:** Fluxo mais complexo que username/password — mais difícil de testar

### Riscos
- SLA do Gov.br não é público — histórico de instabilidades em picos de acesso
- **Mitigação:** Sessions longas (access token 1h, refresh token 30 dias) reduzem frequência de autenticação; modo de manutenção para servidores

---

## Alternativas Consideradas

| Alternativa | Prós | Contras | Motivo da Rejeição |
|---|---|---|---|
| **Identity Provider próprio** | Controle total | Alta responsabilidade de segurança de senhas; mais para desenvolver | Não é core do negócio; risco de segurança |
| **Keycloak local** | Flexível, federado, pode federar Gov.br também | Complexidade operacional adicional; outro serviço para manter | Adiciona componente sem benefício extra sobre Gov.br direto |
| **AWS Cognito** | Gerenciado, escalável | Vendor lock-in; não integra nativamente com Gov.br; custo | Filosofia cloud-agnostic |
| **username + senha próprios** | Simples de implementar | Mais uma senha para o cidadão; responsabilidade de segurança; não tem CPF verificado | Má UX; risco de segurança; sem CPF verificado |

---

## Referências

- [Gov.br — Documentação para Integradores](https://manual-roteiro-integracao-login-unico.servicos.gov.br/)
- [Decreto 10.900/2021](http://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/decreto/D10900.htm)
- [RFC 7636 — PKCE](https://tools.ietf.org/html/rfc7636)
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
