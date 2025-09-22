# Build a Custom Ansible Module

## Overview

Ansible modules are the building blocks for building ansible playbooks. They are small pieces of python code that can be triggered from the `yaml` in a playbook. Ansible provides many modules but sometimes you need to develop your own for specific use-cases. 

Ansible modules are reusable, standalone scripts that can be used by the Ansible API, or by the ansible or ansible-playbook programs. They return information to Ansible by printing a JSON string to stdout before exiting.

Often times custom modules are a nice way to interact more fluently with services that provide a RESTful API. For example GitHub or Pivotal. You can, of course, interact with these services with the URI module, but it can be more complicated.

## Prerequisites

### Create a GitHub account
Create a free GitHub account if you do not already have one.
https://github.com/join

### Create a GitHub Personal Access Token (PAT)
Generate Personal Access Token to authenticate from Ansible to GitHub.
1. In a browser visit: [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Log in to GitHub if prompted
3. Click "Generate new token"
4. Choose "Generate new token (classic)"
  5. Name token
  6. Select "repo" and "delete_repo" scopes
7. At the bottom of page, click "Generate token"
  Make sure you save your token because it will not be shown again.



## Secure the Token with Ansible Vault

Before proceeding, we need to secure the GitHub token using **Ansible Vault**.

1. Create a new Ansible Vault file:

   ```
   ansible-vault create vault.yml
   ```

   This will open an editor where you can enter your encrypted variables.

2. Add the following content to `vault.yml`:

   ```
   github_token: YOUR_GITHUB_TOKEN_HERE
   ```

   Replace `YOUR_GITHUB_TOKEN_HERE` with your actual GitHub token.

3. Save and exit. The file is now encrypted.

To edit the vault file later, use:

```
ansible-vault edit vault.yml
```

To view its contents:

```
ansible-vault view vault.yml
```



## Create a custom module 

Writing an Ansible module is not difficult. Modules can be written in any language, but for this lab we will use Python. 

We'll create a quick little module that can create or delete a repository on github.

Let's start with a basic scaffolding to see how a custom module works. 

Create the following directory / file structure: 


```
play.yml
[library]
  |- github_repo.py
```

The custom module lives in the `library` directory and has the name we will be calling from our playbook `github_repo`. 

Add the following to `github_repo.py`

```python
#!/usr/bin/python3

from ansible.module_utils.basic import *

def main():

	 module = AnsibleModule(argument_spec={})
	 response = {"hello": "world"}
	 module.exit_json(changed=False, meta=response)


if __name__ == '__main__':
    main()
```

**Notes** 

* `main()` is the entrypoint into the module.
* `#!/user/bin/python3` is required. Do not forget it! 
* `AnsibleModule` comes from `from ansible.module_utils.basic import *`. It is imported with the `*`
* `AnsibleModule` handles incoming and outgoing parameters.

Now create a playbook `play.yml` with the following: 

```yml
- hosts: localhost
  tasks:
    - name: Test that my module works
      github_repo:
      register: result

    - debug: var=result
```


This playbook confirms our module is working as expected and dumps the output to `debug`. 

Because we have not specified an inventory, Ansible will run the playbook on `localhost`

Run the playbook:

```
ansible-playbook play.yml
```

Sample output: 
```
PLAY ***************************************************************************

TASK [setup] *******************************************************************
ok: [localhost]

TASK [Test that my module works] ***********************************************
ok: [localhost]

TASK [debug] *******************************************************************
ok: [localhost] => {
    "result": {
        "changed": false,
        "meta": {
            "hello": "world"
        }
    }
}

PLAY RECAP *********************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0

```

It worked! Now that we know the module works we can add code to create/delete GitHub repositories. 

Update the `main` function to handle input so we can create a GitHub repo. 

```python
def main():

    fields = {
        "github_auth_key": {"required": True, "type": "str"},
        "username": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "description": {"required": False, "type": "str"},
        "private": {"default": False, "type": "bool"},
        "has_issues": {"default": True, "type": "bool"},
        "has_wiki": {"default": True, "type": "bool"},
        "has_downloads": {"default": True, "type": "bool"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
    }

    module = AnsibleModule(argument_spec=fields)
    module.exit_json(changed=False, meta=module.params)
```

**Notes** 

* The expected inputs are defined as a dictionary.
* You can specify if a field is  `required`, using a `default` value, and limit possible inputs with `choices`.

The above code accepts and pipes the parsed inputs `module.params` to `exit_json`.

Update the playbook to use the vault encrypted key, and add more fields.

```yml
- hosts: localhost
  vars_files:
    - vault.yml
  tasks:
    - name: Create a github Repo
      github_repo:
        github_auth_key: "{{ github_token }}"
          username: "YOUR GITHUB USERNAME HERE"
          name: "Hello-World"
          description: "This is your first repository"
          private: yes
          has_issues: no
          has_wiki: no
          has_downloads: no
         state: present
      register: result
    - debug: var=result
    
```

Run the playbook and it will display a dictionary of inputs passed in. 

```sh
ansible-playbook play.yml
```


Ansible recommends adding documentation with examples of using the module. At the top of the module add: 
```yml
DOCUMENTATION = r'''
---
module: github_repo

short_description: This module manages GitHub repositories
'''

EXAMPLES = r'''
- name: Create a github Repo
  github_repo:
    github_auth_key: "..."
    name: "Hello-World"
    description: "This is your first repository"
    private: yes
    has_issues: no
    has_wiki: no
    has_downloads: no
  register: result

- name: Delete that repo
  github_repo:
    github_auth_key: "..."
    name: "Hello-World"
    state: absent
  register: result
'''
```


Now update the module with a function to create a GitHub repository

```python
from ansible.module_utils.basic import *
import requests

api_url = "https://api.github.com"


def github_repo_present(data):

    api_key = data['github_auth_key']

    del data['state']
    del data['github_auth_key']

    headers = {
        "Authorization": "token {}" . format(api_key)
    }
    url = "{}{}" . format(api_url, '/user/repos')
    result = requests.post(url, json.dumps(data), headers=headers)

    if result.status_code == 201:
        return False, True, result.json()
    if result.status_code == 422:
        return False, False, result.json()

    # default: something went wrong
    meta = {"status": result.status_code, 'response': result.json()}
    return True, False, meta
```


Add a function to delete the repository. 

```python
def github_repo_absent(data=None):
    headers = {
        "Authorization": "token {}" . format(data['github_auth_key'])
    }
    url = "{}/repos/{}/{}" . format(api_url, data['username'], data['name'])
    result = requests.delete(url, headers=headers)

    if result.status_code == 204:
        return False, True, {"status": "SUCCESS"}
    if result.status_code == 404:
        result = {"status": result.status_code, "data": result.json()}
        return False, False, result
    else:
        result = {"status": result.status_code, "data": result.json()}
        return True, False, result
```

Define the input fields to be used in your playbook. 
```python
def main():

    fields = {
        "github_auth_key": {"required": True, "type": "str"},
        "username": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "description": {"required": False, "type": "str"},
        "private": {"default": False, "type": "bool"},
        "has_issues": {"default": True, "type": "bool"},
        "has_wiki": {"default": True, "type": "bool"},
        "has_downloads": {"default": True, "type": "bool"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
    }

    choice_map = {
        "present": github_repo_present,
        "absent": github_repo_absent,
    }

    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = choice_map.get(
        module.params['state'])(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error deleting repo", meta=result)


if __name__ == '__main__':
    main()

```

This module includes the following: 

* `api_url`: Hard coded URI of GitHub's REST API
* A list of fields passed from the playbook.
  * All of the fields with `data` in front of them are values provided by the playbook.
  * `github_auth_key`: Personal Access Token created earlier.
  * `state`: The state has two options `present`, `absent`.
  * `username`: The GitHub account Ansible is managing.
  * `name`: Name of GitHub repository being created/deleted.
  * `description`: Description for repository
  * `private`: Create a private or public repository

There are additional options listed in the `main` function, which we will not go over in detail. 

## Update our playbook
Update the `play.yml` playbook with tasks to create the repository. 

Here is a sample of what that might look like: 

```yml
- hosts: localhost
  vars_files:
    - vault.yml
  tasks:
    - name: Create a GitHub Repo
      github_repo:
        github_auth_key: {% raw %} "{{github_token}}" {% endraw %}
        username: "YOUR GITHUB USERNAME HERE"
        name: "Hello-World"
        description: "First repo created with custom Ansible module"
        private: yes
        has_issues: no
        has_wiki: no
        has_downloads: no
        state: present
      register: result
```

Run the playbook and confirm it created the `Hello-World` repository. 

```
ansible-playbook play.yml --ask-vault-pass
```



Update the playbook with the following task to delete the repository. Remember to add tags so you can choose which task to run.

```yml
    - name: Delete GitHub Repo
      github_repo:
        github_auth_key: {% raw %} "{{github_token}}" {% endraw %}
        username: "YOUR GITHUB USERNAME HERE"
        name: "Hello-World"
        state: absent
```

Rerun the playbook to delete the repository (using the correct tag)

### Challenge

Now that you've run the playbook using the `--ask-vault-pass` option, create a file that contains the decryption password and run the playbook using that. 

## Congrats 

You have successfully created an Ansible module using Python. This is a straightforward example that can be adapted for various needs.
