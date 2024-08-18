import discord
import random

class AtribuiCargoS3nha():
    def __init__(self, client):
        self.client = client

    global SERVER_ID
    SERVER_ID = 390309756918562823  # ID Do server
    async def atribuiCargo(self):
        guild = self.client.get_guild(SERVER_ID)
        role_ids = [1274512712524628059, 1274512683089268818, 1274512560229453924, 1274512508811739208, 1274512476767256657, 1274512422241308762]  # IDs dos cargos
        if guild:
            print(f"Servidor com ID {SERVER_ID} encontrado: {guild.name}.")
            for member in guild.members:
                if not any(role.id in role_ids for role in member.roles):
                    selected_role_id = random.choice(role_ids)
                    role = discord.utils.get(guild.roles, id=selected_role_id)
                    if role:
                        await member.add_roles(role)
                        print(f"Atribuiu o cargo '{role.name}' a {member.name}.")
                    else:
                        print(f"O cargo com ID {selected_role_id} não foi encontrado.")
        else:
            print(f"Servidor com ID {SERVER_ID} não encontrado.")
