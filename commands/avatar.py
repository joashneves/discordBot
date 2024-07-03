import discord
from discord.ext import commands
import datetime
import json
import os
import aiohttp
import hashlib

prefix = '$'
data = datetime.date
DATA_FILE = os.path.join('memoria', 'userAvatar.json')
AVATAR_DIR = os.path.join('memoria', 'avatars')

# Create the avatars directory if it doesn't exist
if not os.path.exists(AVATAR_DIR):
    os.makedirs(AVATAR_DIR)


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            print("Json de Avatar carregado...")
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}  # Return an empty dictionary if JSON is empty or invalid
    return {}


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
        print("Json de Avatar Salvo...")


def generate_avatar_filename(user_id, avatar_url):
    avatar_hash = hashlib.md5(avatar_url.encode('utf-8')).hexdigest()
    return f"{user_id}_{avatar_hash}.png"


async def save_avatar_locally(url, user_id):
    avatar_filename = generate_avatar_filename(user_id, url)
    avatar_path = os.path.join(AVATAR_DIR, avatar_filename)

    if os.path.exists(avatar_path):
        return avatar_path

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(avatar_path, 'wb') as f:
                    f.write(await response.read())
                return avatar_path
            else:
                raise Exception(f"Failed to download image: status {response.status}")


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
            current_avatar_url = user.avatar.url
            avatar_hash = hashlib.md5(current_avatar_url.encode('utf-8')).hexdigest()
            avatar_changed = not any(entry['hash'] == avatar_hash for entry in all_data[user_id]['avatares'])

            if avatar_changed:
                # Save the avatar image locally
                avatar_path = await save_avatar_locally(current_avatar_url, user_id)

                # Add new avatar entry with local path
                new_avatar = {
                    'url': avatar_path,
                    'data_regeneracao': data_formatada,
                    'hash': avatar_hash
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
                embed.set_image(url=f"attachment://{os.path.basename(avatar['url'])}")
                embed.add_field(name='ID', value=user.id, inline=False)
                embed.add_field(name='Apelido', value=user.display_name, inline=False)
                embed.add_field(name='Data de regeneração', value=avatar['data_regeneracao'], inline=False)
                embed.set_footer(text=f'{regeneracao_count - i}ª regeneração')
                embeds.append(embed)

            # Send the first embed with navigation buttons
            view = ViewInfo(embeds)
            files = [discord.File(avatar['url']) for avatar in all_data[user_id]['avatares']]
            await mensagem.channel.send(embed=embeds[0], view=view, files=files)
