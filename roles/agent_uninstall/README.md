agent_uninstall
=========
This Role uninstalls the Sysdig Agent.

# Requirements
* `ansible-core >= 2.13`

# Role Variables
| Parameter                               | Description                                                                   | Default |
|-----------------------------------------|-------------------------------------------------------------------------------|---------|
| `retain_agent_configuration`            | Whether to leave the contents of `/opt/draios/etc/` after package removal     | `true`  |
| `retain_agent_logs`                     | Whether to leave the contents of `/opt/draios/logs/` after package removal    | `true`  |
| `retain_agent_repository_configuration` | Whether to leave the Sysdig Agent repository configured after package removal | `true`  |

# Example Playbook
```yaml
- hosts: hosts`
  roles:
    - role: sysdig.agent.agent_uninstall
      vars:
        retain_agent_configuration: false
        retain_agent_logs: false
        retain_agent_repository_configuration: false
```
