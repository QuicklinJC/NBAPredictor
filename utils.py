import discord

def build_prediction_embed(player_name, next_game, stats):
    embed = discord.Embed(
        title=f"NBA Prediction: {player_name}",
        description=f"Predicted stats for next game ({next_game['date']} vs {next_game['opponent']})",
        color=0x3498db
    )
    for stat, value in stats.items():
        embed.add_field(name=stat, value=value, inline=True)
    return embed
