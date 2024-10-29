# 6895479913:AAGVPgwKamKbOZ0NWwjhB7uKPdspvlYiz7I
import requests
import time
import logging
import os
from telegram import Bot, Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from sunoApi import custom_generate_audio,get_audio_information
from transcript import takeTranscript2
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Define your Telegram bot API token here
telegram_api_token = '6895479913:AAGVPgwKamKbOZ0NWwjhB7uKPdspvlYiz7I'
bot = Bot(token=telegram_api_token)

# # Custom function to generate audio
# def custom_generate_audio(data):
#     # Simulating the audio generation process
#     prompt = data["prompt"]
#     return [{"id": "audio1"}, {"id": "audio2"}]

# # Custom function to get audio information
# def get_audio_information(ids):
#     # Simulate retrieving audio streaming URLs
#     return [{"status": "streaming", "id": "audio1", "audio_url": "http://example.com/audio1.mp3"},
#             {"status": "streaming", "id": "audio2", "audio_url": "http://example.com/audio2.mp3"}]

# Function to download audio file from the URL
def download_audio_file(audio_url):
    response = requests.get(audio_url)
    filename = audio_url.split("/")[-1]+".mp3"
    with open(filename, 'wb') as audio_file:
        audio_file.write(response.content)
    return filename

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Send me a prompt, and I'll generate an audio file for you."
    )

# Echo handler for processing user input and generating audio
async def generate_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    prompt = takeTranscript2(update.message.text.split("v=")[1])
    print(prompt)
    await update.message.reply_text(prompt)
    # Call the custom audio generation function
    data = custom_generate_audio({
        "prompt": prompt,
        "make_instrumental": False,
        "wait_audio": False
    })

    ids = f"{data[0]['id']},{data[1]['id']}"
    
    # Check if the audio is ready
    for _ in range(60):
        audio_info = get_audio_information(ids)
        if audio_info[0]["status"] == 'streaming':
            audio_url = audio_info[0]['audio_url']
            
            # Download the audio file
            filename = download_audio_file(audio_url)

            # Send the audio file to the user
            with open(filename, 'rb') as audio_file:
                await update.message.reply_audio(audio=InputFile(audio_file), caption="Here is your generated audio.")
            
            # Remove the file after sending
            # os.remove(filename)
            break
        time.sleep(5)
        if audio_info[1]["status"] == 'streaming':
            audio_url = audio_info[1]['audio_url']
            
            # Download the audio file
            filename = download_audio_file(audio_url)

            # Send the audio file to the user
            with open(filename, 'rb') as audio_file:
                await update.message.reply_audio(audio=InputFile(audio_file), caption="Here is your generated audio.")
            
            # Remove the file after sending
            # os.remove(filename)
            break
        time.sleep(5)

# Main function to run the bot
def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(telegram_api_token).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    
    # Register message handler for text prompts
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_audio))

    # Run the bot until Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
