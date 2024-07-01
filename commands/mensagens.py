import discord
import ollama

response_channel = 1255938137499107490  # canal de imagens

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
        if mensagem.content.startswith("$skalart"):
            try:
                prompt = mensagem.content.split('skalart', 1)[1].strip()
                print(f"prompt: {prompt}")
                stream = ollama.chat(
                    model='phi3',
                    messages=[{'role': 'user', 'content': f'Responda em portugues a mensagem: {prompt}'}],
                    stream=True,
                )
                mensagem_bot = ""
                for chunk in stream:
                    mensagem_bot += chunk['message']['content']
                await mensagem.channel.send(mensagem_bot)
            except:
                await mensagem.channel.send("não foi possivel acessar essa função")

## Verifica se é uma imagem e reage
        if mensagem.channel.id == response_channel:
            if mensagem.attachments:
                if mensagem.attachments[0].url:
                    last_message = await mensagem.channel.fetch_message(mensagem.channel.last_message_id)
                    emoji_list = ['👍', '👎', '❤']
                    for emoji in emoji_list:
                        await last_message.add_reaction(emoji)