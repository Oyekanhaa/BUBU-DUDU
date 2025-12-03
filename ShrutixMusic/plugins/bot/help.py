from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message

from ShrutixMusic import nand
from ShrutixMusic.utils import help_pannel
from ShrutixMusic.utils.database import get_lang
from ShrutixMusic.utils.decorators.language import LanguageStart, languageCB
from ShrutixMusic.utils.inline.help import help_back_markup, private_help_panel, help_more_keyboard
from config import BANNED_USERS, START_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers


# =========================
# PRIVATE HELP COMMAND
# =========================
@nand.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@nand.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(client: nand, update: Union[types.Message, types.CallbackQuery]):
    is_callback = isinstance(update, types.CallbackQuery)

    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard
        )

    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_)
        await update.reply_photo(
            photo=START_IMG_URL,
            caption=_["help_1"].format(SUPPORT_CHAT),
            reply_markup=keyboard,
        )


# =========================
# GROUP HELP INVOKE
# =========================
@nand.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


# =========================
# MAIN HELP CALLBACKS (HB1–HB15)
# =========================
@nand.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    cb = CallbackQuery.data.strip().split(None, 1)[1]
    keyboard = help_back_markup(_)

    mapping = {
        "hb1": helpers.HELP_1,
        "hb2": helpers.HELP_2,
        "hb3": helpers.HELP_3,
        "hb4": helpers.HELP_4,
        "hb5": helpers.HELP_5,
        "hb6": helpers.HELP_6,
        "hb7": helpers.HELP_7,
        "hb8": helpers.HELP_8,
        "hb9": helpers.HELP_9,
        "hb10": helpers.HELP_10,
        "hb11": helpers.HELP_11,
        "hb12": helpers.HELP_12,
        "hb13": helpers.HELP_13,
        "hb14": helpers.HELP_14,
        "hb15": helpers.HELP_15,
    }

    await CallbackQuery.edit_message_text(mapping[cb], reply_markup=keyboard)


# =========================
# NEW — MORE MENU CALLBACK
# =========================
@nand.on_callback_query(filters.regex("help_more_menu") & ~BANNED_USERS)
@languageCB
async def help_more_menu_cb(client, cq, _):
    await cq.edit_message_text(
        "📂 **More Help Categories:**",
        reply_markup=help_more_keyboard(_)
    )


# =========================
# NEW — BACK TO HOME MENU
# =========================
@nand.on_callback_query(filters.regex("help_back_main") & ~BANNED_USERS)
@languageCB
async def help_back_main_cb(client, cq, _):
    await cq.edit_message_text(
        _["help_1"].format(SUPPORT_CHAT),
        reply_markup=help_pannel(_, START=True)
    )
