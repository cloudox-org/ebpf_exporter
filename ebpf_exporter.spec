%global debug_package %{nil}
%global user prometheus
%global group prometheus

Name: ebpf_exporter
Version: 2.5.1
Release: 1%{?dist}
Summary: Prometheus exporter for custom eBPF metrics
License: MIT
URL:     https://github.com/cloudflare/ebpf_exporter

Source0: https://github.com/cloudflare/ebpf_exporter/releases/download/v%{version}/%{name}.x86_64
Source1: %{name}.unit
Source2: %{name}.default
Source3: https://raw.githubusercontent.com/cloudflare/%{name}/v%{version}/examples/biolatency.yaml

%{?systemd_requires}
Requires(pre): shadow-utils

%description
eBPF exporter allows you to write eBPF code and export metrics that are not otherwise accessible from the Linux kernel.

%prep

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{SOURCE0} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/prometheus/%{name}.yml

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/prometheus/%{name}.yml

%changelog
* Thu Apr 06 2026 Ivan Garcia <igarcia@cloudox.org> - 2.5.1
- Initial packaging for the 2.5.1 branch
