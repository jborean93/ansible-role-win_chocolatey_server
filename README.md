# Ansible Role win_chocolatey_server

[![Build status](https://ci.appveyor.com/api/projects/status/mw7a34uxoio16vfh?svg=true)](https://ci.appveyor.com/project/jborean93/ansible-role-win-chocolatey-server)
[![win_chocolatey_server Ansible Galaxy Role](https://img.shields.io/ansible/role/27430.svg)](https://galaxy.ansible.com/jborean93/win_chocolatey_server)

Installs [Chocolatey Server](https://chocolatey.org/packages/chocolatey.server)
on a Windows host.

_Note: This role has been tested on chocolatey.server 0.2.5, newer versions should work but this is not guaranteed_

With the defaults this role will;

* Install the `chocolatey.server` package to `C:\tools\chocolatey.server`
* Install various IIS features required for Chocolatey server
* Create an IIS web app pool called `chocolatey_server_app_pool`
* Create an IIS web site called `chocolatey_server_site` with a http binding on port `80`
* Firewall rule to allow traffic in on port `80` for the `domain` and `private` profiles

The following can also be configured as part of the role but require some
optional variables to be set;

* Set an API Token for the Chocolatey server
* Specify users and their SHA1 password hash over basic auth
* Create a HTTPS binding for the site with an existing or self signed certificate
* Specify the path or URL of the `chocolatey` package to configure the server's `install.ps1` script
* Specify the maximum package size allowed on the server

I would like to thank kkolk for the excellent blog post that helped me write
this role. You can read the post [here](http://frostbyte.us/using-ansible-to-install-a-chocolatey-package-repository/).

To add new packages to the Chocolatey server install, copy the .nupkg to
`{{ opt_chocolatey_server_path }}\chocolatey.server\App_Data\Packages` and the
server will pick up the file.

_Note: You first need to activate the file watcher by navigating to `http://server/chocolatey/Packages` at least once the IIS app pool is warm. Any restarts of pool recycles require you to do this again before any packages are picked up in this dir._

## Requirements

* Windows Server 2008 R2+
* Chocolatey client to be installed on the remote host if the remote host cannot access the internet


## Variables

### Mandatory Variables

None, this role will run with the default options set.

### Optional Variables

* `opt_chocolatey_server_api_token`: The API token/key that is used when uploading new packages to the server. If not specified then this will use the default token specified by the `chocolatey.server` package.
* `opt_chocolatey_server_credentials`: Dictionary of username and password hashes to specify as the basic authentication credentials. The key is the `username` while the value is an upper case SHA1 hash of the `password`. If not set then basic auth is disabled and anonymous access is allowed.
* `opt_chocolatey_server_firewall_profiles`: The firewall profiles to use that will allow access to the Chocolatey Server (default: `domain,private`). This can be a combination of `domain`, `private`, and/or `public`.
* `opt_chocolatey_server_http_port`: The port to use for http access (default: `80`).
* `opt_chocolatey_server_https_port`: The port to use for https access, by default no https binding is created unless this is specified.
* `opt_chocolatey_server_https_certificate`: The certificate thumbprint to use for the HTTPS binding, if not specified then .
* `opt_chocolatey_server_max_package_size`: The maximum allowed size, in bytes, of a package that can be stored on the server (default: `2147483648`).
* `opt_chocolatey_server_path`: The root directory that the `chocolatey.server` package is installed to (default: `C:\tools`).
* `opt_chocolatey_server_source`: The source location of the [chocolatey.server](https://chocolatey.org/packages/chocolatey.server) package (default: `https://chocolatey.org/api/v2/`). This can be the name/url of a Nuget repository or a local path that contains the nupkg file.

To set up the Chocolatey server to create an `install.ps1` script and source
the installer file from the repo instead of the internet, download the
[chocolatey nupkg](https://chocolatey.org/packages/chocolatey) file and set one
of the following two variables that point to this file;

* `opt_chocolatey_server_chocolatey_path`: The path that is accessible from the remote host to the Chocolatey nupkg file.
* `opt_chocolatey_server_chocolatey_url`: The URL that is accessible from the remote host to the Chocolatey nupkg file.

If neither of these values are set, then the `install.ps1` script from this
server will default to the public install script on the Chocolatey site.

### Output Variables

These variables are set as a host fact with `set_fact` during the execution.
They can be used by any downstream roles or tasks for that host.

* `out_chocolatey_server_https_certificate`: If a https binding is created with a self signed certificate, this is the certificate hash of the certificate created.


## Role Dependencies

None


## Example Playbook

```
- name: install Chocolatey Server with the defaults
  hosts: windows
  gather_facts: no
  roles:
  - jborean93.win_chocolatey_server

- name: setup Chocolatey with HTTPS listener on custom path and enable basic authentication
  hosts: windows
  gather_facts: no
  vars:
    opt_chocolatey_server_api_token: eb82582c-2214-4ce9-9689-8c823ae33e45
    opt_chocolatey_server_credentials:
      build-team: '{{ build_team_pass | hash("sha1") | upper }}'
      test-team: '{{ test_team_pass | hash("sha1") | upper }}'
      build-team: '{{ build_team_pass | hash("sha1") | upper }}'
    opt_chocolatey_server_http_port: 8080
    opt_chocolatey_server_https_port: 8443
    opt_chocolatey_server_path: D:\tools
    opt_chocolatey_server_chocolatey_url: https://internalrepo.domain/chocolatey.0.10.11.nupkg

  roles:
  - jborean93.win_chocolatey_server

  post_tasks:
  - name: output the cert hash used for the HTTPS bindings
    debug:
      var: out_chocolatey_server_https_certificate
```


## Backlog

None - feature requests are welcome
