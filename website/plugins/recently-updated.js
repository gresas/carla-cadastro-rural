'use strict';

/**
 * Docusaurus plugin — recently-updated
 *
 * Para cada arquivo .md/.mdx em docs/, lê o timestamp do último commit via
 * `git log -1 --pretty=format:"%ct"` — a mesma fonte que o plugin-content-docs
 * usa para popular metadata.lastUpdatedAt (requer showLastUpdateTime: true).
 *
 * Docs atualizados nos últimos THRESHOLD_DAYS dias são expostos via globalData:
 *   { docs: string[], thresholdDays: number }
 *
 * Consumido pelos componentes swizzlados:
 *   src/theme/DocSidebarItem/Link/index.tsx      — badge na sidebar
 *   src/theme/DocSidebarItem/Category/index.tsx  — badge em seções
 *   src/theme/DocItem/Layout/index.tsx           — banner no topo da página
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const PLUGIN_ID = 'docusaurus-plugin-recently-updated';
const THRESHOLD_DAYS = 7;

function findDocFiles(dir, base) {
  const result = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const rel = base ? `${base}/${entry.name}` : entry.name;
    if (entry.isDirectory()) {
      result.push(...findDocFiles(path.join(dir, entry.name), rel));
    } else if (/\.mdx?$/.test(entry.name)) {
      result.push(rel);
    }
  }
  return result;
}

module.exports = function pluginRecentlyUpdated(context) {
  return {
    name: PLUGIN_ID,

    async loadContent() {
      const repoRoot = path.resolve(context.siteDir, '..');
      const docsDir = path.join(context.siteDir, 'docs');
      const cutoff = Math.floor(Date.now() / 1000) - THRESHOLD_DAYS * 86400;
      const manifestPath = path.join(context.siteDir, '.recently-updated-manifest.json');

      // Verifica se git está disponível (pode não estar em builds Docker)
      let gitAvailable = false;
      try {
        execSync('git --version', { cwd: repoRoot, stdio: 'ignore' });
        gitAvailable = true;
      } catch {}

      if (!gitAvailable) {
        // Fallback: manifest pré-gerado pelo CI antes do docker build
        try {
          const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
          if (Array.isArray(manifest.docs)) {
            console.log(
              `\n[recently-updated] Git indisponível — usando manifest pré-gerado (${manifest.docs.length} docs)\n`
            );
            return { docs: manifest.docs, thresholdDays: THRESHOLD_DAYS };
          }
        } catch {}
        console.log('\n[recently-updated] Git indisponível e manifest não encontrado — badges desativados\n');
        return { docs: [], thresholdDays: THRESHOLD_DAYS };
      }

      const docFiles = findDocFiles(docsDir, '');
      const recentDocs = [];

      for (const relPath of docFiles) {
        const absPath = path.join(docsDir, relPath);
        const gitRelPath = path.relative(repoRoot, absPath).replace(/\\/g, '/');

        try {
          const raw = execSync(
            `git log -1 --pretty=format:"%ct" -- "${gitRelPath}"`,
            { cwd: repoRoot, stdio: ['pipe', 'pipe', 'ignore'] }
          )
            .toString()
            .trim()
            .replace(/"/g, '');

          if (raw && parseInt(raw, 10) > cutoff) {
            recentDocs.push(relPath.replace(/\.mdx?$/, ''));
          }
        } catch {
          // arquivo ainda não commitado — ignorado
        }
      }

      return { docs: recentDocs, thresholdDays: THRESHOLD_DAYS };
    },

    async contentLoaded({ content, actions }) {
      if (content.docs.length > 0) {
        console.log(
          `\n[recently-updated] ${content.docs.length} doc(s) atualizados nos últimos ${THRESHOLD_DAYS} dias: ${content.docs.join(', ')}\n`
        );
      }
      actions.setGlobalData(content);
    },
  };
};
