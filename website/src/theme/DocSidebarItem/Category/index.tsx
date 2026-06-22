import React from 'react';
import OriginalDocSidebarItemCategory from '@theme-original/DocSidebarItem/Category';
import type DocSidebarItemCategoryType from '@theme/DocSidebarItem/Category';
import type { WrapperProps } from '@docusaurus/types';
import type { PropSidebarItem } from '@docusaurus/plugin-content-docs';
import { usePluginData } from '@docusaurus/useGlobalData';
import clsx from 'clsx';

type Props = WrapperProps<typeof DocSidebarItemCategoryType>;

interface RecentlyUpdatedData {
  docs: string[];
}

// Check if an href (e.g. "/carlos-geo/docs/como-funciona/arquitetura") matches a doc ID
const hrefMatchesAny = (href: string | undefined, newDocs: string[]) =>
  href ? newDocs.some((id) => href.endsWith(`/${id}`)) : false;

function hasNewDoc(items: PropSidebarItem[], newDocs: string[]): boolean {
  return items.some((item) => {
    if (item.type === 'link') return newDocs.includes(item.docId ?? '');
    if (item.type === 'category') {
      if (hrefMatchesAny(item.href, newDocs)) return true;
      return hasNewDoc(item.items, newDocs);
    }
    return false;
  });
}

export default function DocSidebarItemCategoryWrapper(props: Props): React.ReactElement {
  const { docs } = usePluginData('docusaurus-plugin-recently-updated') as RecentlyUpdatedData;

  const isNew =
    hrefMatchesAny(props.item.href, docs) || hasNewDoc(props.item.items, docs);

  return (
    <OriginalDocSidebarItemCategory
      {...props}
      item={{
        ...props.item,
        className: clsx(props.item.className, isNew && 'sidebar-item--new'),
      }}
    />
  );
}
