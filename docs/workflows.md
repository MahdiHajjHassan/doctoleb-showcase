# Clinic workflows

> [!CAUTION]
> **Public showcase; private application.**
> Doctoleb’s application source is private. This showcase documents product and architecture decisions using explanatory illustrations. It includes no patient information, deployment records, clinical certification, or executed implementation checks.

I organized Doctoleb around one connected clinic day: appointments, patient records, and visit administration. The design assigns each activity to the staff who need it.

| Role | Responsibility | Product concern |
| --- | --- | --- |
| Receptionist | Appointments and daily visit administration | A clear schedule and appropriate administrative visibility. |
| Doctor | Patient records and visits | Relevant clinical context and continuity. |
| Administrator | Clinic setup and staff responsibilities | Configuration and appropriate access boundaries. |

Appointments, records, and administration belong to one clinic workflow, while staff interact with different parts of it. I connected these activities in the product design and kept responsibilities explicit.

I designed the interface for English, Arabic, and French, including right-to-left Arabic layouts. Local operation and later synchronization account for connectivity interruptions.

[Project overview](../README.md) · [Architecture](architecture.md)
