# Doctoleb

> [!CAUTION]
> **Public showcase; private application.**
> Doctoleb’s application source is private. This showcase documents product and architecture decisions using explanatory illustrations. It includes no patient information, deployment records, clinical certification, or executed implementation checks.

## A clinic's working day, brought together.

I developed a clinic-management application that brings **appointments, patient records, and visit administration** into one place. Its design connects the work of receptionists, doctors, and clinic administrators.

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 520px)" srcset="assets/clinic-story-v4-mobile-dark.svg">
  <source media="(max-width: 520px)" srcset="assets/clinic-story-v4-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/clinic-story-v4-dark.svg">
  <img src="assets/clinic-story-v4-light.svg" alt="An appointment calendar connects to a patient-record folder and visit timeline. Staff and clinic setup support the connected clinic day." width="680">
</picture>

### The product decisions

- **One connected working day.** Reception handles appointments and daily administration; doctors need relevant records and visit context; administrators configure the clinic and staff responsibilities.
- **The languages a clinic uses.** English, Arabic, and French interfaces, with Arabic layouts designed for right-to-left reading.
- **Connectivity that varies.** The application design centers on local browser storage, synchronization, and server coordination.

### My contribution

I translated clinic workflows into product requirements, designed multilingual interfaces, and defined local operation and synchronization boundaries. The design assigns data visibility to each staff role according to its responsibilities.

---

<details>
<summary><strong>Engineering details: architecture, local storage, and synchronization</strong></summary>

### Application approach

| Area | Architecture approach |
| --- | --- |
| Application | React and TypeScript progressive web application. |
| Local persistence | IndexedDB for browser-resident data; part of the local-first approach. |
| Synchronization | Node-based server coordination for local changes and synchronization. |
| Language and layout | English, Arabic, and French; right-to-left Arabic layouts are part of the product scope. |
| Staff visibility | Receptionists, doctors, and administrators have different responsibilities; application and server boundaries need to reflect them. |

### The engineering questions

A locally accepted change and a server-confirmed change are different states. The synchronization design distinguishes those states and addresses retries, duplicate submissions, concurrent edits, conflicts, device access, and recovery.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/local-first-dark.svg">
  <img src="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/local-first-light.svg" alt="Existing architecture illustration: clinic roles use local browser storage, with dashed paths showing synchronization and server coordination." width="500">
</picture>

### Read further

- [Application architecture](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/docs/architecture.md)
- [Clinic workflows](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/docs/workflows.md)

</details>

[Mahdi Hajj Hassan](https://github.com/MahdiHajjHassan)
