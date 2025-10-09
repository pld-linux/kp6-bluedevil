#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.4.5
%define		qtver		5.15.2
%define		kpname		bluedevil
Summary:	Integrate the Bluetooth technology within KDE workspace and applications
Name:		kp6-%{kpname}
Version:	6.4.5
Release:	3
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	8aa53fc542bdfc0d6f8e4d00d8dd744e
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Quick-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-bluez-qt-devel
BuildRequires:	kf6-extra-cmake-modules >= 1.4.0
BuildRequires:	kf6-kcmutils-devel
BuildRequires:	kf6-kconfigwidgets-devel
BuildRequires:	kf6-kdbusaddons-devel
BuildRequires:	kf6-kdeclarative-devel
BuildRequires:	kf6-kded-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kio-devel
BuildRequires:	kf6-kirigami-devel
BuildRequires:	kf6-knotifications-devel
BuildRequires:	kf6-ksvg-devel
BuildRequires:	kf6-kwidgetsaddons-devel
BuildRequires:	kf6-kwindowsystem-devel
BuildRequires:	kp6-libplasma-devel >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Integrate the Bluetooth technology within KDE workspace and
applications.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang bluedevil --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun


%files -f bluedevil.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bluedevil-sendfile
%attr(755,root,root) %{_bindir}/bluedevil-wizard
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kded/bluedevil.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/kio_bluetooth.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/kio/kio_obexftp.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_bluetooth.so
%dir %{_libdir}/qt6/qml/org/kde/plasma/private/bluetooth
%{_libdir}/qt6/qml/org/kde/plasma/private/bluetooth/bluetoothplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/private/bluetooth/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/plasma/private/bluetooth/libbluetoothplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/private/bluetooth/qmldir
%{_libdir}/qt6/qml/org/kde/plasma/private/bluetooth/SharedDevicesStateProxyModel.qml
%{_desktopdir}/kcm_bluetooth.desktop
%{_desktopdir}/org.kde.bluedevilsendfile.desktop
%{_desktopdir}/org.kde.bluedevilwizard.desktop
%dir %{_datadir}/bluedevilwizard
%{_datadir}/bluedevilwizard/pin-code-database.xml
%{_datadir}/knotifications6/bluedevil.notifyrc
%{_datadir}/metainfo/org.kde.plasma.bluetooth.appdata.xml
%{_datadir}/mime/packages/bluedevil-mime.xml
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.bluetooth
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.bluetooth/contents
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.bluetooth/contents/config
%dir %{_datadir}/plasma/plasmoids/org.kde.plasma.bluetooth/contents/ui
%{_datadir}/plasma/plasmoids/org.kde.plasma.bluetooth/contents/config/main.xml
%{_datadir}/plasma/plasmoids/org.kde.plasma.bluetooth/contents/ui/DeviceItem.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.bluetooth/contents/ui/FullRepresentation.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.bluetooth/contents/ui/MediaPlayerItem.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.bluetooth/contents/ui/Toolbar.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.bluetooth/contents/ui/main.qml
%{_datadir}/plasma/plasmoids/org.kde.plasma.bluetooth/metadata.json
%{_datadir}/qlogging-categories6/bluedevil.categories
%{_datadir}/remoteview/bluetooth-network.desktop

