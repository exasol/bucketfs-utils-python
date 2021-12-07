FROM exasol/script-language-container:python-3.6-minimal-EXASOL-6.2.0-release_SNZAIAUSLUKJOUDSHCUTK7ARK4QQGZYMP2BHE7JLHQMBQRQRRN4A

COPY release/dist /project
RUN pip install /project/*.whl


RUN mkdir -p /build_info/actual_installed_packages/release && \
    /scripts/list_installed_scripts/list_installed_apt.sh > /build_info/actual_installed_packages/release/apt_get_packages && \
    /scripts/list_installed_scripts/list_installed_pip.sh python3.6 > /build_info/actual_installed_packages/release/python3_pip_packages
