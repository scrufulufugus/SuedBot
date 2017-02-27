from isAllowed import *


api = strawpoll.API()


class Strawpoll():

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, help=helpText['strawpoll'][1], brief=helpText['strawpoll'][0])
    async def strawpoll(self, ctx):
        """Strawpoll parent command."""
        if False:
            await self.bot.say(notallowed)
            return
        elif ctx.invoked_subcommand is None:
            await self.bot.say("Please use `strawpoll help` to see how to use this command properly.")

    @strawpoll.command(pass_context=True, aliases=['push', 'make'])
    async def post(self, ctx):
        raw = ctx.message.content.split(' ', 2)[2]
        nameStuff = raw.split('\n')
        nameOf = nameStuff[0]
        toMulti = False
        if nameStuff[-1].lower() in ['true', 'false', 'multi']:
            toMulti = {'true': True, 'false': False, 'multi': True}\
                [nameStuff[-1].lower()]
            del(nameStuff[-1])
        del(nameStuff[0])
        tick = 0
        while True:
            try:
                toSub = strawpoll.Poll(nameOf, nameStuff, multi=toMulti)
                break
            except TypeError:
                tick += 1
                if tick == 4:
                    await self.bot.say("The bot broke.")
                    return

        await api.submit_poll(toSub)
        await self.bot.say('<%s>' % toSub.url)

    @strawpoll.command(pass_context=True, aliases=['get', 'results'])
    async def pull(self, ctx):
        raw = ctx.message.content.split(' ', 2)[2]
        # idPost = raw.split('http://www.strawpoll.me/')[0][0:8]
        # await self.bot.say(idPost)
        results = await api.get_poll(raw)
        await self.bot.say(results.results())


def setup(bot):
    bot.add_cog(Strawpoll(bot))
