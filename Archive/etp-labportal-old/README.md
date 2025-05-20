
# Lab Exceptions Portal

## Running the Project (Docker)

```bash
docker compose up --build
```

Visit http://localhost:8000 to access the app.

## Modes of Admin CSV Import

- **Overwrite**: Replace all existing data.
- **Merge**: Update fields and flag conflicts.
- **Retain**: Skip duplicates.
- **Revert**: Restore from backup.

## Requirements

- Flask
- SQLAlchemy
- Bootstrap (included via CDN)
