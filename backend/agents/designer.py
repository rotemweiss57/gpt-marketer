class DesignerAgent:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def design(self, email_content, email_title: str):
        # Design the email
        email_html = f"<html><body><h1>{email_title}</h1><p>{email_content}</p></body></html>"
        return email_html

    def run(self, email: dict):
        email["html"] = self.design(email['email_content'], email['title'])
        return email