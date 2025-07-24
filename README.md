# Sample FastAPI Project with Pytest and Allure Reporting

This repository contains a small FastAPI application together with a test
suite written for `pytest`.  The tests are instrumented with the
`allure‑pytest` plugin so that you can generate rich HTML test reports.

The API exposes a single resource (`/items/{item_id}`) and allows you to
create, retrieve and update items via HTTP requests.  A simple in‑memory
dictionary is used as the data store, so you do not need a database to
experiment with the endpoints.

## Prerequisites

- **Python 3.9 or newer**.  If you do not already have Python
  installed on your machine, install it before proceeding.
- **Pip** – the Python package manager.
- **Allure command‑line tools** (optional for viewing HTML reports).  You
  can download the CLI from the [Allure GitHub releases](https://github.com/allure-framework/allure2) or
  install it via your package manager.
- A terminal or command prompt with basic Unix commands.

It is recommended to work inside a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to isolate the
project’s dependencies from your global Python installation.  The
FastAPI documentation also notes that you should create and activate a
virtual environment before installing server applications【958030133469584†L320-L339】.

## Project Structure

```
sample_api/
├── app/
│   ├── __init__.py
│   └── main.py      # FastAPI application with GET/POST/PUT endpoints
├── tests/
│   ├── __init__.py
│   └── test_api.py  # pytest test suite with Allure annotations
├── requirements.txt # Dependency specification
└── README.md
```

## Set‑up and Installation

1. **Clone or download** this repository to your local machine.

2. **Create and activate a virtual environment** (recommended).  On Linux
   or macOS you can do:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows:

   ```cmd
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies** using pip:

   ```bash
   pip install -r requirements.txt
   ```

   The FastAPI documentation notes that you can install the ASGI server
   `uvicorn` by running `pip install "uvicorn[standard]"`【958030133469584†L320-L339】.
   However, this project’s `requirements.txt` already includes
   `fastapi`, `uvicorn`, `pytest` and `allure‑pytest` so a single
   installation command suffices.

4. **Install the Allure CLI** (optional).  While the `allure‑pytest` Python
   plugin collects test metadata, the report must be rendered using
   Allure’s command‑line tool.  Follow the [official installation
   instructions](https://docs.qameta.io/allure/#_installing_a_commandline) for your
   operating system.

## Running the API Server

Once the dependencies are installed you can start the FastAPI server.  The
server is run with `uvicorn`, specifying the module and object that
export the application.  According to the FastAPI documentation, the
command `uvicorn main:app` refers to the file `main.py` and the object
`app` within that file【958030133469584†L347-L359】.  Uvicorn’s `--reload`
flag restarts the server when you change the code, which is helpful
during development but should not be used in production【958030133469584†L369-L374】.

From the root of the repository run:

```bash
uvicorn app.main:app --reload --port 8000
```

You should see output similar to the following:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Now you can interact with the API using `curl`, a browser, or tools like
Postman.  For example, create an item:

```bash
curl -X POST http://127.0.0.1:8000/items/1 \
     -H "Content-Type: application/json" \
     -d '{"name": "Widget", "description": "A useful widget"}'
```

Retrieve the same item:

```bash
curl http://127.0.0.1:8000/items/1
```

Update the item:

```bash
curl -X PUT http://127.0.0.1:8000/items/1 \
     -H "Content-Type: application/json" \
     -d '{"name": "Widget", "description": "An updated description"}'
```

## Running Tests

This project uses `pytest` for testing and the `allure‑pytest` plugin to
collect reporting information.  First ensure that the package
`allure‑pytest` is installed.  The QA Automation Expert blog notes that
you can install it via pip: `pip install allure-pytest`【177359106055276†L139-L146】.

To execute the test suite run the following command from the root of the
repository:

```bash
pytest --alluredir=allure-results
```

The `--alluredir` option tells pytest to store the raw test results in
the specified directory.  The Allure documentation explains that
supplying this option will save the necessary data in the test
results directory【307334137263701†L468-L480】.  The same blog
demonstrates invoking pytest with `--alluredir`【177359106055276†L180-L186】.

After the tests complete you should see output indicating that three
tests passed (plus one that checks for a 404 error).  A new folder
named `allure-results` will be created containing the data used to
generate the HTML report.

### Generating the Allure Report

With the test results available, you can generate and view the HTML
report using the Allure CLI.  Run:

```bash
allure serve allure-results
```

This command starts a temporary web server and automatically opens your
default browser to display the report【307334137263701†L484-L490】.  Alternatively, you can
use `allure generate allure-results -o allure-report` to generate the
HTML files into a directory of your choice and then open them manually.

## Notes

- The project stores items in memory.  If you restart the API server
  the items collection will be reset.
- When running the server with `uvicorn app.main:app --reload`, any
  changes to the Python files will cause the server to restart
  automatically.  The FastAPI documentation cautions that `--reload` is
  intended for development only【958030133469584†L369-L374】.
- You can extend this project by adding DELETE endpoints, integrating a
  database layer, or deploying it via Docker.

Feel free to fork and modify this sample project for your own
experiments!
