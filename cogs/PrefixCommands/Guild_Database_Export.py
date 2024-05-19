import json
import csv
import sqlite3
import discord
from discord.ext import commands
import io  # Import the io module

# SQLite3 database connection
conn = sqlite3.connect('guilddatabase.db')
cursor = conn.cursor()


class databaseexport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)  # Permission Settings
    async def export_data(self, ctx, file_format: str = 'json'):
        if file_format not in ['json', 'csv']:
            await ctx.send("Invalid file format. Please choose 'json' or 'csv'.")
            return

        data = {}

        # Query table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        tables = [table[0] for table in tables if table[0] != 'sqlite_sequence']  # Exclude sqlite_sequence table

        # Function to get username from ID
        async def get_username(user_id):
            user = self.bot.get_user(user_id)
            if user is None:
                try:
                    user = await self.bot.fetch_user(user_id)
                except discord.NotFound:
                    return "Unknown User"
            return user.name

        # Query and store data for each table
        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            users = cursor.fetchall()
            user_ids = [user[0] for user in users]

            user_data = []
            for user_id in user_ids:
                username = await get_username(user_id)
                user_data.append({"id": user_id, "username": username})

            data[table] = user_data

        # Export data to JSON or CSV
        if file_format == 'json':
            content = json.dumps(data, indent=4)
            file = discord.File(fp=io.StringIO(content), filename="userdata.json")
        elif file_format == 'csv':
            content = io.StringIO()
            writer = csv.writer(content)
            for table, users in data.items():
                writer.writerow([table, "ID", "Username"])  # CSV header
                for user in users:
                    writer.writerow([table, user["id"], user["username"]])
            content.seek(0)
            file = discord.File(fp=content, filename="userdata.csv")

        # Send the file
        await ctx.send("Data exported:", file=file)


async def setup(client):
    await client.add_cog(databaseexport(client))
