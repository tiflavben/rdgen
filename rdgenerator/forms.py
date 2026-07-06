from django import forms
from PIL import Image

class GenerateForm(forms.Form):
    sh_secret_field = forms.CharField(required=False)
    #Platform
    platform = forms.ChoiceField(choices=[('windows','Windows 64位'),('windows-x86','Windows 32位'),('linux','Linux'),('android','Android'),('macos','macOS')], initial='windows')
    version = forms.ChoiceField(choices=[('master','每日构建'),('1.4.8','1.4.8'),('1.4.7','1.4.7'),('1.4.6','1.4.6'),('1.4.5','1.4.5'),('1.4.4','1.4.4'),('1.4.3','1.4.3'),('1.4.2','1.4.2'),('1.4.1','1.4.1'),('1.4.0','1.4.0'),('1.3.9','1.3.9'),('1.3.8','1.3.8'),('1.3.7','1.3.7'),('1.3.6','1.3.6'),('1.3.5','1.3.5'),('1.3.4','1.3.4'),('1.3.3','1.3.3')], initial='1.4.8')
    help_text="'master'（每日构建）是开发版，包含最新特性但可能不稳定'"
    delayFix = forms.BooleanField(initial=True, required=False)

    #General
    exename = forms.CharField(label="Name for EXE file", required=True)
    appname = forms.CharField(label="Custom App Name", required=False)
    direction = forms.ChoiceField(widget=forms.RadioSelect, choices=[
        ('incoming', '仅入站'),
        ('outgoing', '仅出站'),
        ('both', '双向')
    ], initial='both')
    installation = forms.ChoiceField(label="安装设置", choices=[
        ('installationY', '否，启用安装'),
        ('installationN', '是，禁用安装')
    ], initial='installationY')
    settings = forms.ChoiceField(label="设置页面", choices=[
        ('settingsY', '否，启用设置'),
        ('settingsN', '是，禁用设置')
    ], initial='settingsY')
    androidappid = forms.CharField(label="Custom Android App ID (replaces 'com.carriez.flutter_hbb')", required=False)

    #Custom Server
    serverIP = forms.CharField(label="Host", required=False)
    apiServer = forms.CharField(label="API Server", required=False)
    key = forms.CharField(label="Key", required=False)
    urlLink = forms.CharField(label="Custom URL for links", required=False)
    downloadLink = forms.CharField(label="Custom URL for downloading new versions", required=False)
    compname = forms.CharField(label="Company name",required=False)

    #Visual
    iconfile = forms.FileField(label="Custom App Icon (in .png format)", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))
    logofile = forms.FileField(label="Custom App Logo (in .png format)", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))
    privacyfile = forms.FileField(label="Custom privacy screen (in .png format)", required=False, widget=forms.FileInput(attrs={'accept': 'image/png'}))
    iconbase64 = forms.CharField(required=False)
    logobase64 = forms.CharField(required=False)
    privacybase64 = forms.CharField(required=False)
    theme = forms.ChoiceField(choices=[
        ('light', '浅色'),
        ('dark', '深色'),
        ('system', '跟随系统')
    ], initial='system')
    themeDorO = forms.ChoiceField(choices=[('default', '默认'),('override', '覆盖')], initial='default')

    #Security
    passApproveMode = forms.ChoiceField(choices=[('password', '通过密码接受会话'),('click', '通过点击接受会话'),('password-click', '同时支持密码和点击')],initial='password-click')
    permanentPassword = forms.CharField(widget=forms.PasswordInput(), required=False)
    #runasadmin = forms.ChoiceField(choices=[('false','No'),('true','Yes')], initial='false')
    denyLan = forms.BooleanField(initial=False, required=False)
    enableDirectIP = forms.BooleanField(initial=False, required=False)
    #ipWhitelist = forms.BooleanField(initial=False, required=False)
    autoClose = forms.BooleanField(initial=False, required=False)

    #Permissions
    permissionsDorO = forms.ChoiceField(choices=[('default', '默认'),('override', '覆盖')], initial='default')
    permissionsType = forms.ChoiceField(choices=[('custom', '自定义'),('full', '完全访问权限'),('view', '仅屏幕共享')], initial='custom')
    enableKeyboard =  forms.BooleanField(initial=True, required=False)
    enableClipboard = forms.BooleanField(initial=True, required=False)
    enableFileTransfer = forms.BooleanField(initial=True, required=False)
    enableAudio = forms.BooleanField(initial=True, required=False)
    enableTCP = forms.BooleanField(initial=True, required=False)
    enableRemoteRestart = forms.BooleanField(initial=True, required=False)
    enableRecording = forms.BooleanField(initial=True, required=False)
    enableBlockingInput = forms.BooleanField(initial=True, required=False)
    enableRemoteModi = forms.BooleanField(initial=False, required=False)
    hidecm = forms.BooleanField(initial=False, required=False)
    enablePrinter = forms.BooleanField(initial=True, required=False)
    enableCamera = forms.BooleanField(initial=True, required=False)
    enableTerminal = forms.BooleanField(initial=True, required=False)

    #Other
    removeWallpaper = forms.BooleanField(initial=True, required=False)

    defaultManual = forms.CharField(widget=forms.Textarea, required=False)
    overrideManual = forms.CharField(widget=forms.Textarea, required=False)

    #custom added features
    cycleMonitor = forms.BooleanField(initial=False, required=False)
    xOffline = forms.BooleanField(initial=False, required=False)
    removeNewVersionNotif = forms.BooleanField(initial=False, required=False)

    # Recording Settings
    autoRecordIncoming = forms.BooleanField(initial=False, required=False)
    autoRecordOutgoing = forms.BooleanField(initial=False, required=False)

    # Connection Advanced
    enableUdpPunch = forms.BooleanField(initial=True, required=False)
    disableUdp = forms.BooleanField(initial=False, required=False)
    enableIpv6 = forms.BooleanField(initial=False, required=False)
    https = forms.BooleanField(initial=False, required=False)
    websocket = forms.BooleanField(initial=False, required=False)

    # Remote Control Behavior
    alwaysSoftwareRender = forms.BooleanField(initial=False, required=False)
    allowLogonScreenPassword = forms.BooleanField(initial=False, required=False)
    numericOneTimePassword = forms.BooleanField(initial=False, required=False)
    allowOnlyConnOpen = forms.BooleanField(initial=False, required=False)
    trustedDevices = forms.CharField(required=False)

    # Performance
    autoUpdate = forms.BooleanField(initial=False, required=False)
    hwcodec = forms.BooleanField(initial=True, required=False)
    abr = forms.BooleanField(initial=False, required=False)
    directXCapture = forms.BooleanField(initial=False, required=False)
    secureCommunication = forms.BooleanField(initial=False, required=False)
    language = forms.ChoiceField(choices=[('en','English'),('zh','中文'),('fr','Français'),('de','Deutsch')], initial='zh', required=False)

    # UI
    allowHideRemoteWindow = forms.BooleanField(initial=False, required=False)
    enableTray = forms.BooleanField(initial=True, required=False)
    oneWayClipboard = forms.BooleanField(initial=False, required=False)
    oneWayFileTransfer = forms.BooleanField(initial=False, required=False)
    disableTransferPause = forms.BooleanField(initial=False, required=False)
    disableTemporaryPassword = forms.BooleanField(initial=False, required=False)
    allowOverrideCursor = forms.BooleanField(initial=False, required=False)
    allowBlockInput = forms.BooleanField(initial=False, required=False)
    allowLockScreenAfterDisconnect = forms.BooleanField(initial=False, required=False)
    allowAutoRecord = forms.BooleanField(initial=False, required=False)
    allowAutoDisconnect = forms.BooleanField(initial=False, required=False)
    allowRejectSessions = forms.BooleanField(initial=False, required=False)
    allowRejectInverse = forms.BooleanField(initial=False, required=False)
    allowReportClipboard = forms.BooleanField(initial=False, required=False)
    allowWaitForAdmission = forms.BooleanField(initial=True, required=False)
    allowCaptureScreen = forms.BooleanField(initial=False, required=False)
    allowScreenshot = forms.BooleanField(initial=False, required=False)
    allowVoiceCall = forms.BooleanField(initial=False, required=False)
    allowInputEvents = forms.BooleanField(initial=False, required=False)
    allowClipboardSync = forms.BooleanField(initial=False, required=False)
    allowFileDrop = forms.BooleanField(initial=False, required=False)
    allowPointer = forms.BooleanField(initial=False, required=False)
    allowWindowDrag = forms.BooleanField(initial=False, required=False)
    allowIdleInhibit = forms.BooleanField(initial=False, required=False)

    # Proxy Settings
    proxyUrl = forms.CharField(label="Proxy URL", required=False)
    proxyUsername = forms.CharField(label="Proxy Username", required=False)
    proxyPassword = forms.CharField(label="Proxy Password", widget=forms.PasswordInput(), required=False)
    relayServer = forms.CharField(label="Relay Server", required=False)
    
    # Network Advanced
    whitelist = forms.CharField(label="IP Whitelist", required=False)
    directServer = forms.CharField(label="Direct Server Host", required=False)
    directAccessPort = forms.CharField(label="Direct Access Port", required=False)
    
    # UI Hiding Options  
    hideSecurity = forms.BooleanField(initial=False, required=False)
    hideNetwork = forms.BooleanField(initial=False, required=False)
    hideServer = forms.BooleanField(initial=False, required=False)
    hideProxy = forms.BooleanField(initial=False, required=False)
    hideWebsocket = forms.BooleanField(initial=False, required=False)
    hideRemotePrinter = forms.BooleanField(initial=False, required=False)
    hideTray = forms.BooleanField(initial=False, required=False)
    hideHelpCards = forms.BooleanField(initial=False, required=False)
    hideUsernameOnCard = forms.BooleanField(initial=False, required=False)
    hideStopService = forms.BooleanField(initial=False, required=False)
    
    # Render & Performance  
    d3dRender = forms.BooleanField(initial=True, required=False)
    textureRender = forms.BooleanField(initial=False, required=False)
    enableFileCopyPaste = forms.BooleanField(initial=False, required=False)
    enableConfirmClosingTabs = forms.BooleanField(initial=True, required=False)
    enablePrivacyMode = forms.BooleanField(initial=True, required=False)
    enableLanDiscovery = forms.BooleanField(initial=True, required=False)
    
    # Behavior
    viewOnly = forms.BooleanField(initial=False, required=False)
    lockAfterSessionEnd = forms.BooleanField(initial=False, required=False)
    showRemoteCursor = forms.BooleanField(initial=False, required=False)
    followRemoteCursor = forms.BooleanField(initial=False, required=False)
    followRemoteWindow = forms.BooleanField(initial=False, required=False)
    reverseMouseWheel = forms.BooleanField(initial=False, required=False)
    swapLeftRightMouse = forms.BooleanField(initial=False, required=False)
    zoomCursor = forms.BooleanField(initial=False, required=False)
    mainWindowAlwaysOnTop = forms.BooleanField(initial=False, required=False)
    
    # Input
    touchMode = forms.ChoiceField(choices=[('touch','Touch Mode'),('mouse','Mouse Mode')], initial='mouse', required=False)
    trackpadSpeed = forms.CharField(initial='100', required=False)
    peerCardUiType = forms.ChoiceField(choices=[('card','Card View'),('tile','Tile View')], initial='tile', required=False)
    peerSorting = forms.CharField(required=False)
    
    # Customization
    displayName = forms.CharField(required=False)
    codecPreference = forms.ChoiceField(choices=[('auto','Auto'),('vp8','VP8'),('vp9','VP9'),('av1','AV1'),('h264','H264')], initial='auto', required=False)
    verificationMethod = forms.ChoiceField(choices=[('use-permanent-password','Use Permanent Password'),('both','Both')], initial='use-permanent-password', required=False)
    
    # Management
    disableChangeID = forms.BooleanField(initial=False, required=False)
    disableDiscoveryPanel = forms.BooleanField(initial=False, required=False)
    disableChangePermanentPassword = forms.BooleanField(initial=False, required=False)
    disableUnlockPin = forms.BooleanField(initial=False, required=False)
    
    # Misc
    registerDevice = forms.BooleanField(initial=False, required=False)
    syncInitClipboard = forms.BooleanField(initial=True, required=False)
    syncABTags = forms.BooleanField(initial=False, required=False)
    syncABWithRecent = forms.BooleanField(initial=True, required=False)
    removePresetPasswordWarning = forms.BooleanField(initial=False, required=False)
    filterABByIntersection = forms.BooleanField(initial=False, required=False)
    enablePermChangeInAcceptWindow = forms.BooleanField(initial=False, required=False)
    presetAddressBookName = forms.CharField(required=False)
    enableAndroidSoftwareEncodingHalfScale = forms.BooleanField(initial=False, required=False)
    showVirtualJoystick = forms.BooleanField(initial=False, required=False)
    showVirtualMouse = forms.BooleanField(initial=False, required=False)
    allowRemoveWallpaper = forms.BooleanField(initial=True, required=False)
    videoSaveDirectory = forms.CharField(required=False)
    lang = forms.CharField(required=False)
    enableChangeID = forms.BooleanField(initial=False, required=False)
    allowCommandLineSettings = forms.BooleanField(initial=False, required=False)
    allowLinuxHeadless = forms.BooleanField(initial=False, required=False)
    allowInsecureTLSFallback = forms.BooleanField(initial=False, required=False)
    allowHttps21114 = forms.BooleanField(initial=False, required=False)

    # Missing fields referenced in template
    autoReconnect = forms.BooleanField(initial=False, required=False)
    disableAudio = forms.BooleanField(initial=False, required=False)
    disableClipboard = forms.BooleanField(initial=False, required=False)
    disableFileTransfer = forms.BooleanField(initial=False, required=False)
    disableRemoteRestart = forms.BooleanField(initial=False, required=False)
    disableRecording = forms.BooleanField(initial=False, required=False)
    enableBluetooth = forms.BooleanField(initial=False, required=False)
    enableTcpTunneling = forms.BooleanField(initial=True, required=False)
    useRendezvousSignature = forms.BooleanField(initial=False, required=False)
    customFps = forms.CharField(required=False)
    disableOpenGL = forms.BooleanField(initial=False, required=False)
    removeToolbox = forms.BooleanField(initial=False, required=False)
    removeNewVersionButton = forms.BooleanField(initial=False, required=False)
    disableChat = forms.BooleanField(initial=False, required=False)
    disableSessionReuse = forms.BooleanField(initial=False, required=False)

    def clean_iconfile(self):
        print("checking icon")
        image = self.cleaned_data['iconfile']
        if image:
            try:
                # Open the image using Pillow
                img = Image.open(image)

                # Check if the image is a PNG (optional, but good practice)
                if img.format != 'PNG':
                    raise forms.ValidationError("Only PNG images are allowed.")

                # Get image dimensions
                width, height = img.size

                # Check for square dimensions
                if width != height:
                    raise forms.ValidationError("Custom App Icon dimensions must be square.")
                
                return image
            except OSError:  # Handle cases where the uploaded file is not a valid image
                raise forms.ValidationError("Invalid icon file.")
            except Exception as e: # Catch any other image processing errors
                raise forms.ValidationError(f"Error processing icon: {e}")
