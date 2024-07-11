import discord
import os
import json

prefix = '$'
COINS_FILE = os.path.join('memoria', 'coins.json')

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return {}

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

class Coins:
    def __init__(self, client):
        self.client = client
        self.coins_data = load_data(COINS_FILE)

    async def processar_mensagem(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith(prefix + 'bank'):
            await self.mostrar_coins(message)

    async def mostrar_coins(self, message):
        coins_data = load_data(COINS_FILE)
        user_id = str(message.author.id)
        if user_id in self.coins_data:
            coins = coins_data[user_id]
            await message.channel.send(f"{message.author.mention}, você tem {coins} pixel's.")
        else:
            await message.channel.send(f"{message.author.mention}, você ainda não possui pixel.")
