# Для начала работы с нашей библиотекой необходимо установить её в терминале через pip3 install vkbottle.
# Затем импортируем её в наш главный файл, как показано ниже.
# Также стоит произвести импорт файла settings.py, в который ранее мы внесли ключ API и ID нашего бота
# (пример файла так же лежит в проекте).

import settings
from vkbottle.bot import Bot, Message
from random import randint
import simplemysql

# Подключение токена, прописанного в settings.
bot = Bot(token=settings.token)


# Затем для восприятия ботом каких-либо команд необходимо прописать их с последующим выполнением функции.


async def getUser(user_id):  # Позволяет получить информацию о пользователе (id, имя, фамилию и т.д.)
    try:
        return (await bot.api.users.get(user_ids=user_id))[0]
    except:
        return None

async def getid(pattern):
    pattern = str(pattern)
    if pattern.isdigit():
        return pattern
    elif "vk.com/" in pattern:
        uid = (await bot.api.users.get(user_ids=pattern.split("/")[-1]))[0]
        return uid.id
    elif "[id" in pattern:
        uid = pattern.split("|")[0]
        uid = (await bot.api.users.get(user_ids=uid.replace("[id", "")))[0]
        return uid


# async def getChat(chat_id):
#     try:
#         result = (await bot.api.messages.get_conversations_by_id(peer_ids=int(chat_id) + 2e9,
#                                                                  group_id=settings.GROUP_ID)).items
#         if result != []:
#             return result[0]
#         else:
#             return False
#     except:
#         return None


# async def getGroup():
#     try:
#         result = (await bot.api.groups.join(group_id=int(settings.ILLUSTRATE_ID)))
#         return result
#     except:
#         return False


name = ['Бобёр', 'Сова', 'Заяц']
subs = []  # Создаём пустой список подписчиков на рассылку админа
admin = 266911299  # Добавление id администратора




# В данном примере бот видит лишь ключевую фразу "Скажи привет",
# воспринимая её командой для выполнения ниженаписанной функции.
@bot.on.message(text=['Привет'])
# Сама функция, выполняемая при получении ботом текста "Скажи привет",
# в качестве события бот принимает сообщения.
async def SayHi(event: Message):
    member = await getUser(event.from_id)
    await event.answer(f"Привет, [id{member.id}|{member.first_name} {member.last_name}]")


@bot.on.message(text=['/reg'])
async def Register(event: Message):
    user = await getUser(event.from_id)
    subs.append(int(user.id))
    member = await getUser(event.from_id)
    await event.answer(f"Здравствуйте, {member.first_name}, подписка на новости активна)))")


@bot.on.message(text=['Кто я'])
async def Who(event: Message):
    index = randint(0, 2)
    member = await getUser(event.from_id)
    await event.answer(f"{member.first_name}, сегодня вы {name[index]}")


@bot.on.message(text=['<text>'])
async def Steal(event: Message, text = None):
    user = await getUser(event.from_id)
    with open('new.txt', 'w+', encoding='utf-8') as file:
        file.write(f'Пользователь {user.first_name} {user.last_name}\n\n {text}\n\n')


# В attachments помещается быстрая ссылка на фото/видео/аудио/пост
# https://vk.com/kartinochkistekstom?z=photo-157889932_457565872%2Falbum-157889932_00%2Frev
# Необходимо из ссылок извлекать лишь текст после '='


@bot.on.message(text=['/send <text>'])
async def Sending(event: Message, text=None):
    member = await getUser(event.from_id)
    if member.id != admin:
        await event.answer(f"Вы не админ!")
    else:
        for i in subs:  # Attachment Можно применять и в bot.api.messages.send
            await bot.api.messages.send(peer_id=i,
                                        message=f"Пользователь {member.first_name} {member.last_name} написал следующее сообщение: \n {text}",
                                        attachment='photo-157889932_457565872%2Falbum-157889932_00%2Frev', random_id=0)


@bot.on.message(text=[
    'Сложи <a> <b>'])  # Тэги a и b указаны через пробел, они выполняют роль контейнеров, которые передадут значения в сам код функции.
async def union(event: Message, a=None, b=None):
    try:  # Бот получает сообщение пользователя ТОЛЬКО В ТЕКСТОВОМ ФОРМАТЕ, поэтому его необходимо преобразовать в число.
        a = int(a)
        b = int(b)

    except ValueError:  # В данном случае представлена обработка исключений, о ней мы поговорим на следующем занятии.
        await event.answer(f"Вы ввели некорректно команду.\n Пример команды: 'Сложить 1 3'")
    # Метод try except просто предотвратит ошибку, но не остановит код,
    # поэтому нужно сделать повторную проверку правильности введённх значений.
    if type(a) == int and type(b) == int:
        await event.answer(f"Сумма равна {a + b}")


@bot.on.chat_message(text=['/statics <domain>'])
async def Stat(event: Message, domain = None):
    member = await getid(domain)
    await event.answer(f'Пользователь [id{member.id}|{member.first_name} {member.last_name}]')

# @bot.on.chat_message(text=['/ctstat <domain>'])
# async def ChatStat(event: Message, domain = None):
#     inf = getChat(domain)
#     await event.answer(f"{inf}")


@bot.on.message(text=['/ctchat', '/ctchat <name> <team>', '/ctchat <name>'])
async def CreateChat(event: Message, name=None, team=None):
    if name:
        await event.answer(f"Группа успешно создана")
        chat = await bot.api.messages.create_chat(group_id=settings.GROUP_ID, title=name)
        id_chat = int(chat) + 2e9
        invite_chat = await bot.api.messages.get_invite_link(peer_id=id_chat, reset=0, group_id=settings.GROUP_ID)
        await event.answer(f"Чат успешно создан: {invite_chat.link}")
        # chat_inf = await bot.api.messages.get_chat(chat_id=id_chat)
        # await event.answer(chat_inf)
    else:
        await event.answer(f"Не указано название беседы.")


bot.run_forever()  # Необходимо для того, чтобы бот всегда ожидал какой-либо прописанной команды.

# @bot.on.message(text=['Хочу фотку'])
# async def GetPhoto(event: Message):
#     id = await bot.api.groups.join(group_id='125688382')
#     await event.answer(f'{id}')
