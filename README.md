# Doctoleb | AI Clinic Management

> [!CAUTION]
> **Private clinic application.** Doctoleb is in development and its application source is private. This page explains the product and architecture through diagrams; it contains no patient records or deployment, clinical certification, or application test results.

## Manage clinic work through conversation

Doctoleb is AI clinic software for receptionists, doctors and administrators. Staff tell an agent what they want to do; it plans the task, navigates the application and interacts with clinic workflows for appointments, patient profiles, reports and payment analysis.

Patients can also talk to an AI assistant on WhatsApp to book appointments and update their profiles. Those changes return to the clinic software, connecting patient conversations to the staff's working environment.

**My contribution:** I developed the clinic product and defined its staff and WhatsApp AI workflows, multilingual interfaces, staff access rules, and local browser operation and synchronization design.

**Tools:** React · TypeScript · IndexedDB · Node.js

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 520px)" srcset="assets/clinic-story-v6-mobile-dark.svg">
  <source media="(max-width: 520px)" srcset="assets/clinic-story-v6-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/clinic-story-v6-dark.svg">
  <img src="assets/clinic-story-v6-light.svg" alt="A staff request passes through AI planning, navigation and actions into appointments, patient profiles, reports and payment analysis. A separate WhatsApp conversation updates booking and profiles. Generated reports go to clinic review and validation." width="680">
</picture>

### Two conversational paths into the clinic

| User | What they can ask for | Result in the software |
| --- | --- | --- |
| Clinic staff | Book appointments, manage profiles, generate reports and analyze payments or financials. | The agent plans, navigates and carries out the task in the application. |
| Patient on WhatsApp | Book an appointment or update profile information. | Booking and profile changes return to the clinic's records. |

Generated reports go to each clinic for review and validation. Staff can use payment and financial analysis alongside the appointment and patient workflows.

### What I built and designed

- **Connected clinic workflows:** scheduling, patient information and visit administration within the same product.
- **Conversational AI interaction:** staff instructions become planned application actions; patient messages connect to booking and profiles.
- **Multilingual interfaces:** English, Arabic and French, including right-to-left Arabic layouts.
- **Local operation and synchronization:** distinguish a change saved in the browser from a change accepted by the server.
- **Staff access rules:** separate reception, clinical and administrative responsibilities.

<details>
<summary><strong>Engineering details: AI workflows, application structure, and synchronization</strong></summary>

### Application responsibilities

| Component | Responsibility |
| --- | --- |
| Staff AI agent | Plan, navigate and perform clinic tasks from conversational instructions. |
| WhatsApp AI assistant | Connect patient messages to appointments and profile updates. |
| Reports and financial analysis | Produce reports for clinic validation and analyze payments and financials. |
| React and TypeScript PWA | Present appointments, records and visit administration in the browser. |
| IndexedDB | Store application data locally. |
| Node-based server coordination | Synchronize changes and report acceptance or conflicts. |
| Multilingual UI | Present English, Arabic and French content with appropriate text direction. |
| Staff access rules | Apply role boundaries to application data and actions. |

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/local-first-dark.svg">
  <img src="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/local-first-light.svg" alt="Clinic architecture: clinic roles use local browser storage, with dashed paths showing synchronization and server coordination." width="500">
</picture>

### Make saved and synchronized states clear

A local save and a server-confirmed change are distinct states. I designed synchronization around pending changes, retries, duplicate submissions, concurrent edits, conflicts and recovery, so the interface can communicate what still needs synchronization.

Staff authorization applies to data access and application actions as well as interface controls.

- [Application architecture](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/docs/architecture.md)
- [Clinic workflows](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/docs/workflows.md)

</details>

[Back to my portfolio](https://github.com/MahdiHajjHassan)
