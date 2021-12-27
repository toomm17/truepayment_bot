import os

from aiogram.types import Message

from data.config import ADMINS_ID
from loader import dp, db, bot

# async?
def write_csv(emails: list):
    with open('data/emails.csv', 'w') as file:
        file.write('\n'.join(emails))
        
        
@dp.message_handler(user_id=ADMINS_ID, text='Выгрузить почты в .csv')
async def send_csv(message: Message):
    emails = await db.get_all_emails()
    csv_emails = [email['email'] for email in emails if email['email'] != None]

    write_csv(csv_emails)
    
    with open('data/emails.csv', 'rb') as file:
        f = file.read()
    
    await bot.send_document(message.from_user.id, ('emails.csv', f))

    os.remove('data/emails.csv')

