import os
import discord
from discord.ext import commands
from nba_data import get_player_id, get_recent_game_logs, get_next_game_info
from predictor import predict_stats
from utils import build_prediction_embed

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.slash_command(name="nba_predict", description="Predict next NBA game stats for a player")
async def nba_predict(ctx, *, player_name: str):
    await ctx.defer()
    try:
        player_id = get_player_id(player_name)
        logs = get_recent_game_logs(player_id, n=10)
        predictions = predict_stats(logs)
        next_game = get_next_game_info(player_id)
        if next_game is None:
            await ctx.send("No upcoming games found for this player.")
            return
        embed = build_prediction_embed(player_name, next_game, predictions)
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error: {e}")

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    if not TOKEN:
        print("DISCORD_TOKEN environment variable not set.")
    else:
        bot.run(TOKEN)
