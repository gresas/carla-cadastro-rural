import React from 'react';
import OriginalDocSidebarItemLink from '@theme-original/DocSidebarItem/Link';
import type DocSidebarItemLinkType from '@theme/DocSidebarItem/Link';
import type { WrapperProps } from '@docusaurus/types';
import { usePluginData } from '@docusaurus/useGlobalData';
import clsx from 'clsx';

type Props = WrapperProps<typeof DocSidebarItemLinkType>;

interface RecentlyUpdatedData {
  docs: string[];
}

export default function DocSidebarItemLinkWrapper(props: Props): React.ReactElement {
  const { docs } = usePluginData('docusaurus-plugin-recently-updated') as RecentlyUpdatedData;
  const isNew = docs.includes(props.item.docId ?? '');

  return (
    <OriginalDocSidebarItemLink
      {...props}
      item={{
        ...props.item,
        className: clsx(props.item.className, isNew && 'sidebar-item--new'),
      }}
    />
  );
}
