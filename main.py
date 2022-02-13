# Для начала работы с нашей библиотекой необходимо установить её в терминале через pip3 install vkbottle.
# Затем импортируем её в наш главный файл, как показано ниже.
# Также стоит произвести импорт файла settings.py, в который ранее мы внесли ключ API и ID нашего бота
# (пример файла так же лежит в проекте).

import settings
from vkbottle.bot import Bot, Message
from random import randint

# Подключение токена, прописанного в settings.
bot = Bot(token=settings.token)


# Затем для восприятия ботом каких-либо команд необходимо прописать их с последующим выполнением функции.


async def getUser(user_id):
    try:
        return (await bot.api.users.get(user_ids=user_id))[0]
    except:
        return None

name = ['Бобёр', 'Сова', 'Заяц']
subs = []
admin = 266911299

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
    await event.answer(f"Здравствуйте, {member.first_name}, подписка на новости активна))){subs}")

@bot.on.message(text=['Кто я'])
async def Photo(event: Message):
    index = randint(0, 2)
    member = await getUser(event.from_id)
    await event.answer(f"{member.first_name}, сегодня вы {name[index]}")


@bot.on.message(text=['/send <text>'])
async def Sending(event: Message, text=None):
    member = await getUser(event.from_id)
    if member.id != admin:
        await event.answer(f"Вы не админ!")
    else:
        for i in subs:
            await bot.api.messages.send(peer_id=i,
                                        message=f"Пользователь {member.first_name} {member.last_name} написал следующее сообщение: \n {text}",
                                        random_id=0)


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


bot.run_forever()  # Необходимо для того, чтобы бот всегда ожидал какой-либо прописанной команды.
