import os
import imaplib
import email
from email.header import decode_header

# Email account credentials
IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
REPO = os.getenv("REPO")  # Not used in the current script

def fetch_emails_with_subject(subject_filter):
    try:
        # Connect to the IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        
        # Select the mailbox (e.g., INBOX)
        mail.select("inbox")
        
        # Search emails with the given subject
        status, messages = mail.search(None, f'SUBJECT "{subject_filter}"')
        
        if status != "OK":
            print("Error searching emails!")
            return []
        
        email_ids = messages[0].split()
        
        if not email_ids:
            print(f"No emails found with subject '{subject_filter}'.")
            return []
        
        # List to hold email data
        email_list = []
        
        # Loop through the email IDs
        for email_id in email_ids:
            # Fetch the email by ID
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
            if status != "OK":
                print(f"Error fetching email ID {email_id.decode()}.")
                continue  # Skip to the next email
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Parse the email content
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    # Extract the sender
                    sender = msg.get("From")
                    
                    # Extract the email body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            
                            # Skip attachments
                            if "attachment" in content_disposition:
                                continue
                            
                            if content_type == "text/plain":
                                charset = part.get_content_charset() or "utf-8"
                                body = part.get_payload(decode=True).decode(charset, errors="replace")
                                break  # Stop after finding the first text/plain part
                    else:
                        content_type = msg.get_content_type()
                        if content_type == "text/plain":
                            charset = msg.get_content_charset() or "utf-8"
                            body = msg.get_payload(decode=True).decode(charset, errors="replace")
                    
                    # Append email details to the list
                    email_list.append({"subject": subject, "sender": sender, "body": body})
        
        # Logout from the mail server
        mail.logout()
        return email_list

    except imaplib.IMAP4.error as imap_err:
        print(f"IMAP error occurred: {imap_err}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# Main logic
if __name__ == "__main__":
    subject_filter = "Refresh failed:"  # Filter for subject
    emails = fetch_emails_with_subject(subject_filter)
    
    if emails:
        print(f"Found {len(emails)} email(s) with subject '{subject_filter}':")
        for i, email_data in enumerate(emails, start=1):
            print(f"\nEmail {i}:")
            print(f"Subject: {email_data['subject']}")
            print(f"Sender: {email_data['sender']}")
            print(f"Body:\n{email_data['body']}")
    else:
        print(f"No emails found with subject '{subject_filter}'.")
