import os
from dotenv import load_dotenv
import telebot

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
api_key = os.getenv('API_KEY')
api_host = "hotels4.p.rapidapi.com"
