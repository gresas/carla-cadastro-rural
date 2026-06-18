import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import AudienceCards from '../components/AudienceCards';

export default function Home(): React.ReactElement {
  return (
    <Layout
      title="Documentação"
      description="Plataforma inteligente de atendimento para o Cadastro Ambiental Rural (CAR)"
    >
      {/* Hero */}
      <header className="hero hero--primary">
        <div className="container" style={{ textAlign: 'center', padding: '4rem 1rem 3rem' }}>
          <h1 className="hero__title">CARla</h1>
          <p className="hero__subtitle">
            Assistente Inteligente do Cadastro Ambiental Rural
          </p>
          <p style={{ fontSize: '1rem', opacity: 0.8, maxWidth: 600, margin: '0 auto 2rem' }}>
            Porque regularizar um imóvel rural não deveria ser um pesadelo.
            Uma camada inteligente sobre o SICAR que guia o cidadão, agiliza o analista
            e usa IA com responsabilidade.
          </p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link
              className="button button--secondary button--lg"
              to="/docs/intro"
            >
              O que é o CARla
            </Link>
            <Link
              className="button button--outline button--secondary button--lg"
              href="https://github.com/gresas/carla-cadastro-rural"
            >
              GitHub →
            </Link>
          </div>
        </div>
      </header>

      {/* Escolha sua área */}
      <main>
        <section style={{ padding: '1rem 0 0' }}>
          <div className="container">
            <h2 style={{ textAlign: 'center', marginBottom: '0.25rem' }}>
              Por onde você quer começar?
            </h2>
            <p style={{ textAlign: 'center', color: 'var(--ifm-color-secondary-darkest)', marginBottom: 0 }}>
              A documentação é organizada por audiência — escolha a área mais próxima do seu trabalho.
            </p>
          </div>
          <AudienceCards />
        </section>

        {/* Stats */}
        <section style={{ background: 'var(--ifm-color-emphasis-100)', padding: '3rem 0' }}>
          <div className="container">
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
              gap: '2rem',
              textAlign: 'center',
            }}>
              {[
                { num: '9,6 mi', label: 'propriedades no CAR nacional' },
                { num: '30 dias', label: 'tempo médio de análise atual' },
                { num: '-50%', label: 'redução de pendências esperada' },
                { num: '6', label: 'Bounded Contexts (DDD)' },
                { num: '6', label: 'ADRs documentadas' },
                { num: 'LGPD', label: 'conformidade completa' },
              ].map(({ num, label }) => (
                <div key={label}>
                  <div style={{
                    fontSize: '2rem',
                    fontWeight: 800,
                    color: 'var(--ifm-color-primary)',
                    lineHeight: 1.1,
                  }}>
                    {num}
                  </div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--ifm-color-secondary-darkest)', marginTop: '0.3rem' }}>
                    {label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Quick links por seção */}
        <section style={{ padding: '3rem 0 4rem' }}>
          <div className="container">
            <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>Acesso Rápido</h2>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
              gap: '1rem',
            }}>
              {[
                { label: '🏛️ Domínio (DDD)', to: '/docs/dominio/glossario', desc: 'Linguagem ubíqua, bounded contexts, event storming' },
                { label: '⚙️ Arquitetura', to: '/docs/arquitetura/visao-geral', desc: 'Modelo C4, serviços, banco de dados, mensageria' },
                { label: '🔌 APIs REST', to: '/docs/apis/principios', desc: 'Endpoints, schemas, autenticação, rate limiting' },
                { label: '🔒 Segurança & LGPD', to: '/docs/seguranca/lgpd', desc: 'Dados pessoais, RBAC, auditoria, OWASP' },
                { label: '🧪 Testes', to: '/docs/testes/estrategia', desc: 'Pirâmide, pytest, Playwright, k6' },
                { label: '🤝 Contribuindo', to: '/docs/contribuindo/setup', desc: 'Setup, convenções, padrão de documentação' },
              ].map(({ label, to, desc }) => (
                <Link key={to} to={to} style={{
                  display: 'block',
                  padding: '1rem 1.25rem',
                  border: '1px solid var(--ifm-color-emphasis-200)',
                  borderRadius: 8,
                  textDecoration: 'none',
                  color: 'inherit',
                  transition: 'border-color 0.15s',
                }}>
                  <div style={{ fontWeight: 700, marginBottom: '0.3rem' }}>{label}</div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--ifm-color-secondary-darkest)' }}>{desc}</div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
