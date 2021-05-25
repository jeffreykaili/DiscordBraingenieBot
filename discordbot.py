import discord 
from discord.ext import commands 
from selenium import webdriver
from PIL import Image
import time

bot = commands.Bot(command_prefix='!!')
bot.remove_command('help')

option = webdriver.ChromeOptions()
option.add_argument('headless')
dr = webdriver.Chrome("C:/Users/16479/Desktop/BraingenieBot/chromedriver.exe",options=option)
dr.set_window_size(1920, 1080)

@bot.command()
async def solve(ctx, url, *param):
	cache = {}
	# print(param)
	dr.get(url)
	time.sleep(1)
	for i in range(100):  
		question = dr.find_elements_by_xpath('//*[@id="new_student_problem_record"]/div')
		questiontext = ""
		for x in question:
			questiontext += x.text 
		if(questiontext in cache): continue 

		dr.save_screenshot("problem.png")
		# x: 470 --> 1500 
		# y: 65 --> 800 
		if "enlarge" not in param: 
			image = Image.open("problem.png")
			image = image.crop((470, 65, 1500, 800))
			image.save('problem.png')

		await ctx.send(questiontext)
		await ctx.send(file = discord.File(r'C:/Users/16479/Desktop/BraingenieBot/problem.png')) # path to the folder 
		dr.find_element_by_xpath('//*[@id="practiceTabSubmit"]').click()
		time.sleep(1)

		# If you want the plain text of the solution
		if("print" in param): 
			solution = dr.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div/div[3]/div')
			solutiontext = ""
			for x in solution:
				solutiontext += x.text 
			await ctx.send(solutiontext)
		cache[questiontext] = 1
	
		dr.save_screenshot("solution.png")
		# x: 630 --> 1290 
		# y: 290 --> 785 
		if "enlarge" not in param: 
			image = Image.open("solution.png")
			image = image.crop((620, 180, 1300, 920))
			image.save('solution.png')

		await ctx.send(file = discord.File(r'C:/Users/16479/Desktop/BraingenieBot/solution.png')) # path to the folder 
		time.sleep(3)
		dr.refresh()
		time.sleep(1)
	await ctx.send("**FINISHED**")

@bot.event
async def on_ready():
	print("Bot active!")

bot.run('')