# Identity Reconciliation Service

This Flask application provides a service for identifying and consolidating contacts based on email addresses and phone numbers. It utilizes SQLAlchemy for database management.

## Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the Flask application:

    ```bash
    python main.py
    ```
   
## Project Structure

1. **main.py** : initializes the Flask application, configures the database, and sets up routes.

2. **service.py** : Handles HTTP requests and responses.

3. **handler.py** : Contains business logic for identifying and consolidating contacts.

4. **requirements.txt** : Lists the required Python packages.

## Usage

### Identify Endpoint

To identify contacts, send a POST request to the `/identify` endpoint with JSON data containing either an email address or a phone number. The service will return information about the identified contact, including the primary contact ID, associated emails and phone numbers, and secondary contact IDs.

### Hosted Endpoint
   **API** - /identify

   The API is hosted on the render.com hosting service. You can access the endpoint using https://identity-reconciliation-2-vuph.onrender.com/identify

#### Example request:

You can place the above-mentioned API in POSTMAN and add the JSON body payload as mentioned below - 

```json
POST /identify
Content-Type: application/json

{
    "email": "example@example.com",
    "phoneNumber": "1234567890"
}

