%global goipath codeberg.org/emersion/soju
%global gomodulesmode GO111MODULE=on

Name:           soju
Version:        0.11.1
Release:        1%{?dist}
Summary:        User-friendly IRC bouncer
License:        AGPL-3.0-only AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND LicenseRef-Fedora-Public-Domain AND MIT
URL:            https://codeberg.org/emersion/soju
Source0:        https://codeberg.org/emersion/soju/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Generated with go_vendor_archive; see README.packaging.md.
Source1:        %{name}-%{version}-vendor.tar.bz2
Source2:        go-vendor-tools.toml

BuildRequires:  golang
BuildRequires:  go-rpm-macros
BuildRequires:  go-vendor-tools
BuildRequires:  askalono-cli
BuildRequires:  gcc
BuildRequires:  sqlite-devel
BuildRequires:  scdoc
BuildRequires:  systemd-rpm-macros
%{?systemd_requires}

%description
soju connects to upstream IRC servers on behalf of users and supports
multiple users, IRCv3 extensions, chat history playback and detached channels.

%prep
%setup -q -n soju -a 1
cp %{SOURCE2} .

%build
export GOFLAGS="-mod=vendor -buildvcs=false"
export GO_BUILDTAGS=libsqlite3
export GO_LDFLAGS="-X %{goipath}/config.DefaultPath=%{_sysconfdir}/soju/config -X %{goipath}/config.DefaultUnixAdminPath=%{_rundir}/soju/admin"
%gobuild -o soju ./cmd/soju
%gobuild -o sojuctl ./cmd/sojuctl
%gobuild -o sojudb ./cmd/sojudb
scdoc < doc/soju.1.scd > doc/soju.1
scdoc < doc/sojuctl.1.scd > doc/sojuctl.1

%install
install -Dm0755 soju sojuctl sojudb -t %{buildroot}%{_bindir}
install -Dm0644 doc/soju.1 doc/sojuctl.1 -t %{buildroot}%{_mandir}/man1
install -Dm0644 config.in %{buildroot}%{_sysconfdir}/soju/config
install -Dm0644 contrib/soju.service %{buildroot}%{_unitdir}/soju.service
%go_vendor_license_install -c go-vendor-tools.toml

%check
export GOFLAGS="-mod=vendor -buildvcs=false"
export GO_BUILDTAGS=libsqlite3
go test -tags libsqlite3 ./...
%go_vendor_license_check -c go-vendor-tools.toml

%post
%systemd_post soju.service

%preun
%systemd_preun soju.service

%postun
%systemd_postun_with_restart soju.service

%files -f %{go_vendor_license_filelist}
%doc README.md doc/getting-started.md
%dir %{_sysconfdir}/soju
%config(noreplace) %{_sysconfdir}/soju/config
%{_bindir}/soju
%{_bindir}/sojuctl
%{_bindir}/sojudb
%{_mandir}/man1/soju.1*
%{_mandir}/man1/sojuctl.1*
%{_unitdir}/soju.service

%changelog
* Thu Oct 29 2026 Simon de Vlieger <cmdr@supakeen.com> - 0.11.1-1
- Initial Package
