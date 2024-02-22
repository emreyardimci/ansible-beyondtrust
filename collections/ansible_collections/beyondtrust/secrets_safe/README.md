# Ansible Collection - beyondtrust.secret_safe
[![Code of conduct](https://img.shields.io/badge/code%20of%20conduct-Ansible-silver.svg)](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)
[![License](https://img.shields.io/badge/license-GPL%20v3.0-brightgreen.svg)](LICENSE)

This collection provides Ansible modules and plugins for interacting with the BeyondTrust Secrets Safe. Allowing you to Secure and manage credentials and secrets used in your Ansible environment.

## Ansible version compatibility

This collection is compatible with Ansible core >= v2.14.

## Python version compatibility

This collection is compatible with Python >= v3.11.

## Pip version compatibility

This collection can run pip in its latest version for packages required to run the plugin.

## Installing collection from Ansible Galaxy

To install the collection you can use the next command if the collection is on Ansible Galaxy repository:

```sh
ansible-galaxy collection install beyondtrust.secrets_safe
```

## Installing collection manually

If you have the collection downloaded locally, you can run the next command:

```sh
ansible-galaxy collection install beyondtrust-secrets_safe-<version>.tar.gz
```

Where `<version>` is the version that you downloaded.

if it's not a fresh install, you would need to run the next command to update the collection to its latest version:

```sh
ansible-galaxy collection install --upgrade beyondtrust-secrets_safe-<version>.tar.gz
```

If the installation is successful, run this command:

```sh
ansible-galaxy collection list
```

And you should see the collection installed:

```sh
...

Collection              Version
----------------------- -------
beyondtrust.secrets_safe 1.0.0 

...
```
## Install required modules

To run the plugin in a playbook, you will need to install modules using pip, with the file `requirements.txt`, found locally after installing the collection. Run the following command:

```sh
pip install -r ~/.ansible/collections/ansible_collections/beyondtrust/secrets_safe/requirements.txt
pip install --upgrade -r ~/.ansible/collections/ansible_collections/beyondtrust/secrets_safe/requirements.txt
```

## Lookup Plugin Usage

### Plugin Options:
- api_url:
    - description: BeyondTrust Password Safe API URL.
    - type: string
    - required: True
- retrieval_type:
    - description: Type of secret to retrieve (use MANAGED_ACCOUNT or SECRET)
    - type: string
    - required: True
- client_id:
    - description: API OAuth Client ID.
    - type: string
    - required: True
- client_secret:
    - description: API OAuth Client Secret.
    - type: string
    - required: True
- secret_list:
    - description: List of secrets (path/title,path/title) or managed accounts (ms/ma,ms/ma) to be retrieved, separated by a comma.
    - type: string
    - required: True
- certificate_path:
    - description: Password Safe API pfx Certificate Path. For use when authenticating using a Client Certificate.
    - type: string
    - required: False
- certificate_password:
    - description: Password Safe API pfx Certificate Password. For use when authenticating using a Client Certificate.
    - type: string
    - required: False
- verify_ca:
    - description: Indicates whether to verify the certificate authority on the Secrets Safe instance.
    - type: boolean 
    - default: True
    - required: False

### Return:

 - description: list of retrieved  secret(s) in the requested order.   
 - type: list 
 - elements: str

### Example Playbook
Use the plugin from the collection in a playbook:
```
export PASSWORD_SAFE_CLIENT_ID=********************
export PASSWORD_SAFE_CLIENT_SECRET=********************
export CERTIFICATE_PASSWORD=********************
export PASSWORD_SAFE_API_URL=https://example.com:443/BeyondTrust/api/public/v3
```
 ```yml
---
- name: book
  hosts: localhost
  connection: local
  vars:
      apiURL: "{{ lookup('ansible.builtin.env', 'PASSWORD_SAFE_API_URL') }}"

      clientIdFromEnvVar: "{{ lookup('ansible.builtin.env', 'PASSWORD_SAFE_CLIENT_ID') }}"
      secretFromEnvVar: "{{ lookup('ansible.builtin.env', 'PASSWORD_SAFE_CLIENT_SECRET') }}"

      certificatePasswordFromEnVar:  "{{ lookup('ansible.builtin.env', 'CERTIFICATE_PASSWORD') }}"
      certificatePath: "<path>/ClientCertificate.pfx"

      secretManagedAccounts: "fake_system/fake_ managed_account,fake_system/fake_managed_account01"
      gotManagedAccount: "{{lookup('beyondTrust.secrets_safe.secrets_safe_lookup', api_url=apiURL, retrieval_type='MANAGED_ACCOUNT', client_id=clientIdFromEnvVar, client_secret=secretFromEnvVar, secret_list=secretManagedAccounts, certificate_path=certificatePath, certificate_password=certificatePasswordFromEnVar, wantlist=False)}}"

      secretList: "fake_grp/credential,fake_grp/file"
      gotSecrets: "{{lookup('beyondTrust.secrets_safe.secrets_safe_lookup', api_url=apiURL, retrieval_type='SECRET', client_id=clientIdFromEnvVar, client_secret=secretFromEnvVar, secret_list=secretList, certificate_path=certificatePath, certificate_password=certificatePasswordFromEnVar, wantlist=False, verify_ca=True)}}"
  tasks:
    - name: Display Retrieved Managed accounts
      ansible.builtin.debug:
        msg: "{{ gotManagedAccount }}"
    - name: Display Retrieved Secrets
      ansible.builtin.debug:
        msg: "{{ gotSecrets }}"
```
## Run
```
ansible-playbook book.yml
```

## Verbosity
| WARNING          |
|:---------------------------|
Take precautions to not accidentally log the secrets to stdout. It is important that security-minded engineers review playbooks composition before changes are run with access to secrets.

| WARNING          |
|:---------------------------|
Ansible writes lookup plugin arguments to stdout so be careful not to put secret text directly in the lookup plugin arguments, using variables is one alternative.

In Ansible, the "verbose" mode is used to control the level of detail displayed in the output when running Ansible playbooks and commands. By default, Ansible provides a reasonable amount of information, but you can increase the verbosity to get more detailed information about what Ansible is doing behind the scenes.

To export or set the verbosity level in Ansible, you can use the -v or --verbose option followed by the desired verbosity level. There are different levels of verbosity that you can choose from:

-v or --verbose: This is the default verbosity level. It provides some basic information about the tasks being executed.

-vv: This increases the verbosity to level 2, providing more detailed information, including variables and task results.

-vvv: This increases the verbosity to level 3, providing even more detailed debugging information.

-vvvv: This is the highest verbosity level, providing extensive debugging information, including information about module calls and other internal details.

Here's an example of how you can use the verbosity options:
```sh
ansible-playbook book.yml -v
```
You can also combine multiple -v options to increase verbosity further. For example:
```sh
ansible-playbook book.yml -vvv
```
Keep in mind that higher verbosity levels can generate a significant amount of output, which might be overwhelming for larger playbooks or tasks. Use increased verbosity only when troubleshooting or debugging specific issues.

## License

GNU General Public License v3.0

See [LICENSE](LICENSE) to see the full text.

## Collection Signature Verification

If you want to verify the ansible collection installer, you have to:

1. Download the public key from the resource kit

2. Download ansible collection compress installer (beyondtrust-secrets_safe-1.0.0.tar.gz)

3. Download detached signed file (beyondtrust-secrets_safe-1.0.0.tar.gz.asc) from the resource kit

4. Open the terminal and go where you downloaded the files previously mention.
    ```sh 
    cd path/to/the/files/
    ```
5. Import the public key into your system:
    ```sh 
    gpg --import key_filename
    ```
    Where key_filename is the how the key is named.

6. Check the key in the key list and copy its ID:
    ```sh 
    gpg --list-keys

    pub   rsa4096 2023-08-22 [SC]
      491F6B69DB9A1DF827208A57CFA8BE947D00D138  <-- THIS ID
    uid           [unknown] BeyondTrust Corporation <support@beyondtrust.com>
    sub   rsa4096 2023-08-22 [E]
    ```

7. Give the key ultimate trust level:
    ```sh 
    gpg --edit-key 491F6B69DB9A1DF827208A57CFA8BE947D00D138 trust
    ```

    When you run the command, you have to input the next options:
    ```sh 
    Please decide how far you trust this user to correctly verify other users keys
    (by looking at passports, checking fingerprints from different sources, etc.)

    1 = I don't know or won't say
    2 = I do NOT trust
    3 = I trust marginally
    4 = I trust fully
    5 = I trust ultimately
    m = back to the main menu

    Your decision? 5 <-- Here you have to type 5.
    Do you really want to set this key to ultimate trust? (y/N) y <-- Here you have to type y.

    pub  rsa4096/CFA8BE947D00D138
        created: 2023-08-22  expires: never       usage: SC
        trust: ultimate      validity: ultimate
    sub  rsa4096/2E70108ADAEF68B1
        created: 2023-08-22  expires: never       usage: E
    [ultimate] (1). BeyondTrust Corporation <support@beyondtrust.com>

    gpg> save <-- Here you have to type save.
    ```

    To remind:

    On `Your decision?` input you have to type 5.

    On `Do you really want to set this key to ultimate trust?` input you have to type y.

    On `gpg>` cli input you have to type save.

8. Now that we trust the public key we can verify the ansible collection compress installer:

    ```sh 
    gpg --verify beyondtrust-secrets_safe-1.0.0.tar.gz.asc beyondtrust-secrets_safe-1.0.0.tar.gz
    ```

    This is the output of the command
    ```sh
    gpg: Signature made Fri Aug 25 08:41:43 2023 -05
    gpg:                using RSA key 491F6B69DB9A1DF827208A57CFA8BE947D00D138
    gpg: checking the trustdb
    gpg: marginals needed: 3  completes needed: 1  trust model: pgp
    gpg: depth: 0  valid:   2  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 2u
    gpg: Good signature from "BeyondTrust Corporation <support@beyondtrust.com>" [ultimate]
    ```

    If you get this output, congratulations, you have now an ansible collection compress installer for Secrets Safe plugin for Ansible.