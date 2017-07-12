from isAllowed import *


steam.api.key.set(tokens['Steam'])
wolfClient = wolframalpha.Client(tokens['Wolfram'])
# r_e = praw.Reddit(user_agent="A post searcher for a Discord user.")
imgurUsr = ImgurClient(tokens['ImgurClient'], tokens['ImgurSecret'])


def getSteamIDFromURL(urlInQuestion):
    print("    Converting vanity url...")
    van = steam.user.vanity_url(urlInQuestion)
    van = van.id64
    return van


def steamGameGetter(userIdentity):
    print("    Getting user's games...")
    games = interface('IPlayerService').GetOwnedGames(
        steamid=userIdentity, include_appinfo=1, aggressive=True)
    x = []
    for i in games['response']['games']:
        x.append(i['name'])
    return x


def steamUserComparison(listOfUserGames):
    a = len(listOfUserGames) - 2
    b = 1
    t = list(set(listOfUserGames[0]).intersection(listOfUserGames[b]))
    while a > 0:
        b += 1
        t = list(set(t).intersection(listOfUserGames[b]))
        a -= 1
    return t


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


class Search():

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, description='Compares the games that you and any number of given Steam users have.',aliases=['sc'])
    async def steamcompare(self, ctx):
        edit = await self.bot.say(waitmessage)
        print("Comparing Steam users.")
        try:
            users = ctx.message.content.split(' ', 1)[1].split(" ")
        except IndexError:
            await self.bot.edit_message(edit, "Please enter two or more profile URLs.")
            return
        users2 = []
        for i in users:
            aye = i.split("/")
            if aye[-1] == "":
                aye = aye[-2]
            else:
                aye = aye[-1]
            try:
                int(aye)
            except ValueError:
                try:
                    aye = getSteamIDFromURL(i)
                except steam.user.VanityError:
                    await self.bot.edit_message(edit, "User {} does not exist".format(i))
                    return
            users2.append(aye)
        if len(users2) <= 1:
            await self.bot.edit_message(edit, "Please enter two or more profile URLs.")
            return
        for i in users2:
            print("    ID :: %s" % i)
        x = []
        for i in users2:
            x.append(steamGameGetter(i))
        z = steamUserComparison(x)
        z.sort()
        v = "You have these games in common :: \n```"
        for i in z:
            v += "* %s\n" % i
        v = v[:-1] + '```'
        print("    Done.")
        if len(v) > 2000:
            await self.bot.edit_message(edit, "This message would be over 2000 characters.")
            return
        await self.bot.edit_message(edit, v)

    @commands.command(pass_context=True, description='Returns the result of a Google search.', aliases=['sg'])
    async def searchgoogle(self, ctx):
        edit = await self.bot.say(waitmessage)
        try:
            query = ctx.message.content.split(' ', 1)[1]
        except IndexError:
            await self.bot.say("Please enter a search query.")
            return
        print("Searching Google :: %s" % query)
        for i in search(query):
            await self.bot.edit_message(edit, i)
            return

    @commands.command(pass_context=True, description='Gives info on the mentioned user.')
    async def info(self, ctx):
        mea = ctx.message
        try:
            u = mea.mentions[0]
        except IndexError:
            await self.bot.say("You need to mention a user in your message.")
            return

        z = u.avatar_url if u.avatar_url != None else u.default_avatar_url
        a = discord.Embed(color=0xDEADBF)
        a.set_author(name=str(u), icon_url=z)
        s = {
             'Username' : u.name,
             'Discriminator' : u.discriminator,
             'Display Name' : u.display_name if u.display_name != None else u.name,
             'ID' : u.id,
             'Bot' : u.bot,
             'Created' : str(u.created_at)[:-10],
             'Account Age' : str(datetime.datetime.now() - u.created_at).split(",")[0],
             'Server Age' : str(datetime.datetime.now() - u.joined_at).split(",")[0],
             'Roles' : ', '.join([g.name for g in u.roles][1:])
             }
        for i in s:
            if s[i] == '':
                s[i] = 'None'
            a.add_field(name=i, value='{}'.format(s[i]), inline=True)

        await self.bot.say(z, embed=a)
        print("Giving info on user :: %s" % mea.content.split(' ', 1)[1])


    @commands.command(pass_context=True, description='Searches Wolfram Alpha.', enabled=False, hidden=True)
    async def wolfram(self, ctx):
        edit = await self.bot.say(waitmessage)
        message = ctx.message
        print("Getting query to Wolfram :: %s" %
              message.content.split(' ', 1)[1])
        res = wolfClient.query(message.content.split(' ', 1)[1])
        print("    Sent and recieved.")
        # try:
        a = "```\n"
        for pod in res.pods:
            try:
                a += pod.text + "\n"
            except TypeError:
                pass
        a = a + "```"
        if a == "```\n```":
            a = "```Could not find any results for this query.```"
        print("    Result ::")
        x = a[3:-3]
        print('        ', end="")
        for i in x:
            if i == "\n":
                i = '\n        '
            print(i, end="")

        q = 0
        z = ''
        for pod in res.pods:
            # await self.bot.say(pod.main)
            z = z + pod.img + '\n'
            q += 1
            # if q == 4: break

        await self.bot.edit_message(edit, z)
        return

    @commands.command(pass_context=True, description='Searches Wikipedia for a given string.', aliases=['wp'])
    async def wiki(self, ctx):
        edit = await self.bot.say(waitmessage)
        searchTerm = ctx.message.content.split(' ', 1)[1]
        try:
            page = wikipedia.page(searchTerm)
            await bot.edit_message(edit, "**%s**\n```%s```\n'%s'" % (page.title, wikipedia.summary(searchTerm, sentences=10), page.url))
        except wikipedia.exceptions.DisambiguationError:
            page = wikipedia.search(searchTerm)
            toPost = ''
            for i in page:
                toPost = toPost + '* %s\n' % i
            toPost = '```%s```' % toPost[:-1]
            await self.bot.edit_message(edit, "Please specify ::\n%s" % toPost)
        except Exception as e:
            await self.bot.edit_message(exit, "Unknown error. Please alert {}.\n\n```\n{}```".format(discord.Object("141231597155385344").mention, str(repr(e))))
        return


    @commands.command(pass_context=True, description='Searches a subreddit for a query.', enabled=False, hidden=True)
    async def sr(self, ctx):
        edit = await self.bot.say(waitmessage)
        mes = ctx.message.content
        sub = mes.split(" ")[1]
        try:
            que = mes.split(' ', 2)[2]
        except IndexError:
            await self.bot.edit_message(edit, "Please provide a subreddit/query.")
            return

        try:
            search = r_e.search(que, subreddit=r_e.get_subreddit(sub))
            ret = []
            for i in search:
                ret.append(i)
                break
            ret = ret[0]
            rUrl = ret.url
            # if 'imgur' in rUrl.lower():
            #     rUrl = imgurAlbumToItems(rUrl)
            await self.bot.edit_message(edit, '**%s**\n%s' % (ret.title, rUrl))

        except praw.errors.InvalidSubreddit:
            await bot.edit_message(edit, "That subreddit does not exist.")
        except IndexError:
            await self.bot.edit_message(edit, "There are no results for this search term.")
        return

    @commands.command(pass_context=True, description='Returns the result of a Imgur search.', aliases=['si'])
    async def searchimgur(self, ctx):
        edit = await self.bot.say(waitmessage)
        query = ctx.message.content.split(' ', 1)[1]
        if query == '':
            await self.bot.edit_message(edit, "Please provide a search term.")
            return

        print("Searching Imgur :: %s" % query)
        for i in imgurUsr.gallery_search(query, sort='viral'):
            await self.bot.edit_message(edit, '**%s**\n%s' % (i.title, imgurAlbumToItems(i)))
            # await self.bot.edit_message(edit, '**%s**\n%s' % (i.title, i.url))
            return

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
    bot.add_cog(Search(bot))
