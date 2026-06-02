import React from 'react';
import Link from '@docusaurus/Link';

interface Card {
  icon: string;
  role: string;
  title: string;
  desc: string;
  href: string;
  tags: string[];
}

const cards: Card[] = [
  {
    icon: '📋',
    role: 'Time de Produto',
    title: 'Sou de Produto',
    desc: 'Visão do produto, personas, casos de uso, roadmap e métricas de sucesso.',
    href: '/docs/produto/visao',
    tags: ['PRD', 'Personas', 'Roadmap', 'KPIs'],
  },
  {
    icon: '🎨',
    role: 'Design & UX',
    title: 'Sou de Design',
    desc: 'Princípios de UX, jornadas do usuário, acessibilidade e fluxos de interação.',
    href: '/docs/design/principios',
    tags: ['Fluxos', 'Personas UX', 'WCAG', 'WhatsApp'],
  },
  {
    icon: '⚙️',
    role: 'Engenharia',
    title: 'Sou de Engenharia',
    desc: 'Domínio DDD, arquitetura, APIs REST, banco de dados, segurança e testes.',
    href: '/docs/dominio/glossario',
    tags: ['DDD', 'C4', 'APIs', 'ADRs'],
  },
];

export default function AudienceCards(): React.ReactElement {
  return (
    <div className="audience-cards">
      {cards.map((card) => (
        <Link key={card.role} to={card.href} className="audience-card">
          <div className="audience-card__icon">{card.icon}</div>
          <div className="audience-card__role">{card.role}</div>
          <div className="audience-card__title">{card.title}</div>
          <div className="audience-card__desc">{card.desc}</div>
          <div className="audience-card__links">
            {card.tags.map((tag) => (
              <span key={tag} className="audience-card__tag">
                {tag}
              </span>
            ))}
          </div>
        </Link>
      ))}
    </div>
  );
}
