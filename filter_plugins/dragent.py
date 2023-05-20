from abc import ABCMeta, abstractmethod


class UserSettings(metaclass=ABCMeta):
    def __init__(self, configuration: dict, features: dict):
        self._configuration = configuration
        self._features = features


class UserConnectionSettings(UserSettings):
    @property
    def access_key(self) -> str:
        return self._configuration["access_key"]

    @property
    def ca_certificate_path(self) -> str:
        return self._configuration.get("network_proxy", {}).get("ca_certificate_path")

    @property
    def collector_url(self) -> str:
        return self._configuration.get("custom_collector", {}).get("url")

    @property
    def collector_port(self) -> int:
        return self._configuration.get("custom_collector", {}).get("port")

    @property
    def proxy_defined(self) -> bool:
        return "network_proxy" in self._configuration

    @property
    def proxy_host(self) -> str:
        return self._configuration["network_proxy"].get("url")

    @property
    def proxy_port(self) -> int:
        return self._configuration["network_proxy"].get("port")

    @property
    def ssl(self) -> bool:
        return self._configuration["network_proxy"].get("ssl_enabled")

    @property
    def ssl_verify_certificate(self) -> bool:
        return self._configuration["network_proxy"].get("ssl_verify_certificate")


########################################################
# Above are User settings
# Below are Dragent config file items
########################################################


class DragentSettings(metaclass=ABCMeta):
    def __init__(self, config: dict):
        """

        :param config: All user vars
        """
        pass

    @abstractmethod
    def generate(self) -> dict:
        """ Given the provided configuration, return a dict with the expected values set

        :return: dict
        """
        pass


class DragentConnectionSettings(DragentSettings):
    def __init__(self, config):
        self.config = UserConnectionSettings(configuration=config["configuration"]["connection"], features={})
        super().__init__(config)

    def generate(self) -> dict:
        ret = {
            "collector": self.config.collector_url,
            "collector_port": self.config.collector_port,
            "customerid": self.config.access_key
        }
        if self.config.proxy_defined:
            proxy_settings = {}
            if self.config.proxy_host:
                proxy_settings.update({'proxy_host': self.config.proxy_host})
            if self.config.proxy_host:
                proxy_settings.update({'proxy_port': self.config.proxy_port})
            if self.config.ssl:
                proxy_settings.update({'ssl': self.config.ssl})
            if self.config.ssl_verify_certificate:
                proxy_settings.update({'ssl_verify_certificate': self.config.ssl_verify_certificate})
            if self.config.ca_certificate_path:
                proxy_settings.update({'ca_certificate': self.config.ca_certificate_path})
            ret.update({'http_proxy': proxy_settings})
        return ret


class Dragent:
    def __init__(self, config: dict):
        """

        :param config:
        """
        self._config_types = [
            DragentConnectionSettings(config=config)
        ]

    def generate(self) -> dict:
        ret = {}
        for config_type in self._config_types:
            ret.update(config_type.generate())
        return ret


def to_dragent_configuration(data):
    return Dragent(data).generate()


class FilterModule:
    @staticmethod
    def filters():
        return {
            "toDragentConfiguration": to_dragent_configuration
        }
