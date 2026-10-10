# Application architecture

> [!CAUTION]
> **Public showcase; private application.**
> Doctoleb’s application source is private. This showcase documents product and architecture decisions using explanatory illustrations. It includes no patient information, deployment records, clinical certification, or executed implementation checks.

Doctoleb connects clinic workflows through a React and TypeScript application, local persistence, and server coordination.

## Components

| Component | Approach | Design responsibility |
| --- | --- | --- |
| Browser application | React and TypeScript progressive web application | Connected appointments, records, and visit administration. |
| Local persistence | IndexedDB for browser-resident data | Browser-resident data for local operation. |
| Validation | Shared validation for application data | Consistent application data contracts. |
| Synchronization | Node-based server coordination | Explicit pending, retry, acceptance, and conflict states. |
| Languages | English, Arabic, and French, with right-to-left Arabic layouts | Multilingual interface design. |

## Local operation and synchronization

I designed local persistence around clinic workflows with unreliable connectivity. A locally accepted change and a server-confirmed change are different states. The synchronization design distinguishes them and accounts for retries, duplicate submissions, concurrent edits, conflicts, device access, and recovery.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/sync-states-dark.svg">
  <img alt="A local change waits for synchronization, retries offline, and is accepted after server review or returned for conflict resolution." src="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/sync-states-light.svg" width="500">
</picture>

## Staff visibility

Receptionists, doctors, and administrators have different responsibilities. I defined their visibility boundaries in the application design. Application and server authorization remain the relevant controls; interface visibility alone does not establish authorization.

[Project overview](../README.md) · [Clinic workflows](workflows.md)
