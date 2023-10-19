def to_agent_driver_type(data):
    """ Return the desired Sysdig Agent driver type """
    try:
        user_input = data['agent']['driver']['type']
        if user_input == "ebpf":
            return "legacy_ebpf"
        if user_input == "kmodule":
            return "kmod"
        else:
            return user_input
    except KeyError:
        return "kmod"


def to_agent_version(data):
    """ Returns the agent version to install if provided, otherwise empty string
    """
    try:
        return data['agent']['version']
    except KeyError:
        return "latest"


def to_agent_install_probe_build_dependencies(data):
    """ Return true or false depending on if the probe (legacy_ebpf|kmod) build
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
