#Install following modules: googletrans, pyTelegramBotAPI, pytesseract, opencv-python, scikit-image

import googletrans
import telebot
import pytesseract
import cv2
import numpy as np
from googletrans import Translator


#Creating bot
bot = telebot.TeleBot('Telegram Bot API Token')

#Translator and class with its languages
translator = Translator()
languages = googletrans.LANGUAGES

#Direction of Tesseract installed on PC
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#Method for greeting
@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>. Что ты хочешь перевести?'
    bot.send_message(message.chat.id, mess, parse_mode='html')

#Method to handle with text messages
@bot.message_handler(content_types=['text'])
def get_user_text(message):
    text = translator.translate(message.text, dest='ru').text
    language_code = translator.translate(message.text, dest='ru').src
    language = translator.translate(languages[language_code], dest='ru').text
    bot.send_message(message.chat.id, f'{text}\n<i>Язык оригинала - {language}</i>', parse_mode='html')

#Method to handle with sent images
@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    photo_id = message.photo[-1].file_id
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    image = cv2.imread('image.jpg')

    #A few step for image preprocessing to increase OCR accuracy:
        # Discolor image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Remove noise
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
        # Binarize image
    ret, image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY_INV)

    # Extract text from preprocessed image using Tesseract and translate it
    string = pytesseract.image_to_string(image)
    text = translator.translate(string, dest='ru').text
    language_code = translator.translate(string, dest='ru').src
    language = translator.translate(languages[language_code], dest='ru').text
    bot.send_message(message.chat.id, f'{text}\n<i>Язык оригинала - {language}</i>', parse_mode='html')

# Launch bot
bot.polling(non_stop=True)