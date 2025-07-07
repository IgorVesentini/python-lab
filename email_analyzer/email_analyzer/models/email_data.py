from dataclasses import dataclass

@dataclass
class EmailData:
    sender: str
    recipient: str
    subject: str
    date: str
    body: str