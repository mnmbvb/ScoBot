''' ScoBot [0.01]
With StrangeCodeTeam'''

import discord, asyncio, requests, random, socket
from discord import *
from discord.ext import commands
from datetime import datetime
from ip2geotools.databases.noncommercial import DbIpCity
import xml.etree.ElementTree as ET
#---------------------------------------------
client = discord.Client()
token = ''
version = '0.01'
p = ';'
#---------------------------------------------
@client.event
async def on_ready():
  print('ScoBot online!')
  await bt([';help, ;도움', f'스코봇 {version}'])
async def bt(games):
  await client.wait_until_ready()
  while not client.is_closed():
    for g in games:
      await client.change_presence(status = discord.Status.online, activity = discord.Game(g))
      await asyncio.sleep(5)
#---------------------------------------------
@client.event
async def on_message(message):
  if message.author.bot:
      return None

  if message.content == f'{p}help' or message.content == f'{p}도움':
    embed=discord.Embed(title="ScoBot 도움말", description=f"ver {version}", color=0x00d9ff)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="도움", value="```;help / ;도움```", inline=False)
    embed.add_field(name="1 Page", value="```스코봇 명령어들의 설명을 볼 수 있어요.```", inline=False)
    embed.add_field(name="2 Page", value="```스코봇 테스트 전용 명령어들이에요.```", inline=False)
    embed.add_field(name="3 Page", value="```스코봇 관리 명령어들이에요.```", inline=False)
    embed.add_field(name=";hmd", value="```전체 명령어 목록을 불러와요.```", inline=True)
    embed.set_footer(text=f"ScoBot {version} with StrangeCodeTeam")
    msg = await message.channel.send(embed=embed)
    page = ['1️⃣', '2️⃣', '3️⃣']
    for r in page:
      await msg.add_reaction(r)
    def check(reaction, user):
            return str(reaction) in page and user == message.author and reaction.message.id == msg.id
    try:
          reaction, _user = await client.wait_for("reaction_add", check=check, timeout=15)
    except asyncio.TimeoutError:
            pass
    else:
      if str(reaction) == '1️⃣':
        embed=discord.Embed(title="ScoBot 도움말", description="스코봇의 명령어들이에요.", color=0x0098b3)
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.set_footer(text="1 Page")
        embed.add_field(name=";랜덤", value="```설정한 수 범위 사이의 무작위 수를 출력해요.```", inline=False)
        embed.add_field(name=";time, ;시간", value="```현재 시간을 나타내요.```", inline=False)
        embed.add_field(name=";날씨", value="```기상청의 예상 온도를 불러와요.(Beta)```", inline=False)
        await msg.edit(embed=embed)

      if str(reaction) == '2️⃣':
        embed=discord.Embed(title="스코봇 Help", description="스코봇 테스트 전용 명령어들이에요.", color=0x62c1cc)
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.set_footer(text="2 Page")
        embed.add_field(name=";주사위", value="```1~6의 랜덤 수를 출력해요.```", inline=False)
        embed.add_field(name=";time, ;시간", value="```현재 시간을 나타내요.```", inline=False)
        embed.add_field(name=";tts", value="```입력된 메세지를 tts로 읽어줘요.```", inline=False)
        embed.add_field(name=";타자연습", value="```타자연습을 진행해요. (0.2 신규 업데이트!)```", inline=False)
        await msg.edit(embed=embed)

      else:
        pass
      return
  
  if message.content == f'{p}시간' or message.content == f';time':
    t_kr = datetime.now()
    t_kr = t_kr.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')
    t_utc = datetime.utcnow()
    t_utc = t_utc.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')
    embed=discord.Embed(title='현재시간 :clock3:', description='표준 시간대, 대한민국의 시간이에요.', color=0x62c1cc)
    embed.add_field(name='표준 시간대(UTC)', value=(f'```{t_utc}```'), inline=False)
    embed.add_field(name='대한민국(UTC+9)', value=(f'```{t_kr}```'), inline=False)
    embed.set_footer(text=f"ScoBot {version} with StrangeCodeTeam")
    await message.channel.send(embed=embed)

  if message.content == f'{p}날씨':
    api_url='http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2823753000'
    weather_data = requests.get(api_url).text
    xml_data = ET.fromstring(weather_data)
    time_list = []
    temp_list = []
    for tag in xml_data.iter("data"):
        time1 = (tag.find("hour").text)
        temp1 = (tag.find("temp").text)
        time_list.append(time1)
        temp_list.append(temp1)

    embed=discord.Embed(title="스코봇 날씨정보 Beta", description="기상청 동네예보 웹서비스 - 인천광역시 부평구 부평3동", color=0x62c1cc)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/846738919444709376/899656330447556658/368e507125ff2f24.png")
    embed.set_footer(text=f"ScoBot {version} with StrangeCodeTeam")
    a = 1
    while (a<16):
      embed.add_field(name=f"{time_list[a]}시", value=f"{temp_list[a]}°C", inline=True)
      a += 1
    await message.channel.send(embed=embed)

  if message.content == f"{p}타자연습":
    scotaja=0
    embed=discord.Embed(title="스코봇 타자연습", color=0x000000)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="3초 후 10회의 타자게임을 시작합니다.", value=f"10초 안에 해당 문장을 적어주세요. / 종료하기 위해선 아무 말이나 적어주세요.", inline=False)
    channel = message.channel
    msg1 = await message.channel.send(embed=embed)
    await asyncio.sleep(3)
    while scotaja < 11:
      f = open('ScoBot\\Source\\Typing.txt', 'rt', encoding='UTF8')
      randomLine = random.choice(list(f.readlines())).splitlines()[0]
      embed=discord.Embed(title="스코봇 타자연습", description="아래 문장을 적어주세요!", color=0x000000)
      embed.add_field(name=f"{randomLine}", value=f"ScoBot {version} with StrangeCodeTeam", inline=False)
      await message.channel.send(embed=embed)
      def check(m):
        return m.author == message.author and m.channel == channel
      try:
        msg2 = await client.wait_for('message', timeout=10.0, check=check)
      except asyncio.TimeoutError:
        embed=discord.Embed(title="스코봇 타자연습", color=0x000000)
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.add_field(name="타자게임 종료", value=f"10초의 시간제한이 끝났습니다! 다시 도전해주세요!", inline=False)
        await message.channel.send(embed=embed)
        return
      else:
        bot_prov=str(randomLine)
        user_prov=str(msg2.content)
        anwser = ""
        if bot_prov == user_prov:
          if scotaja == 10:
            await message.channel.send(":star: 타자연습 완료! :star:")
            break
          else:
            await message.channel.send("맞았습니다!")
            msg2 = 'empty'
            scotaja += 1
        else:
          embed=discord.Embed(title="스코봇 타자연습", color=0x000000)
          embed.set_thumbnail(url=client.user.avatar_url)
          embed.add_field(name="타자게임 종료", value="틀렸습니다! 다시 도전해주세요!", inline=False)
          await message.channel.send(embed=embed)
          scotaja += 55
    f.close()

  if message.content.startswith(f"{p}ping"):
    url = message.content.split(' ')[1]
    ip = socket.gethostbyname(url)
    response = DbIpCity.get(ip, api_key='free')
    embed=discord.Embed(title=f'{url}', description='핑 결과', color=0x37ff00)
    embed.add_field(name='IP', value=f'{ip}', inline=False)
    embed.add_field(name='국가', value=f'{response.country}', inline=False)
    embed.add_field(name='지역', value=f'{response.region}', inline=False)
    embed.add_field(name='도시', value=f'{response.country}', inline=False)
    embed.set_footer(text=f'ScoBot {version} with StrangeCodeTeam')
    await message.channel.send(embed=embed)

  if message.content == f'{p}ping':
    embed=discord.Embed(title='ScoBot ping', description=str(client.latency*1000)[0:6] + 'ms', color=0x37ff00)
    await message.channel.send(embed=embed)
client.run(token)