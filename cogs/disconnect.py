from discord.ext import commands

class DisconnectCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="disconnect", help="Disconnect from the remote server")
    async def disconnect_command(self, ctx):
        cog = self.bot.get_cog("SSHCog")
        if cog and cog.is_connected():
            cog.disconnect()
            await ctx.send("Disconnected.")
        else:
            await ctx.send("Not currently connected.")

def setup(bot):
    bot.add_cog(DisconnectCog(bot))
