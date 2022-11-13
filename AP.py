# import module
import os
import subprocess
 
# function to establish a new connection
def createNewConnection(name, SSID, password):
    config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>"""+name+"""</name>
    <SSIDConfig>
        <SSID>
            <name>"""+SSID+"""</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>"""+password+"""</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
    with open(name+".xml", 'w') as file:
        file.write(config)
    os.system(command)
 
# function to connect to a network   
def connect(name, SSID):
    #command = "netsh interface set interface name=\"Wi-Fi\" admin=disabled"
    #os.system(command)
    #command = "./WlanScan.exe"
    #os.system(command)
    subprocess.call("WlanScan.exe", stdin=None, stdout=None, stderr=None, shell=False)
    command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
    return os.system(command)

