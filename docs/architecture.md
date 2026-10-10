# Architecture and evidence boundaries

Doctoleb is my clinic-management application. This public overview documents the architecture and its design decisions. Application source stays private; the documentation provides no deployment instructions or public runtime results.

## Components

| Component | Approach | Public evidence |
| --- | --- | --- |
| Browser application | React and TypeScript progressive web application | Architecture overview; application source is private. |
| Local persistence | IndexedDB for browser-resident data | Local-first design; no stored records are included here. |
| Validation | Shared validation for application data | Validation boundaries are documented; executed test results are not published here. |
| Synchronization | Node-based server coordination | Synchronization states and responsibilities are documented; no multi-device runtime results are supplied here. |
| Languages | English, Arabic, and French, with right-to-left Arabic layouts | Multilingual interface design. |

## Local operation and synchronization

I designed local persistence around clinic workflows with unreliable connectivity. A locally accepted change and a server-confirmed change are different states. The synchronization design distinguishes them and accounts for retries, duplicate submissions, concurrent edits, conflicts, device access, and recovery.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/sync-states-dark.svg">
  <img alt="A local change waits for synchronization, retries offline, and is accepted after server review or returned for conflict resolution." src="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/sync-states-light.svg" width="500">
</picture>

The diagram documents synchronization states. It is an architecture illustration, not evidence of an executed protocol or conflict-resolution test.

## Visibility and verification

Receptionists, doctors, and administrators have different responsibilities. I defined their visibility boundaries in the application design. Application and server authorization remain the relevant controls; interface visibility alone does not establish authorization.

The public showcase contains no patient information, executed unit or integration test results, security assessment, clinical outcomes, or certification.

[Project overview](../README.md) · [Clinic workflows](workflows.md)
