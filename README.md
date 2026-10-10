# Doctoleb

## A clinic's working day, brought together.

I developed a clinic-management application that brings **appointments, patient records, and visit administration** into one place. Its design connects the work of receptionists, doctors, and clinic administrators.

*Personal project · Application source private · Public architecture showcase*

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 520px)" srcset="assets/clinic-story-v3-mobile-dark.svg">
  <source media="(max-width: 520px)" srcset="assets/clinic-story-v3-mobile-light.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/clinic-story-v3-dark.svg">
  <img src="assets/clinic-story-v3-light.svg" alt="Doctoleb concept illustration: an appointment calendar connects to a patient-record folder and visit timeline; not an application screenshot." width="680">
</picture>

*Concept illustration of the clinic workflow, not an application screenshot.*

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

| Area | Architecture and evidence boundary |
| --- | --- |
| Application | React and TypeScript progressive web application with private source. |
| Local persistence | IndexedDB for browser-resident data; part of the local-first approach. |
| Synchronization | Node-based server coordination documented in the design; no multi-device runtime results are provided by the public showcase. |
| Language and layout | English, Arabic, and French; right-to-left Arabic layouts are part of the product scope. |
| Staff visibility | Receptionists, doctors, and administrators have different responsibilities; application and server boundaries need to reflect them. |

### The engineering questions

A locally accepted change and a server-confirmed change are different states. The synchronization design distinguishes those states and addresses retries, duplicate submissions, concurrent edits, conflicts, device access, and recovery.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/local-first-dark.svg">
  <img src="https://raw.githubusercontent.com/MahdiHajjHassan/doctoleb-showcase/main/assets/local-first-light.svg" alt="Existing architecture illustration: clinic roles use local browser storage, with dashed paths showing synchronization and server coordination." width="500">
</picture>

The existing diagram illustrates the architecture direction. It does not establish verified production behavior.

### Read further

- [Architecture and evidence boundaries](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/docs/architecture.md)
- [Clinic workflows](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/docs/workflows.md)

</details>

This public showcase contains no patient records and does not claim a production rollout, clinical certification, or executed implementation checks.

[Mahdi Hajj Hassan](https://github.com/MahdiHajjHassan)
