import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
gemini_key = os.getenv('GEMINI_API_KEY') 


genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-flash-latest')


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True 


bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Botul e conectat ca {bot.user.name}') 

@bot.event
async def on_member_join(member):
   
    await member.send(f'Bine ai venit pe serverul nostru, {member.name}! Sperăm să te simți bine aici!')

@bot.event
async def on_message(message):
    
    if message.author == bot.user:
        return
        
    
    if "gunoi" in message.content.lower() or "caca" in message.content.lower():
        await message.delete()
        await message.channel.send(f'{message.author.mention} Nu folosi cuvinte urâte!')
        return 
        
    
    await bot.process_commands(message)    


@bot.command(name='ask')
async def ask_ai(ctx, *, prompt: str):
   
    async with ctx.typing():
        try:
            
            response = await model.generate_content_async(prompt)
            
            
            answer = response.text
            if len(answer) > 2000:
                answer = answer[:1996] + "..."
                
            await ctx.send(answer)
            
        except Exception as e:
            await ctx.send(f"A apărut o eroare la comunicarea cu AI: {e}")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)