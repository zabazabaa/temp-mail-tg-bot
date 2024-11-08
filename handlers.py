from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from funcs import generate_email, get_messages

router = Router()

home_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='New mail✉️')]
],
        resize_keyboard=True)
in_mail_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Check messages📥')],
    [KeyboardButton(text='Delete Mail🗑')]
],
        resize_keyboard=True)

@router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer('Welcome to Temp Mail bot',
                         reply_markup=home_kb)

@router.message(F.text == 'New mail✉️')
async def new_mail(message: Message, state: FSMContext):
    try:
        email = generate_email()
        await state.update_data(email=email)
        await message.answer('Email has been successful created',
                             reply_markup=in_mail_kb)
        await message.answer(f'Your email: `{email}`',
                             parse_mode=ParseMode.MARKDOWN_V2)
    except:
        await message.answer('Something has happened\nPlease try again')

@router.message(F.text == 'Check messages📥')
async def check_messages(message: Message, state: FSMContext):
    data = await state.get_data()
    email = data.get('email')
    income_messages = await get_messages(email)
    if not income_messages:
        await message.answer('No messages yet')
    else:
        for income_message in income_messages:
            await message.answer(f"""`{income_message['date']}`
from: `{income_message['from']}`
 
{income_message['subject']}

{income_message['body']}""",
parse_mode=ParseMode.MARKDOWN_V2)

@router.message(F.text == 'Delete Mail🗑')
async def delete_mail(message: Message):
    await message.answer('Email has been deleted',
                         reply_markup=home_kb)