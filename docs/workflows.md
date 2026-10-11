# Doctoleb | Reception, Doctors, and Administration

> [!CAUTION]
> **Private clinic application.** Doctoleb is in development and its application source is private. This page explains the product and architecture through diagrams; it contains no patient records or deployment, clinical certification, or application test results.

I organized Doctoleb around a connected clinic day. Appointments, patient records, and visit administration share a workflow while each staff role has a distinct job.

| Role | Main task | Product need |
| --- | --- | --- |
| Receptionist | Manage appointments and visit administration. | A clear schedule and the relevant administrative information. |
| Doctor | Work with patient records and visits. | Patient context and continuity between visits. |
| Administrator | Configure the clinic and staff responsibilities. | Clinic settings and staff access management. |

## Language and connectivity

I designed English, Arabic, and French interfaces, including right-to-left Arabic layouts. Local browser operation and synchronization account for connectivity interruptions during the working day.

## Contribution

I translated these roles into requirements, connected the appointment and record workflows, designed the multilingual interfaces, and defined staff visibility and synchronization responsibilities.

[Project overview](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/README.md) · [Architecture](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/docs/architecture.md)
