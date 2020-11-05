import asyncio
from telethon import TelegramClient, events

bots = [1358259148, 1109485632]
bot = TelegramClient('session_name')


@bot.on(events.NewMessage(from_users=bots))
async def redirection(event):
    print(event.raw_text)
    if event.chat_id == 1109485632:     # home_assistant_
        message_id = await bot.send_message(1358259148, event.raw_text)
        message_id = message_id.id
        await bot.delete_messages(1358259148, message_id, revoke=True)
    else:
        message_id = await bot.send_message(1109485632, "bot: " + event.raw_text)
        message_id = message_id.id
        await bot.delete_messages(1109485632, message_id, revoke=True)


async def main():
    while True:
        await pass_function()


async def pass_function():
    await asyncio.sleep(1)


if __name__ == '__main__':
    with bot:
        bot.loop.run_until_complete(main())
