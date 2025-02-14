# Application name

Purpose of the application here...

## Requirements

- Python >= 3.8.5
- Node >= 16.19

## Backend

Please, before you start with the process, create your own virtual environment. Remember to activate it every time you are developing the tool

Create virtual environment:

```bash
python -m venv <env_name>
```

Activate virtual environment:

```bash
<env_name>\Scripts\activate
```

### Install Pyhthondependencies

```bash
pip install -r back\requirements.txt
```

### Environment variables

Create a file called as settings.py manually in the back folder wit this content:

```python
DB_PATH = r'db\tech_exercise.db'
DEBUG_MODE = True
```

### Populate DB

Run the file populate_db.py to create Data Base schemas and add testing entries.

```bash
python back\utils\populate_db.py
```

## Frontend

### Install npm dependencies

```bash
cd front\
npm i
```

### Launch frontend server

This commando will release the frontend server on the port 5173 (by default) for development purposes:

```bash
cd front\
npm run dev
```

## Run application

```bash
python app_front.py
```

## Run build

Generate the statict HTML files for production

```bash
cd front\
npm run build
```
