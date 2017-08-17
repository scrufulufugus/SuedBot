from isAllowed import *


# Start up some logging for debugging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='%sbot.log' %
                              workingDirectory, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# Create the bot
description = '''SuedBot:\nThe ultimate evolution in bot technology'''
bot = commands.Bot(command_prefix=['.', "<@{}>".format(tokens['discordID'])], description=description, pm_help=True)


# Create all of the tokens and keys
discordToken = tokens['discord']
mashapeKey = {"X-Mashape-Key":
              tokens['Mashape']}
htmlHead = {'Accept-Endoding': 'identity'}
youtubeData = yapi.YoutubeAPI(tokens['YoutubeData'])

# Set the paths
mainPath = os.path.dirname(os.path.realpath(__file__))
addonsPath = mainPath + \
    "addons/"

# Make the bot more unicode-friendly
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


# This uses the imgur API to convert an album into a list of links
def imgurAlbumToItems(albumLink):
    if type(albumLink) == str:
        imgObj = imgurUsr.get_album_images(albumLink)
        ret = ''
        for i in imgObj:
            ret = ret + i.link + '\n'
        ret = ret[:-1]
    elif albumLink.is_album:
        imgObj = imgurUsr.get_album_images(albumLink.id)
        ret = ''
        for i in imgObj:
            ret = ret + i.link + '\n'
        ret = ret[:-1]
    else:
        ret = albumLink.link
    return ret
    
    
@bot.event
async def on_member_join(member):
    server = member.server
    i = giveAllowances(server)
    if i['Joins']['Channel'] != '':
        server = discord.Object(i['Joins']['Channel'])
    if i['Joins']['Enabled'] == 'True':
        fmt = i['Joins']['Text'].replace('{mention}',member.mention).replace('{name}',member.name)
        await bot.send_message(server, fmt)


@bot.event
async def on_member_ban(member):
    server = member.server
    i = giveAllowances(server)
    if i['Bans']['Channel'] != '':
        server = discord.Object(i['Bans']['Channel'])
    if i['Bans']['Enabled'] == 'True':
        fmt = i['Bans']['Text'].replace('{mention}',member.mention).replace('{name}',member.name)
        await bot.send_message(server, fmt)


@bot.event
async def on_member_remove(member):
    server = member.server
    i = giveAllowances(server)
    if i['Leaves']['Channel'] != '':
        server = discord.Object(i['Leaves']['Channel'])
    if i['Leaves']['Enabled'] == 'True':
        fmt = i['Leaves']['Text'].replace('{mention}',member.mention).replace('{name}',member.name)
        await bot.send_message(server, fmt)


@bot.event
async def on_channel_update(before, after):
    i = giveAllowances(after.server)
    toSay = []

    if i['ChannelUpdates']['Enabled'] != 'True':
        return

    if before.name != after.name:
        # This will run if the channel's name changed
        toSay = toSay + ["This channel's name was changed from `{0.name}` to `{1.name}`".format(before, after)]
    if before.topic != after.topic:
        # This will run if the chanenl's topic changed
        if before.topic in [None, '', ' ']: before.topic = '[None]'
        if after.topic in [None, '', ' ']: after.topic = '[None]'
        toSay = toSay + ["This channel's topic was changed from `{0.topic}` to `{1.topic}`".format(before, after)]

    await bot.send_message(after, '\n\n'.join(toSay))


@bot.event
async def on_server_update(before, after):
    i = giveAllowances(after)
    toSay = []

    if i['ServerUpdates']['Enabled'] != 'True':
        return

    server = after
    if i['ServerUpdates']['Channel'] != '':
        server = discord.Object(i['ServerUpdates']['Channel'])

    if before.name != after.name:
        # This runs if the server's name has changed
        toSay = toSay + ["This server's name changed from `{0.name}` to `{1.name}`".format(before, after)]
    if before.icon_url != after.icon_url:
        # This runs if the icon has changed
        bef = '`[None]`' if before.icon_url in [None, '', ' '] else '<{}>'.format(before.icon_url)
        aft = '`[None]`' if after.icon_url in [None, '', ' '] else '<{}>'.format(after.icon_url)
        toSay = toSay + ["This server's icon changed from {0} to {1}".format(bef, aft)]

    await bot.send_message(server, '\n\n'.join(toSay))


@bot.event
async def on_ready():
    print("----------")
    print("Logged in as:")
    print("    " + str(bot.user.name))
    print("    " + str(bot.user.id))
    with open(workingDirectory+'game.txt') as a:
        gameThingy = a.read()
    await bot.change_presence(game=discord.Game(name=gameThingy))
    print("Game changed to '%s'." % gameThingy)

    try:
        with open(workingDirectory + 'restartFile.txt', 'r') as a:
            cha = discord.Object(id=a.readlines()[0])
        await bot.send_message(cha, "\"I'm back, you subnormal halfwit!\"")
        os.remove(workingDirectory + 'restartFile.txt')
    except FileNotFoundError:
        pass

    startup_extensions = []
    for i in os.listdir(mainPath):
        if i.startswith('addon_'):
            startup_extensions.append(i[:-3])
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    print("----------")


@bot.event
async def on_message(message):

    if message.author.bot:
        return

    z = {
        'weed':'🌿',
        'blaze':'🔥',
        'nice':'👌',
        'weed.':'🌿',
        'blaze.':'🔥',
        'nice.':'👌'
    }
    try:
        await bot.add_reaction(message, z[message.content.lower()])
    except:
        pass
    if message.content.lower() in ('kill me', 'kill me.', '*kill me*'):
        await bot.send_message(message.channel, '{} *Later*'.format(str(message.author.mention)))
        
    # The people on my server are idiots.
    if message.content.lower().startswith('+volume') and message.server.id == '178070516353990657':
        num = message.content.split(' ')[1]
        try:
            if int(num) > 100:
                await bot.send_message(message.channel, "+volume 100")
        except:
            pass

    # Get custom commands
    continueWithComms = True
    aq = giveAllowances(message.server.id)

    # Read custom commands
    try:
        with open(serverConfigs + message.server.id + '.json', 'r', encoding='utf-8') as data_file:
            customCommands = json.load(data_file)['CustomCommands']

        try:
            await bot.send_message(message.channel, eval(customCommands[message.content.lower()]).translate(non_bmp_map))
            continueWithComms = False
        except KeyError:
            pass
    except KeyError:
        pass
    except FileNotFoundError:
        pass

    # Read Imgur album into images
    if 'imgur.com/' in message.content and aq['ImgurAlbum']['Enabled'] == 'True':
        print('yee')
        if 'imgur.com/a/' in message.content:
            imLink = message.content.split('imgur.com/a/')[1][:5]
        elif 'imgur.com/gallery/' in message.content:
            imLink = message.content.split('imgur.com/gallery/')[1][:5]
        try:
            imLink = imgurAlbumToItems(imLink)
            x = [message.author.mention] + [i for i in imLink.split('\n')]
            y = z = ''
            while True:
                if x == []:
                    break 
                y = z + x[0] + '\n'
                if len(y) > 2000:
                    await bot.send_message(message.channel, z)
                    y = z = ''
                else:
                    z = y 
                    del x[0]
            # await bot.send_message(message.channel, '{}\n{}'.format(message.author.mention, imLink))
        except UnboundLocalError:
            pass

    if continueWithComms:
        await bot.process_commands(message)

bot.run(discordToken)