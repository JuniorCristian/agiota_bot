# import logging
# from db import get_database
import configparser
import telebot

config = configparser.ConfigParser()
config.read_file(open('config.ini'))

CHAVE_API = config['TELEGRAM']['token']

ID_GRUPO = config['TELEGRAM']['chat_id']

bot = telebot.TeleBot(CHAVE_API)


# dbname = get_database()


@bot.message_handler(commands=["resultado"])
def resultado(mensagem):
    bot.send_message(mensagem.chat.id, "Por favor digite apenas números entre 1 e 25")


def verificar(mensagem):
    return True


@bot.message_handler(func=verificar)
def responder(mensagem):
    print(mensagem)
    texto = """
    Teste
    """
    send_message(texto)


def send_message(texto):
    bot.send_message(ID_GRUPO, texto)


bot.polling()
