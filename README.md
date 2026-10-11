# Doctoleb | AI Clinic Management

> [!CAUTION]
> **Private clinic application.** Doctoleb is in development and its application source is private. This page explains the product and architecture through diagrams; it contains no patient records or deployment, clinical certification, or application test results.

## Run clinic workflows by talking to an AI agent

I developed Doctoleb as AI clinic software for receptionists, doctors, and administrators. Staff describe what they want to accomplish in a conversation. The agent plans the task, navigates the application, and interacts with its workflows to book appointments, manage patient profiles, generate reports for each clinic to review and validate, and analyze payments and financials.

A WhatsApp AI assistant extends this workflow to patients: they can book appointments and update their profiles through conversation, with those changes returned to the clinic software.

**My contribution:** clinic workflow requirements, conversational AI workflows for staff and WhatsApp, multilingual interfaces, staff access rules, and the design of local browser operation and synchronization.

**Tools:** React · TypeScript · IndexedDB · Node.js

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 520px)" srcset="assets/clinic-story-v6-mobile-dark.svg">
  <source media="(max-width: 520px)" srcset="assets/clinic-story-v6-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/clinic-story-v6-dark.svg">
  <img src="assets/clinic-story-v6-light.svg" alt="A staff request passes through AI planning, navigation and actions into appointments, patient profiles, reports and payment analysis. A separate WhatsApp conversation updates booking and profiles. Generated reports go to clinic review and validation." width="680">
</picture>

### Built around a clinic's working day

- **Conversational control across the platform:** tell the staff agent what to do; it plans and carries out the workflow in the application.
- **Clinic reports and financial analysis:** generate reports for clinic validation and analyze payments and financials.
- **Patient conversations on WhatsApp:** book appointments and update patient profiles through the connected AI assistant.
- **A connected schedule and record:** appointments, patient information, and visit administration belong to the same workflow.
- **Languages used by the staff:** English, Arabic, and French, with right-to-left Arabic layouts.
- **Interrupted connectivity:** local browser storage and synchronization distinguish a saved local change from one accepted by the server.
- **Staff responsibilities:** receptionists, doctors, and administrators interact with the parts of the application their work requires.

<details>
<summary><strong>Engineering details: AI workflows, application structure, and synchronization</strong></summary>

| Component | Purpose |
| --- | --- |
| Staff AI agent | Plan, navigate and carry out clinic tasks from conversational instructions. |
| WhatsApp AI assistant | Connect patient conversations to appointment booking and patient-profile updates. |
| Reports and financial analysis | Produce reports for each clinic to review and validate; analyze payments and financials. |
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
