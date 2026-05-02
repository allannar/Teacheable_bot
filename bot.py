import telebot
from cfg import TOKEN
from model import classification
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот от allannar. Сейчас он в стадии разработки, но это временно... A little bit of waiting ")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['help'])
def send_help(massage):
    bot.reply_to(massage, 'Тут скоро появиться список команд бота, A little bit of waiting')

@bot.message_handler(content_types=['photo'])
def save_photo(message):
    # Берем ID самого большого фото и получаем путь к нему
    path = bot.get_file(message.photo[-1].file_id).file_path
    # Скачиваем файл
    downloaded_file = bot.download_file(file_path)
    
    # Сохраняем с оригинальным именем (из конца пути)
    with open(file_path.split('/')[-1], 'wb') as new_file:
        new_file.write(downloaded_file)
    
    bot.reply_to(message, "Картинка у меня!")

    
    file_path = list(path.keys())[0]
    result = classification(path,"keras_model.h5","labels.txt")
    bot.reply_to(message,"На изображении:", result[0].replace('\n',""), "с вероятностью: ", int(result[1]*100),"%")


@bot.message_handler(content_types=['text'])
def no_photo(message):
    bot.reply_to(message, "Это текст, а мне нужно фото.")

bot.polling()