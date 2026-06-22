import React, { useState, useEffect } from 'react';
import OriginalDocItemLayout from '@theme-original/DocItem/Layout';
import type DocItemLayoutType from '@theme/DocItem/Layout';
import type { WrapperProps } from '@docusaurus/types';
import { usePluginData } from '@docusaurus/useGlobalData';
import { useDoc } from '@docusaurus/plugin-content-docs/client';

type Props = WrapperProps<typeof DocItemLayoutType>;

interface RecentlyUpdatedData {
  thresholdDays: number;
}

function NewDocBanner(): React.ReactElement | null {
  const { metadata } = useDoc();
  const { thresholdDays } = usePluginData(
    'docusaurus-plugin-recently-updated'
  ) as RecentlyUpdatedData;

  // useState(false) garante que SSR e o render inicial do cliente concordam
  // (ambos retornam null). useEffect calcula com Date.now() real do browser,
  // eliminando a hydration mismatch do React 19.
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const lastUpdatedAt = metadata.lastUpdatedAt;
    if (!lastUpdatedAt) return;
    setVisible(lastUpdatedAt > Date.now() - thresholdDays * 86400 * 1000);
  }, [metadata.lastUpdatedAt, thresholdDays]);

  if (!visible) return null;

  const updatedDate = new Date(metadata.lastUpdatedAt!).toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  });

  return (
    <div className="doc-recently-updated-banner">
      <span className="doc-recently-updated-banner__badge">Novo</span>
      <span className="doc-recently-updated-banner__text">
        Esta página foi atualizada em <strong>{updatedDate}</strong>
        {metadata.lastUpdatedBy ? ` por ${metadata.lastUpdatedBy}` : ''}.
      </span>
    </div>
  );
}

export default function DocItemLayoutWrapper(props: Props): React.ReactElement {
  return (
    <>
      <NewDocBanner />
      <OriginalDocItemLayout {...props} />
    </>
  );
}
