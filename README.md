#  Translation bot (with OCR)
## Introduction
A simple Telegram bot that translates text you send him in message or photo. This bot uses Google Translate API for translation and Tesseract API for text recognition (OCR). The bot himself defines language of original text and translates to Russian but you can change translation language to any.
## Built with
The bot is based on the following APIs:
1. [Google Translate API](https://translate.google.com/)
2. [Tesseract API](https://github.com/tesseract-ocr/tesseract)
## Examples
In the Examples directory you can find a few screenshots of this bot in action
# Code
Modules that must be installed for this this bot:
1. [googletrans](https://pypi.org/project/googletrans/)
2. [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
3. [pytesseract](https://pypi.org/project/pytesseract/)
4. [opencv-python](https://pypi.org/project/opencv-python/)
5. [scikit-image](https://pypi.org/project/scikit-image/)
Import necessary libraries:
```python
import googletrans
import telebot
import pytesseract
import cv2
import numpy as np
from googletrans import Translator
```
Create Telegram bot and get a token using Telegram bot named "@botfarther". Then use this token
```python
bot = telebot.TeleBot('Telegram Bot API Token')
```
Initialize translator and class with languages
```python
translator = Translator()
languages = googletrans.LANGUAGES
```
Bot will use Tesseract installed on PC. Here we show the direction of it
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
This method will handle with **/Start** command and greet user
```python
@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>. Что ты хочешь перевести?'
    bot.send_message(message.chat.id, mess, parse_mode='html')
```
Method to handle with text messages users wants to translate
```python
@bot.message_handler(content_types=['text'])
def get_user_text(message):
    text = translator.translate(message.text, dest='ru').text
    language_code = translator.translate(message.text, dest='ru').src
    language = translator.translate(languages[language_code], dest='ru').text
    bot.send_message(message.chat.id, f'{text}\n<i>Язык оригинала - {language}</i>', parse_mode='html')
```
This method will handle with images which contain text user wants to translate
```python
@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    photo_id = message.photo[-1].file_id
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    image = cv2.imread('image.jpg')

    # A few steps of image preprocessing to increase OCR accuracy:
        # Discolor it
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
```
This command launches bot
```python
bot.polling(non_stop=True)
```





