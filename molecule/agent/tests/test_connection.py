import yaml

# Test that the agent(s) have created a connection to the backend


def test_conn_settings(host):
    f = host.file("/opt/draios/etc/dragent.yaml")
    y = yaml.safe_load(f.content_string)
    assert "collector" in y
    assert y["collector"]
    assert "customerid" in y
    assert y["customerid"]


def test_be_connection(host):
    with host.sudo():
        f = host.file("/opt/draios/logs/draios.log")

        assert f.contains("Processing messages")
        assert f.contains("Sent msgtype=1")


def test_conn_failure(host):
    with host.sudo():
        f = host.file("/opt/draios/logs/draios.log")

        assert not f.contains("connect():IOException: Host not found")
        assert not f.contains("Connection attempt failed. Retrying...")
