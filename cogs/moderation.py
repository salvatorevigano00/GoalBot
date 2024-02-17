# Importa le librerie necessarie
from os import execv
import sys
import discord, asyncio, random
from discord.ext import commands
from discord import app_commands

# Definisce la classe Moderation per la gestione dei comandi di moderazione
class Moderation(commands.Cog):
    def __init__(self, bot):
        """
        Inizializza la classe Moderation, collegando il bot.
        """
        self.bot = bot

    # Comando "stop" per fermare il bot
    @commands.hybrid_command('stop', description='Ferma il bot')
    @commands.has_permissions(administrator=True)  # Controlla se l'utente ha il permesso di amministratore
    async def stop(self, ctx: commands.Context):
        """
        Ferma il bot.
        """
        await ctx.send('Bot fermato.')
        await ctx.bot.close()

    # Comando "cancella" per eliminare tutti i messaggi in una chat
    @commands.hybrid_command('cancella', description='Elimina tutti i messaggi in una chat')
    @commands.has_permissions(manage_messages=True)  # Controlla i permessi dell'utente
    async def cancella(self, ctx: commands.Context):
        """
        Elimina tutti i messaggi nella chat.
        """
        # Recupera la chat
        channel = ctx.channel

        # Elimina tutti i messaggi
        await channel.purge(limit=None)

        # Invia un messaggio di conferma che viene eliminato dopo 3 secondi
        await ctx.send('Tutti i messaggi sono stati eliminati', delete_after=3)

    # Comando "riavvia" per riavviare il bot
    @commands.hybrid_command('riavvia', description='Riavvia il bot')
    @commands.has_permissions(administrator=True)
    async def riavvia(self, ctx: commands.Context):
        """
        Riavvia il bot.
        """
        try:
            await ctx.send('Riavvio in corso...')
            await asyncio.sleep(2)  # Attesa di 2 secondi prima del riavvio
            execv(sys.executable, ['python3'] + sys.argv)
        except Exception as e:
            # Gestisce le eccezioni generiche
            await ctx.send('Errore durante il riavvio del bot.')
            print(f'Errore in Moderation.riavvia: {e}')

# Funzione per aggiungere il cog al bot
async def setup(bot):
    await bot.add_cog(Moderation(bot))