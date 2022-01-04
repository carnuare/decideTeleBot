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

@bot.message_handler(commands=["votaciones"]) #devuelve listado de todas las votaciones
def resolver(message):
    try:
        url= 'https://decide-full-alcazaba-develop.herokuapp.com/visualizer/all'
        response = requests.get(url)
        print(response.json())
        reply = 'Votaciones: \n'
        for clave in response.json():
          reply += response.json()[clave]['name'] + ' - ' + clave
        bot.reply_to(message, reply)
    except Exception:
        bot.reply_to(message, 'Error llamando a la API')

@bot.message_handler(func=lambda msg: msg.text is not None and '/votacion' in msg.text) #devuelve detalle de votacion por su id
def detalle(message):
   try:
      url= 'https://decide-full-alcazaba-develop.herokuapp.com/visualizer/all'
      response = requests.get(url)
      texts = message.text.split(' ')
      vid = texts[1]
      reply = 'Nombre de la votacion: ' + response.json()[vid]['name'] + '\n'
      if(response.json()[vid]['description'] is not None):
        reply += 'Descripcion: ' + response.json()[vid]['description'] + '\n'
      if(response.json()[vid]['fecha_inicio'] is not None):
        reply += 'Fecha de inicio: ' + response.json()[vid]['fecha_inicio'] + '\n'
      if(response.json()[vid]['fecha_fin'] is not None):
        reply += 'Fecha de finalizacion: ' + response.json()[vid]['fecha_fin'] + '\n'
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
   bot.set_webhook(url='https://telebot-decide-alcazaba.herokuapp.com/' + TOKEN)
   return "!", 200
if __name__ == "__main__":
   server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))




bot.polling()