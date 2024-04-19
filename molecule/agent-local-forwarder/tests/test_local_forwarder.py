def test_forwarder_emitter(host):
    with host.sudo():
        f = host.file("/opt/draios/logs/draios.log")
        assert f.contains("local forwarder enabled: true")
