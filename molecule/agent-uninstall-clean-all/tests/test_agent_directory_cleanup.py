def test_configuration_cleanup(host):
    assert not host.file("/opt/draios").exists

