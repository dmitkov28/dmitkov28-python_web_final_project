
### Background
This is my first ever fullstack app. I'm keeping it here for posterity (and out of nostalgia 😆)

I added the Docker setup in 2024 to make it easier to run the app, the rest of the code was written in early 2022.

The app is a job board with the following features:
- user authentication (job applicants & businesses)
- user profiles (resume, skills, etc)
- search
- job ads
- applicants can apply for jobs
- companies can post job ads
- good ol' Bootstrap CSS 🚀

### Setup

**Docker (recommended)**:
```
docker compose up -d
```

Run locally:

1. Configure a Postgres db instance:
    
```
DB_NAME: "postgres"
DB_USER: "postgres"
DB_PASSWORD: "super secret"
DB_HOST: "postgres"
DB_PORT: 5432
```

2. Configure a virtual environment
```
pipenv install
```

3. Start Django
```
pipenv shell
python manage.py runserver
```

