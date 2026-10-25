# Validation scope

The workflow runs the new Aurora 2 unit tests with Python 3.11.9 on GitHub-hosted Windows Server 2022 and Ubuntu 24.04 runners. It does not install audio software or models, access the user's computer, test Windows 11 audio devices, compile Ardour, or certify a master release.

Download tests use controlled in-memory responses and temporary files, not real upstream downloads. A passing result validates only the exercised module behavior. Real HTTPS transfers and installation integration require separate tests.

No third-party Python packages are required by this test job. The existing prototype installer is not invoked or approved by this workflow. The main branch is not modified.
