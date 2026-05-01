from discord.ui import View, Button
import discord

class BasicPaginator(View):
    def __init__(self, pages):
        super().__init__(timeout=60)
        self.pages = pages
        self.current_page = 0
    async def update(self,interaction:discord.Interaction):
        await interaction.response.edit_message(content=self.pages[self.current_page],view=self)

    @discord.ui.button(label="⬅️",style=discord.ButtonStyle.secondary)
    async def previous(self,interaction:discord.Interaction):
        if self.current_page > 0:
            self.current_page -= 1
            await self.update(interaction)
            
    @discord.ui.button(label="➡️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
        await self.update(interaction)