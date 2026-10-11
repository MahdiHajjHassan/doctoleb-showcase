# Doctoleb | AI Staff Workflows and WhatsApp Booking

> [!CAUTION]
> **Private clinic application.** Doctoleb is in development and its application source is private. This page explains the product and architecture through diagrams; it contains no patient records or deployment, clinical certification, or application test results.

I organized Doctoleb around a connected clinic day with conversational AI for staff and patients. Appointments, patient records, reports and financial analysis share the platform while each staff role has a distinct job.

| Role | Main task | Product need |
| --- | --- | --- |
| Receptionist | Manage appointments and visit administration. | A clear schedule and the relevant administrative information. |
| Doctor | Work with patient records and visits. | Patient context and continuity between visits. |
| Administrator | Configure the clinic and staff responsibilities. | Clinic settings and staff access management. |

## Give the staff agent a goal

Staff describe a task in chat, much as they would instruct a coding agent. The agent plans how to complete it, navigates the application, and interacts with the relevant workflows.

- Book appointments and update patient profiles.
- Generate reports for the clinic to review and validate.
- Analyze payments and clinic financials.

Each clinic validates its own reports. These reporting and administration workflows support the staff's work.

## Book and update profiles on WhatsApp

Patients talk to a WhatsApp AI assistant to arrange appointments or update their profiles. The assistant connects the conversation to the clinic software and writes the booking or profile change back to the platform.

## Language and connectivity

I designed English, Arabic, and French interfaces, including right-to-left Arabic layouts. Local browser operation and synchronization account for connectivity interruptions during the working day.

## Contribution

I translated these roles into requirements, connected conversational AI to staff and patient workflows, designed the multilingual interfaces, and defined staff visibility and synchronization responsibilities.

[Project overview](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/README.md) · [Architecture](https://github.com/MahdiHajjHassan/doctoleb-showcase/blob/main/docs/architecture.md)
