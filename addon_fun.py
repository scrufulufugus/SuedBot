from isAllowed import *


mashapeKey = {"X-Mashape-Key":
              tokens['Mashape']}
htmlHead = {'Accept-Endoding': 'identity'}
owm = OWM(tokens['OwmKey'])
owm = OWM(API_key=tokens['OwmKey'], version='2.5')
owm_en = OWM()
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)


def txtFileToList(nameOfFile):
    nameOfFile = addonFiles + nameOfFile + '.txt'
    file = open(nameOfFile, 'r', encoding="utf-8")
    fileContent = file.read()
    file.close()
    fileContent = fileContent.split("\n")
    return fileContent


def randFromList(listThing):
    return listThing[random.randint(0, len(listThing) - 1)]


class Fun():


    def __init__(self, bot):
        self.bot = bot


    @commands.group()
    async def aes(self):
        pass


    @aes.command(pass_context=True, description='Makes your string into a coolio thingmie.')
    async def sq(self, ctx, *, message : str):
        a = message
        for i in a:
            if i == '\n':
                return self.bot.say("Please have your word on one line.")
        ret = []
        length = len(a)
        temp = ''
        spa = ' ' * (((len(a) - 1) * 2) - 1)
        for i in a:
            temp = temp + i + ' '
        temp = temp[:-1]
        ret.append(temp)
        temp = ''
        for i in range(1, length - 1, 1):
            temp = a[i] + spa + a[length - i - 1]
            ret.append(temp)

        temp = ''
        for i in a[::-1]:
            temp = temp + i + ' '
        ret.append(temp)

        acRet = '```\n'
        for i in ret:
            acRet += i + '\n'
        acRet += '```'

        if len(acRet) > 2000:
            await self.bot.say("Please shorten your input string.")
            return

        print('Aes command :: %s' % a)

        await self.bot.say(acRet)


    @commands.command(pass_context=True, description='Gives you a random picture of a cat.',aliases=['kitty','kitten','kittycat','kittykat','cittycat','kittykit'])
    async def cat(self, ctx):
        try:
            await self.bot.add_reaction(ctx.message, '👀')
            edit = None
        except:
            edit = await self.bot.say(waitmessage)

        while True:
            try:
                page = requests.get('http://thecatapi.com/api/images/get?format=src')
                break
            except:
                pass
        print("Got a cat picture :: %s" % page.url)
        await self.bot.say(page.url + ' :3') if edit == None else await self.bot.edit_message(edit, page.url + ' :3')


    @commands.command(pass_context=True, description='Prints out some Skyrim guard text.')
    async def guard(self, ctx):
        msg = randFromList(txtFileToList("skyrimText"))
        print("Spat out guard dialogue :: %s" % msg)
        await self.bot.say(msg)


    @commands.command(pass_context=True, aliases=['complement', 'complements', 'compliments'], description='Prints out some Skyrim guard text.')
    async def compliment(self, ctx):
        with open(addonFiles + "complements.txt") as a:
            es = a.read()
        es = es.split('\n')
        msg = randFromList(es)
        print("Spat out complement :: %s" % msg)
        await self.bot.say(msg)


    @commands.command(pass_context=True, description='Gives the lenny face.')
    async def lenny(self, ctx):
        try:
            await self.bot.delete_message(ctx.message)
        except:
            pass
        await self.bot.say("( ͡° ͜ʖ ͡°)")


    @aes.command(pass_context=True)
    async def sp(self, ctx, *, message : str):
        ret = '```\n'
        if '\n' in ctx.message.content:
            await self.bot.say("Please only use one line in your input.")
            return
        toAlt = list(message)
        for i in range(0, 4):
            for o in toAlt:
                ret = ret + o + ' ' * i
            ret = ret + '\n'
        for i in range(2, -1, -1):
            for o in toAlt:
                ret = ret + o + ' ' * i
            ret = ret + '\n'
        ret = ret + '```'
        if len(ret) > 2000:
            await self.bot.say("Please shorten your input string.")
            return
        await self.bot.say(ret)


    @commands.command(pass_context=True, description='Gives you love, gives you life.')
    async def love(self, ctx, *, message : str):
        a = message
        if a == '':
            p = "What do you love?"
        else:
            a = "%s is love, %s is life." % (a, a)
            print("This guy is love :: %s" %(a))
            p = a
        await self.bot.say(p)


    @commands.command(pass_context=True, aliases=['joke'], description='Gives a random pin from punoftheday.com.')
    async def pun(self, ctx):
        try:
            await self.bot.add_reaction(ctx.message, '👀')
            edit = None
        except:
            edit = await self.bot.say(waitmessage)

        page = requests.get('http://www.punoftheday.com/cgi-bin/randompun.pl',
                            headers=htmlHead)
        out = page.text.split('dropshadow1')[1][6:].split('<')[0]
        print("Said a pun :: %s" % out)
        await self.bot.say(out) if edit == None else await self.bot.edit_message(edit, out)


    @commands.command(pass_context=True, description='')
    async def weather(self, ctx, *, message : str = ''):
        placeName = message
        if placeName == '':
            await self.bot.say("Please provide a location to check the weather of.")
            return

        try:
            await self.bot.add_reaction(ctx.message, '👀')
            edit = None
        except:
            edit = await self.bot.say(waitmessage)

        weatherAtPlace = owm.weather_at_place(placeName)
        weath = weatherAtPlace.get_weather()
        wea_wind = weath.get_wind()['speed']  # mph
        wea_temp = weath.get_temperature(unit='celsius')['temp']
        wea_gene = weath.get_status()

        try:
            wea_gene = {'Clouds': 'Cloudy'}[wea_gene]
        except KeyError:
            pass

        ret = 'Weather in **%s**\n```\nWeather     :: %s\nTemperature :: %sC\nWindspeed   :: %smph```' % (
            weatherAtPlace.get_location().get_name(), wea_gene, wea_temp, wea_wind)

        await self.bot.say(ret) if edit == None else await self.bot.edit_message(edit, ret)


    @commands.command(pass_context=True, description='Gives the look of disapproval.')
    async def disapprove(self, ctx):
        await self.bot.say("ಠ_ಠ")

    @commands.command(pass_context=True, description='Evaluates the given codeset.')
    async def ev(self, ctx, *, toEx):
        server = ctx.message.server 
        author = ctx.message.author 
        channel = ctx.message.channel
        if 'sys' in toEx.lower() and 'exit' in toEx.lower():
            await self.bot.say("Nice try, asshole.")
            return
        try:
            out = eval(toEx)
        except Exception as e:
            out = str(repr(e))

        await self.bot.say(out)


    @commands.group(pass_context=True, description='Turns binary into ascii and vice versa')
    async def binary(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("Please use `help binary` to see how to use this command properly.")


    @binary.command(pass_context=True, name='tobinary', aliases=['tonumbers','fromtext','fromascii'])
    async def toBinary(self, ctx, *, text : str):
        letters = list(text)
        binary = []
        for i in letters:
            binary.append('{0:08b}'.format(ord(i)))
        out = 'That text in binary is \n```'
        for i in binary:
            out = out + i + ' '
        out = out[:-1] + '```'
        await self.bot.say(out)


    @binary.command(pass_context=True, name='totext', aliases=['frombinary','toascii','fromnumbers'])
    async def toAscii(self, ctx, *, text : str):
        if len(text.split(' ')) > 1:
            binary = text.split(' ')
        else:
            binary = [text[i:i + 8] for i in range(0, len(text), 8)]

        out = 'That text in ASCII is \n```'
        for i in binary:
            out = out + chr(int(i, 2))
        out = out + '```'

        await self.bot.say(out)


    @commands.command(pass_context=True)
    async def mc(self, ctx, character : str = None):
        if character != None:
            pass
        else:
            await self.bot.say("Please provide a Minecraft username.")
            return

        returnString = "https://mcapi.ca/skin/2d/%s/85/false" % character
        await self.bot.say(returnString)


    @commands.command(pass_context=True)
    async def meme(self, ctx, *, message : str = None):
        if message == None:
            await self.bot.say("Please give an image and top/bottom text.")
            return
        spl = message.split('\n')

        url = spl[0].replace(' ', '')
        try:
            topText = spl[1].replace(
                '-', '--').replace('_', '__').replace(' ', '-').replace('?', '~q')
        except IndexError:
            await self.bot.say("You can't leave the top or bottom blank.")
            return
        try:
            botText = spl[2].replace(
                '-', '--').replace('_', '__').replace(' ', '-').replace('?', '~q')
        except IndexError:
            await self.bot.say("You can't leave the top or bottom blank.")
            return

        cont = False
        for i in ['.png', '.jpg', '.jpeg']:
            if url.lower().endswith(i):
                cont = True
        if not cont:
            await self.bot.say("The URL provided for the meme was not retrieved successfully.")
            return

        try:
            await self.bot.delete_message(ctx.message)
        except:
            pass
        await self.bot.say("{} http://memegen.link/custom/{}/{}.jpg?alt={}".format(
            ctx.message.author.mention,
            topText,
            botText,
            url))


    @commands.command(pass_context=True)
    async def big(self, ctx, *, toReplace : str):
        toReplace = toReplace.lower()
        qw = ''
        zzz = {}
        zz = 0
        for z in 'abcdefghijklmnopqrstuvwxyz':
            zzz[z] = '🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿'[zz]
            zz += 1
        for o in toReplace:
            if o in 'abcdefghijklmnopqrstuvwxyz':
                # o = ":regional_indicator_{}: ".format(o)
                o = '{} '.format(zzz[o])
            if o == ' ':
                o = " ▫ "
            if o in '01236456789':
                o = ':' + humanize.apnumber(int(o)) + ': '
            qw = qw + o
        await self.bot.say(qw.replace(':0:',':zero:'))


    @commands.command(pass_context=True)
    async def time(self, ctx):
        time = str(datetime.datetime.now()).split(' ',1)[1][:-7]
        await self.bot.say('The current time, in GMT, is `{}`'.format(time))


    @commands.command(pass_context=True)
    async def insult(self, ctx):
        try:
            await self.bot.add_reaction(ctx.message, '👀')
            edit = None
        except:
            edit = await self.bot.say(waitmessage)

        page = requests.get('http://www.insultgenerator.org/')
        con = page.content
        insult = con[431:-742]
        toOut = str(insult)[2:-1]
        await self.bot.say(toOut) if edit == None else await self.bot.edit_message(edit, toOut)


    @commands.command(pass_context=True)
    async def jpeg(self, ctx):
        quality = 5
        message = ctx.message.content
        if len(message.split(' ')) > 2:
            quality = int(message.split(' ',2)[1])
            message = message.split(' ',2)[2]
        try:
            urlretrieve(message, 'jpegTEMP.jpg')
        except:
            await self.bot.say("I couldn't get that image rip")
            return
        im = Image.open('jpegTEMP.jpg')
        im.save('jpegTEMP.jpg', "JPEG", quality=quality)
        im.close()
        with open("jpegTEMP.jpg", "rb") as a:
            await self.bot.send_file(ctx.message.channel, a)


    @commands.command(pass_context=True, description='Gives the lenny face.')
    async def urban(self, ctx, *, message : str):
        try:
            await self.bot.add_reaction(ctx.message, '👀')
            edit = None
        except:
            edit = await self.bot.say(waitmessage)

        try:
            x = urbandictionary.define(message)[0]
        except:
            await self.bot.say("There were no definitions for `{}`.".format(message))
            return
        y = "`{}` :: {}".format(x.word, x.definition)
        await self.bot.say(y) if edit == None else await self.bot.edit_message(edit, y)


def setup(bot):
    bot.add_cog(Fun(bot))
