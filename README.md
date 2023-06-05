Ansible Collection - sysdig.agent
=================================

The Sysdig Ansible Collection handles the installation and configuration of the Sysdig Agent.

# Configuration
## Requirements
* `ansible-core >= 2.13` 
* Host Operating Systems:
  * Alma Linux 7+
  * Amazon Linux (AL2 and AL2023)
  * CentOS 7+
  * Debian 10+
  * Red Hat 7+
  * Rocky Linux 7+
  * Ubuntu 20.04+ (LTS Only)

### Installation
To install the Sysdig Agent with this Role you first need to install the Role from the Ansible Galaxy.
```bash
?> ansible-galaxy collection install sysdig.agent
```

### Install a Specific Version 
If a specific version of the Collection is necessary it can be installed in the following manner
```bash
?> ansible-galaxy collection install sysdig.agent:==1.1.0
```

### Upgrade 
To install the Sysdig Agent with this Role you first need to install the Role from the Ansible Galaxy.
```bash
?> ansible-galaxy collection install sysdig.agent --upgrade
```

# Example Playbook
Once the Collection has been installed it will then be possible to use the `agent_install` Role in Playbooks to install and configure the Sysdig Agent.
```yaml
- hosts: hosts
  become: true
  roles:
  - role: sysdig.agent.agent_install
    vars:
      configuration:
        connection:
          access_key: <your_sysdig_access_key>
          region: <your_sysdig_region>
```
