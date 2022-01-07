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
url = 'http://localhost:8081/'
tokenSesion = {}

@bot.message_handler(commands=['start'])
def comienzo(message):
    bot.reply_to(message, "¡Hola! Probando")

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Buenas tardes")

@bot.message_handler(commands=["votaciones"]) #devuelve listado de todas las votaciones
def resolver(message):
    try:
        url = 'http://localhost:8081/visualizer/all'
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
      url = 'http://localhost:8081/visualizer/all'
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

@bot.message_handler(func=lambda msg: msg.text is not None and '/login' in msg.text)
def login(message):
   #bot.send_message(message.chat.id, "")
   texts = message.text.split(' ')
   if(len(texts)==3):
      try:
         user = texts[1].strip() #strip para quitarle los espacios iniciales y finales
         password = texts[2].strip()
         url = 'http://localhost:8081/authentication/login-bot/'
         payload={"username":user,"password":password}
         files=[]
         headers = {}
         respuesta = requests.request("POST", url, headers=headers, data=payload, files=files)
         listaclaves = list(respuesta.json().keys())
         if 'non_field_errors' in listaclaves:
            bot.reply_to(message, 'No puede iniciar sesión con las credenciales proporcionadas. Por favor vuelva a intentarlo.')
         elif 'token' in listaclaves:
            diccionario = {respuesta.json()['token']: True}
            tokenSesion.update(diccionario)
            bot.reply_to(message,'Ha iniciado sesión correctamente. Su id para votar es:'+str(respuesta.json()['user_id'])+'. !Por favor, no la comparta con nadie¡')
         else:
            raise Exception()
      except Exception:
         bot.reply_to(message, 'Error llamando a la API')

   else:
      bot.reply_to(message, 'Por favor, use correctamente el comando /login      (ver en /help)')
      print("Error en /login, al introducir el comando: "+str(message.text))

@bot.message_handler(func=lambda msg: msg.text is not None and '/logout' in msg.text)
def logout(message):
   print('Logout del token: '+str(tokenSesion))
   try:
      if(message.text!='/logout'):
         raise Exception()
      else:
         if(tokenSesion['9a12ac4f0bd11ebe364b8bdc0c9e5319204aa982'] == False):
            bot.send_message(message.chat.id, "No ha iniciado sesion, introduzca el comando: \"/login <usuario> <contraseña>\" para iniciar sesion")
         else:
            tokenSesion==None
            if(tokenSesion==None):
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