# Organization Management API

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/suruthi-gobika-S/organisation_management
    cd organization_management
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```sh
    python manage.py migrate
    ```


## API Endpoints

- `GET /api/organizations/` - List all organizations
- `GET /api/roles/` - List all roles
- `GET /api/users/` - List all users

## Running Tests

1. To run tests and generate a report, use:
    ```sh
    pytest --html=report.html
    ```

## Authentication

To access the API, you need to be authenticated. 

## Permissions

Permissions are enforced based on the user's role. Refer to the project requirements for details.

## need to work  
5. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```sh
    python manage.py runserver
    ```
