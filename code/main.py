import discord
import json
from discord.ext import commands,tasks
import Spotify
import spotipy.util as util
import time
import os
import sys

passed_song = sys.argv[1:]

def convert(lst):
      
    return ' '.join(lst)
    
passed_song = convert(passed_song)

def getCreds():
	with open(os.path.expanduser('~/.bot_creds'), 'r') as file:
		content = file.read()
	if '\r' in content:
		data = content.split('\r\n')
	else:
		data = content.split('\n')
	return {'token' : data[0]}
	
bot_cred = getCreds()
print(Spotify.cred)


playlist = "https://open.spotify.com/playlist/7uhggSvWHcNLnJL8hTEd3q"
intents = discord.Intents().default()
bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
	print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))
	channel = bot.get_channel(947790182042726400)
	channel2 = bot.get_channel(946643918257283092)
	if Spotify.addToPlaylist(passed_song) != None:
		S_L = "https://open.spotify.com/track/" + (Spotify.songUri(passed_song).split(":"))[2]
		await channel2.send("Added "+ passed_song + " to the playlist!\n"+ S_L)
		time.sleep(1)
		await channel.send("Added "+ passed_song + " to the playlist!\n"+ S_L)
	else:
		await channel2.send("Couldn't find '" + passed_song + "', try again in a few seconds.")

	

@bot.command(name='rec', help='Adds song to playlist')
async def stop(ctx):
	name = ctx.message.content[4:]
	os.system("python3 main.py " + name)

@bot.command(name='yt', help='Adds video to youtube playlist queue')
async def modYT(ctx):	
	vid_id = ctx.message.content[3:]
	file = open("yt_ids.list","a")
	file.write(vid_id.split('=')[1]+"\n")
	file.close()
	ctx.send("Added your link to the playlist queue :)")

@bot.command(name='getyt', help='Generates youtube link')
async def genlink(ctx):
	empty_link = "http://www.youtube.com/watch_videos?video_ids="
	file = open("yt_ids.list","r")
	data = file.read()
	link_list = data.split("\n")
	file.close()
	for i in range(len(link_list)-1):
		empty_link = empty_link + link_list[i]+","
	await ctx.channel.send(empty_link[:-1] +"\n Clear the queue if videos are super old using '!clearQ'")

@bot.command(name='clearQ', help='Clears YouTube queue')
async def clearQ(ctx):
	os.system("mv yt_ids.list yt_ids.bk")
	os.system("touch yt_ids.list")
	await ctx.channel.send("Cleared!")


bot.run(bot_cred['token'])
