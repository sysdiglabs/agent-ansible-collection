def test_agent_service_cleanup(host):
    with host.sudo():
        assert not host.file("/run/systemd/generator.late/dragent.service").exists
