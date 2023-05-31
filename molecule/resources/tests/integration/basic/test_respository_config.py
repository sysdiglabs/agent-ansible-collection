def test_repository_configuration(host):
    with host.sudo():
        if host.file("/usr/bin/apt").exists:
            f = host.file("/etc/apt/trusted.gpg.d/sysdig.asc")
            assert f.exists
            assert f.is_file
            assert f.user == "root"
            assert f.mode == 0o644
        else:
            f = host.file("/etc/yum.repos.d/draios.repo")
            assert f.exists
            assert f.is_file
            assert f.user == "root"
            assert f.mode == 0o644

            assert f.contains("""
            [draios]
            baseurl = https://download.sysdig.com/stable/rpm/$basearch
            gpgkey = https://download.sysdig.com/DRAIOS-GPG-KEY.public
            name = Sysdig Agent Repository""")
