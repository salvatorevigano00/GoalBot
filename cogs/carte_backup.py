import discord
import asyncio
import random
import os
import json
import time
from discord.ext import commands
from PIL import Image

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giocatori_persi = {}
        self.collezioni_giocatori = {}
        self.last_stamp = {}
        self.last_grab = {}

        # Carica le collezioni degli utenti dal file JSON all'avvio del bot
        self.caricaCollezioni()

    async def generaCarte(self, ctx: commands.Context):
        current_time = time.time()
        last_drop_time = self.last_stamp.get(ctx.author.id, 0)
        drop_cooldown = 600  # Tempo in secondi tra due drop consecutivi (10 minuti)

        if current_time - last_drop_time < drop_cooldown:
            await ctx.send(f"Devi aspettare ancora {drop_cooldown - int(current_time - last_drop_time)} secondi prima di poter generare un'altra immagine.")
            return

        cartella_immagini = "Immagini"

        try:
            nomi_file = os.listdir(cartella_immagini)
            immagini_selezionate = random.sample(nomi_file, 3)
            nomi_file_senza_estensione = [os.path.splitext(nome_file)[0] for nome_file in immagini_selezionate]
            nome_file_combinato = "_".join(nomi_file_senza_estensione) + ".png"
            immagini = [Image.open(os.path.join(cartella_immagini, nome_file)) for nome_file in immagini_selezionate]

            larghezza_totale = sum(immagine.width for immagine in immagini) + (len(immagini) - 1) * 10
            immagine_combinata = Image.new("RGBA", (larghezza_totale, max(immagine.height for immagine in immagini)))

            offset = 0
            for indice, immagine in enumerate(immagini):
                immagine_combinata.paste(immagine, (offset, 0))
                offset += immagine.width
                if indice < len(immagini) - 1:
                    offset += 10

            for x in range(immagine_combinata.width):
                for y in range(immagine_combinata.height):
                    if immagine_combinata.getpixel((x, y))[3] == 0:
                        immagine_combinata.putpixel((x, y), (255, 255, 255, 0))

            immagine_combinata.save(nome_file_combinato)

            file = discord.File(nome_file_combinato, filename=nome_file_combinato)
            message = await ctx.send(file=file)

            emoji_reazioni = set()
            for i in range(len(immagini_selezionate)):
                emoji = f"{i+1}\N{variation selector-16}\N{combining enclosing keycap}"
                await message.add_reaction(emoji)
                emoji_reazioni.add(emoji)

            for emoji in emoji_reazioni:
                await message.add_reaction(emoji)

            self.giocatori_persi[message.id] = {"1️⃣": None, "2️⃣": None, "3️⃣": None, "message": message, "immagini": immagini_selezionate}

            # Aggiorna l'ultimo tempo di "kd" per l'utente
            self.last_stamp[ctx.author.id] = current_time

        except Exception as e:
            await ctx.send(f"Errore durante la generazione dell'immagine: {e}")

        finally:
            os.remove(nome_file_combinato)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        if reaction.message.id not in self.giocatori_persi:
            return

        # Verifica se è passato abbastanza tempo dall'ultimo grab per l'utente
        current_time = time.time()
        last_grab_time = self.last_grab.get(user.id, 0)
        last_drop_time = self.last_stamp.get(user.id, 0)
        grab_cooldown = 300  # Tempo in secondi tra due grab consecutivi (5 minuti)
        drop_cooldown = 600  # Tempo in secondi tra due drop consecutivi (10 minuti)

        if current_time - last_grab_time < grab_cooldown:
            await reaction.message.channel.send(f"{user.mention}, devi aspettare ancora {grab_cooldown - int(current_time - last_grab_time)} secondi prima di poter effettuare un altro grab.")
            return
    
        if current_time - last_grab_time < drop_cooldown:
            await reaction.message.channel.send(f"{user.mention}, devi aspettare ancora {drop_cooldown - int(current_time - last_drop_time)} secondi prima di poter effettuare un altro grab.")
            return

        message = self.giocatori_persi[reaction.message.id]["message"]
        nomi_calciatori = [os.path.splitext(nome)[0] for nome in self.giocatori_persi[reaction.message.id]["immagini"]]
        emoji_index = int(reaction.emoji[0]) - 1

        if self.giocatori_persi[reaction.message.id][reaction.emoji] is not None:
            await message.channel.send("Non è possibile prendere un giocatore già preso da un altro utente.")
            return

        if emoji_index < len(nomi_calciatori):
            nome_giocatore = nomi_calciatori[emoji_index]
            self.giocatori_persi[reaction.message.id][reaction.emoji] = user
            await reaction.message.channel.send(f"L'utente {user.mention} ha preso il seguente giocatore: {nome_giocatore}")
            
            # Aggiungi il giocatore alla collezione dell'utente
            self.aggiungiGiocatoreACollezione(user.id, nome_giocatore)
            # Salva le collezioni aggiornate
            self.salvaCollezioni()

            # Aggiorna l'ultimo tempo di grab per l'utente
            self.last_grab[user.id] = current_time

        else:
            await message.channel.send("Nessun calciatore corrispondente.")

    @commands.command(description='Mostra 3 immagini casuali di calciatori')
    async def kd(self, ctx: commands.Context):
        await self.generaCarte(ctx)

    @commands.command(description='Visualizza la collezione di giocatori dell\'utente')
    async def kc(self, ctx: commands.Context):
        await self.inviaGiocatori(ctx, ctx.author)

    async def inviaGiocatori(self, ctx: commands.Context, user: discord.User):
        giocatori_ottenuti = self.getCollezioneGiocatori(user.id)
        if giocatori_ottenuti:
            await ctx.send(f"Giocatori ottenuti da {user}: {', '.join(giocatori_ottenuti)}")
        else:
            await ctx.send("Nessun giocatore ottenuto.")

    def aggiungiGiocatoreACollezione(self, user_id, nome_giocatore):
        for collezione in self.collezioni_giocatori:
            if collezione['user_id'] == user_id:
                collezione['giocatori'].append(nome_giocatore)
                return
        # Se l'utente non ha ancora una collezione, aggiungi una nuova voce
        self.collezioni_giocatori.append({'user_id': user_id, 'giocatori': [nome_giocatore]})
        # Aggiorna l'ultimo tempo di "kd" per l'utente
        self.last_stamp[user_id] = time.time()

    def getCollezioneGiocatori(self, user_id):
        for collezione in self.collezioni_giocatori:
            if collezione['user_id'] == user_id:
                return collezione['giocatori']
        return []

    def salvaCollezioni(self):
        with open('collezioni_giocatori.json', 'w') as f:
            json.dump(self.collezioni_giocatori, f)

    def caricaCollezioni(self):
        try:
            with open('collezioni_giocatori.json', 'r') as f:
                self.collezioni_giocatori = json.load(f)
        except FileNotFoundError:
            print("Il file delle collezioni non esiste ancora.")

# Funzione per aggiungere il cog al bot
async def setup(bot):
    await bot.add_cog(Fun(bot))