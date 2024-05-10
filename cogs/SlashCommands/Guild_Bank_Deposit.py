import discord
from discord.ext import commands
from discord import app_commands, ui


class MyModal(ui.Modal, title="Guild Bank Deposit"):
    item = ui.TextInput(label="Please Enter Item",
                        placeholder="Onyx Essence",
                        custom_id="itemField",
                        style=discord.TextStyle.short)
    amount = ui.TextInput(label="Please Enter Amount",
                          placeholder="100",
                          custom_id="amountTextField",
                          style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):
        # Acknowledge the interaction with an ephemeral message
        message = await interaction.response.send_message(f"✅ Successfully deposited {self.item} {self.amount}x", ephemeral=True)

        # Replace with your desired channel ID
        target_channel_id = 1224556858480791623

        # Try to get the channel from the guild
        target_channel = interaction.guild.get_channel(target_channel_id)
        if target_channel:
            # Send the message to the specified channel
            embed = discord.Embed(title=f"{interaction.user.display_name} ",
                                  description=f"Has Deposited **{self.item}**",
                                  color=discord.Color.green())  # Adding a color to indicate success
            embed.add_field(name="Item Amount", value=f"`{self.amount}`x")

            sent_message = await target_channel.send(embed=embed)

            # Edit the original ephemeral message to indicate success
            await interaction.edit_original_message(content="Your request has been processed successfully!",
                                                    ephemeral=True)

            # Edit the original ephemeral message to indicate success

        else:
            print("Target channel not found.")


class ModalTest(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slash Cogs Loaded")

    @app_commands.command(name="bankdeposit", description="Deposit Items into Guild Bank")
    async def deposititem(self, interaction: discord.Interaction):
        await interaction.response.send_modal(MyModal())


async def setup(client):
    client.remove_command("help")
    await client.add_cog(ModalTest(client), guilds=[discord.Object(id="1041205088657616898")])


