import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  docs: [
    'intro',
    {
      type: 'category',
      label: '📋 Produto',
      link: { type: 'doc', id: 'produto/visao' },
      items: [
        'produto/visao',
        'produto/personas',
        'produto/casos-de-uso',
        'produto/requisitos',
        'produto/metricas',
        'produto/riscos',
        'produto/roadmap',
      ],
    },
    {
      type: 'category',
      label: '🎨 Design & UX',
      link: { type: 'doc', id: 'design/principios' },
      items: [
        'design/principios',
        'design/personas',
        {
          type: 'category',
          label: 'Fluxos de Usuário',
          items: [
            'design/fluxos/cidadao',
            'design/fluxos/analista',
            'design/fluxos/whatsapp',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: '🏛️ Domínio (DDD)',
      link: { type: 'doc', id: 'dominio/glossario' },
      items: [
        'dominio/glossario',
        'dominio/bounded-contexts',
        'dominio/event-storming',
        'dominio/agregados',
        'dominio/pra',
      ],
    },
    {
      type: 'category',
      label: '⚙️ Arquitetura',
      link: { type: 'doc', id: 'arquitetura/visao-geral' },
      items: [
        'arquitetura/visao-geral',
        'arquitetura/servicos',
        'arquitetura/banco-de-dados',
        'arquitetura/mensageria',
        'arquitetura/ia',
        {
          type: 'category',
          label: 'Decisões (ADRs)',
          link: { type: 'doc', id: 'arquitetura/decisoes/index' },
          items: [
            'arquitetura/decisoes/index',
            'arquitetura/decisoes/adr-001-fastapi',
            'arquitetura/decisoes/adr-002-postgresql',
            'arquitetura/decisoes/adr-003-eda',
            'arquitetura/decisoes/adr-004-rabbitmq',
            'arquitetura/decisoes/adr-005-govbr',
            'arquitetura/decisoes/adr-006-ia',
            'arquitetura/decisoes/adr-007-whatsapp',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: '🔌 APIs REST',
      link: { type: 'doc', id: 'apis/principios' },
      items: [
        'apis/principios',
        'apis/autenticacao',
        'apis/processos',
        'apis/documentos',
        'apis/assistente',
        'apis/analista',
        'apis/whatsapp',
        'apis/erros',
      ],
    },
    {
      type: 'category',
      label: '🔒 Segurança & LGPD',
      link: { type: 'doc', id: 'seguranca/lgpd' },
      items: [
        'seguranca/lgpd',
        'seguranca/autenticacao',
        'seguranca/auditoria',
      ],
    },
    {
      type: 'category',
      label: '🧪 Testes',
      link: { type: 'doc', id: 'testes/estrategia' },
      items: [
        'testes/estrategia',
        'testes/unitarios',
        'testes/integracao',
        'testes/e2e',
        'testes/carga',
      ],
    },
    {
      type: 'category',
      label: '🤝 Contribuindo',
      link: { type: 'doc', id: 'contribuindo/setup' },
      items: [
        'contribuindo/setup',
        'contribuindo/convencoes',
        'contribuindo/como-escrever-docs',
        'contribuindo/novo-adr',
      ],
    },
  ],
};

export default sidebars;
