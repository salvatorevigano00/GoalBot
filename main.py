# Importa le librerie necessarie
import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Recupera il token del bot dal file .env
TOKEN = os.getenv("TOKEN")

# ID del canale testuale desiderato
TEST_CHANNEL_ID = 1207263685332959233  # Sostituisci con l'ID del tuo canale

# Definisce la classe del bot che eredita da commands.Bot
class Bot(commands.Bot):
    def __init__(self):
        """
        Inizializza il bot con le impostazioni desiderate.
        """
        # Imposta gli intenti del bot
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        # Chiama il costruttore della classe padre
        super().__init__(command_prefix="!", intents=intents)

    async def on_ready(self):
        """
        Funzione eseguita quando il bot è pronto e online.
        """
        try:
            # Stampa informazioni sul bot
            print(f"Bot online come {self.user}")
        except Exception as e:
            print(f"Errore durante l'esecuzione di on_ready: {e}")

    async def setup_hook(self):
        """
        Funzione eseguita all'avvio del bot per sincronizzare i comandi.
        """
        try:
            # Sincronizza i comandi con l'albero dei comandi di Discord
            commands = await self.tree.sync()
            print(f"Comandi sincronizzati: {commands}")
        except Exception as e:
            # Gestisce l'eccezione e stampa l'errore
            print(f"Errore durante la sincronizzazione dei comandi: {e}")
            # Inviare un messaggio di errore all'amministratore o registrare l'errore su un file

    async def load_cogs(self):
        """
        Funzione per caricare automaticamente i cogs (estensioni) del bot.
        """
        # Elenco dei percorsi dei cogs
        cog_paths = ["cogs.moderation", "cogs.carte"]  # Aggiornare con i percorsi corretti
        for path in cog_paths:
            try:
                # Carica il cog specificato dal percorso
                await self.load_extension(path)
                print(f"Cog caricato: {path}")
            except Exception as e:
                # Gestisce l'eccezione e stampa l'errore
                print(f"Errore durante il caricamento del cog {path}: {e}")
                # Inviare un messaggio di errore all'amministratore o registrare l'errore su un file

    async def on_message(self, message):
        """
        Funzione eseguita quando il bot riceve un messaggio.
        """
        try:
            # Controlla se il messaggio è stato inviato nel canale testuale desiderato
            if message.channel.id != TEST_CHANNEL_ID:
                return  # Ignora il messaggio se non è nel canale desiderato
            
            # Se necessario, aggiungi qui il codice per gestire il messaggio
            
            # Assicurati di chiamare il comando process_commands per l'esecuzione dei comandi
            await self.process_commands(message)
        except Exception as e:
            print(f"Errore durante l'esecuzione di on_message: {e}")

async def main():
    """
    Funzione principale che avvia il bot.
    """
    # Crea un'istanza del bot
    bot = Bot()

    try:
        # Carica i cogs
        await bot.load_cogs()

        # Avvia il bot con il token
        await bot.start(TOKEN)
    except Exception as e:
        # Gestisce l'eccezione e stampa l'errore
        print(f"Errore durante l'avvio del bot: {e}")
        # Inviare un messaggio di errore all'amministratore o registrare l'errore su un file

if __name__ == "__main__":
    # Esegue la funzione principale
    asyncio.run(main())
