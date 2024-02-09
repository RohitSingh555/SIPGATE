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
Tim_01	Tim cook	+4915207181215	4921187973990565	0211-87973990565	c533fb19-c9f9-412b-a37e-b91aeb9b1519	token-5KIN89
Sarvesh_01	Tim Daniel SipGate	+4921187973990565	4921187973990566	0211-87973990565	c533fb19-c9f9-412b-a37e-b91aeb9b1519	token-5KIN89

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
e0	0211-87973990565	1
e0	0211-87973990565	2

### 3. Making Outgoing Calls

To make outgoing calls, follow these steps:

1. **Navigate to the Home Page:**
    - Select a User (Important)
   - Use the provided interface to navigate to the outgoing call page.

2.  **Create Contacts**
    - Can use our homepage contact form or can use the admin panel
    for example these were our contacts: name and phone_number fields
Tim Da	+4915207181215
Test user	0211-87973990565
Sarvesh	0211-87973990566

4. **Enter Phone Number:**
   - Enter the phone number you wish to call into the designated field.
   Or click on the call Icon in front of the number given in the SIPgate contacts below to copy that number into the calling field.

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
