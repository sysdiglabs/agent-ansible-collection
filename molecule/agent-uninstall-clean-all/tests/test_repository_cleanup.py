def test_repository_cleanup(host):
    with host.sudo():
        if host.file("/usr/bin/apt").exists:
            key_file = host.file("/etc/apt/trusted.gpg.d/sysdig.asc")
            repo_file = host.file("/etc/apt/sources.list.d/sysdig.list")
            assert not key_file.exists
            assert not repo_file.exists
        else:
            repo_file = host.file("/etc/yum.repos.d/draios.repo")
            assert not repo_file.exists
