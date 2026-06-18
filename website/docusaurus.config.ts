import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'CARla',
  tagline: 'Assistente Inteligente do Cadastro Ambiental Rural',
  favicon: 'img/favicon.ico',

  url: 'https://gresas.github.io',
  baseUrl: '/carla-cadastro-rural/',

  organizationName: 'gresas',
  projectName: 'carla-cadastro-rural',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'pt-BR',
    locales: ['pt-BR'],
  },

  markdown: {
    mermaid: true,
  },

  themes: ['@docusaurus/theme-mermaid'],

  plugins: [
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: ['pt'],
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
      },
    ],
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/gresas/carla-cadastro-rural/edit/docusaurus/website/',
          showLastUpdateTime: true,
          showLastUpdateAuthor: true,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/og-image.png',

    colorMode: {
      defaultMode: 'light',
      disableSwitch: false,
    },

    mermaid: {
      theme: { light: 'neutral', dark: 'dark' },
    },

    navbar: {
      title: 'CARla',
      logo: {
        alt: 'CARla',
        src: 'img/carla-logo.svg',
      },
      items: [
        { label: 'Produto', to: '/docs/produto/visao', position: 'left' },
        { label: 'Design & UX', to: '/docs/design/principios', position: 'left' },
        { label: 'Engenharia', to: '/docs/dominio/glossario', position: 'left' },
        {
          type: 'dropdown',
          label: 'Referência',
          position: 'left',
          items: [
            { label: 'APIs REST', to: '/docs/apis/principios' },
            { label: 'Segurança & LGPD', to: '/docs/seguranca/lgpd' },
            { label: 'Testes', to: '/docs/testes/estrategia' },
            { label: 'Decisões (ADRs)', to: '/docs/arquitetura/decisoes/' },
          ],
        },
        { label: 'Contribuindo', to: '/docs/contribuindo/setup', position: 'right' },
        {
          href: 'https://github.com/gresas/carla-cadastro-rural',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },

    footer: {
      style: 'dark',
      links: [
        {
          title: 'Para Produto',
          items: [
            { label: 'Visão e Objetivos', to: '/docs/produto/visao' },
            { label: 'Personas', to: '/docs/produto/personas' },
            { label: 'Roadmap', to: '/docs/produto/roadmap' },
          ],
        },
        {
          title: 'Para Design',
          items: [
            { label: 'Princípios UX', to: '/docs/design/principios' },
            { label: 'Fluxo do Cidadão', to: '/docs/design/fluxos/cidadao' },
            { label: 'Fluxo do Analista', to: '/docs/design/fluxos/analista' },
          ],
        },
        {
          title: 'Para Engenharia',
          items: [
            { label: 'Arquitetura Geral', to: '/docs/arquitetura/visao-geral' },
            { label: 'APIs REST', to: '/docs/apis/principios' },
            { label: 'ADRs', to: '/docs/arquitetura/decisoes/' },
          ],
        },
        {
          title: 'Projeto',
          items: [
            { label: 'GitHub', href: 'https://github.com/gresas/carla-cadastro-rural' },
            { label: 'Contribuindo', to: '/docs/contribuindo/setup' },
          ],
        },
      ],
      copyright: `CARla — Hackathon GovTech 2026. Licença Apache 2.0.`,
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'sql', 'bash', 'typescript', 'yaml', 'json'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
