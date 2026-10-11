# Doctoleb | Clinic Management

> [!CAUTION]
> **Private clinic application.** Doctoleb is in development and its application source is private. This page explains the product and architecture through diagrams; it contains no patient records or deployment, clinical certification, or application test results.

## Appointments, patient records, and administration in one clinic workflow

Receptionists manage the schedule, doctors need patient and visit context, and administrators manage the clinic and staff. I developed Doctoleb to connect those activities in one application.

**My contribution:** clinic workflow requirements, multilingual interfaces, staff access rules, and the design of local browser operation and synchronization.

**Tools:** React · TypeScript · IndexedDB · Node.js

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 520px)" srcset="assets/clinic-story-v4-mobile-dark.svg">
  <source media="(max-width: 520px)" srcset="assets/clinic-story-v4-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/clinic-story-v4-dark.svg">
  <img src="assets/clinic-story-v4-light.svg" alt="An appointment calendar connects to a patient-record folder and visit timeline. Staff and clinic setup support the connected clinic day." width="680">
</picture>

### Built around a clinic's working day

- **A connected schedule and record:** appointments, patient information, and visit administration belong to the same workflow.
- **Languages used by the staff:** English, Arabic, and French, with right-to-left Arabic layouts.
- **Interrupted connectivity:** local browser storage and synchronization distinguish a saved local change from one accepted by the server.
- **Staff responsibilities:** receptionists, doctors, and administrators interact with the parts of the application their work requires.

<details>
<summary><strong>Engineering details: application structure, local storage, and synchronization</strong></summary>

| Component | Purpose |
| --- | --- |
| React and TypeScript PWA | Appointments, records, and visit administration in the browser. |
| IndexedDB | Store application data locally. |
| Node-based server coordination | Synchronize changes and report their acceptance or conflicts. |
| Multilingual UI | English, Arabic, and French presentation, including right-to-left layouts. |
| Staff access rules | Separate administrative and clinical responsibilities. |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/local-first-dark.svg">
  <img src="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/local-first-light.svg" alt="Clinic architecture: clinic roles use local browser storage, with dashed paths showing synchronization and server coordination." width="500">
</picture>

### Make synchronization state understandable

A saved local change and a server-confirmed change are different states. I designed synchronization around pending changes, retries, duplicate submissions, concurrent edits, conflicts, and recovery.

Staff access rules apply to data access as well as interface controls. Hiding a button alone does not establish authorization.

- [Application architecture](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/docs/architecture.md)
- [Clinic workflows](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/docs/workflows.md)

</details>

[Back to my portfolio](https://github.com/MahdiHajjHassan)
