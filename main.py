# Main bot color hex code: 0xd9880f
from re import A
import discord
import json
from discord.ext import commands, tasks
from discord import ui
from discord.ui import Button, View, Select
import asyncio
import os
import threading
import re
import random
import sys
import datetime
from discord import app_commands
import time
import requests
import sqlite3


COLORS = {
  (0, 0, 0): "⬛",
  (0, 0, 255): "🟦",
  (255, 0 , 0): "🟥",
  (255, 255, 0): "🟨",
  (255, 165, 0): "🟧",
  (255, 255, 255): "⬜",
  (0, 255, 0): "🟩",
  (160, 140, 210): "🟪",
  # (190, 100, 80):  "🟫",
}

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

class PersistentViewBot(commands.Bot):
  def __init__(self):
    intents = discord.Intents.all()
    super().__init__(command_prefix=commands.when_mentioned_or("!"), intents=intents)

bot = PersistentViewBot()

@bot.event
async def on_ready():
    print("The bot is online.")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# Channel ID where the bot will log deleted messages
LOG_CHANNEL_ID = 1269358261384122440  # Replace with your log channel ID

def restart_bot():
  os.execv(sys.executable, ['python'] + sys.argv)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user.mentioned_in(message):
        responses = {
            "hello": ["Hi there!", "Hello!", "Hey!", "Hi!", "Greetings!", "Salutations!", "Howdy!", "Heya!"],
            "bye": ["Goodbye!", "See you later!", "Bye!", "Take care!", "Farewell!", "Catch you later!", "Adios!", "See ya!"],
            "thanks": ["You're welcome!", "No problem!", "Anytime!", "Glad to help!", "No worries!", "My pleasure!", "You're welcome anytime!", "It was nothing!"],
            "good morning": ["Good morning!", "Morning!", "Hope you have a great day!", "Good day to you!", "Rise and shine!", "Morning sunshine!", "Top of the morning to you!", "Wishing you a great morning!"],
            "good night": ["Good night!", "Sleep tight!", "Sweet dreams!", "Nighty night!", "Rest well!", "Have a good sleep!", "Goodnight and sweet dreams!", "Until tomorrow!"],
            "how are you": ["I'm just a bot, but I'm doing great!", "All systems operational!", "I'm here and ready to assist!", "Feeling chatty!", "I'm good, thanks for asking!", "Doing well, how about you?", "I'm always ready to help!", "Running smoothly, how can I assist?"],
            "what's up": ["Not much, just here to help you!", "Just hanging out in the server.", "Waiting for your commands!", "Ready to assist you!", "Not much, what about you?", "At your service!", "Here to chat!", "What can I do for you?"],
            "who are you": ["I'm a helpful bot!", "Your friendly server assistant.", "I'm a bot created to assist you.", "Just a bot, here to help!", "Your virtual assistant.", "A helpful bot at your service.", "I'm here to make your life easier!", "I'm your server's assistant."],
            "joke": ["Why don't scientists trust atoms? Because they make up everything!", "What do you call fake spaghetti? An impasta!", "Why did the scarecrow win an award? Because he was outstanding in his field!", "What do you call cheese that isn't yours? Nacho cheese!", "Why don’t skeletons fight each other? They don’t have the guts.", "What do you get when you cross a snowman and a vampire? Frostbite.", "Why don’t seagulls fly over the bay? Because then they’d be bagels!", "What’s orange and sounds like a parrot? A carrot!"],
            "quote": ["“The best way to predict the future is to invent it.” – Alan Kay", "“Life is 10% what happens to us and 90% how we react to it.” – Charles R. Swindoll", "“The only way to do great work is to love what you do.” – Steve Jobs", "“Don’t watch the clock; do what it does. Keep going.” – Sam Levenson", "“You miss 100% of the shots you don’t take.” – Wayne Gretzky", "“Whether you think you can or you think you can’t, you’re right.” – Henry Ford", "“The future belongs to those who believe in the beauty of their dreams.” – Eleanor Roosevelt", "“The only limit to our realization of tomorrow is our doubts of today.” – Franklin D. Roosevelt"],
            "inspire me": ["Believe you can and you're halfway there.", "Keep your face always toward the sunshine—and shadows will fall behind you.", "The only way to achieve the impossible is to believe it is possible.", "Don’t stop until you’re proud.", "Dream big and dare to fail.", "Start where you are. Use what you have. Do what you can.", "You are capable of amazing things.", "Push yourself, because no one else is going to do it for you."],
            "weather": ["I'm not sure about the weather right now, but I hope it's nice where you are!", "I don't have weather data, but I hope it's sunny and bright!", "Weather is beyond my reach, but I hope it's pleasant!", "I can't check the weather, but I hope it's a beautiful day!", "Weather updates are not my thing, but I hope it's great outside!", "I don't know the weather, but I hope it's a wonderful day!", "Weather info isn't in my system, but I hope it's nice!", "I'm not equipped for weather updates, but I hope it's good!"],
            "meme": ["Here's a meme for you: *insert meme here*", "Check out this meme: *insert meme here*", "Enjoy this meme: *insert meme here*", "How about a meme? *insert meme here*", "Meme time! *insert meme here*", "Laugh at this meme: *insert meme here*", "Here's a funny meme: *insert meme here*", "Meme incoming: *insert meme here*"]
            # Add more words and responses as needed
        }

        message_content = message.content.lower()

        for word, word_responses in responses.items():
            if word in message_content:
                response = random.choice(word_responses)
                await message.channel.send(response)
                break

    await bot.process_commands(message)

@bot.event
async def on_member_update(before, after):
    # Check if the member has boosted the server
    if before.premium_since is None and after.premium_since is not None:
        # The member has started boosting the server
        channel_id = 1267772723908837469  # Replace with your channel ID
        channel = bot.get_channel(channel_id)
        if channel:
            # Send a thank you message to the specified channel
            await channel.send(f"Thank you {after.mention} for boosting the server! 🚀 Your support helps us grow and improve our community!\n<@&1269384222586699806> Y'all should do the same. ^^")
        else:
            print(f"Channel with ID {channel_id} not found.")
    elif before.premium_since is not None and after.premium_since is None:
        # The member has stopped boosting the server
        print(f"{after} has stopped boosting the server.")

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if log_channel is not None:
        embed = discord.Embed(
            title="Message Deleted",
            description=f"Message from {message.author.mention} deleted in {message.channel.mention}",
            color=discord.Color.red()
        )
        embed.add_field(name="Content", value=message.content, inline=False)
        embed.set_footer(text=f"Author ID: {message.author.id} • Message ID: {message.id}")
        await log_channel.send(embed=embed)

@bot.tree.command(name="members", description="Shows the member count of the server")
async def members(interaction: discord.Interaction):
    guild = interaction.guild
    if guild:
        await interaction.response.send_message(f'This server has {guild.member_count} members!')
    else:
        await interaction.response.send_message('This command can only be used in a server.')

@bot.tree.command(name="membercount", description="Shows the member count of the server")
async def membercount(interaction: discord.Interaction):
    guild = interaction.guild
    if guild:
        await interaction.response.send_message(f'This server has {guild.member_count} members!')
    else:
        await interaction.response.send_message('This command can only be used in a server.')

@bot.tree.command(name="group", description="Sends RSS Group link to you")
async def group(interaction: discord.Interaction):
 await interaction.response.send_message("https://www.roblox.com/groups/12662534/RSS-Riverside-Secondary#!/about")

@bot.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.reply("☑️ Restarted bot!")
    restart_bot()

@bot.command()
@commands.has_role("Executive Leadership Team")  # Ensure only users with this role can use the command
async def strike(ctx, member: discord.Member = None, *, reason: str = None):
    if member is None or reason is None:
        # Check if either member or reason is missing
        await ctx.send("Please provide both a member and a reason for the strike.")
        return

    try:
        # Format the strike message with the reason, server name, and sender's username
        strike_message = (
            f"__**Staff Strike**__\n"
            f"<:RSS:1268215346209226886> | You have been struck from {ctx.guild.name} for {reason}.\n\n"
            f"Please use your words sensibly to keep our community a safe place. Thank you!\n\n"
            f"Signed,\n{ctx.author.display_name}"
        )
        
        # Send a DM to the user with the strike message
        await member.send(strike_message)
        await ctx.send(f"Message sent to {member.mention} with reason: {reason}!")
    except discord.Forbidden:
        # Handle cases where the bot cannot send DMs
        await ctx.send(f"Could not send a DM to {member.mention}. They may have DMs disabled.")
    except Exception as e:
        # Handle other exceptions
        await ctx.send(f"An error occurred: {e}")

@bot.command()
@commands.has_role("Executive Leadership Team")  # Ensure only users with this role can use the command
async def dm(ctx, member: discord.Member = None, *, text: str = None):
    if member is None or text is None:
        # Check if either member or reason is missing
        await ctx.send("Please provide both a member and a text for the DM.")
        return

    try:
        # Send a DM to the user with the strike message
        await member.send(f"{text}")
        await ctx.send(f"Message sent to {member.mention} with text: {text}")
    except discord.Forbidden:
        # Handle cases where the bot cannot send DMs
        await ctx.send(f"Could not send a DM to {member.mention}. They may have DMs disabled.")
    except Exception as e:
        # Handle other exceptions
        await ctx.send(f"An error occurred: {e}")

@bot.command()
@commands.has_role("Executive Leadership Team")  # Ensure only admins can use this command
async def unstrike(ctx, member: discord.Member, *, reason: str = None):
    if reason is None:
        await ctx.send("Please provide a reason to remove the strike.")
        return
    
    try:
        # Send a DM to the user with the reason
        await member.send(f"<:RSS:1268215346209226886> You have been removed the strike.\nReason: {reason}")
        await ctx.send(f"Message sent to {member.mention} with reason: {reason}!")
    except discord.Forbidden:
        # Handle cases where the bot cannot send DMs
        await ctx.send(f"Could not send a DM to {member.mention}. They may have DMs disabled.")
    except Exception as e:
        # Handle other exceptions
        await ctx.send(f"An error occurred: {e}")

@bot.command()
@commands.has_role("Executive Leadership Team")  # Ensure only admins can use this command
async def add(ctx, user: discord.Member):
    # Define the role ID
    role_id = 1269380153935401112  # Replace with your actual role ID

    # Get the role object using the role ID
    role = discord.utils.get(ctx.guild.roles, id=role_id)
    if not role:
        await ctx.send("The specified role could not be found.")
        return

    # Create a new text channel
    try:
        channel_name = f"{user.name}"
        category = discord.utils.get(ctx.guild.categories, name="RSS | Under Review")  # Optional: Specify a category
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True)
        }
        
        # Create the channel
        channel = await ctx.guild.create_text_channel(
            name=channel_name,
            category=category,  # Remove this line if you don't want to specify a category
            overwrites=overwrites
        )
        
        # Add the role to the user
        await user.add_roles(role)
        await ctx.send(f"Sent {user.mention} to UNDER REVIEW!")

        # Send a message to the newly created channel
        await channel.send(
            f"Hello {user.mention},\n"
            f"You are now UNDER REVIEW. Please wait for someone to arrive to review/interrogate you.\n"
            f"Note: This process may not be completed in a single sitting."
        )
    except discord.Forbidden:
        # Handle permission errors
        await ctx.send("I do not have permission to create channels or manage roles.")
    except Exception as e:
        # Handle other potential exceptions
        await ctx.send(f"An error occurred: {e}")

OWNER_ID = 898255050592366642

@bot.command()
@commands.is_owner()  # Ensure only the bot owner can use this command
async def addrole(ctx, role: discord.Role):
    # Ensure the bot has the permission to manage roles
    if not ctx.guild.me.guild_permissions.manage_roles:
        await ctx.send("I don't have permission to manage roles.")
        return

    # Ensure the role is lower than the bot's highest role
    if role.position >= ctx.guild.me.top_role.position:
        await ctx.send("The specified role is higher or equal to my highest role.")
        return

    # Iterate over each member and add the role
    for member in ctx.guild.members:
        try:
            # Skip if the member already has the role
            if role in member.roles:
                continue
            
            # Add the role to the member
            await member.add_roles(role)
            
            # Sleep for a bit to avoid rate limits
            await asyncio.sleep(1)  # Adjust the sleep time as needed

        except discord.Forbidden:
            # Handle cases where the bot can't add the role
            await ctx.send(f"Could not add role to {member.name}.")
        except Exception as e:
            # Handle other potential exceptions
            await ctx.send(f"An error occurred with {member.name}: {e}")

    await ctx.send("Role assignment complete!")

bot.run("")
