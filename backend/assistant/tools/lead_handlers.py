
import json
import asyncio
from datetime import datetime
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


class LeadHandlers:
    """
    Utility functions for handling chat history, saving lead data, and invoking chat chains.
    """
    buffer_saver_file_path = 'assistant/buffer/buffer.json'
    exported_lead_datas = 'assistant/buffer/lead_datas.json'
    exported_lead_html_path = 'assistant/buffer'

    async def send_leads_info(self) -> None:
        """
        Sends the data for lead generation to the server email.
        """
        try:
            self.lead = json.loads(self.lead)

            lead = {
                "User ID": self.user_id,
                "Contact Reason": self.subject_name,
                "Lead generated at": str(datetime.now())
            }

            lead.update(self.lead)

            await asyncio.create_task(self.save_locally_lead_info(lead))

            lead_to_email_body = await asyncio.create_task(self.format_json_for_email(lead))
            chat_formated = await asyncio.create_task(self.format_chat_history_for_email(self.chat_history))

            await asyncio.create_task(self.send_lead_by_email(lead_to_email_body, chat_formated))
            await asyncio.create_task(self.save_locally_lead_html(lead_to_email_body, chat_formated))

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print(f"send_leads_info(): Error {e}")

    async def send_lead_by_email(self, lead_to_email_body: str, chat_formated = None) -> None:
        """
        Sends the data for lead generation to the server email.
        """
        try:

            print("send_leads_info() - Trying to send the email")
            # Building the e-mail
            sender_email = 'assistant@kobu.agency'
            receiver_email = sender_email
            subject = f'New Lead Generated - {self.lead.get("brand")}, sent by {self.lead.get("person_name")}'

            print("Email subject: ", subject)
            print("Body recived:\n", lead_to_email_body)
            body = lead_to_email_body + chat_formated

            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

            # SMTP server config
            smtp_server = 'mail.kobu.agency'
            port = 465  # SSL/TLS Port
            password = '5Ze!m0aJkG#cElC#'

            # Starting the connection with the SMTP server
            with smtplib.SMTP_SSL(smtp_server, port) as server:
                server.login(sender_email, password)  # Login at SMTP server
                server.send_message(message)  # Sending the e-mail

            print("send_leads_info(): Email sent successfully!")

        except smtplib.SMTPException as e:
            logging.error(f"SMTP Exception: {e}")
            print(f"send_leads_info(): Error {e}")

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print(f"send_leads_info(): Error {e}")

    async def save_locally_lead_info(self, lead: json) -> None: 
        """
        Write the data for lead generation to a JSON file.
        """
        try:
            new_data = lead

            # Read the current content of the file if it exists
            try:
                with open(self.exported_lead_datas, 'r', encoding='utf-8') as json_file:
                    existing_data = json.load(json_file)
            except FileNotFoundError:
                existing_data = []

            # Add the new data to the end of the existing list
            existing_data.append(new_data)

            # Write the updated data to the JSON file
            with open(self.exported_lead_datas, 'w', encoding='utf-8') as json_file:
                json.dump(existing_data, json_file, ensure_ascii=False, indent=2)

            print(f'save_locally_lead_info() Lead datas has been exported to {self.exported_lead_datas}')

        except Exception as e:
            print(f"save_locally_lead_info Error {e}")

    async def save_locally_lead_html(self, lead_to_email_body: str, chat_formated = None) -> None:
        """
        Creates an HTML file with the given body content and user ID as the filename.

        Parameters:
            lead_to_email_body (str): The body content of the HTML page.
        """

        html_body_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>User Profile</title>
        </head>
        <body>
            <h1>User: {self.user_id}</h1>
            <p> {lead_to_email_body} </p>
            <br>
            <h1>Conversation </h1>
            <p> {chat_formated} </p>

        </body>
        </html>
        """

        try:
            filename = os.path.join(self.exported_lead_html_path, f"{self.user_id}.html")
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_body_content)
            print(f"HTML file '{filename}' created successfully.")
        except Exception as e:
            print(f"Error creating HTML file: {e}")

    async def format_chat_history_for_email(self, chat_history: list) -> str:
        """
        Formats a chat history list into a string for email.

        Parameters:
            chat_history (list): A list containing chat history entries.

        Returns:
            str: A formatted string containing the chat history for display in an email.
        """
        try:
            formatted_history = ""
            for entry in chat_history:
                formatted_history += f"{entry.content}\n"
            
            return formatted_history
        except Exception as e:
            print(f"Error formatting chat history for email: {e}")
            return ""

    async def format_json_for_email(self, json_data: json) -> str:
        """
        Formats a JSON object into a formatted string for email.

        Parameters:
            json_data (dict or str): A JSON object or a JSON string.

        Returns:
            str: A formatted string containing the JSON data for display in an email.

        Raises:
            TypeError: If the provided data is not a valid JSON object or JSON string.
        """
        try:
            # Check if the provided data is a JSON string and convert it to a dictionary
            if isinstance(json_data, str):
                json_data = json.loads(json_data)
            
            # Format the data into visually appealing format for email
            email_body = ""
            for key, value in json_data.items():
                email_body += f"{key}: {value}\n"

            return email_body
        
        except Exception as e:
            # Return the original JSON in case of error
            print(f"format_json_for_email() - Error formatting JSON for email: {e}")
            return json.dumps(json_data, indent=4)
