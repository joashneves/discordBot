
import discord
import random


class AtribuiCargo():
    def __init__(self, client):
        self.client = client

    global SERVER_ID
    SERVER_ID = 1252065347016593488  # ID Do server
    async def atribuiCargo(self):
        guild = self.client.get_guild(SERVER_ID)
        role_ids = [1252262448120205372, 1252077450280702035]  # IDs dos cargos
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
