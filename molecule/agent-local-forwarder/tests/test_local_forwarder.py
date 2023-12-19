def test_forwarder_emitter(host):
    f = host.file("/opt/draios/logs/draios.log")
    assert f.contains("local forwarder enabled: true")
