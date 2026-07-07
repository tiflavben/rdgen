
import re

with open('rdgenerator/views.py', 'r') as f:
    content = f.read()

# Replace the GitHub Actions API URL with Drone CI API URL for each platform
# Old: url = 'https://api.github.com/repos/.../workflows/generator-....yml/dispatches'
# New: url = 'https://deone.arm64linux.vip/api/repos/' + _settings.GHUSER + '/' + _settings.REPONAME + '/builds'

# Step 1: Replace all the GitHub Actions workflow URL patterns with Drone CI URLs
# Windows x86_64 uses a different Drone pipeline

# Replace windows URL
content = content.replace(
    "if platform == 'windows':\n                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows.yml/dispatches'\n                if selfhosted:\n                    url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/sh-generator-windows.yml/dispatches'",
    "if platform == 'windows':\n                url = 'https://deone.arm64linux.vip/api/repos/' + _settings.GHUSER + '/' + _settings.REPONAME + '/builds'\n                if selfhosted:\n                    url = 'https://deone.arm64linux.vip/api/repos/' + _settings.GHUSER + '/' + _settings.REPONAME + '/builds'"
)

# Replace windows-x86 URL
content = content.replace(
    "if platform == 'windows-x86':\n                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows-x86.yml/dispatches'",
    "if platform == 'windows-x86':\n                url = 'https://deone.arm64linux.vip/api/repos/' + _settings.GHUSER + '/' + _settings.REPONAME + '/builds'"
)

# Replace linux URL
content = content.replace(
    "elif platform == 'linux':\n                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-linux.yml/dispatches'",
    "elif platform == 'linux':\n                url = 'https://deone.arm64linux.vip/api/repos/' + _settings.GHUSER + '/' + _settings.REPONAME + '/builds'"
)

# Replace android URL
content = content.replace(
    "elif platform == 'android':\n                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-android.yml/dispatches'",
    "elif platform == 'android':\n                url = 'https://deone.arm64linux.vip/api/repos/' + _settings.GHUSER + '/' + _settings.REPONAME + '/builds'"
)

# Replace macos URL
content = content.replace(
    "elif platform == 'macos':\n                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-macos.yml/dispatches'",
    "elif platform == 'macos':\n                url = 'https://deone.arm64linux.vip/api/repos/' + _settings.GHUSER + '/' + _settings.REPONAME + '/builds'"
)

# Replace fallback URL
content = content.replace(
    "else:\n                url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-windows.yml/dispatches'\n                if selfhosted:\n                    url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/sh-generator-windows.yml/dispatches'",
    "else:\n                url = 'https://deone.arm64linux.vip/api/repos/' + _settings.GHUSER + '/' + _settings.REPONAME + '/builds'\n                if selfhosted:\n                    url = 'https://deone.arm64linux.vip/api/repos/' + _settings.GHUSER + '/' + _settings.REPONAME + '/builds'"
)

# Step 2: Replace the data payload
# Old: data = {"ref": ..., "inputs": {...}}
# New: data = {"branch": ..., "parameters": {...}}

old_data = '''            data = {
                "ref":_settings.GHBRANCH,
                "inputs":{
                    "version":version,
                    "zip_url":zip_url
                },
                "return_run_details": True
            }'''

new_data = '''            data = {
                "branch": _settings.GHBRANCH,
                "parameters": {
                    "VERSION": version,
                    "ZIP_URL": zip_url,
                    "PLATFORM": platform
                }
            }'''

content = content.replace(old_data, new_data)

# Step 3: Replace the headers
old_headers = '''            headers = {
                'Accept':  'application/vnd.github+json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer '+_settings.GHBEARER,
                'X-GitHub-Api-Version': '2026-03-10'
            }'''

new_headers = '''            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + _settings.GHBEARER
            }'''

content = content.replace(old_headers, new_headers)

# Step 4: Replace the response handling
old_response = '''                if response.status_code == 204 or response.status_code == 200:
                    github_data = {}
                    if response.status_code == 200:
                        try:
                            github_data = response.json()
                        except Exception:
                            pass
                    new_github_run.github_run_id = github_data.get('workflow_run_id')
                    new_github_run.status = "in_progress"
                    new_github_run.save()

                    log_url = github_data.get('html_url', '')'''

new_response = '''                if response.status_code in [200, 201]:
                    drone_data = {}
                    try:
                        drone_data = response.json()
                    except Exception:
                        pass
                    new_github_run.github_run_id = drone_data.get('id', drone_data.get('number', ''))
                    new_github_run.status = "in_progress"
                    new_github_run.save()

                    log_url = 'https://deone.arm64linux.vip/' + _settings.GHUSER + '/' + _settings.REPONAME + '/' + str(drone_data.get('number', drone_data.get('id', '')))'''

content = content.replace(old_response, new_response)

# Step 5: Replace the error handling
old_error = '''                else:
                    #new_github_run.delete()
                    return JsonResponse({"error": "GitHub rejected the start request (status %d)" % response.status_code}, status=500)'''
new_error = '''                else:
                    #new_github_run.delete()
                    return JsonResponse({"error": "Drone rejected the start request (status %d)" % response.status_code}, status=500)'''
content = content.replace(old_error, new_error)

# Step 6: Replace the exception error message
old_except = '''            except Exception as e:
                #new_github_run.delete()
                return JsonResponse({"error": f"Connection error: {str(e)}"}, status=500)'''
new_except = '''            except Exception as e:
                #new_github_run.delete()
                return JsonResponse({"error": f"Drone connection error: {str(e)}"}, status=500)'''
content = content.replace(old_except, new_except)

# Step 7: Also update the startgh function to use Drone
old_startgh = """    url = 'https://api.github.com/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/actions/workflows/generator-'+data_.get('platform')+'.yml/dispatches'"""
new_startgh = """    url = 'https://deone.arm64linux.vip/api/repos/'+_settings.GHUSER+'/'+_settings.REPONAME+'/builds'"""
content = content.replace(old_startgh, new_startgh)

# Step 8: Update startgh data payload
old_startgh_data = '''    data = {
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
    }'''
new_startgh_data = '''    data = {
        "branch": _settings.GHBRANCH,
        "parameters":{
            "server":data_.get('server'),
            "key":data_.get('key'),
            "apiServer":data_.get('apiServer'),
            "custom":data_.get('custom'),
            "uuid":data_.get('uuid'),
            "iconlink":data_.get('iconlink'),
            "logolink":data_.get('logolink'),
            "appname":data_.get('appname'),
            "extras":data_.get('extras'),
            "filename":data_.get('filename'),
            "platform":data_.get('platform')
        }
    }'''
content = content.replace(old_startgh_data, new_startgh_data)

# Step 9: Update startgh headers
old_startgh_headers = '''    headers = {
        'Accept':  'application/vnd.github+json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+_settings.GHBEARER,
        'X-GitHub-Api-Version': '2026-03-10'
    }'''
new_startgh_headers = '''    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+_settings.GHBEARER
    }'''
content = content.replace(old_startgh_headers, new_startgh_headers)

# Step 10: Update startgh response handling
old_startgh_response = '''    response = requests.post(url, json=data, headers=headers)
    print(response)'''
new_startgh_response = '''    response = requests.post(url, json=data, headers=headers)
    print(f"Drone response: {response.status_code} {response.text[:200]}")'''
content = content.replace(old_startgh_response, new_startgh_response)

with open('rdgenerator/views.py', 'w') as f:
    f.write(content)

print("Done! Views patched for Drone CI.")
