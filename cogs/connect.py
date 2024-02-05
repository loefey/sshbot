import discord
from discord.ext import commands
import paramiko

class SSHCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ssh_client = None

    def is_connected(self):
        return self.ssh_client is not None

    @commands.slash_command(name="connect", help="Connect to a remote server via SSH and run terminal commands")
    async def connect_command(self, ctx, host: str, username: str, password: str):
        try:
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(host, username=username, password=password)

            await ctx.respond("Connection established. Type your terminal commands below.", ephemeral=True)

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel

            while True:
                message = await self.bot.wait_for('message', check=check)

                if message.content.lower() == "/disconnect":
                    await ctx.respond("Disconnected.")
                    break

                if self.ssh_client:
                    stdin, stdout, stderr = self.ssh_client.exec_command(message.content)
                    output = stdout.read().decode()

                    await ctx.send(f"{output}")

        except Exception as e:
            await ctx.respond(f"An error occurred: {e}")

        finally:
            self.disconnect()

    def disconnect(self):
        if self.is_connected():
            self.ssh_client.close()
            self.ssh_client = None

    @commands.command(name="disconnect", help="Disconnect from the remote server")
    async def disconnect_command(self, ctx):
        if self.is_connected():
            self.disconnect()
            await ctx.respond("Disconnected.")
        else:
            await ctx.respond("Not currently connected.")

def setup(bot):
    bot.add_cog(SSHCog(bot))