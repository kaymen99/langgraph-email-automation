import os
import re
from datetime import datetime, timedelta
from agentmail import AgentMail
from bs4 import BeautifulSoup


class AgentMailToolsClass:
    """
    Alternative email provider using AgentMail (https://agentmail.to).

    AgentMail provides a simpler setup compared to Gmail API:
    - No OAuth flow required — just an API key
    - Programmatic inbox creation (each agent gets its own email)
    - AI-native features like extracted_text and auto-labeling

    Set the following environment variables:
        AGENTMAIL_API_KEY: Your AgentMail API key
        AGENTMAIL_INBOX_ID: The inbox ID to monitor and send from
    """

    def __init__(self):
        api_key = os.environ.get("AGENTMAIL_API_KEY")
        if not api_key:
            raise ValueError(
                "AGENTMAIL_API_KEY environment variable is required. "
                "Get your API key at https://agentmail.to"
            )
        self.client = AgentMail(api_key=api_key)
        self.inbox_id = os.environ.get("AGENTMAIL_INBOX_ID")
        if not self.inbox_id:
            raise ValueError(
                "AGENTMAIL_INBOX_ID environment variable is required. "
                "Create an inbox via the AgentMail dashboard or SDK."
            )

    def fetch_unanswered_emails(self, max_results=50):
        """
        Fetches recent unanswered emails from the AgentMail inbox.

        @param max_results: Maximum number of recent emails to fetch
        @return: List of dictionaries, each representing an email
        """
        try:
            messages = self.client.inboxes.messages.list(
                inbox_id=self.inbox_id
            )

            unanswered_emails = []
            my_email = os.environ.get("MY_EMAIL", "")
            cutoff = datetime.now() - timedelta(hours=8)

            for msg in messages:
                # Skip emails sent by us
                sender = getattr(msg, "from_", "") or ""
                if my_email and my_email in sender:
                    continue

                # Parse email info into the expected format
                email_info = self._format_email(msg)
                if email_info:
                    unanswered_emails.append(email_info)

                if len(unanswered_emails) >= max_results:
                    break

            return unanswered_emails

        except Exception as e:
            print(f"An error occurred fetching emails: {e}")
            return []

    def create_draft_reply(self, initial_email, reply_text):
        """
        Creates a draft reply. AgentMail doesn't have a native draft concept,
        so this sends the reply directly. Override with send_reply behavior.
        """
        print(
            "Note: AgentMail does not support drafts natively. "
            "Sending reply directly instead."
        )
        return self.send_reply(initial_email, reply_text)

    def send_reply(self, initial_email, reply_text):
        """
        Sends a reply to the given email.
        """
        try:
            subject = initial_email.subject
            if not subject.startswith("Re: "):
                subject = f"Re: {subject}"

            # Convert reply text to HTML
            html_text = reply_text.replace("\n", "<br>").replace("\\n", "<br>")
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body>{html_text}</body>
            </html>
            """

            result = self.client.inboxes.messages.send(
                inbox_id=self.inbox_id,
                to=initial_email.sender,
                subject=subject,
                text=reply_text,
                html=html_body,
            )
            return result

        except Exception as error:
            print(f"An error occurred while sending reply: {error}")
            return None

    def _format_email(self, msg):
        """
        Converts an AgentMail message object into the dictionary format
        expected by the rest of the workflow.
        """
        try:
            message_id = getattr(msg, "message_id", "") or ""
            sender = getattr(msg, "from_", "") or ""
            subject = getattr(msg, "subject", "No Subject") or "No Subject"

            # Prefer extracted_text (AI-processed), fall back to text, then html
            body = getattr(msg, "extracted_text", "") or ""
            if not body:
                body = getattr(msg, "text", "") or ""
            if not body:
                html = getattr(msg, "html", "") or ""
                if html:
                    body = self._extract_text_from_html(html)

            body = self._clean_body_text(body)

            return {
                "id": message_id,
                "threadId": message_id,  # Use message_id as thread identifier
                "messageId": message_id,
                "references": "",
                "sender": sender,
                "subject": subject,
                "body": body,
            }

        except Exception as e:
            print(f"Error formatting email: {e}")
            return None

    def _extract_text_from_html(self, html_content):
        """Extract text from HTML content."""
        soup = BeautifulSoup(html_content, "html.parser")
        for tag in soup(["script", "style", "head", "meta", "title"]):
            tag.decompose()
        return soup.get_text(separator="\n", strip=True)

    def _clean_body_text(self, text):
        """Clean up email body text."""
        return re.sub(
            r"\s+", " ", text.replace("\r", "").replace("\n", "")
        ).strip()
