import html
import random
import tg_bot.modules.truth_and_dare_string as truth_and_dare_string
from tg_bot import dispatcher
from telegram import ParseMode, Update, Bot
from tg_bot.modules.disable import DisableAbleCommandHandler
from telegram.ext import run_async


@run_async
def animeqoute(bot: Bot, update: Update):
    update.effective_message.reply_photo(random.choice(truth_and_dare_string.ANIMEQOUTE))


ANIMEQOUTE_HANDLER = DisableAbleCommandHandler("animequote", animeqoute)

dispatcher.add_handler(ANIMEQOUTE_HANDLER)
