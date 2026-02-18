# HubSpot → Monday.com Migration Engine

A Python-based one-time data migration engine designed to transfer structured CRM data from HubSpot to Monday.com.

This tool focuses on reliability, strict validation, and controlled concurrency. It is **not** a real-time integration or bi-directional sync system.

---

## 📌 Project Overview

This project migrates large datasets (10k–20k+ records) from HubSpot CRM (v3 REST API) to Monday.com (GraphQL API).

It was built to handle:
- Large record volumes
- Strict column mapping requirements
- Controlled parallel API execution
- Resume capability after interruption
- Fail-fast validation to prevent silent data loss

The system follows a modular architecture separating data fetching, transformation, mutation, and orchestration logic.

---

## 🎯 Problem Statement

Migrating CRM data between platforms introduces challenges such as:
- Cursor-based pagination handling
- API rate limits and complexity budgets
- Data type mismatches (e.g., timestamps → date columns)
- Strict column mapping validation
- Safe recovery after unexpected interruption

This engine addresses those challenges with explicit architectural decisions.

---

## 🏗️ Architecture & Design Decisions

### 1️⃣ Cursor-Based Pagination (HubSpot)
HubSpot records are fetched using the `after` cursor mechanism to:
- Safely iterate over large datasets
- Avoid memory overload
- Maintain deterministic processing order

### 2️⃣ Modular Separation of Concerns
The project is structured into clear layers:
- **Clients Layer**
  - `hubspot_client.py` – Handles HubSpot API authentication and fetching
  - `monday_client.py` – Handles Monday GraphQL mutations
- **Transformation Layer**
  - `company_mapper.py` – Transforms HubSpot objects into Monday item structure
- **Configuration Layer**
  - Environment variables and column mapping definitions
- **State Layer**
  - Checkpoint persistence logic
- **Orchestration Layer**
  - `main.py` – Controls the fetch → transform → load workflow

This design allows adding new object types without modifying the core engine.

### 3️⃣ Controlled Concurrency
The workload is I/O-bound (API-heavy). To improve throughput:
- `ThreadPoolExecutor` is used for parallel mutation calls
- Worker count is configurable
- Execution remains bounded to respect Monday.com API limits

Threading was selected for simplicity and sufficient performance at the target dataset size.

### 4️⃣ Fail-Fast Validation
The system enforces strict validation:
- Missing column mappings raise immediate errors
- Invalid mutation responses halt execution
- No silent column skipping

This ensures data integrity during migration.

### 5️⃣ Date Normalization
HubSpot ISO timestamps (e.g. `2026-02-16T09:55:32.363Z`) are converted into Monday.com's required Date column format:

```json
{ "date": "YYYY-MM-DD" }
```

### 6️⃣ Checkpoint Recovery
A checkpoint file stores the last processed pagination cursor. If the script is interrupted:
- It resumes from the last successful batch.
- Previously processed records are not re-fetched.

Checkpoint updates occur only after successful batch completion.

---

## ✨ Core Features

- Cursor-based pagination
- Configurable page limits
- Strict column mapping validation
- Date formatting normalization
- Controlled parallel execution
- Resume-safe checkpoint system
- Explicit error handling
- Modular architecture

---

## 📂 Project Structure

```text
hubspot_monday_migration/
├── clients/
│   ├── hubspot_client.py
│   └── monday_client.py
├── transformers/
│   └── company_mapper.py
├── config/
│   ├── settings.py
│   ├── hubspot_columns.py
│   └── monday_columns.py
├── state/
│   └── checkpoint.py
├── main.py
├── requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```ini
# HubSpot
HUBSPOT_ACCESS_TOKEN=your_hubspot_private_app_token
HUBSPOT_PAGE_LIMIT=100

# Monday
MONDAY_API_TOKEN=your_monday_api_token
MONDAY_COMPANY_BOARD_ID=1234567890
```

---

## 🚀 Running the Migration

To start the migration:

```bash
python main.py
```

### Execution Flow
1. Load configuration
2. Load checkpoint cursor
3. Fetch HubSpot records in batches
4. Transform records
5. Push to Monday.com (concurrently)
6. Update checkpoint after successful batch
7. Continue until dataset is exhausted

---

## ⚡ Performance Characteristics

- Optimized for I/O-bound API workloads
- Concurrency significantly improves throughput over sequential execution
- Suitable for ~20k+ records depending on API latency and complexity limits
- Worker count can be tuned based on Monday.com API constraints
- **Example observed performance**: ~2–3 records per second with 6 workers (subject to API latency)

---

## 🛡️ Error Handling Strategy

- API errors are surfaced immediately
- Missing column mappings trigger hard failure
- No silent column skipping
- Checkpoint persists only after successful batch completion
- **Correctness is prioritized over partial completion.**

---

## ⚠️ Limitations

- Designed for one-time migration (not real-time sync)
- No bulk mutation batching implemented
- API rate limits and complexity constraints apply
- Does not implement conflict reconciliation logic

---

## 🔮 Potential Improvements

- Bulk mutation batching (with controlled complexity)
- Exponential backoff retry strategy
- Structured logging
- Support for additional HubSpot object types
- Dry-run validation mode
