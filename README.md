# Odoo local development with Docker

This stack runs Odoo 18, PostgreSQL 16, and Adminer (a PostgreSQL web GUI).

## Start

Make sure Docker Desktop is running, then run:

```bash
docker compose up -d
```

On every startup, the one-shot `odoo-init` service first creates/updates the
database and installs the local security module. Open:

- Odoo: http://localhost:8079

The database is created automatically. Default local logins are:

- `admin@gmail.com` / `password` — full administrator permissions
- `staff@gmail.com` / `password` — POS selling, POS-only menu, and read-only
  access to all other backend models

These intentionally simple credentials are for local development only.

### Adminer (local dev only)

Adminer is excluded from production by default. To use it locally:

```bash
docker compose --profile dev up -d
```

- PostgreSQL web GUI (Adminer): http://localhost:8081

Adminer login values:

- System: `PostgreSQL`
- Server: `db`
- Username: `odoo`
- Password: `odoo`
- Database: leave blank to list databases, or enter `postgres` / your Odoo database name

The values above come from `.env`. Change the passwords there before using this
outside local development.

## Common commands

```bash
# View service status
docker compose ps

# Follow Odoo logs
docker compose logs -f odoo

# Restart the stack
docker compose restart

# Stop the stack (keeps database data)
docker compose down

# Stop and permanently delete all local Odoo/PostgreSQL data
docker compose down -v
```

Put custom Odoo modules in `addons/`, then restart Odoo and update the Apps list.

If ports `8079` or `8081` are already in use, change `ODOO_PORT` or
`ADMINER_PORT` in `.env`.
