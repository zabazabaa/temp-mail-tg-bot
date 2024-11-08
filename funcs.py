import aiohttp
from random import choice
import string

API = 'https://www.1secmail.com/api/v1/'
domains = [
  "1secmail.com",
  "1secmail.org",
  "1secmail.net"
]

def escape_markdown_v2(text: str) -> str:
    special_characters = r"_*[]()~`>#+-=|{}.!"
    for char in special_characters:
        text = text.replace(char, f"\\{char}")
    return text

def generate_email():
    syms = string.ascii_lowercase + string.digits
    username = ''.join(choice(syms) for i in range(10))
    email = f'{username}@{choice(domains)}'
    return email

async def get_messages_ids_list(email: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{API}?action=getMessages&login={email.split("@")[0]}&domain={email.split("@")[1]}') as response:
            if response.status == 200:
                messages = await response.json()
                if not messages:
                    return None
                return [message['id'] for message in messages]
            return None

async def get_messages(email: str):
    messages = []
    message_ids = await get_messages_ids_list(email)
    if not message_ids:
        return None
    
    async with aiohttp.ClientSession() as session:
        for message_id in message_ids:
            async with session.get(f'{API}?action=readMessage&login={email.split("@")[0]}&domain={email.split("@")[1]}&id={message_id}') as response:
                if response.status == 200:
                    message = await response.json()
                    messages.append({
                        'date': escape_markdown_v2(message['date']),
                        'from': escape_markdown_v2(message['from']),
                        'subject': escape_markdown_v2(message['subject']),
                        'body': escape_markdown_v2(message['textBody'])
                    })
    return messages