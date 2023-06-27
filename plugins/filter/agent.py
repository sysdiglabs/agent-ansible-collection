def to_agent_driver_type(data):
    """ Return the desired Sysdig Agent driver type """
    try:
        return data['agent']['driver']['type']
    except KeyError:
        return "kmodule"


def to_agent_version(data):
    """ Returns the agent version to install if provided, otherwise empty string
    """
    try:
        return data['agent']['version']
    except KeyError:
        return "latest"


def to_agent_install_probe_build_dependencies(data):
    """ Return true or false depending on if the probe (ebpf|kmodule) build
    dependencies should be installed
    """
    try:
        return data['agent']['driver']['install_build_dependencies']
    except KeyError:
        return False


class FilterModule:
    def filters(self):
        return {
            "toAgentDriverType": to_agent_driver_type,
            "toAgentVersion": to_agent_version,
            "toAgentInstallProbeBuildDependencies": to_agent_install_probe_build_dependencies
        }
