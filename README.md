# Odoo local development with Docker

This stack runs Odoo 19, PostgreSQL 16, and Adminer (a PostgreSQL web GUI).

## Start

Make sure Docker Desktop is running, then run:

```bash
docker compose up -d
```

On every startup, the one-shot `odoo-init` service first creates/updates the
database and ensures Sales, Invoicing, Inventory, Purchase, Point of Sale, and
the local administrator bootstrap module are installed. Open:

- Odoo: http://localhost:8079

The database is created automatically. The sole local login is:

- `admin@gmail.com` / `password` — full administrator permissions

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
The Odoo configuration and custom modules are copied into the image during the
build, so changes to either are included automatically on the next deployment.

## Coolify deployment

Create a Docker Compose application from this repository and select
`compose.yaml`. Configure the values from `.env.example` in Coolify's
Environment Variables page, using a strong `POSTGRES_PASSWORD`.

Enable automatic deployment for the production branch in Coolify. When the Git
provider webhook is connected, each push rebuilds the custom Odoo image, runs
the module initialization service, and then starts Odoo. Repository bind mounts
are intentionally not used, so **Preserve Repository During Deployment** is not
required.

If ports `8079` or `8081` are already in use, change `ODOO_PORT` or
`ADMINER_PORT` in `.env`.
