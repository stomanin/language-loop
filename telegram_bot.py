import os
import time
import logging
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

from db import create_database, save_user_data, load_user_data

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# Telegram Bot token from BotFather
TOKEN = os.getenv('LANGUAGE_LOOP_TELEGRAM_BOT_TOKEN')


# OPENAI token and configs
MODEL = "gpt-4o"
TEMPERATURE = 0 #degree of randomness of the model's output

def get_completion_from_messages(messages, model=MODEL, temperature=TEMPERATURE):
    time.sleep(1)  # Pause for 1 second between requests
    response = client.chat.completions.create(model=model,messages=messages,temperature=temperature)
    return response.choices[0].message.content

def save_context_get_response(user_id, text):
    messages = load_user_data(user_id)
    print("1")
    messages.append({'role': 'user', 'content': f"{text}"})
    print("2")
    response = get_completion_from_messages(messages)
    print("3")
    print(response)
    messages.append({'role': 'assistant', 'content': f"{response}"})
    print("4")
    save_user_data(user_id, messages)
    print("5")
    print(user_id)
    print(messages)
    return response

#def save_context_get_response(text):
    #adds the user input to the context with user role
#    messages.append({'role':'user', 'content':f"{text}"})
    #gets the response
#    response = get_completion_from_messages(messages) 
#    print(response)
    #saves the context for history
#    messages.append({'role':'assistant', 'content':f"{response}"})
#    print(messages)
#    return response

# system instructions
from prompt import system_instructions
#messages =  []
#messages.append({'role':'system', 'content':f"{system_instructions}"})
system_message = {'role': 'system', 'content': f"{system_instructions}"}

# setting up logging module, to know when (and why) things don't work as expected
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# start function called every time the Bot receives a Telegram message that contains the /start command
#async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    if update.message.from_user.is_bot == False:
#        await context.bot.send_message(
#            chat_id=update.effective_chat.id,
#            text="Hello, I'm your LanguageLoop Bot!"
#        )
#        responses = get_completion_from_messages(messages)
#        await context.bot.send_message(chat_id=update.effective_chat.id, text=responses)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not update.message.from_user.is_bot:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm your LanguageLoop Bot!")
        messages = load_user_data(user_id)
        if not messages:
            messages.append(system_message)
            save_user_data(user_id, messages)
        response = get_completion_from_messages(messages)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def audio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("audio handler")
    user_id = update.message.from_user.id
    if update.message.from_user.is_bot == False:
        if update.message.voice:
            file_id = update.message.voice.file_id
            # download file
            file = await context.bot.get_file(file_id)
            await file.download_to_drive(f"downloaded_audio_{file_id}.ogg")  # You can specify the desired file name
            
            # use whisper to transcribe audio messages
            from openai import OpenAI
            client = OpenAI()

            with open(f"downloaded_audio_{file_id}.ogg", 'rb') as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file,
                    response_format="text"
                )
            # delete downloaded audio file after the transcription is done
            os.remove(f"downloaded_audio_{file_id}.ogg")
            
            response = save_context_get_response(user_id, transcription)
            #returns the submitted audio in text for feedback
            transcribed_message = "You said:"+transcription
            print(transcribed_message)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=transcribed_message)

            # text to speech
            synthesis_result = client.audio.speech.create(input=response, model="tts-1", voice='fable')
            synthesis_result.stream_to_file("speech.ogg")

            # Send the audio as a voice message
            with open("speech.ogg", "rb") as audio_file:
                await context.bot.send_voice(chat_id=update.effective_chat.id, voice=audio_file)
            
            os.remove("speech.ogg")  # Clean up by removing the file

            #returns the response also in writing
            await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# triggers the openai bot 
#async def chatgptbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    if update.message.from_user.is_bot == False:
#        response = save_context_get_response(update.message.text)
        #returns the response
#        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def chatgptbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not update.message.from_user.is_bot:
        response = save_context_get_response(user_id, update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == '__main__':
    create_database()
    application = ApplicationBuilder().token(TOKEN).build()
    # /start command handler
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    #prompt handler
    prompt_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chatgptbot)    
    application.add_handler(prompt_handler)

    #audio handler
    audio_handler_instance = MessageHandler(filters.VOICE, audio_handler)
    application.add_handler(audio_handler_instance)

    application.run_polling()