Building a Cloud-Scheduled Data Notifier with DigitalOcean Functions

This guide will walk you through setting up a Python script that fetches data from an API, processes it, and sends you a notification, all running on DigitalOcean Functions with a schedule.

Project Overview

Your project aims to:
- Fetch Data: Connect to an external API (you'll replace the example with your chosen API).
- Process Data: Perform some basic logic on the fetched data.
- Notify: Send an update via email (or SMS, which can be a next step).
- Automate: Run this entire process automatically at defined intervals using a cloud-based scheduler.

Why DigitalOcean Functions?

- Serverless: You don't manage servers. DigitalOcean handles all the infrastructure, scaling, and maintenance.
- Cost-Effective: You only pay when your function runs, making it ideal for periodic tasks.
- Built-in Scheduling: Functions can be triggered by a timer, simplifying automation.
- Python Support: Excellent support for Python, allowing you to use familiar libraries.
- Beginner-Friendly: Easier to get started with than provisioning and configuring a full virtual machine 
  for a simple script.

Prerequisites

Before you start, make sure you have:
- A DigitalOcean Account: If you don't have one, sign up at DigitalOcean.
- Python 3 Installed: On your local machine.
- doctl CLI (DigitalOcean command-line tool): This is essential for deploying functions. 
  Follow the installation guide here: DigitalOcean doctl install (https://docs.digitalocean.com/reference/doctl/how-to-install/)
- An Email Service: For sending notifications. 
  For simplicity in this example, we'll use Python's built-in smtplib which requires access to an SMTP server 
  (e.g., from Gmail, Outlook, or your web host). For production, consider dedicated email APIs like SendGrid or Mailgun.

Core Components Explained
- API Interaction (requests library): Python's requests library is the standard for making HTTP requests to APIs.
- Email Notification (smtplib): Python's smtplib module provides an SMTP client session object that can be used  
  to send mail to any Internet machine with an SMTP or ESMTP listener.
- DigitalOcean Functions: Your Python code will be deployed as a "function" that executes in response to a trigger.
- Scheduling: DigitalOcean Functions allows you to set up cron-like schedules that automatically invoke your function.
- Environment Variables: Crucial for securely storing sensitive information like API keys, email passwords, etc., 
  without hardcoding them in your script.

Step-by-Step Guide
Let's break down the process.

1. The Python Script

First, you'll write the Python script that performs the data fetching, processing, and notification.
- requests for API Calls: You'll use this to get data from your chosen API.
- smtplib for Email: This will send the email. 
  You'll need the SMTP server address, port, your email address, and password.

The example code in the next immersive document will show you a basic structure. 
You'll need to adapt it for the specific API you want to monitor and the specific information 
you want to extract and include in your email.

Important Note on smtplib and Security:
Using smtplib directly with your personal email (like Gmail) might require "App Passwords" or 
"Less secure app access" enabled in your email provider's settings, especially for Gmail, due to security policies. 
For robust, scalable, and more secure email sending in a production environment, 
dedicated services like SendGrid, Mailgun, or Amazon SES are highly recommended. 
They handle deliverability and provide APIs that are easier to integrate securely.

2. Setting Up Your DigitalOcean Function Project

On your local machine:

a.  Initialize a Function Project:
Navigate to an empty directory where you want to store your function code.
bash mkdir my-api-notifier cd my-api-notifier doctl serverless init 
This command will create a basic project structure, including a project.yml file.

b.  Create Your Function:
Inside my-api-notifier, create a new folder for your function, e.g., api-monitor.
Inside api-monitor, create two files: __main__.py (your Python script) and requirements.txt.

Your directory structure will look like this:

```
my-api-notifier/
├── api-monitor/
│   ├── __main__.py
│   └── requirements.txt
└── project.yml
```

c.  Populate requirements.txt:
If your Python script uses external libraries (like requests), list them here.

d.  Update project.yml:
This file defines your functions and their configurations. 
You'll need to add an entry for your api-monitor function and configure its runtime and environment variables.

```yaml
# project.yml
apiVersion: 1.0
functions:
  - name: api-monitor # The name of your function
    source_dir: api-monitor # The directory containing your __main__.py
    runtime: python:3.9 # Specify Python runtime
    main: __main__.py # The entry point file
    environment: # Define environment variables for your function
      TARGET_API_URL: "https://jsonplaceholder.typicode.com/posts/1" # Example API
      SENDER_EMAIL: "your_email@example.com"
      SENDER_EMAIL_PASSWORD: "your_email_password" # Use app password if needed
      RECEIVER_EMAIL: "your_recipient@example.com"
      SMTP_SERVER: "smtp.gmail.com" # Or your email provider's SMTP server
      SMTP_PORT: "587" # Or your email provider's SMTP port
    routes: # No HTTP route needed for a scheduled function
      - method: POST
        path: /
    # Add a trigger for scheduling
    triggers:
      - name: hourly-schedule
        type: schedule
        schedule: "0 * * * *" # Cron expression for every hour (minute 0 of every hour)
```
**Important:** You'll replace the placeholder values for `SENDER_EMAIL`, `SENDER_EMAIL_PASSWORD`, `RECEIVER_EMAIL`, `SMTP_SERVER`, `SMTP_PORT`, and `TARGET_API_URL` with your actual details.

3. The Python Script (api-monitor/__main__.py)

Here's an example Python script. This will be provided in a separate immersive document.

4. Deploying Your Function

Once your __main__.py, requirements.txt, and project.yml are set up in the correct directory structure:

a.  Authenticate doctl:
If you haven't already, authenticate doctl with your DigitalOcean account:
bash doctl auth init 
This will open a browser window for authentication.

b.  Deploy Your Function:
From your my-api-notifier directory (the root of your project), run:
bash doctl serverless deploy 
This command will package your function, upload it to DigitalOcean, and set up the project.yml configuration, 
including the scheduler.

5. Scheduling Your Function

In the project.yml above, I've already included a basic schedule:
schedule: "0 * * * *"

This is a cron expression:

0: At minute 0 (the beginning of the hour)
*: Of every hour
*: Of every day
*: Of every month
*: Of every day of the week

So, this function will run once every hour at the top of the hour. 
You can adjust this cron expression to fit your desired interval.

Common Cron Expressions:

*/5 * * * *: Every 5 minutes
0 9 * * 1-5: At 9:00 AM on weekdays (Monday-Friday)
0 0 * * *: Once a day at midnight
You can find more cron examples online, or use a cron expression generator (search "cron expression generator").

6. Managing Secrets (Environment Variables)

In the project.yml above, I've included SENDER_EMAIL_PASSWORD directly. 
For production applications, this is generally NOT recommended.

DigitalOcean Functions provides a way to store secrets more securely. 
While project.yml environment variables are encrypted at rest, for highly sensitive information, 
you might want to manage them directly in the DigitalOcean console under the function's settings, 
or explore DigitalOcean's App Platform for more integrated secret management.

For this beginner project, using environment variables in project.yml is a good starting point 
to understand how to pass dynamic data to your functions.

Next Steps and Refinements
- Error Handling: Add try-except blocks in your Python script to gracefully handle API request failures or email sending issues.
- Logging: Use Python's logging module to print messages to the console (which will appear in your DigitalOcean function logs).
- More Advanced Notifications: Explore Twilio for SMS notifications or a dedicated email API like SendGrid for better deliverability and features.
- Specific API Integration: Replace the dummy API with the actual API you want to monitor. Understand its documentation to parse the response correctly.
- Data Persistence: If you need to store (e.g., track changes over time), consider using DigitalOcean's managed databases (PostgreSQL, MySQL, Redis) or Spaces (object storage).

This structure should give you a solid foundation to build and deploy your first cloud-scheduled Python application!

======================================
Q: is there some good api that you 
could recommend i use in this project?
======================================

A: That's a great question, and choosing the right API is key to a successful learning project! 
Based on your goals and your index.html content (which shows an interest in a specific item, 
implying you might like data related to real-world objects or events), I have a couple of solid recommendations.

For a beginner project focusing on regular intervals and notifications, 
an API that provides easily consumable, frequently updated, and relevant information is ideal.

Recommended API: OpenWeatherMap API (Current Weather)
This is an excellent choice for your project.

Why it's good:

- Publicly Accessible: It has a very generous free tier (1,000,000 calls/month, 60 calls/minute for current weather data), which is more than enough for hourly updates.
- Relevant Data: Weather changes frequently, making it interesting for regular notifications. You can monitor conditions for your location, a favorite sailing spot, or anywhere relevant to your interests.
- Simple to Use: The current weather API endpoint is straightforward. You make a GET request, and it returns a JSON object with temperature, humidity, weather description, wind speed, etc.
- API Key: It requires a free API key, which is a good learning experience for securely handling credentials using environment variables, as discussed in the cloud-deployment-guide.

What you could monitor/notify about:

"Current temperature in [City]: [X]°C, [Weather Description]. Wind: [Y] m/s."
"Heads up! Rain expected in [City] today." (Requires parsing forecast data, slightly more complex but achievable).
"Wind speed at [Sailing Spot] is currently [X] knots, [Direction]."

Getting Started:

Sign up for a Free API Key: Visit https://openweathermap.org/api and sign up for a free account. Your API key (APPID) will be available on your account page.

Current Weather Endpoint: The basic current weather API call looks like this: https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key} You can specify units (metric for Celsius, imperial for Fahrenheit) with &units=metric or &units=imperial. 

Example for London: 
https://api.openweathermap.org/data/2.5/weather?q=London&units=metric&appid={API key}

Documentation: Refer to their "Current weather data" documentation: https://openweathermap.org/current

=========================
Q: Using SMTP with gmail:
=========================
Yes, you absolutely can use a Gmail account for the SMTP functionality in your Python script\!
However, Gmail has strong security measures, and you typically **cannot use your regular Gmail account password directly** 
with `smtplib` unless you enable "Less secure app access" 
(which Google has largely phased out or strongly discourages) or, more securely, use an **App Password**.

The recommended and more secure way is to generate an **App Password** for your Gmail account. 
This is a unique, 16-digit password that you generate specifically for an application (like your Python script) 
to access your Gmail. It's much safer than enabling "Less secure app access" or exposing your main password.

Here's how to set up an App Password for your Gmail account:

### Step-by-Step: Generating a Gmail App Password

1.  **Enable 2-Step Verification (if you haven't already):**

      * App Passwords only work if you have 2-Step Verification enabled on your Google Account.
      * Go to your Google Account: [myaccount.google.com](https://myaccount.google.com/)
      * Navigate to **Security**.
      * Under "How you sign in to Google," find "2-Step Verification" and turn it on if it's off. Follow the prompts to set it up (requires a phone number for verification codes).

2.  **Generate the App Password:**

      * Once 2-Step Verification is enabled, stay in the **Security** section of your Google Account ([myaccount.google.com/security](https://myaccount.google.com/security)).
      * Under "How you sign in to Google," click on **App Passwords**.
          * *(You might need to sign in again for security purposes.)*
      * On the "App passwords" page:
          * From the "Select app" dropdown, choose **"Mail"**.
          * From the "Select device" dropdown, choose **"Other (Custom name)"**.
          * Enter a name that helps you remember what this password is for (e.g., "DigitalOcean Weather Notifier" or "Python SMTP Script"). Click **"Generate"**.
      * A 16-character code will be displayed in a yellow bar. **This is your App Password.**
      * **Copy this password immediately.** You will not see it again. If you lose it, you'll need to generate a new one.

### Using the App Password in Your Python Script

Now, in your `api-monitor/__main__.py` file (and in your `project.yml` for DigitalOcean Functions), 
you will use this 16-character App Password as the `SENDER_EMAIL_PASSWORD` instead of your regular Gmail password.

**Your `project.yml` (example):**

```yaml
# project.yml
# ... (other parts of your project.yml)
        environment:
          TARGET_API_URL: "https://api.openweathermap.org/data/2.5/onecall?lat=34.05&lon=-118.25&exclude=minutely,daily&appid={your_open_weather_api_key}" # Replace with actual API & your key
          SENDER_EMAIL: "your_actual_gmail_address@gmail.com"
          SENDER_EMAIL_PASSWORD: "YOUR_16_CHARACTER_APP_PASSWORD_HERE" # <<< USE THIS GENERATED PASSWORD
          RECEIVER_EMAIL: "your_recipient_email@example.com"
          SMTP_SERVER: "smtp.gmail.com"
          SMTP_PORT: "587"
# ... (rest of project.yml)
```

**Your Python script (`__main__.py`) already uses `os.getenv("SENDER_EMAIL_PASSWORD")`, 
so no code change is needed there once the environment variable is updated.**

### Important Considerations for Using Gmail for Automated Emails:

  * **Rate Limits:** Personal Gmail accounts are not designed for bulk emailing. 
      Google imposes limits (e.g., around 100-150 emails per day). For your hourly notification, 
      this should be fine, but be aware if your needs scale up.
  * **Deliverability:** Emails sent from personal Gmail accounts can sometimes be flagged as spam 
      by recipients' mail servers, especially if the content is generic or repetitive.
  * **Security for Credentials:** While App Passwords are more secure than your main password, 
      storing any sensitive credentials (even App Passwords) directly in `project.yml` 
      (even if encrypted at rest) should be done with care. For a small personal project, 
      it's generally acceptable. For production-grade applications, 
      consider DigitalOcean's managed secrets or a dedicated secrets management service.
  * **Error Handling:** Your current script has good error handling for SMTP exceptions. 
      Make sure you monitor your DigitalOcean Function logs if you suspect email delivery issues.

For anything beyond simple personal notifications, 
I strongly recommend dedicated transactional email services like 
**SendGrid**, **Mailgun**, or **Amazon SES**. They offer free tiers suitable for many projects, 
handle deliverability, provide better analytics, and have more robust APIs for integration.