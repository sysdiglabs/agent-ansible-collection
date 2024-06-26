from ansible.utils.display import Display
from distutils.version import LooseVersion

def to_agent_driver_type(data):
    """ Return the desired Sysdig Agent driver type """
    try:
        user_input = data['agent']['driver']['type']
        if user_input == "ebpf":
            Display().warning("'ebpf' is a deprecated option for agent.driver.type.  Please use 'legacy_ebpf' instead.")
            return "legacy_ebpf"
        if user_input == "kmodule":
            Display().warning("'kmodule' is a deprecated option for agent.driver.type.  Please use 'kmod' instead.")
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


def to_agent_version_pinned(data):
    """ Returns True when the agent version to install is pinned, False otherwise
    """
    v = to_agent_version(data)
    if v and v != '' and v != "latest":
        return True
    return False

def to_agent_install_packages(data):
    """ Returns the agent packages to install
    """
    pinned = to_agent_version_pinned(data)
    older = False
    if pinned:
        version = to_agent_version(data)
        minver = LooseVersion("1.0.0")
        maxver = LooseVersion("13.1.0")
        older = minver < LooseVersion(version) < maxver
    if older:
        return ["draios-agent"]
    package_map = {
        "universal_ebpf": ["draios-agent-slim"],
        "legacy_ebpf": ["draios-agent-slim", "draios-agent-legacy-ebpf"],
        "kmod": ["draios-agent", "draios-agent-slim", "draios-agent-kmodule"]
    }
    return package_map[to_agent_driver_type(data)]

def to_agent_uninstall_packages(data):
    """ Return the list of packages to be uninstalled
    """
    all_packages = ["draios-agent", "draios-agent-legacy-ebpf", "draios-agent-slim", "draios-agent-kmodule"]
    return [p for p in all_packages if p not in to_agent_install_packages(data)]

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
            "toAgentVersionPinned": to_agent_version_pinned,
            "toAgentInstallPackages": to_agent_install_packages,
            "toAgentUninstallPackages": to_agent_uninstall_packages,
            "toAgentInstallProbeBuildDependencies": to_agent_install_probe_build_dependencies
        }
