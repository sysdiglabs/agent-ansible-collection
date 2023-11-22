class LocalForwarder:
    def __init__(self, data):
        self.data = data

    def generate(self):
        integrations = self.data.get("features", {}).get("security", {}).get("local_forwarder", {}).get("integrations", [])
        return {
            "integrations": integrations
        }


def local_forwarder_configuration(data):
    return LocalForwarder(data).generate()


class FilterModule:
    def filters(self):
        return {
            "toLocalForwarderConfiguration": local_forwarder_configuration
        }
