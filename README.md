# Synacktive test

## Run

### Env vars

Please fill a `.env` file at the repository root with the following values:

```txt
POSTGRES_PASSWORD=
POSTGRES_USER=user
POSTGRES_DB=
DB_URL=d
SECRET_PASSPHRASE=
```

### Prod

#### python

```sh
fastapi run app/main.py --port 8000
```

#### Docker

The app will be running on port `8000`

```sh
docker compose build
docker compose up
```

### dev

```sh
fastapi dev app/main.py --port 8000
```
