import logging

from discord import Bot, Emoji, Message, Webhook


class ICodeBot(Bot):
    """
    The BOT made for 'iCODE' Discord server.
    """

    async def on_ready(self) -> None:
        """
        Called when the bot has finished logging in and setting things up 
        """

        logging.info(msg=f"Logged in as {self.user}")

    async def on_message(self, message: Message) -> None:
        """
        Called when some user sends a messsage in the server

        Args:
            message (Message): Message sent by the user
        """

        if message.webhook_id:
            return
        
        emoji = False
        for word in message.content.split():
            if word[0] == word[-1] == ":" and len(word) > 2:
                emoji = True

                emoji: Emoji
                for emoji in self.emojis:
                    if emoji.name == word[1:-1]:
                        if emoji.animated:
                            message.content = message.content \
                                .replace(word, f"<a:{emoji.name}:{emoji.id}>")
                        else:
                            message.content = message.content \
                                .replace(word, f"<:{emoji.name}:{emoji.id}>")

        if emoji:
            webhooks = await message.channel.webhooks()

            webhook: Webhook
            for webhook in webhooks:
                if webhook.name == message.author.display_name:
                    break
            else:
                avatar: bytes = await message.author.display_avatar.read()

                webhook: Webhook = await message.channel.create_webhook(
                    name=message.author.display_name,
                    avatar=avatar,
                    reason="Animated Emoji Usage"
                )

            await message.delete()
            await webhook.send(message.content)
