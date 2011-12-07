%define openswan_version  2.6.24-7

%define snapshot .20100411git
%define realversion 0.8

Summary:   NetworkManager VPN plug-in for openswan
Name:      NetworkManager-openswan
Version:   0.8.0
Release:   5%{snapshot}%{?dist}
License:   GPLv2+
Group:     System Environment/Base
URL:       http://people.redhat.com/avagarwa/files/NetworkManager-openswan/
# To get source, either download from the above url, or follow these commands
# Check out NetworkManager-openswan
# "cd" to specfic fedora release
# run "make test-srpm"
Source0:    http://people.redhat.com/avagarwa/files/%{name}/%{name}-%{realversion}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


Patch1: nm-secret-whack.patch
Patch2: nm-changes.patch
Patch3: nm-616910.patch

BuildRequires: gtk2-devel
#BuildRequires: dbus-devel
#BuildRequires: NetworkManager-devel
BuildRequires: NetworkManager-glib-devel
BuildRequires: GConf2-devel
BuildRequires: gnome-keyring-devel
BuildRequires: libglade2-devel
BuildRequires: intltool gettext

Requires: NetworkManager
Requires: gnome-keyring
Requires: openswan  >= %{openswan_version}


%description
This package contains software for integrating the openswan VPN software
with NetworkManager and the GNOME desktop

%prep
%setup -q  -n NetworkManager-openswan-%{realversion}

%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%configure --disable-static --enable-more-warnings=yes
make %{?_smp_mflags}

%install

make install DESTDIR=$RPM_BUILD_ROOT

rm -f %{buildroot}%{_libdir}/NetworkManager/lib*.la

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-, root, root,-)
%config /etc/NetworkManager/VPN/nm-openswan-service.name
%config /etc/dbus-1/system.d/nm-openswan-service.conf

%doc AUTHORS ChangeLog COPYING
%{_libdir}/NetworkManager/lib*.so*
%{_libexecdir}/nm-openswan-auth-dialog
%{_sysconfdir}/dbus-1/system.d/nm-openswan-service.conf
%{_sysconfdir}/NetworkManager/VPN/nm-openswan-service.name
%{_libexecdir}/nm-openswan-service
%{_libexecdir}/nm-openswan-service-helper
%{_datadir}/gnome-vpn-properties/openswan/nm-openswan-dialog.glade
%dir %{_datadir}/gnome-vpn-properties/openswan

%changelog
* Mon Jul 26 2010 Avesh Agarwal <avagarwa@redhat.com> - 0.8.0-5.20100411git
Resolves: #617016
- Support for reading phase1 and phase2 algorithms through GUI
- Fixed chanelog to reference correct bz 617016, and bumped release number.

* Tue Jul 13 2010 Avesh Agarwal  <avagarwa@redhat.com> - 0.8.0-3.20100411git
Resolves: #609595
- Due to changes in NMVpnPluginUiInterface struct in NM, import and export
  fields had to be changed to import_from_file and export_to_file, respectively
- Rebuilding as build was failing due to the above changes

* Tue Jul 13 2010 Avesh Agarwal  <avagarwa@redhat.com> - 0.8.0-2.20100411git
Resolves: #609595
- Fix to read connection configuration from stdin, so no conf file is stored now
- Fix to read Xauth user password from stdin
- Fix to delete the secret file as soon as read by Openswan
- Fixed the issue of world readable conf and secret files
- Modifed GUI to remove unused configuration boxes

* Fri Jun 18 2010 Avesh Agarwal  <avagarwa@redhat.com> - 0.8.0-1.20100411git
- Initial build
