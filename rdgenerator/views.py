import io
from pathlib import Path
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
import os
import secrets
import re
import requests
import base64
import json
import uuid
import pyzipper
from django.conf import settings as _settings
from django.db.models import Q
from .forms import GenerateForm
from .models import GithubRun
from PIL import Image
from urllib.parse import quote

def generator_view(request):
    if request.method == 'POST':
        form = GenerateForm(request.POST, request.FILES)
        if form.is_valid():
            user_secret = form.cleaned_data['sh_secret_field']
            if _settings.SH_SECRET == user_secret:
                selfhosted = True
            else:
                selfhosted = False
            platform = form.cleaned_data['platform']
            version = form.cleaned_data['version']

            # Validate: Windows builds cannot use 'master' version (NuGet requires valid version string)
            if platform in ('windows', 'windows-x86') and version == 'master':
                return render(request, 'failure.html', {
                    'error': 'Windows 版本不支持使用 nightly(master) 构建，请选择 1.4.8 或更高版本。'
                })

            delayFix = form.cleaned_data['delayFix']
            cycleMonitor = form.cleaned_data['cycleMonitor']
            xOffline = form.cleaned_data['xOffline']
            hidecm = form.cleaned_data['hidecm']
            removeNewVersionNotif = form.cleaned_data['removeNewVersionNotif']
            server = form.cleaned_data['serverIP']
            key = form.cleaned_data['key']
            apiServer = form.cleaned_data['apiServer']
            urlLink = form.cleaned_data['urlLink']
            downloadLink = form.cleaned_data['downloadLink']
            if not server:
                server = 'rs-ny.rustdesk.com' #default rustdesk server
            if not key:
                key = 'OeVuKk5nlHiXp+APNn0Y3pC1Iwpwn44JGqrQCsWqmBw=' #default rustdesk key
            if not apiServer:
                apiServer = server+":21114"
            if not urlLink:
                urlLink = "https://rustdesk.com"
            if not downloadLink:
                downloadLink = "https://rustdesk.com/download"
            direction = form.cleaned_data['direction']
            autoReconnect = form.cleaned_data['autoReconnect']
            disableAudio = form.cleaned_data['disableAudio']
            disableClipboard = form.cleaned_data['disableClipboard']
            disableFileTransfer = form.cleaned_data['disableFileTransfer']
            disableRemoteRestart = form.cleaned_data['disableRemoteRestart']
            disableRecording = form.cleaned_data['disableRecording']
            enableBluetooth = form.cleaned_data['enableBluetooth']
            enableTcpTunneling = form.cleaned_data['enableTcpTunneling']
            useRendezvousSignature = form.cleaned_data['useRendezvousSignature']
            customFps = form.cleaned_data['customFps']
            disableOpenGL = form.cleaned_data['disableOpenGL']
            removeToolbox = form.cleaned_data['removeToolbox']
            removeNewVersionButton = form.cleaned_data['removeNewVersionButton']
            disableChat = form.cleaned_data['disableChat']
            disableSessionReuse = form.cleaned_data['disableSessionReuse']
            autoRecordIncoming = form.cleaned_data['autoRecordIncoming']
            autoRecordOutgoing = form.cleaned_data['autoRecordOutgoing']
            enableUdpPunch = form.cleaned_data['enableUdpPunch']
            disableUdp = form.cleaned_data['disableUdp']
            enableIpv6 = form.cleaned_data['enableIpv6']
            https = form.cleaned_data['https']
            websocket = form.cleaned_data['websocket']
            alwaysSoftwareRender = form.cleaned_data['alwaysSoftwareRender']
            allowLogonScreenPassword = form.cleaned_data['allowLogonScreenPassword']
            numericOneTimePassword = form.cleaned_data['numericOneTimePassword']
            allowOnlyConnOpen = form.cleaned_data['allowOnlyConnOpen']
            trustedDevices = form.cleaned_data['trustedDevices']
            autoUpdate = form.cleaned_data['autoUpdate']
            hwcodec = form.cleaned_data['hwcodec']
            abr = form.cleaned_data['abr']
            directXCapture = form.cleaned_data['directXCapture']
            secureCommunication = form.cleaned_data['secureCommunication']
            language = form.cleaned_data['language']

            allowHideRemoteWindow = form.cleaned_data['allowHideRemoteWindow']
            enableTray = form.cleaned_data['enableTray']
            oneWayClipboard = form.cleaned_data['oneWayClipboard']
            oneWayFileTransfer = form.cleaned_data['oneWayFileTransfer']
            disableTransferPause = form.cleaned_data['disableTransferPause']
            disableTemporaryPassword = form.cleaned_data['disableTemporaryPassword']
            allowOverrideCursor = form.cleaned_data['allowOverrideCursor']
            allowBlockInput = form.cleaned_data['allowBlockInput']
            allowLockScreenAfterDisconnect = form.cleaned_data['allowLockScreenAfterDisconnect']
            allowAutoRecord = form.cleaned_data['allowAutoRecord']
            allowAutoDisconnect = form.cleaned_data['allowAutoDisconnect']
            allowRejectSessions = form.cleaned_data['allowRejectSessions']
            allowRejectInverse = form.cleaned_data['allowRejectInverse']
            allowReportClipboard = form.cleaned_data['allowReportClipboard']
            allowWaitForAdmission = form.cleaned_data['allowWaitForAdmission']
            allowCaptureScreen = form.cleaned_data['allowCaptureScreen']
            allowScreenshot = form.cleaned_data['allowScreenshot']
            allowVoiceCall = form.cleaned_data['allowVoiceCall']
            allowInputEvents = form.cleaned_data['allowInputEvents']
            allowClipboardSync = form.cleaned_data['allowClipboardSync']
            allowFileDrop = form.cleaned_data['allowFileDrop']
            allowPointer = form.cleaned_data['allowPointer']
            allowWindowDrag = form.cleaned_data['allowWindowDrag']
            allowIdleInhibit = form.cleaned_data['allowIdleInhibit']
            proxyUrl = form.cleaned_data['proxyUrl']
            proxyUsername = form.cleaned_data['proxyUsername']
            proxyPassword = form.cleaned_data['proxyPassword']
            relayServer = form.cleaned_data['relayServer']
            whitelist = form.cleaned_data['whitelist']
            directServer = form.cleaned_data['directServer']
            directAccessPort = form.cleaned_data['directAccessPort']
            hideSecurity = form.cleaned_data['hideSecurity']
            hideNetwork = form.cleaned_data['hideNetwork']
            hideServer = form.cleaned_data['hideServer']
            hideProxy = form.cleaned_data['hideProxy']
            hideWebsocket = form.cleaned_data['hideWebsocket']
            hideRemotePrinter = form.cleaned_data['hideRemotePrinter']
            hideTray = form.cleaned_data['hideTray']
            hideHelpCards = form.cleaned_data['hideHelpCards']
            hideUsernameOnCard = form.cleaned_data['hideUsernameOnCard']
            hideStopService = form.cleaned_data['hideStopService']
            d3dRender = form.cleaned_data['d3dRender']
            textureRender = form.cleaned_data['textureRender']
            enableFileCopyPaste = form.cleaned_data['enableFileCopyPaste']
            enableConfirmClosingTabs = form.cleaned_data['enableConfirmClosingTabs']
            enablePrivacyMode = form.cleaned_data['enablePrivacyMode']
            enableLanDiscovery = form.cleaned_data['enableLanDiscovery']
            viewOnly = form.cleaned_data['viewOnly']
            lockAfterSessionEnd = form.cleaned_data['lockAfterSessionEnd']
            showRemoteCursor = form.cleaned_data['showRemoteCursor']
            followRemoteCursor = form.cleaned_data['followRemoteCursor']
            followRemoteWindow = form.cleaned_data['followRemoteWindow']
            reverseMouseWheel = form.cleaned_data['reverseMouseWheel']
            swapLeftRightMouse = form.cleaned_data['swapLeftRightMouse']
            zoomCursor = form.cleaned_data['zoomCursor']
            mainWindowAlwaysOnTop = form.cleaned_data['mainWindowAlwaysOnTop']
            touchMode = form.cleaned_data['touchMode']
            trackpadSpeed = form.cleaned_data['trackpadSpeed']
            peerCardUiType = form.cleaned_data['peerCardUiType']
            peerSorting = form.cleaned_data['peerSorting']
            displayName = form.cleaned_data['displayName']
            codecPreference = form.cleaned_data['codecPreference']
            verificationMethod = form.cleaned_data['verificationMethod']
            disableChangeID = form.cleaned_data['disableChangeID']
            disableDiscoveryPanel = form.cleaned_data['disableDiscoveryPanel']
            disableChangePermanentPassword = form.cleaned_data['disableChangePermanentPassword']
            disableUnlockPin = form.cleaned_data['disableUnlockPin']
            registerDevice = form.cleaned_data['registerDevice']
            syncInitClipboard = form.cleaned_data['syncInitClipboard']
            syncABTags = form.cleaned_data['syncABTags']
            syncABWithRecent = form.cleaned_data['syncABWithRecent']
            removePresetPasswordWarning = form.cleaned_data['removePresetPasswordWarning']
            filterABByIntersection = form.cleaned_data['filterABByIntersection']
            enablePermChangeInAcceptWindow = form.cleaned_data['enablePermChangeInAcceptWindow']
            presetAddressBookName = form.cleaned_data['presetAddressBookName']
            enableAndroidSoftwareEncodingHalfScale = form.cleaned_data['enableAndroidSoftwareEncodingHalfScale']
            showVirtualJoystick = form.cleaned_data['showVirtualJoystick']
            showVirtualMouse = form.cleaned_data['showVirtualMouse']
            allowRemoveWallpaper = form.cleaned_data['allowRemoveWallpaper']
            videoSaveDirectory = form.cleaned_data['videoSaveDirectory']
            lang = form.cleaned_data['lang']
            enableChangeID = form.cleaned_data['enableChangeID']
            allowCommandLineSettings = form.cleaned_data['allowCommandLineSettings']
            allowLinuxHeadless = form.cleaned_data['allowLinuxHeadless']
            allowInsecureTLSFallback = form.cleaned_data['allowInsecureTLSFallback']
            allowHttps21114 = form.cleaned_data['allowHttps21114']
            installation = form.cleaned_data['installation']
            settings = form.cleaned_data['settings']
            appname = form.cleaned_data['appname']
            if not appname:
                appname = "rustdesk"
            filename = form.cleaned_data['exename']
            compname = form.cleaned_data['compname']
            if not compname:
                compname = "Purslane Ltd"
            androidappid = form.cleaned_data['androidappid']
            if not androidappid:
                androidappid = "com.carriez.flutter_hbb"
            compname = compname.replace("&","\\&")
            permPass = form.cleaned_data['permanentPassword']
            theme = form.cleaned_data['theme']
            themeDorO = form.cleaned_data['themeDorO']
            #runasadmin = form.cleaned_data['runasadmin']
            passApproveMode = form.cleaned_data['passApproveMode']
            denyLan = form.cleaned_data['denyLan']
            enableDirectIP = form.cleaned_data['enableDirectIP']
            #ipWhitelist = form.cleaned_data['ipWhitelist']
            autoClose = form.cleaned_data['autoClose']
            permissionsDorO = form.cleaned_data['permissionsDorO']
            permissionsType = form.cleaned_data['permissionsType']
            enableKeyboard = form.cleaned_data['enableKeyboard']
            enableClipboard = form.cleaned_data['enableClipboard']
            enableFileTransfer = form.cleaned_data['enableFileTransfer']
            enableAudio = form.cleaned_data['enableAudio']
            enableTCP = form.cleaned_data['enableTCP']
            enableRemoteRestart = form.cleaned_data['enableRemoteRestart']
            enableRecording = form.cleaned_data['enableRecording']
            enableBlockingInput = form.cleaned_data['enableBlockingInput']
            enableRemoteModi = form.cleaned_data['enableRemoteModi']
            removeWallpaper = form.cleaned_data['removeWallpaper']
            defaultManual = form.cleaned_data['defaultManual']
            overrideManual = form.cleaned_data['overrideManual']
            enablePrinter = form.cleaned_data['enablePrinter']
            enableCamera = form.cleaned_data['enableCamera']
            enableTerminal = form.cleaned_data['enableTerminal']

            if all(char.isascii() for char in filename):
                filename = re.sub(r'[^\w\s-]', '_', filename).strip()
                filename = filename.replace(" ","_")
            else:
                filename = "rustdesk"
            if not all(char.isascii() for char in appname):
                appname = "rustdesk"
            myuuid = str(uuid.uuid4())
            protocol = _settings.PROTOCOL
            host = request.get_host()
            # --- Fix: Port in URL for setup / download-zip
            # --- protocol = _settings.PROTOCOL
            # --- host = request.get_host()
            # --- full_url = f"{protocol}://{host}"
            full_url = _settings.GENURL if _settings.GENURL else f"{_settings.PROTOCOL}://{request.get_host()}"
            try:
                iconfile = form.cleaned_data.get('iconfile')
                if not iconfile:
                    iconfile = form.cleaned_data.get('iconbase64')
                iconlink_url, iconlink_uuid, iconlink_file = save_png(iconfile,myuuid,full_url,"icon.png")
            except:
                print("failed to get icon, using default")
                iconlink_url = "false"
                iconlink_uuid = "false"
                iconlink_file = "false"
            try:
                logofile = form.cleaned_data.get('logofile')
                if not logofile:
                    logofile = form.cleaned_data.get('logobase64')
                logolink_url, logolink_uuid, logolink_file = save_png(logofile,myuuid,full_url,"logo.png")
            except:
                print("failed to get logo")
                logolink_url = "false"
                logolink_uuid = "false"
                logolink_file = "false"
            try:
                privacyfile = form.cleaned_data.get('privacyfile')
                if not privacyfile:
                    privacyfile = form.cleaned_data.get('privacybase64')
                privacylink_url, privacylink_uuid, privacylink_file = save_png(privacyfile,myuuid,full_url,"privacy.png")
            except:
                print("failed to get logo")
                privacylink_url = "false"
                privacylink_uuid = "false"
                privacylink_file = "false"

            ###create the custom.txt json here and send in as inputs below
            decodedCustom = {}
            if direction != "Both":
                decodedCustom['conn-type'] = direction
            if installation == "installationN":
                decodedCustom['disable-installation'] = 'Y'
            if settings == "settingsN":
                decodedCustom['disable-settings'] = 'Y'
            if appname.upper != "rustdesk".upper and appname != "":
                decodedCustom['app-name'] = appname
            decodedCustom['override-settings'] = {}
            decodedCustom['default-settings'] = {}
            if permPass != "":
                decodedCustom['password'] = permPass
            if theme != "system":
                if themeDorO == "default":
                    if platform == "windows-x86":
                        decodedCustom['default-settings']['allow-darktheme'] = 'Y' if theme == "dark" else 'N'
                    else:
                        decodedCustom['default-settings']['theme'] = theme
                elif themeDorO == "override":
                    if platform == "windows-x86":
                        decodedCustom['override-settings']['allow-darktheme'] = 'Y' if theme == "dark" else 'N'
                    else:
                        decodedCustom['override-settings']['theme'] = theme
            decodedCustom['enable-lan-discovery'] = 'N' if denyLan else 'Y'
            #decodedCustom['direct-server'] = 'Y' if enableDirectIP else 'N'
            decodedCustom['allow-auto-disconnect'] = 'Y' if autoClose else 'N'
            if permissionsDorO == "default":
                decodedCustom['default-settings']['access-mode'] = permissionsType
                decodedCustom['default-settings']['enable-keyboard'] = 'Y' if enableKeyboard else 'N'
                decodedCustom['default-settings']['enable-clipboard'] = 'Y' if enableClipboard else 'N'
                decodedCustom['default-settings']['enable-file-transfer'] = 'Y' if enableFileTransfer else 'N'
                decodedCustom['default-settings']['enable-audio'] = 'Y' if enableAudio else 'N'
                decodedCustom['default-settings']['enable-tunnel'] = 'Y' if enableTCP else 'N'
                decodedCustom['default-settings']['enable-remote-restart'] = 'Y' if enableRemoteRestart else 'N'
                decodedCustom['default-settings']['enable-record-session'] = 'Y' if enableRecording else 'N'
                decodedCustom['default-settings']['enable-block-input'] = 'Y' if enableBlockingInput else 'N'
                decodedCustom['default-settings']['allow-remote-config-modification'] = 'Y' if enableRemoteModi else 'N'
                decodedCustom['default-settings']['direct-server'] = 'Y' if enableDirectIP else 'N'
                decodedCustom['default-settings']['verification-method'] = 'use-permanent-password' if hidecm else 'use-both-passwords'
                decodedCustom['default-settings']['approve-mode'] = passApproveMode
                decodedCustom['default-settings']['allow-hide-cm'] = 'Y' if hidecm else 'N'
                decodedCustom['default-settings']['allow-remove-wallpaper'] = 'Y' if removeWallpaper else 'N'
                decodedCustom['default-settings']['enable-remote-printer'] = 'Y' if enablePrinter else 'N'
                decodedCustom['default-settings']['enable-camera'] = 'Y' if enableCamera else 'N'
                decodedCustom['default-settings']['enable-terminal'] = 'Y' if enableTerminal else 'N'
            else:
                decodedCustom['override-settings']['access-mode'] = permissionsType
                decodedCustom['override-settings']['enable-keyboard'] = 'Y' if enableKeyboard else 'N'
                decodedCustom['override-settings']['enable-clipboard'] = 'Y' if enableClipboard else 'N'
                decodedCustom['override-settings']['enable-file-transfer'] = 'Y' if enableFileTransfer else 'N'
                decodedCustom['override-settings']['enable-audio'] = 'Y' if enableAudio else 'N'
                decodedCustom['override-settings']['enable-tunnel'] = 'Y' if enableTCP else 'N'
                decodedCustom['override-settings']['enable-remote-restart'] = 'Y' if enableRemoteRestart else 'N'
                decodedCustom['override-settings']['enable-record-session'] = 'Y' if enableRecording else 'N'
                decodedCustom['override-settings']['enable-block-input'] = 'Y' if enableBlockingInput else 'N'
                decodedCustom['override-settings']['allow-remote-config-modification'] = 'Y' if enableRemoteModi else 'N'
                decodedCustom['override-settings']['direct-server'] = 'Y' if enableDirectIP else 'N'
                decodedCustom['override-settings']['verification-method'] = 'use-permanent-password' if hidecm else 'use-both-passwords'
                decodedCustom['override-settings']['approve-mode'] = passApproveMode
                decodedCustom['override-settings']['allow-hide-cm'] = 'Y' if hidecm else 'N'
                decodedCustom['override-settings']['allow-remove-wallpaper'] = 'Y' if removeWallpaper else 'N'
                decodedCustom['override-settings']['enable-remote-printer'] = 'Y' if enablePrinter else 'N'
                decodedCustom['override-settings']['enable-camera'] = 'Y' if enableCamera else 'N'
                decodedCustom['override-settings']['enable-terminal'] = 'Y' if enableTerminal else 'N'

            for line in defaultManual.splitlines():
                k, value = line.split('=')
                decodedCustom['default-settings'][k.strip()] = value.strip()

            for line in overrideManual.splitlines():
                k, value = line.split('=')
                decodedCustom['override-settings'][k.strip()] = value.strip()
            
            decodedCustomJson = json.dumps(decodedCustom)

            string_bytes = decodedCustomJson.encode("ascii")
            base64_bytes = base64.b64encode(string_bytes)
            encodedCustom = base64_bytes.decode("ascii")

            # #github limits inputs to 10, so lump extras into one with json
            # extras = {}
            # extras['genurl'] = _settings.GENURL
            # #extras['runasadmin'] = runasadmin
            # extras['urlLink'] = urlLink
            # extras['downloadLink'] = downloadLink
            # extras['delayFix'] = 'true' if delayFix else 'false'
            # extras['rdgen'] = 'true'
            # extras['cycleMonitor'] = 'true' if cycleMonitor else 'false'
            # extras['xOffline'] = 'true' if xOffline else 'false'
            # extras['removeNewVersionNotif'] = 'true' if removeNewVersionNotif else 'false'
            # extras['compname'] = compname
            # extras['androidappid'] = androidappid
            # extra_input = json.dumps(extras)

            ####from here run the github action, we need user, repo, access token.
            if platform == 'windows':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows.yml/dispatches'
                if selfhosted:
                    url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/sh-generator-windows.yml/dispatches'
            if platform == 'windows-x86':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows-x86.yml/dispatches'
            elif platform == 'linux':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-linux.yml/dispatches'
            elif platform == 'android':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-android.yml/dispatches'
            elif platform == 'macos':
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-macos.yml/dispatches'
            else:
                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows.yml/dispatches'
                if selfhosted:
                    url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/sh-generator-windows.yml/dispatches'

            #url = 'https://api.github.com/repos/'+_settings.GHUSER+'/rustdesk/actions/workflows/test.yml/dispatches'  
            inputs_raw = {
                "server":server,
                "key":key,
                "apiServer":apiServer,
                "custom":encodedCustom,
                "uuid":myuuid,
                "iconlink_url":iconlink_url,
                "iconlink_uuid":iconlink_uuid,
                "iconlink_file":iconlink_file,
                "logolink_url":logolink_url,
                "logolink_uuid":logolink_uuid,
                "logolink_file":logolink_file,
                "privacylink_url":privacylink_url,
                "privacylink_uuid":privacylink_uuid,
                "privacylink_file":privacylink_file,
                "appname":appname,
                "genurl":_settings.GENURL,
                "urlLink":urlLink,
                "downloadLink":downloadLink,
                "delayFix": 'true' if delayFix else 'false',
                "rdgen":'true',
                "cycleMonitor": 'true' if cycleMonitor else 'false',
                "xOffline": 'true' if xOffline else 'false',
                "removeNewVersionNotif": 'true' if removeNewVersionNotif else 'false',
                "compname": compname,
                "androidappid":androidappid,
                "filename":filename
            }

            temp_json_path = f"data_{uuid.uuid4()}.json"
            zip_filename = f"secrets_{uuid.uuid4()}.zip"
            zip_path = "temp_zips/%s" % (zip_filename)
            Path("temp_zips").mkdir(parents=True, exist_ok=True)

            with open(temp_json_path, "w") as f:
                json.dump(inputs_raw, f)

            with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(_settings.ZIP_PASSWORD.encode())
                zf.write(temp_json_path, arcname="secrets.json")

            if os.path.exists(temp_json_path):
                os.remove(temp_json_path)

            zipJson = {}
            zipJson['url'] = full_url
            zipJson['file'] = zip_filename

            zip_url = json.dumps(zipJson)

            data = {
                "ref":_settings.GHBRANCH,
                "inputs":{
                    "version":version,
                    "zip_url":zip_url
                },
                "return_run_details": True
            } 
            #print(data)
            headers = {
                'Accept':  'application/vnd.github+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+_settings.GHBEARER,
                'X-GitHub-Api-Version': '2026-03-10'
            }
            new_github_run = GithubRun(
                uuid=myuuid,
                status="Starting generator...please wait"
            )
            try:
                response = requests.post(url, json=data, headers=headers)
                #print(response)
                if response.status_code == 204 or response.status_code == 200:
                    github_data = {}
                    if response.status_code == 200:
                        try:
                            github_data = response.json()
                        except Exception:
                            pass
                    new_github_run.github_run_id = github_data.get('workflow_run_id')
                    new_github_run.status = "in_progress"
                    new_github_run.save()

                    log_url = github_data.get('html_url', '')

                    # AJAX: return JSON so the page can show an inline build card
                    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                        return JsonResponse({
                            'uuid': myuuid,
                            'platform': platform,
                            'filename': filename,
                            'status': 'started',
                            'log_url': log_url,
                        })

                    return render(request, 'waiting.html', {'filename':filename, 'uuid':myuuid, 'status':"Starting generator...please wait", 'platform':platform, 'log_url': log_url})
                else:
                    #new_github_run.delete()
                    return JsonResponse({"error": "GitHub rejected the start request (status %d)" % response.status_code}, status=500)
            except Exception as e:
                #new_github_run.delete()
                return JsonResponse({"error": f"Connection error: {str(e)}"}, status=500)
    else:
        form = GenerateForm()
    #return render(request, 'maintenance.html')
    return render(request, 'generator.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from django.db.models import Q

def check_for_file(request):
    filename = request.GET.get('filename')
    uuid = request.GET.get('uuid')
    platform = request.GET.get('platform')
    gh_run = get_object_or_404(GithubRun, uuid=uuid)
    github_log_url = f"https://github.com/{_settings.GHUSER}/{_settings.REPONAME}/actions/runs/{gh_run.github_run_id}"

    if gh_run.status not in ['success', 'failure', 'cancelled', 'timed_out', 'skipped']:
        headers = {
            "Authorization": f"Bearer {_settings.GHBEARER}",
            "Accept": "application/vnd.github+json"
        }
        api_url = f"https://api.github.com/repos/{_settings.GHUSER}/{_settings.REPONAME}/actions/runs/{gh_run.github_run_id}"
        
        try:
            gh_response = requests.get(api_url, headers=headers)
            if gh_response.status_code == 200:
                gh_data = gh_response.json()
                
                if gh_data['status'] == 'completed':
                    gh_run.status = gh_data['conclusion']
                    gh_run.save()
        except Exception as e:
            print(f"Error checking GitHub: {e}")
    
    if gh_run.status == "success":
        return render(request, 'generated.html', {
            'filename': filename, 
            'uuid': uuid, 
            'platform': platform
        })
        
    elif gh_run.status in ['failure', 'cancelled', 'timed_out', 'skipped', 'action_required']:
        return render(request, 'failure.html', {
            'log_url': github_log_url, 
            'filename': filename, 
            'uuid': uuid, 
            'platform': platform,
            'status': gh_run.status
        })
        
    else:
        return render(request, 'waiting.html', {
            'filename': filename, 
            'uuid': uuid, 
            'status': gh_run.status, 
            'platform': platform, 
            'log_url': github_log_url
        })



def build_status_json(request):
    uuid = request.GET.get('uuid')
    if not uuid:
        return JsonResponse({'error': 'missing uuid'}, status=400)
    try:
        gh_run = GithubRun.objects.get(uuid=uuid)
    except GithubRun.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)

    platform = request.GET.get('platform', '')
    filename = request.GET.get('filename', '')

    # Refresh status from GitHub if not terminal
    if gh_run.status not in ['success', 'failure', 'cancelled', 'timed_out', 'skipped', 'action_required']:
        if gh_run.github_run_id:
            headers = {
                "Authorization": f"Bearer {_settings.GHBEARER}",
                "Accept": "application/vnd.github+json"
            }
            api_url = f"https://api.github.com/repos/{_settings.GHUSER}/{_settings.REPONAME}/actions/runs/{gh_run.github_run_id}"
            try:
                gh_response = requests.get(api_url, headers=headers)
                if gh_response.status_code == 200:
                    gh_data = gh_response.json()
                    if gh_data.get('status') == 'completed':
                        gh_run.status = gh_data['conclusion']
                        gh_run.save()
            except Exception as e:
                print(f"Error checking GitHub: {e}")

    log_url = ''
    if gh_run.github_run_id:
        log_url = f"https://github.com/{_settings.GHUSER}/{_settings.REPONAME}/actions/runs/{gh_run.github_run_id}"

    downloads = []
    if gh_run.status == 'success':
        base = f"/download?uuid={uuid}&filename="
        # Scan actual files in exe/<uuid>/ directory
        exe_dir = os.path.join('exe', uuid)
        if os.path.isdir(exe_dir):
            for f in sorted(os.listdir(exe_dir)):
                if os.path.isfile(os.path.join(exe_dir, f)):
                    downloads.append({'name': f, 'url': f'{base}{f}'})
        # Fallback: if directory is empty or doesn't exist, use expected names
        if not downloads:
            if platform in ('windows', 'windows-x86'):
                downloads.append({'name': f'{filename}.exe', 'url': f'{base}{filename}.exe'})
            elif platform == 'linux':
                for ext in ('x86_64.deb','aarch64.deb','x86_64.rpm','suse-x86_64.rpm',
                            'aarch64.rpm','suse-aarch64.rpm','x86_64.pkg.tar.zst',
                            'aarch64.pkg.tar.zst','x86_64.AppImage','aarch64.AppImage',
                            'x86_64.flatpak','aarch64.flatpak'):
                    name = f'{filename}-{ext}'
                    downloads.append({'name': name, 'url': f'{base}{name}'})
            elif platform == 'android':
                for ext in ('aarch64.apk','x86_64.apk','armv7.apk'):
                    name = f'{filename}-{ext}'
                    downloads.append({'name': name, 'url': f'{base}{name}'})
            elif platform == 'macos':
                for ext in ('x86_64.dmg','aarch64.dmg'):
                    name = f'{filename}-{ext}'
                    downloads.append({'name': name, 'url': f'{base}{name}'})

    return JsonResponse({
        'status': gh_run.status,
        'platform': platform,
        'filename': filename,
        'log_url': log_url,
        'downloads': downloads,
    })
def download(request):
    filename = request.GET['filename']
    uuid = request.GET['uuid']
    file_path = os.path.join('exe', uuid, filename)
    with open(file_path, 'rb') as file:
        content = file.read()
    response = HttpResponse(content, headers={
        'Content-Type': 'application/vnd.microsoft.portable-executable',
        'Content-Disposition': f'attachment; filename="{filename}"'
    })
    return response

def get_png(request):
    filename = request.GET['filename']
    uuid = request.GET['uuid']
    #filename = filename+".exe"
    file_path = os.path.join('png',uuid,filename)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, headers={
            'Content-Type': 'application/vnd.microsoft.portable-executable',
            'Content-Disposition': f'attachment; filename="{filename}"'
        })

    return response

def create_github_run(myuuid):
    new_github_run = GithubRun(
        uuid=myuuid,
        status="Starting generator...please wait"
    )
    new_github_run.save()

def update_github_run(request):
    data = json.loads(request.body)
    myuuid = data.get('uuid')
    mystatus = data.get('status')
    GithubRun.objects.filter(Q(uuid=myuuid)).update(status=mystatus)
    return HttpResponse('')

def resize_and_encode_icon(imagefile):
    maxWidth = 200
    try:
        with io.BytesIO() as image_buffer:
            for chunk in imagefile.chunks():
                image_buffer.write(chunk)
            image_buffer.seek(0)

            img = Image.open(image_buffer)
            imgcopy = img.copy()
    except (IOError, OSError):
        raise ValueError("Uploaded file is not a valid image format.")

    # Check if resizing is necessary
    if img.size[0] <= maxWidth:
        with io.BytesIO() as image_buffer:
            imgcopy.save(image_buffer, format=imagefile.content_type.split('/')[1])
            image_buffer.seek(0)
            return_image = ContentFile(image_buffer.read(), name=imagefile.name)
        return base64.b64encode(return_image.read())

    # Calculate resized height based on aspect ratio
    wpercent = (maxWidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))

    # Resize the image while maintaining aspect ratio using LANCZOS resampling
    imgcopy = imgcopy.resize((maxWidth, hsize), Image.Resampling.LANCZOS)

    with io.BytesIO() as resized_image_buffer:
        imgcopy.save(resized_image_buffer, format=imagefile.content_type.split('/')[1])
        resized_image_buffer.seek(0)

        resized_imagefile = ContentFile(resized_image_buffer.read(), name=imagefile.name)

    # Return the Base64 encoded representation of the resized image
    resized64 = base64.b64encode(resized_imagefile.read())
    #print(resized64)
    return resized64
 
#the following is used when accessed from an external source, like the rustdesk api server
def startgh(request):
    #print(request)
    data_ = json.loads(request.body)
    ####from here run the github action, we need user, repo, access token.
    url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-'+data_.get('platform')+'.yml/dispatches'  
    data = {
        "ref": _settings.GHBRANCH,
        "inputs":{
            "server":data_.get('server'),
            "key":data_.get('key'),
            "apiServer":data_.get('apiServer'),
            "custom":data_.get('custom'),
            "uuid":data_.get('uuid'),
            "iconlink":data_.get('iconlink'),
            "logolink":data_.get('logolink'),
            "appname":data_.get('appname'),
            "extras":data_.get('extras'),
            "filename":data_.get('filename')
        }
    } 
    headers = {
        'Accept':  'application/vnd.github+json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+_settings.GHBEARER,
        'X-GitHub-Api-Version': '2026-03-10'
    }
    response = requests.post(url, json=data, headers=headers)
    print(response)
    return HttpResponse(status=204)

def save_png(file, uuid, domain, name):
    file_save_path = "png/%s/%s" % (uuid, name)
    Path("png/%s" % uuid).mkdir(parents=True, exist_ok=True)

    if isinstance(file, str):  # Check if it's a base64 string
        try:
            header, encoded = file.split(';base64,')
            decoded_img = base64.b64decode(encoded)
            file = ContentFile(decoded_img, name=name) # Create a file-like object
        except ValueError:
            print("Invalid base64 data")
            return None  # Or handle the error as you see fit
        except Exception as e:  # Catch general exceptions during decoding
            print(f"Error decoding base64: {e}")
            return None
        
    with open(file_save_path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)
    # imageJson = {}
    # imageJson['url'] = domain
    # imageJson['uuid'] = uuid
    # imageJson['file'] = name
    #return "%s/%s" % (domain, file_save_path)
    return domain, uuid, name

def save_custom_client(request):
    file = request.FILES['file']
    myuuid = request.POST.get('uuid')
    file_save_path = "exe/%s/%s" % (myuuid, file.name)
    Path("exe/%s" % myuuid).mkdir(parents=True, exist_ok=True)
    with open(file_save_path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)

    return HttpResponse("File saved successfully!")

def cleanup_secrets(request):
    # Pass the UUID as a query param or in JSON body
    data = json.loads(request.body)
    my_uuid = data.get('uuid')
    
    if not my_uuid:
        return HttpResponse("Missing UUID", status=400)

    # 1. Find the files in your temp directory matching the UUID
    temp_dir = os.path.join('temp_zips')
    
    # We look for any file starting with 'secrets_' and containing the uuid
    for filename in os.listdir(temp_dir):
        if my_uuid in filename and filename.endswith('.zip'):
            file_path = os.path.join(temp_dir, filename)
            try:
                os.remove(file_path)
                print(f"Successfully deleted {file_path}")
            except OSError as e:
                print(f"Error deleting file: {e}")

    return HttpResponse("Cleanup successful", status=200)

def get_zip(request):
    filename = request.GET['filename']
    #filename = filename+".exe"
    file_path = os.path.join('temp_zips',filename)
    with open(file_path, 'rb') as file:
        response = HttpResponse(file, headers={
            'Content-Type': 'application/vnd.microsoft.portable-executable',
            'Content-Disposition': f'attachment; filename="{filename}"'
        })

    return response


