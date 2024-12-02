import imaplib
import email
from email.header import decode_header

# Email account credentials
IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
REPO = os.getenv("REPO")

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
            print("No messages found!")
            return []
        
        # List to hold email data
        email_list = []
        
        # Loop through the email IDs
        for email_id in messages[0].split():
            # Fetch the email by ID
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
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
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    # Append email details to the list
                    email_list.append({"subject": subject, "sender": sender, "body": body})
        
        # Logout from the mail server
        mail.logout()
        return email_list

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Main logic
if __name__ == "__main__":
    subject_filter = "Refresh failed:"  # Filter for subject
    emails = fetch_emails_with_subject(subject_filter)
    
    if emails:
        print(f"Found {len(emails)} emails with subject '{subject_filter}':")
        for i, email_data in enumerate(emails, start=1):
            print(f"\nEmail {i}:")
            print(f"Subject: {email_data['subject']}")
            print(f"Sender: {email_data['sender']}")
            print(f"Body:\n{email_data['body']}")
    else:
        print(f"No emails found with subject '{subject_filter}'.")
