# 📊 Personal Finance Tracker — Fi MCP Integration

A developer-friendly project that integrates **[Fi Money’s Model Context Protocol (MCP)](https://fi.money/features/getting-started-with-fi-mcp)** to fetch, normalize, and analyze **real-time personal finance data** (assets, liabilities, cash balances, investments, PF/NPS, etc.).

This README includes architecture diagrams, quick start steps, and a minimal API spec so you can clone-and-run or showcase the project in your portfolio.

---

## ✨ Highlights

- 🔐 **Secure, passcode-based connection** to Fi MCP (short‑lived sessions; credentials never shared).
- ⚙️ **Connector → Normalizer → Storage** pipeline (PostgreSQL + Mongo/TSDB + Redis).
- 📈 **Dashboards & Insights**: net worth trends, portfolio movers, leakages, goal checks.
- 🧩 **AI‑ready JSON** that plugs into Claude/Cursor/Windsurf for natural‑language queries.

---

## 🖼️ Architecture Diagrams

### 1) High‑level Flow
![High-level flow](./Project-documentation/high-level-flow.png)

### 2) Auth & Ingest — Sequence
![Auth & Ingest](./Project-documentation/sequence-diagram.png)

### 3) Data Flow & Query Paths
![Data flow](./Project-documentation/data-flow.png)

> **Tip:** Keep these images in `./docs/` in your repo. If you change locations, update the paths above.

---

## 🚀 Getting Started

### Prerequisites
- Node.js (LTS) and npm/yarn/pnpm
- PostgreSQL + MongoDB/TimeSeries DB + Redis
- Fi App (Android/iOS) with **Net Worth Tracker** enabled

### 1. Clone
```bash
git clone <your-repo-url>.git
cd <repo-folder>
```

### 2. Configure Environment
Create a `.env` file in the project root:

```bash
# Fi MCP
FI_MCP_STREAM_URL=https://mcp.fi.money:8080/mcp/stream

# API
PORT=8080
JWT_SECRET=change-this

# Datastores
DATABASE_URL_PG=postgres://user:pass@localhost:5432/fin_db
DATABASE_URL_MONGO=mongodb://localhost:27017/fin_stream
REDIS_URL=redis://localhost:6379
```

### 3. Install & Run
```bash
npm install
npm run start:dev
# or: pnpm i && pnpm dev
```

### 4. Connect Fi MCP
1. In the Fi App, go to **Net Worth Dashboard → Talk to AI → Get Passcode**.
2. Call your API to connect:
   ```bash
   curl -X POST http://localhost:8080/mcp/connect \
     -H "Content-Type: application/json" \
     -d '{"passcode":"<PASTE_FROM_FI_APP>"}'
   ```
3. You should see the connector open a **websocket stream**, normalize payloads, and persist to DBs.

---

## 🔌 Minimal API Spec

> Adjust paths/names to your codebase. These are sensible defaults.

### `POST /mcp/connect`
Exchange Fi passcode, start the MCP websocket stream, and begin ingestion.

**Body**
```json
{"passcode":"123456"}
```

**Response**
```json
{"status":"connected","sessionExpiresInSec":1800}
```

### `GET /insights?range=6m`
Returns computed aggregates for dashboards (net worth trend, top movers, leakages).

**Response (example)**
```json
{
  "netWorthTrend": [{"t":"2025-03-01","v":123456}, { "t":"2025-08-01","v":171234 }],
  "topMovers": [{"name":"HDFC Flexi Cap","deltaPct":3.2}],
  "leakage": {"idleCash": 25000, "highInterestLoanPct": 14.5}
}
```

### `GET /positions?assetClass=mf`
Raw/normalized positions by filter (mutual funds, stocks, debt, etc.).

---

## 🗄️ Data Model Overview

- **Entities (PostgreSQL):** `users`, `accounts`, `snapshots`, `alerts`
- **Timeseries (Mongo/TSDB):** `positions`, `nav`, `txn`
- **Aggregates (Redis):** `networth:<window>`, `top:<assetClass>`

The **Normalizer/ETL** converts Fi MCP JSON chunks into a common schema and pushes to the right store. See the **Data Flow** diagram above for paths.

---

## 🔒 Security & Privacy

- Encrypted transport (HTTPS/TLS) to MCP and your API.
- **Short‑lived passcodes**; never store Fi credentials.
- Per‑user consent for connecting and revoking sessions.
- Use **RBAC** and **scoped JWTs** on your API for multi‑user setups.

---

## 🧱 Tech Stack

- **Backend:** Node.js / NestJS (or Express/Fastify)
- **Finance Layer:** Fi MCP (websocket stream)
- **Data:** PostgreSQL, MongoDB/TSDB, Redis
- **Deployment:** Docker, Kubernetes (optional)
- **Clients:** Web Dashboard (Next.js), optional AI tools (Claude/Cursor/Windsurf)

---

## 📂 Suggested Structure

```
.
├─ src/
│  ├─ api/               # REST/GraphQL routes
│  ├─ mcp-connector/     # websocket client, reconnection, backpressure
│  ├─ normalizer/        # schema mapping, validation
│  ├─ services/          # insights, alerts, goals
│  ├─ stores/            # pg/mongo/redis clients
│  └─ utils/
├─ docs/                 # diagrams used in README
├─ .env.example
└─ README.md
```

---

## 🛣️ Roadmap

- [ ] OAuth‑style session broker for multi‑device access
- [ ] Derived metrics (CAGR/XIRR) and ML‑based leakage detection
- [ ] Goal simulator API (`/goals/simulate`)
- [ ] Webhooks for third‑party integrations

---

## 🤝 Contributing
Pull requests are welcome! Please open an issue to discuss major changes first.

---

## 📄 License
MIT © Your Name
