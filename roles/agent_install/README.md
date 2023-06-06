agent_install
=============
This Role installs and configures the Sysdig Agent.

# Requirements
* `ansible-core >= 2.13`

#  Role Variables
| Parameter                                                       | Description                                                                                                                                                                                                                               |
|-----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `configuration.connection.access_key`                           | The Sysdig Agent Access Key to use                                                                                                                                                                                                        |
| `configuration.connection.region`                               | The Sysdig SaaS region code for the SaaS backend to connect to. See `configuration.connection.custom_collector` for OnPrem                                                                                                                |
| `configuration.connection.custom_collector.url`                 | The URL/hostname/IP of the Sysdig Collector to connect to                                                                                                                                                                                 |
| `configuration.connection.custom_collector.port`                | The port of the custom Sysdig Collector to use when connecting                                                                                                                                                                            |
| `configuration.connection.network_proxy.host`                   | The URL/hostname/IP of a proxy server the Agents should use when connecting to the Sysdig Collectors                                                                                                                                      |
| `configuration.connection.network_proxy.port`                   | The port of the proxy server the Agents should use when connecting to the Sysdig Collectors                                                                                                                                               |
| `configuration.connection.network_proxy.username`               | The username to provide when authenticating with the configured network proxy                                                                                                                                                             |
| `configuration.connection.network_proxy.password`               | The password to provide when authenticating with the configured network proxy                                                                                                                                                             |
| `configuration.connection.network_proxy.ssl_enabled`            | Whether or not to use an SSL encrypted connection when the Agents connect to the proxy server                                                                                                                                             |
| `configuration.connection.network_proxy.ssl_verify_certificate` | Whether or not to validate the authenticity of the certificate provided by the proxy server                                                                                                                                               |
| `configuration.connection.network_proxy.ca_certificate_path`    | The path to the CA certificate, relative to the systems on which the Sysdig Agent is being installed, to use when connecting to the configured proxy server                                                                               |
| `configuration.agent.driver.type`                               | The syscall driver for the Sysdig Agent to use (`kmodule` or `ebpf`)                                                                                                                                                                      |
| `configuration.agent.driver.install_build_dependencies`         | In addition to the Sysdig Agent, install the various packages needed to build either the kernel module or eBPF probe                                                                                                                      |
| `configuration.agent.override`                                  | Content to directly insert into the generated Sysdig Agent configuration                                                                                                                                                                  |
| `configuration.agent.version`                                   | The version of the Sysdig Agent to install                                                                                                                                                                                                |
| `configuration.monitoring`                                      | The Sysdig Monitor use case to install. `standard` or `disabled`                                                                                                                                                                          |
| `configuration.security`                                        | The Sysdig Secure use case to install. `standard`, `light`, or `disabled`                                                                                                                                                                 |
| `features.monitoring.application_checks`                        | The configuration to use for App Checks. See the [docs](https://docs.sysdig.com/en/docs/sysdig-monitor/integrations/working-with-integrations/legacy-integrations/legacyintegrate-applications-default-app-checks/) for more details      |
| `features.monitoring.jmx`                                       | The configuration to use for JMX monitoring. See the [docs](https://docs.sysdig.com/en/docs/sysdig-monitor/integrations/working-with-integrations/custom-integrations/integrate-jmx-metrics-from-java-virtual-machines/) for more details |
| `features.monitoring.statsd`                                    | The configuration to use for StatsD monitoring. See the [docs](https://docs.sysdig.com/en/docs/sysdig-monitor/integrations/working-with-integrations/custom-integrations/integrate-statsd-metrics/) for more details                      |
| `features.monitoring.prometheus`                                | The configuration to use for Prometheus monitoring. See the [docs](https://docs.sysdig.com/en/docs/sysdig-monitor/integrations/working-with-integrations/custom-integrations/collect-prometheus-metrics/) for more details                |
| `features.security.activity_audit`                              | Advanced configuration for the Sysdig Activity Audit functionality                                                                                                                                                                        |
| `features.security.captures`                                    |                                                                                                                                                                                                                                           |
| `features.security.drift_detection`                             | Advanced configuration for Sysdig Drift Control. See the [docs](https://docs.sysdig.com/en/docs/sysdig-secure/policies/threat-detect-policies/#understanding-driftcontrol) for more details                                               |
| `features.security.image_profiling`                             | Advanced configuration for the Sysdig Image Profiling functionality                                                                                                                                                                       |

# Sample Configurations
## Sysdig Monitor and Sysdig Secure
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
      monitoring: standard
      security: standard
```
## Sysdig Monitor Only
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
      monitoring: standard
      security: disabled
```
## Sysdig Secure Only
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
      monitoring: disabled 
      security: standard
```
## OnPremise (Custom Endpoint)
```yaml
- hosts: hosts
  become: true
  roles:
  - role: sysdig.agent.agent_install
    vars:
    configuration:
      connection:
        access_key: <your_sysdig_access_key>
        custom_endpoint: 
          url: <custom_endpoint_url>
          port: <custom_endpoint_port>
      monitoring: standard 
      security: standard
```
## Sysdig Monitor with JMX disabled
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
      monitoring: standard 
      security: disabled
    features:
      monitoring:
        jmx:
          enabled: false
```