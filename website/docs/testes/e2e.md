---
sidebar_position: 4
title: Testes E2E
description: Playwright — fluxos críticos do cidadão e do analista.
tags: [engenharia, testes, e2e, playwright]
---

# Testes E2E com Playwright

:::info Para quem é esta página
Engenheiros front-end e QA.
:::

## Configuração

```typescript
// playwright.config.ts
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: false,   // E2E sequencial para evitar conflitos de dados
  retries: 1,
  timeout: 120_000,
  use: {
    baseURL: process.env.E2E_BASE_URL || 'http://localhost:3000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: devices['Desktop Chrome'] },
    { name: 'firefox',  use: devices['Desktop Firefox'] },
  ],
});
```

## Fluxo do Cidadão

```typescript
// tests/e2e/registro-car.spec.ts
test('cidadão completa registro CAR — happy path', async ({ page }) => {
  // Login mock
  await page.goto('/login');
  await page.fill('[data-testid="cpf-input"]', '529.982.247-25');
  await page.click('[data-testid="btn-login"]');
  await expect(page).toHaveURL('/dashboard');

  // Novo processo
  await page.click('[data-testid="btn-novo-processo"]');
  await page.fill('[data-testid="nome-imovel"]', 'Fazenda Boa Vista');
  await page.selectOption('[data-testid="estado-select"]', 'MA');
  await page.click('[data-testid="btn-proximo"]');

  // Upload
  const [chooser] = await Promise.all([
    page.waitForEvent('filechooser'),
    page.click('[data-testid="upload-matricula"]'),
  ]);
  await chooser.setFiles('./tests/fixtures/sample_matricula.pdf');

  // Aguardar validação (OCR assíncrono, até 60s)
  await expect(page.locator('[data-testid="status-matricula"]'))
    .toHaveText('Válido', { timeout: 60_000 });

  // Submeter
  await page.click('[data-testid="btn-submeter"]');
  await expect(page.locator('[data-testid="status-processo"]'))
    .toHaveText('Submetido');
});
```

## Fluxo de Autorização

```typescript
test('produtor não acessa portal do analista', async ({ page }) => {
  await loginAs(page, 'produtor');
  await page.goto('/analista/processos');
  // Deve redirecionar ou mostrar erro
  await expect(page).not.toHaveURL('/analista/processos');
});
```

:::tip data-testid em vez de seletores frágeis
Use `data-testid` em todos os elementos interativos testáveis. Nunca selecione por classe CSS ou texto que pode mudar com tradução.
:::
