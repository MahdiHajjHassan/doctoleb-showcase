# Clinic workflows

I organized Doctoleb around one connected clinic day: appointments, patient records, and visit administration. The design assigns each activity to the staff who need it.

| Role | Responsibility | Product concern |
| --- | --- | --- |
| Receptionist | Appointments and daily visit administration | A clear schedule and appropriate administrative visibility. |
| Doctor | Patient records and visits | Relevant clinical context and continuity. |
| Administrator | Clinic setup and staff responsibilities | Configuration and appropriate access boundaries. |

Appointments, records, and administration belong to one clinic workflow, while staff interact with different parts of it. I connected these activities in the product design and kept responsibilities explicit.

I designed the interface for English, Arabic, and French, including right-to-left Arabic layouts. Local operation and later synchronization account for connectivity interruptions.

## Public showcase boundary

This showcase contains no real patients, clinical examples, or appointment records. Application source is private. The public material documents product and architecture decisions; it supplies no production rollout, privacy audit, recovery test, or synchronization runtime results.

[Project overview](../README.md) · [Architecture](architecture.md)
