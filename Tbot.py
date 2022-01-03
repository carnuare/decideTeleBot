'''
bot.delete_webhook()
#https://api.telegram.org/bot5094239712:AAEWOtGe55YZ1GFjwNpmyrSF_kWPtO1Y2yk/setWebhook?url=
'''
import os
import telebot 
from telebot import types
import json
import time
import requests
from flask import Flask, request
TOKEN = '5094239712:AAEWOtGe55YZ1GFjwNpmyrSF_kWPtO1Y2yk'#os.getenv('5094239712:AAEWOtGe55YZ1GFjwNpmyrSF_kWPtO1Y2yk') #Ponemos nuestro Token generado con el @BotFather
bot = telebot.TeleBot(TOKEN)  #Creamos nuestra instancia "bot" a partir de ese TOKEN
server = Flask(__name__) 


@bot.message_handler(commands=['start'])
def comienzo(message):
   bot.reply_to(message, "¡Hola! Probando")

@bot.message_handler(commands=['help',''])
def send_welcome(message):
   bot.send_message(message.chat.id, """Usa \"/login <usuario> <contraseña>\" para iniciar sesión.
Usa \"/vote <id_de_la_votacion>\" para poder votar.""")

@bot.message_handler(func=lambda msg: msg.text is not None and '/login' in msg.text)
def login(message):
   #bot.send_message(message.chat.id, "")
   texts = message.text.split(' ')
   if(len(texts)==3):
      user = texts[1].strip() #strip para quitarle los espacios iniciales y finales
      password = texts[2].strip()
      id_votante_api = 1 #simula el id del votante logeado 
      id_votante = id_votante_api #se guarda en una variable para saber que está logeado
      print(id_votante)
      #bot.send_message(message.chat.id, "Id del votante"+str(id_votante)+"")
      #bot.send_message(message.chat.id,"¿Es usted\""+ user +"\"con contraseña \""+password+"\"?")
   else:
      bot.reply_to(message, 'Por favor, use correctamente el comando /login      (ver en /help)')
      print("Error en /login, al introducir el comando: "+str(message.text))

@bot.message_handler(func=lambda msg: msg.text is not None and '/logout' in msg.text)
def logout(message):
   try:
      if(message.text!='/logout'):
         raise Exception()
      else:
         if(id_votante==-1):
            bot.send_message(message.chat.id, "No ha iniciado sesion, introduzca el comando: \"/login <usuario> <contraseña>\" para iniciar sesion")
         else:
            id_votante==-1
            if(id_votante==-1):
               bot.send_message(message.chat.id, "Sesión cerrada!!")
            else:
               raise Exception()
            
   except Exception:
      bot.reply_to(message, 'Por favor, use correctamente el comando /logut      (ver /help)')
      print("Error en /logout, al introducir el comando: "+str(message.text))

@bot.message_handler(func=lambda msg: msg.text is not None and not '/' in msg.text)
def no_command_message(message):
   bot.send_message(message.chat.id, 'Por favor introduzca algun comando del listado siguiente:')
   send_welcome(message)

'''
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
'''

bot.polling()