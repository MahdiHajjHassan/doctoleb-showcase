# Doctoleb | Application Architecture

> [!CAUTION]
> **Private clinic application.** Doctoleb is in development and its application source is private. This page explains the product and architecture through diagrams; it contains no patient records or deployment, clinical certification, or application test results.

Doctoleb connects appointments, patient records, and visit administration through a React and TypeScript application, local storage, and server coordination.

## Components

| Component | Responsibility |
| --- | --- |
| React and TypeScript progressive web application | Staff workflows in the browser. |
| IndexedDB | Local application data for interrupted connectivity. |
| Shared validation | Consistent application data formats. |
| Node-based synchronization | Pending changes, retries, server acceptance, and conflicts. |
| Multilingual interface | English, Arabic, and French, including right-to-left Arabic layouts. |

## Local changes and server confirmation

I designed the application to distinguish a saved local change from one accepted by the server. Synchronization accounts for retries, duplicate submissions, concurrent edits, conflicts, device access, and recovery.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/sync-states-dark.svg">
  <img alt="A local change waits for synchronization, retries offline, and is accepted after server review or returned for conflict resolution." src="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/sync-states-light.svg" width="500">
</picture>

## Staff access

Receptionists manage appointments and administration; doctors need patient and visit context; administrators manage clinic configuration and staff responsibilities. I defined visibility around those tasks.

Authorization applies to application data and server requests, as well as the controls displayed on screen.

[Project overview](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/README.md) · [Clinic workflows](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/docs/workflows.md)
