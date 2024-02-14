# SIPGATE Django Application

## Introduction

This Django application enables users to make outgoing calls using the Sipgate API and stores logs of both incoming and outgoing calls in the database. It provides a convenient interface for managing SIPGATE users, devices, and call logs.

## Installation

1. Clone the GitHub repository:

    ```bash
    git clone https://github.com/RohitSingh555/SIPGATE.git
    ```

2. Navigate to the project folder:

    ```bash
    cd SIPGATE
    ```

3. Create and activate a virtual environment (optional but recommended):

    ```bash
    python -m venv env
    source env/bin/activate  # For Linux/Mac
    .\env\Scripts\activate   # For Windows
    ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Apply migrations to set up the database:

    ```bash
    python manage.py migrate
    ```

6. Create a superuser for accessing the admin dashboard:

    ```bash
    python manage.py createsuperuser
    ```

    Follow the prompts to create a superuser account. For testing purposes, you can use "admin" for both the username and password.

7. Start the development server:

    ```bash
    python manage.py runserver
    ```

8. Access the Django admin dashboard in your web browser:

    ```
    http://localhost:8000/admin/
    ```

## Usage

### 1. Managing SIPGATE Users

To manage SIPGATE users, follow these steps:

1. **Login to the Django Admin Dashboard:**
   - Access the Django admin dashboard using the superuser credentials created during installation. The URL is typically: `http://localhost:8000/admin/`.

2. **Create SIPGATE Users:**
   - Navigate to the "Sipgate users" section.
   - Click on "Add Sipgate user".
   - Fill in the required details:
     - **User ID:** A unique identifier for the user (e.g., Tim_01).
     - **Display Name:** The name to be displayed (e.g., Tim Cook).
     - **Phone Number:** The phone number associated with the user (e.g., +4915207181215).
     - **Caller ID:** The ID to be displayed when making calls (e.g., 0211-87973990565).
     - **Sipgate API Token:** The token required for API authentication.
     - **Sipgate API Token ID:** The ID associated with the API token.
   - Save the user.
   - For example these two users can be there
    | User ID    | Display Name       | Phone Number       | Caller             | Caller ID           | API Token                             | Token ID   |
    |------------|--------------------|--------------------|--------------------|---------------------|---------------------------------------|------------|
    | Tim_01     | Tim Cook           | +4915207181215     | 49021187973990565 | 0211-87973990565   | c533fb19-c9f9-412b-a37e-b91aeb9b1519  | token-5KIN89|
    | Sarvesh_01 | Tim Daniel SipGate | +4921187973990565  | 49021187973990566 | 0211-87973990565   | c533fb19-c9f9-412b-a37e-b91aeb9b1519  | token-5KIN89|





### 2. Managing Devices

To manage devices, follow these steps:

1. **Create Devices:**
   - Navigate to the "Devices" section.
   - Click on "Add Device".
   - Enter the device details:
     - **Device ID:** (optional) A unique identifier for the device.
     - **Caller ID:** The ID to be displayed when using this device.
     - **Assigned User:** Choose the SIPGATE user to whom this device should be assigned.
   - Save the device.
  
   - for example these were our devices
     | Device ID | Caller ID        | Assigned User |
     |-----------|------------------|---------------|
     | e0        | 0211-87973990565 | 1             |
     | e1        | 0211-87973990565 | 2             |

### 3. Making Outgoing Calls

To make outgoing calls, follow these steps:

1. **Navigate to the Home Page:**
    - Select a User (Important)
   - Use the provided interface to navigate to the outgoing call page.

2.  **Create Contacts**
    - Can use our homepage contact form or can use the admin panel
    for example these were our contacts: name and phone_number fields
    | Name      | Phone Number     |
    |-----------|------------------|
    | Tim Da    | +4915207181215   |
    | Test user | 0211-87973990565 |
    | Sarvesh   | 0211-87973990566 |

4. **Enter Phone Number:**
   - Enter the phone number you wish to call into the designated field.
   Or click on the call Icon in front of the number given in the SIPgate contacts below to copy that number into the calling field.

### Integrating Ngrok for Call Logging in Django

To seamlessly generate logs for incoming and outgoing calls in your SIPGATE Django application, follow these steps:

1. **Install Ngrok:**
   - Download Ngrok from the official website or install it via package manager (e.g., Homebrew on macOS). or just directly install ngrok in Django itself and authenticate yourself only then you will be able to run the following commands and steps.
   - Follow the installation instructions provided for your operating system.

2. **Integrate Ngrok with Django:**
   - After installation, navigate to your Django project directory.
   - Start Ngrok alongside your Django server using the command:
     ```
     ngrok http <django_server_port>
     ```
   - Ngrok will create a tunnel to your local server, providing a forwarding URL.

3. **Update Webhook Endpoints:**
   - Configure your webhook endpoints to use Ngrok's forwarding URLs. For example:
     - For incoming calls: `<ngrok_forwarding_url>/incoming-call`
     - For hangup events: `<ngrok_forwarding_url>/hangup`

4. **Update Allowed Hosts Endpoint:**
   - In your Django settings (`settings.py`), update the `ALLOWED_HOSTS` variable to include the Ngrok forwarding URL:
     ```python
     ALLOWED_HOSTS = ['<ngrok_forwarding_url>', 'localhost', '127.0.0.1']
     ```

5. **Update Global Variable in Views:**
   - In your views, define a global variable for Ngrok to ensure consistency across endpoints:
     ```python
     ON_HANGUP_URL = '<ngrok_forwarding_url>'
     ```

These steps will ensure that your Django application effectively logs incoming and outgoing calls using Ngrok, allowing for seamless call management and monitoring.


5. **Initiate Call:**
   - Click on the call button to initiate the call. The call will be made using the configured SIPGATE user and device.

### 5. Viewing Call Logs

To view call logs, follow these steps:

1. **Navigate to the Call Logs Page:**
   - Access the call logs section in the Django admin dashboard.

2. **Filter and View Logs:**
   - Filter logs based on criteria such as user, device, call type (incoming/outgoing), etc.
   - View detailed call logs including timestamps, call duration, and other relevant information.

This comprehensive guide should help users effectively utilize the SIPGATE Django application to manage users, devices, make outgoing calls, and view call logs seamlessly.
