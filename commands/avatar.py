import discord
from discord.ext import commands
import datetime
import json
import os

prefix = '$'
data = datetime.date
DATA_FILE = os.path.join('memoria', 'userAvatar.json')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            print("Json de Avatar carregado...")
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
        print("Json de Avatar Salvo...")

class ViewInfo(discord.ui.View):
    def __init__(self, embeds):
        super().__init__()
        self.embeds = embeds
        self.current = 0

    @discord.ui.button(label='<<<', style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current = (self.current - 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

    @discord.ui.button(label='>>>', style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current = (self.current + 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current], view=self)

class AvatarComandos:

    def __init__(self, client):
        self.client = client

    async def avatar(self, mensagem):
        if mensagem.author == self.client.user:
            return

        if mensagem.content.startswith(prefix + 'avatar'):
            data_atual = data.today()
            data_formatada = data_atual.strftime("%d/%m/%Y")

            if mensagem.mentions:
                user = mensagem.mentions[0]
            else:
                user = mensagem.author

            user_id = str(user.id)

            # Load existing data
            all_data = load_data()

            # Check if the user exists in the JSON
            if user_id not in all_data:
                all_data[user_id] = {
                    'nome': user.name,
                    'id': user.id,
                    'apelido': user.display_name,
                    'avatares': []
                }

            # Check if the avatar has changed
            avatar_changed = not any(entry['url'] == user.avatar.url for entry in all_data[user_id]['avatares'])
            if avatar_changed:
                # Add new avatar entry
                new_avatar = {
                    'url': user.avatar.url,
                    'data_regeneracao': data_formatada
                }
                all_data[user_id]['avatares'].append(new_avatar)
                save_data(all_data)

            # Get the regeneration count for the user
            regeneracao_count = len(all_data[user_id]['avatares'])

            # Create embeds for each avatar
            embeds = []
            for i, avatar in enumerate(reversed(all_data[user_id]['avatares'])):
                embed = discord.Embed(
                    title=f'Nome: {user.name}',
                    description=f'Informações da regeneração: {user.name}'
                )
                embed.set_image(url=avatar['url'])
                embed.add_field(name='ID', value=user.id, inline=False)
                embed.add_field(name='Apelido', value=user.display_name, inline=False)
                embed.add_field(name='Data de regeneração', value=avatar['data_regeneracao'], inline=False)
                embed.set_footer(text=f'{regeneracao_count - i}ª regeneração')
                embeds.append(embed)

            # Send the first embed with navigation buttons
            view = ViewInfo(embeds)
            await mensagem.channel.send(embed=embeds[0], view=view)
