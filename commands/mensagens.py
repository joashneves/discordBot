import discord

response_channel = 1058880199414005852  # canal de imagens

class messagensBotRespostas():
    def __init__(self, client):
        self.client = client

    async def processar_mensagem(self, mensagem):
        if mensagem.author == self.client.user:
            return
        if mensagem.content.endswith("que"):
            await mensagem.channel.send("JO!")
        if "s3nha" in mensagem.content:
            await mensagem.add_reaction('❤')
        if "skalart" in mensagem.content.lower():
            await mensagem.channel.send("aopa!")

## Verifica se é uma imagem e reage
        if mensagem.channel.id == response_channel:
            if mensagem.attachments:
                if mensagem.attachments[0].url:
                    last_message = await mensagem.channel.fetch_message(mensagem.channel.last_message_id)
                    emoji_list = ['👍', '👎', '❤']
                    for emoji in emoji_list:
                        await last_message.add_reaction(emoji)