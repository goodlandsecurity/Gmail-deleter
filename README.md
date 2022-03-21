# Gmail-deleter

Getting started
---------------
Tired of Google telling you to upgrade your storage? Tired of Gmail making you manually page through your folders to delete your emails?  I have the solution you've been dreaming of!

Programmatically clean your Gmail inbox and delete messages en masse by specific labels or Gmail search filter syntax!


Prerequisites
-------------

 - Python 3 (tested and working on Mac with Python 3.10.2)
 - A Google Cloud Platform project with the API enabled. To create a project and enable an API, refer to [Create a project and enable the API](https://developers.google.com/workspace/guides/create-project)
 - Authorization credentials for a desktop application. To learn how to create credentials for a desktop application, refer to [Create credentials](https://developers.google.com/workspace/guides/create-credentials)
 - A Google account with Gmail enabled


Installation
------------

 - Optional: Create a virtual environment 
 
 - Run: 
   
   ```bash 
   python -m pip install -r requirements.txt
   ```
 

Usage
-----

 - For first run, copy credentials.json file generated from Gmail API to the repository directory
 - For subsequent runs you can authenticate with the generated token.json file
 - By default the permissons scope is set to readonly. This is to prevent potential disasters from happening.
   - For write permissions scope, enable in ```gmail_deleter/client.py``` 


Run deleter script with:
```bash
python3 deleter.py
```
You can use -c/--credentials to specify credentials.json file path or -t/--token to specify token.json path

First run:
```bash
python3 deleter.py -c credentials.json
```
This opens a new window prompting you to authorize access to your data:

- If you are not already signed in to your Google account, you are prompted to sign in. If you are signed in to multiple Google accounts, you are asked to select one account to use for the authorization.
- Click Accept. The app is authorized to access your data.


Subsequent runs:
```bash
python3 deleter.py -t token.json
```
Authorization information is stored on the file system, so subsequent executions don't prompt for authorization.


Options
-------
The script provides the following options:  
 - list authenticated user's email address and total number of messages in the mailbox
 - list all labels associated with the authenticated user's mailbox.
 - deletion of all messages with a specified label (Promotions, Forums, Social...)
   - soft delete - move to Trash
   - hard delete - permanently delete
 - deletion of all messages that match a specified Gmail search filter (e.g. from:user@domain.com)
   - soft delete - move to Trash
   - hard delete - permanently delete
 - emptying Trash  
   - hard delete - permanently delete
 - emptying Spam  
   - hard delete - permanently delete
 

Troubleshooting!
----------------
This section describes some common issues that you may encounter while attempting to run this quickstart and suggests possible solutions.
***


```python
AttributeError: 'Module_six_moves_urllib_parse' object has no attribute 'urlparse'
```
This error can occur in Mac OSX where the default installation of the six module (a dependency of the Python library) is loaded before the one that pip installed. To fix the issue, add pip's install location to the PYTHONPATH system environment variable:

1. Determine pip's install location with the following command:
```bash
python3 -m pip show six | grep "Location:" | cut -d " " -f2
```

2. Add the following line to your ~/.bashrc file, replacing <pip_install_path> with the value determined above:
```bash
export PYTHONPATH=$PYTHONPATH:<pip_install_path>
```

3. Reload your ~/.bashrc file in any open terminal windows using the following command:
```bash
source ~/.bashrc
```
***
<br/>

```python
TypeError: sequence item 0: expected str instance, bytes found
```
- This error is due to a bug in httplib2. To resolve this problem, upgrade to the latest version of httplib2 using this command:
```bash
python3 -m pip install --upgrade httplib2
```
***
<br/>

```python
Cannot uninstall 'six'
```
- When running the pip install command you may receive the following error:
  - "Cannot uninstall 'six'. It is a distutils installed project and thus we cannot accurately determine which files belong to it which would lead to only a partial uninstall."
- This error occurs on Mac OSX when pip attempts to upgrade the pre-installed six package. To work around this issue, add the flag --ignore-installed six to the pip install command listed in step 2.
***
<br/>

```bash
This app isn't verified
```
- If the OAuth consent screen displays the warning "This app isn't verified," your app is requesting scopes that provide access to sensitive user data. If your application uses sensitive scopes, your your app must go through the [verification process](https://support.google.com/cloud/answer/7454865) to remove that warning and other limitations. During the development phase you can continue past this warning by clicking Advanced > Go to {Project Name} (unsafe).
***
<br/>

```bash
credentials.json file not found error
```
- When running the deleter script, you might receive a file not found or no such file error regarding credentials.json.
- This error occurs when you have not authorized the desktop application credentials as detailed in the Prerequisites section above. To learn how to create credentials for a desktop application, go to [Create credentials](https://developers.google.com/workspace/guides/create-credentials).
- Once you create the credentials, make sure the downloaded JSON file is saved as credentials.json. Then move the file to the working directory with the deleter script.