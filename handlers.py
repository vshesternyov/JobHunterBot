import asyncio
import datetime
import io

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from database import refresh_db
from scraper import get_vacancy_list

enabled_search = False


def register_handlers(dp):
    @dp.message_handler(Command('start'))
    async def send_welcome(message: types.Message, state: FSMContext):
        await message.reply(
            '\tДоступные команды:\n\t/start_searching_for_vacancies\n\t/stop_looking_for_jobs\n\t/refresh_db'
        )

    @dp.message_handler(Command('start_searching_for_vacancies'))
    async def find_data_analytics_jobs(message: types.Message, state: FSMContext):
        global enabled_search
        enabled_search = True

        while enabled_search:
            await create_job_listing(message)
            await asyncio.sleep(60)

    @dp.message_handler(Command('stop_looking_for_jobs'))
    async def stop_data_analyst(message: types.Message, state: FSMContext):
        global enabled_search
        enabled_search = False
        await message.reply('Поиск приостоновлен')

    @dp.message_handler(Command('refresh_db'))
    async def flush(message: types.Message, state: FSMContext):
        refresh_db()
        await message.reply('Удаленны старые вакансии')


def get_output(sorted_vacancy_list):
    result = ''

    for vacancy in sorted_vacancy_list:
        result += str(vacancy) + '\n'

    return result


async def create_job_listing(message: types.Message):
    vacancy_list = get_vacancy_list()
    sorted_vacancy_list = sorted(
        vacancy_list,
        key=lambda x: ('Junior' not in x[0], x[0], 'Middle' in x[0], 'Senior' in x[0])
    )

    if len(str(sorted_vacancy_list)) > 4096:
        file_obj = io.BytesIO(get_output(sorted_vacancy_list).encode())

        await message.reply_document(file_obj, caption='Long Message.txt')

    elif len(vacancy_list) == 0:
        print('No new vacancies', datetime.datetime.now().time())

    else:
        await message.reply(get_output(sorted_vacancy_list))
