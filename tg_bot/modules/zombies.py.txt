from tg_bot.client import new_message
from tg_bot import oko, SUDO_USERS
from telethon import events, Button
from asyncio import sleep
from os import remove
from tg_bot.modules.helper_funcs.telethon.chat_status import (
    can_delete_messages, user_is_admin, saber_is_admin, can_ban_users)

from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.types import (ChannelParticipantsAdmins, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto)


# =================== CONSTANT ===================

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================

async def is_administrator(user_id: int, message):
    admin = False
    async for user in message.client.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or user_id in SUDO_USERS:
            admin = True
            break
    return admin

@oko.on(events.CallbackQuery(data=b'rmdel'))
async def _(event):
    x = await event.client.get_entity(event.chat_id)
    title = x.title
    all_deleted = False
    if not await is_administrator(user_id=event.query.user_id, message=event):
        return
    async for user in event.client.iter_participants(event.chat_id):
        if user.deleted:
            try:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
                all_deleted = True
            except Exception as e: 
                print(e)

    if all_deleted is True:
          await event.client.edit_message(event.chat_id,event.query.msg_id,f"Removed all deleted accounts in **{title}**.")

@new_message(pattern="^/zombies$")
async def rm_deletedacc(show):
    if not show.is_group:
        await event.reply("`I don't think this is a group.`")
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    if not admin:
        await show.reply("I'm not admin! - REEEEEE")
        return
    if not await user_is_admin(user_id=show.from_id, message=show):
        await show.reply("Who dis non-admin telling me what to do? You want a kick?")
        return
    if not await can_ban_users(message=show):
        await show.reply("Seems like I don't have permission to ban users.")
        return
    del_u = 0
    del_status = "No deleted accounts found, Group is clean."
    x = await show.reply("Searching for deleted accounts...")
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            del_u += 1
            await sleep(1)
    if del_u > 0:
        await show.client.delete_messages(show.chat_id, x.id)
        del_status = f"Found **{del_u}** deleted/zombies account(s) in this group,\
            \nclean them by clicking the button below."
        await show.client.send_message(show.chat_id, del_status, buttons=[Button.inline('Clean Zombies', b'rmdel')], reply_to=show.id)
    else:
        await show.client.edit_message(show.chat_id, x.id, del_status)
