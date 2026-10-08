# Holmium Orchestrator

Holmium is an intelligent, AI-driven customer support platform built with a multi-turn troubleshooting workflow. It acts as a first-line support representative, helping users diagnose and resolve issues interactively before seeking explicit consent to escalate or create formal database-backed support tickets.

## Key Features

- **Intelligent Multi-Turn Conversations:** Maintains chat continuity across requests using session identifiers (`session_id`) and dynamic in-memory session stores (with seamless database persistence mapping).
- **Troubleshoot-First Workflow:** Instructed to actively help solve problems or offer workarounds rather than prematurely triggering ticket creation on the first message.
- **Explicit User Consent Guardrails:** Uses function calling (`create_support_ticket`) only after the user explicitly agrees to file a ticket.
- **Structured Taxonomy:** Categorizes requests into strict boundaries (`account`, `technical`, `billing`, `feature_request`, and `general`) to minimize ticket overlap.
- **Modern UI/UX:** Responsive Next.js frontend featuring Shadcn UI layout primitives, an adaptive collapsible sidebar, and real-time state management.

## Tech Stack

### Backend

- **Framework:** FastAPI (Python)
- **AI Engine:** Google GenAI SDK
- **Validation & Data:** Pydantic, SQLAlchemy
- **Server:** Uvicorn

### Frontend

- **Framework:** Next.js (React / TypeScript)
- **Styling:** Tailwind CSS
- **Components:** Shadcn UI
- **Icons:** Lucide React

## Project Architecture

```text
holmium/
├── backend/
│   ├── alembic/
│   │   └── versions/         # DB migration history
│   ├── app/
│   │   ├── agents/
│   │   │   └── support.py    # Gemini client config, tool definitions, & session store
│   │   ├── db/
│   │   │   ├── base.py       # SQLAlchemy declarative base setup
│   │   │   ├── models.py     # SQLAlchemy ORM DB models
│   │   │   └── seed.py       # Initial DB seeding script
│   │   ├── models/
│   │   │   └── enums.py      # Shared enums
│   │   ├── config.py         # Environment and settings management
│   │   ├── database.py       # Database engine and session dependency injection
│   │   ├── dtos.py           # Pydantic data transfer objects (DTOs)
│   │   └── main.py           # FastAPI entry point and API route handlers
│   ├── test/
│   │   ├── conftest.py       # Pytest fixtures and configuration
│   │   ├── test_db.py        # DB and model tests
│   │   └── test_main.py      # API endoint and routing tests
│   ├── .env.test
│   ├── alembic.ini
│   └── requirements.txt
├── frontend/
│   ├── public/               # Static assets
│   └── src/
│       ├── app/
│       │   ├── globals.css
│       │   ├── layout.tsx    # Root layout
│       │   └── page.tsx      # Main UI
│       ├── components/
│       │   └── ui/           # ShadCN components
│       ├── hooks/            # Custom React hooks
│       ├── lib/
│       │   ├── api.ts        # Backend API fetch function
│       │   ├── chat.ts       # Message helper functions
│       │   └── utils.ts      # General utility helpers
│       └── types/
│           └── agent.ts      # TS interfaces
├── .gitignore
├── Makefile
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- pnpm
- Google AI Studio API Key
- Supabase Account

### Environment Configuration

Copy the example .env file and replace the placeholders with your real credentials:

```bash
cp .env.example .env
```

As mentioned earlier, you will need a Google AI Studio API key (if you don't have one, click [here](https://aistudio.google.com/api-keys)) and a Supabase account (username, password, and port).

### Install Dependencies

Run `make install` in the **root directory**:

```bash
make install
```

### Set Up Database

Run the Alembic migration command to set up your database schema, then seed the initial data:

```bash
make migrate-up
make seed
```

### Configure Gemini Model (Optional)

By default, the Gemini model is set to _Gemini 3.5 Flash Lite_. Optionally, you can change the Gemini model into any one that you prefer by changing the settings in `backend/app/config.py`:

```
class Settings(BaseSettings):
    gemini_api_key: str
    database_url: str
    database_url_async: str
    database_url_sync: str
    fast_model: str = "gemini-3.5-flash-lite"   # Insert your preferred model here
    reasoning_model: str = "gemini-3.6-pro"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore"
    )
```

### Run Development Servers

You can run the backend and frontend development servers in separate terminal windows using the Makefile development targets:

- Run Backend Development Server:
  ```bash
  make dev-backend
  ```
- Run Frontend Development Server:
  `bash
    make dev-frontend
    `
  Once both servers are running, open http://localhost:3000 in your browser to interact with the support agent.

## Database

All tickets are stored in `public.support_tickets` table in Supabase with the following schema:
| Column | Type | Description |
| --- | --- | --- |
| `id` | `uuid` | Unique ticket identifier |
| `user_email` | `varchar` | Ticket submitter's email |
| `subject` | `varchar` | Short ticket title |
| `description` | `text` | Ticket summary |
| `status` | `enum` | Ticket status (`OPEN`, `IN_PROGRESS`, `RESOLVED`, or `CLOSED`) |
| `created_at` | `timestamptz` | Time at which the ticket was created |
| `updated_at` | `timestamptz` | Time at which the ticket was last updated |
| `category` | `enum` | Support ticket category (`TECHNICAL`, `BILLING`, `ACCOUNT`, `FEATURE_REQUEST`, or `GENERAL`) |

## API Overview

| Method | Path             | Description                                   |
| ------ | ---------------- | --------------------------------------------- |
| `GET`  | `/`              | Main chat UI                                  |
| `POST` | `/api/agent/run` | Accept user message and return agent response |

## Makefile Commands

| Command                                     | Description                                                                     |
| ------------------------------------------- | ------------------------------------------------------------------------------- |
| `make install`                              | Install project dependencies and set up backend Python virtual environment      |
| `make migrate-create name=<migration_name>` | Create a new Alembic migration (`name` is required)                             |
| `make migrate-up`                           | Apply all pending migrations                                                    |
| `make migrate-down`                         | Roll back the last migration (by one)                                           |
| `make migrate-reset`                        | Roll back all migrations to the base state                                      |
| `make seed`                                 | Seed the database with initial data                                             |
| `make run-backend`                          | Run backend server                                                              |
| `make run-frontend`                         | Run frontend client                                                             |
| `make dev-backend`                          | Run backend development server                                                  |
| `make dev-frontend`                         | Run frontend development client                                                 |
| `make test`                                 | Run backend and frontend tests                                                  |
| `make test-backend`                         | Run backend tests with `pytest`                                                 |
| `make test-frontend`                        | Run frontend tests with `pnpm`                                                  |
| `make vet`                                  | Run type checking and vetting for backend and frontend                          |
| `make vet-backend`                          | Run backend type checking (`mypy`) and linting (`ruff`)                         |
| `make vet-frontend`                         | Run frontend type checking and linting (`pnpm`)                                 |
| `make lint`                                 | Run lint tool for backend and frontend                                          |
| `make lint-backend`                         | Run lint tool (`ruff`) for backend (without fixing)                             |
| `make lint-backend-fix`                     | Run lint tool (`ruff`) for backend with `auto-fix`                              |
| `make lint-frontend`                        | Run lint tool (`pnpm`) for frontend                                             |
| `make clean`                                | Clean up Python cache files, virtual environments, and frontend build artifacts |

## License

Distributed under the MIT License. See `LICENSE` for more information.
