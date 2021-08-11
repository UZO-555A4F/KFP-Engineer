import io
from PIL import Image
import requests
from discord.ext import commands
from discord import User, File
from common.MemberUtil import MemberUtil
from common.SuperChatUtil import SuperChatUtil
from common.NicknameUtil import NicknameUtil

class SuperChatMeme(commands.Cog):
    # Color = [
    #     "BLUE",
    #     "CYAN",
    #     "LIGHTBLUE",
    #     "MAGENTA",
    #     "ORANGE",
    #     "RED",
    #     "YELLOW",
    #     "RANDOM"
    # ]

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='sc', invoke_without_command=True)
    async def superchat_group(self, ctx: commands.Context, sc_money: int, user: User, sc_msg: str):
        sc_color = "RANDOM"
        # money 0 just for test
        if sc_money == 0:
            sc_color = "RED"
        elif sc_money < 15:
            await ctx.send("至少15硬幣才能使用SuperChat!\n")
            return
        else:
            SuperChatMeme._getColor(sc_money)

        # check author have enough coins or not
        giver = MemberUtil.get_or_add_member(ctx.author.id)
        if giver.coin < sc_money:
            await ctx.send("硬幣不足!快去店外雜談區聊天賺硬幣!")
            return
        adder = MemberUtil.get_or_add_member(user.id)

        # transaction
        MemberUtil.add_coin(member_id=giver.id, amount=-sc_money)
        MemberUtil.add_coin(member_id=adder, amount=sc_money)

        # create image
        avatar = self.downloadUserAvatar(ctx.author)
        imgPath = SuperChatUtil.createSC(ctx.author.name, avatar, sc_money, sc_msg, sc_color)

        img = File(imgPath, filename="result.png")
        await ctx.send(f"感謝{ctx.author.name}給{user.name}的SuperChat!")
        await ctx.send(file=img)

    @superchat_group.command(name="help")
    async def show_help_msg(self, ctx: commands.Command):
        msg = "歡迎大家使用SuperChat功能! 使用方法如下:\n"
        msg += "!sc <硬幣數量> <使用者> <文字> 給該使用者多少硬幣，後面文字可留言(中間不可有空白)\n"
        msg += "每個等級對應的SuperChat文字輸入上限如下:\n"
        msg += "Coin. 15-29 0字元(無法留言)\n"
        msg += "Coin. 30-74 50字元\n"
        msg += "Coin. 75-149 150字元\n"
        msg += "Coin. 150-299 200字元\n"
        msg += "Coin. 300-749 225字元\n"
        msg += "Coin. 750-1499 250字元\n"
        msg += "Coin. 1500以上 270字元\n"
        msg += "註1:避免洗版，最多只會顯示三行\n"
        msg += "註2:每次SuperChat酌收20%手續費，故該用戶只會收到80%的硬幣\n"
        await ctx.send(msg)

    def downloadUserAvatar(self, user: User):
        avatar_url = user.avatar_url
        data = requests.get(avatar_url).content
        return Image.open(io.BytesIO(data))

    def _getColor(money: int):
        if 15 <= money < 30:
            sc_color = "BLUE"
        elif 30 <= money < 75:
            sc_color = "LIGHTBLUE"
        elif 75 <= money < 150:
            sc_color = "CYAN"
        elif 150 <= money < 300:
            sc_color = "YELLO"
        elif 300 <= money < 750:
            sc_color = "ORANGE"
        elif 750 <= money < 1500:
            sc_color = "MAGENTA"
        else:
            sc_color = "RED"
        return sc_color

def setup(client):
    client.add_cog(SuperChatMeme(client))