from telegram.ext import Updater, CommandHandler
import requests
from config import TELEGRAM_API_TOKEN, OPENAI_API_TOKEN
import json
import logging
# test

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def generate_image(update, context):
    print("generate image")
    prompt = " ".join(context.args)
    api_key = OPENAI_API_TOKEN
    response = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        json={
            "prompt": prompt,
            "num_images": 1,
            "size": "512x512",
            "response_format": "url",
        },
    )
    if response.status_code == 200:
        image_url = json.loads(response.content)["data"][0]["url"]
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=image_url
        )
    else:
        logger.error("Error generating image")
        update.message.reply_text("Error generating image. Please try again.")

    # update.message.reply_text(f'Avg. Currency for last 15 mins')


updater = Updater(token=TELEGRAM_API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

inlinequery_handler = CommandHandler("image", generate_image)

dispatcher.add_handler(inlinequery_handler)

updater.start_polling()
updater.idle()
