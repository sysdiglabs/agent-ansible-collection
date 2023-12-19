class LocalForwarder:
    def __init__(self, data):
        self.data = data

    def _get_local_forwarder_settings(self) -> dict:
        return self.data.get("features", {}).get("security", {}).get("local_forwarder", {})

    def generate(self):
        integrations = self._get_local_forwarder_settings().get("integrations", [])
        return {
            "integrations": integrations
        }

    def enabled(self):
        return self._get_local_forwarder_settings().get("enabled", False)


def local_forwarder_configuration(data):
    return LocalForwarder(data).generate()


def local_forwarder_enabled(data):
    return LocalForwarder(data).enabled()


class FilterModule:
    def filters(self):
        return {
            "toLocalForwarderConfiguration": local_forwarder_configuration,
            "toLocalForwarderEnabled": local_forwarder_enabled
        }
