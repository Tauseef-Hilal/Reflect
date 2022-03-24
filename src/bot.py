import logging

from discord import Bot, Emoji, Message, Webhook

from .constants.emoji import EmojiGroup


class ICodeBot(Bot):
    """
    The BOT made for 'iCODE' Discord server.
    """
    emoji_group: EmojiGroup

    async def on_ready(self) -> None:
        """
        Called when the bot has finished logging in and setting things up
        """

        logging.info(msg=f"Logged in as {self.user}")

        logging.info(msg="Initializing EmojiGroup")
        self.emoji_group = EmojiGroup(self)

    async def on_message(self, message: Message) -> None:
        """
        Called when some user sends a messsage in the server

        Args:
            message (Message): Message sent by the user
        """

        if message.webhook_id:
            return

        emoji = None
        temp = []
        for word in message.content.split():
            if word[0] == word[-1] == ":" and len(word) > 2 and word not in temp:

                try:
                    emoji: Emoji = self.emoji_group.get_emoji(word[1:-1])

                    message.content = message.content.replace(word, str(emoji))
                    temp.append(word)

                except AttributeError:
                    pass

        if emoji:
            webhooks = await message.channel.webhooks()

            webhook: Webhook
            for webhook in webhooks:
                if webhook.user.id == self.user.id:
                    break
            else:
                avatar: bytes = await message.author.display_avatar.read()

                webhook: Webhook = await message.channel.create_webhook(
                    name="iCODE-BOT",
                    avatar=avatar,
                    reason="Animated Emoji Usage"
                )

            await webhook.send(content=message.content,
                               username=message.author.display_name, avatar_url=message.author.display_avatar)
            await message.delete()
