from abc import ABCMeta, abstractmethod


class UserSettings(metaclass=ABCMeta):
    def __init__(self, configuration: dict, features: dict):
        self._configuration = configuration
        self._features = features


class UserPlanSettings(UserSettings):
    def is_enabled(self) -> bool:
        pass

    def type(self) -> str:
        pass


class UserMonitorSettings(UserPlanSettings):
    def is_enabled(self) -> bool:
        return self.type() != "disabled"

    def type(self) -> str:
        return self._configuration.get("monitoring", "standard").lower()

    @property
    def app_checks(self) -> dict:
        return self._features.get("app_checks", {})

    @property
    def jmx(self) -> dict:
        return self._features.get("jmx", {})

    @property
    def prometheus(self) -> dict:
        return self._features.get("prometheus", {})

    @property
    def statsd(self) -> dict:
        return self._features.get("statsd", {})


class UserSecureSettings(UserPlanSettings):
    def is_enabled(self) -> bool:
        return self.type() != "disabled"

    def type(self) -> str:
        return self._configuration.get("security", "standard").lower()

    @property
    def secure_audit_streams(self) -> dict:
        return self._features.get("activity_audit", {})

    @property
    def commandlines_capture(self) -> dict:
        return self._features.get("captures", {})

    @property
    def drift_detection(self) -> dict:
        return self._features.get("drift_detection", {})

    @property
    def falcobaseline(self) -> dict:
        return self._features.get("profiling", {})

    @property
    def local_forwarder(self) -> dict:
        cfg = self._features.get("local_forwarder", {})
        cfg = cfg if cfg else {}
        enabled = True if cfg.get("enabled", False) else False

        if not enabled:
            return {}

        default_msg_types = [
            "POLICY_EVENTS",
            "SECURE_AUDIT"
        ]

        return {
            "enabled": enabled,
            "transmit_message_types":
                self._features.get("local_forwarder", {}).get("transmit_message_types", default_msg_types)
        }


class UserConnectionSettings(UserSettings):
    REGION_MAP = {
        "us1": "collector.sysdigcloud.com",
        "us2": "ingest-us2.app.sysdig.com",
        "us3": "ingest.us3.sysdig.com",
        "us4": "ingest.us4.sysdig.com",
        "eu1": "ingest-eu1.app.sysdig.com",
        "au1": "ingest.au1.sysdig.com"
    }

    @property
    def customerid(self) -> str:
        return self._configuration["access_key"]

    @property
    def ca_certificate(self) -> str:
        return self._configuration.get("network_proxy", {}).get("ca_certificate_path")

    @property
    def collector(self) -> str:
        if "custom_collector" in self._configuration:
            return self._configuration.get("custom_collector", {}).get("url", "please-provide-collector-url")
        elif "region" in self._configuration:
            region = self._configuration.get("region", "")
            return UserConnectionSettings.REGION_MAP[region]\
                if region in UserConnectionSettings.REGION_MAP \
                else "unknown-region-{}-specified".format(region)

    @property
    def collector_port(self) -> int:
        return self._configuration.get("custom_collector", {}).get("port")

    @property
    def proxy_defined(self) -> bool:
        return "network_proxy" in self._configuration

    @property
    def proxy_host(self) -> str:
        return self._configuration["network_proxy"].get("host")

    @property
    def proxy_port(self) -> int:
        return self._configuration["network_proxy"].get("port")

    @property
    def ssl(self) -> bool:
        return self._configuration["network_proxy"].get("ssl_enabled")

    @property
    def ssl_verify_certificate(self) -> bool:
        return self._configuration["network_proxy"].get("ssl_verify_certificate")


class UserExtraSettings(UserSettings):
    @property
    def override(self) -> dict:
        return self._configuration.get("agent", {}).get("override", {})

########################################################
# Above are User settings
# Below are Dragent config file items
########################################################


class DragentSettings(metaclass=ABCMeta):
    def __init__(self, config: dict):
        """

        :param config: All user vars
        """
        self.config = None

    def _get_config(self, keys):
        return {k: getattr(self.config, k) for k in keys if getattr(self.config, k)}

    @abstractmethod
    def generate(self) -> dict:
        """ Given the provided configuration, return a dict with the expected values set

        :return: dict
        """
        pass


class DragentConnectionSettings(DragentSettings):
    def __init__(self, config):
        super().__init__(config)
        self.config = UserConnectionSettings(configuration=config["configuration"]["connection"], features={})

    def generate(self) -> dict:
        ret = self._get_config(["collector", "collector_port", "customerid"])

        if self.config.proxy_defined:
            ret.update({'http_proxy': {k: getattr(self.config, k) for k in [
                "proxy_host",
                "proxy_port",
                "ssl",
                "ssl_verify_certificate",
                "ca_certificate"
            ] if getattr(self.config, k)}})
        return ret


class DragentMonitorSettings(DragentSettings):
    def __init__(self, config):
        super().__init__(config)
        self.config = UserMonitorSettings(configuration=config["configuration"],
                                          features=config["features"].get("monitoring", {}))

    def generate(self) -> dict:
        ret = self._get_config(["app_checks", "jmx", "prometheus", "statsd"])
        if not self.config.is_enabled():
            ret.update({feature: {"enabled": False} for feature in [
                "app_checks",
                "jmx",
                "prometheus",
                "statsd"
            ]})
        return ret


class DragentSecureSettings(DragentSettings):
    def __init__(self, config):
        super().__init__(config)
        self.config = UserSecureSettings(configuration=config["configuration"],
                                         features=config["features"].get("security", {}))

    def generate(self) -> dict:
        disabled_features = []
        if not self.config.is_enabled():
            disabled_features.extend([
                "commandlines_capture",
                "drift_control",
                "drift_killer",
                "falcobaseline",
                "network_topology",
                "secure_audit_streams"
            ])
        if self.config.type() == "light":
            disabled_features.extend([
                "drift_control",
                "drift_killer",
                "falcobaseline",
                "network_topology"
            ])

        res = self._get_config(["commandlines_capture", "drift_detection",
                                "falcobaseline", "secure_audit_streams", "local_forwarder"])
        res.update({feature: {"enabled": False} for feature in disabled_features})
        return res


class DragentExtraSettings(DragentSettings):
    def __init__(self, config):
        super().__init__(config)
        self.config = UserExtraSettings(configuration=config["configuration"], features={})

    def generate(self) -> dict:
        if self.config.override:
            return self.config.override
        return {}


class Dragent:
    def __init__(self, config: dict):
        """

        :param config:
        """
        self._config_types = [
            DragentConnectionSettings(config=config),
            DragentMonitorSettings(config=config),
            DragentSecureSettings(config=config),
            DragentExtraSettings(config=config)
        ]

    @staticmethod
    def _patch_configuration(config: dict) -> dict:
        if not config.get("app_checks"):
            return config

        if "enabled" in config["app_checks"]:
            config.update({"app_checks_enabled": config["app_checks"]["enabled"]})

            if not config["app_checks"]["enabled"]:
                del config["app_checks"]
            else:
                del config["app_checks"]["enabled"]

        if config.get("app_checks", {}).get("applications"):
            config["app_checks"] = config["app_checks"]["applications"]

        return config

    def generate(self) -> dict:
        ret = {}
        for config_type in self._config_types:
            ret.update(config_type.generate())

        return self._patch_configuration(ret)


def to_dragent_configuration(data):
    return Dragent(data).generate()


class FilterModule:
    @staticmethod
    def filters():
        return {
            "toDragentConfiguration": to_dragent_configuration
        }
