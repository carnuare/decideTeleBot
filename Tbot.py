print("Iniciando bot")
import os
import telebot 
from telebot import types
import json
import time
import requests
from flask import Flask, request
TOKEN = os.getenv('TELEBOT_TOKEN') # Ponemos nuestro Token generado con el @BotFather
bot = telebot.TeleBot(TOKEN)  #Creamos nuestra instancia "bot" a partir de ese TOKEN
server = Flask(__name__) 
#ola caracola

@bot.message_handler(commands=['start'])
def comienzo(message):
    bot.reply_to(message, "¡Hola! Probando")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Buenas tardes")

@bot.message_handler(commands=["votaciones"])
def resolver(message):
    try:
        uid = message.from_user.id
        url= 'https://decide-full-alcazaba-develop.herokuapp.com/visualizer/all'
        response = requests.get(url)
        print(response.json())
        reply = 'Votaciones: \n'
        for clave in response.json():
          reply = reply + response.json()[clave]['name']
        bot.reply_to(message, reply)
    except Exception:
        bot.reply_to(message, 'Error llamando a la API')
 
# SERVER SIDE 
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
   bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
   return "!", 200
@server.route("/")
def webhook():
   bot.remove_webhook()
   bot.set_webhook(url='https://telebot-decide-alcazaba.herokuapp.com/' + ' 5094239712:AAEWOtGe55YZ1GFjwNpmyrSF_kWPtO1Y2yk')
   return "!", 200
if __name__ == "__main__":
   server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))




bot.polling()