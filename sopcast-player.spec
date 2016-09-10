Name:          sopcast-player
Version:       0.8.5
Release:       1%{?dist}
Group:         Applications/Internet
Summary:       A GUI front-end to SopCast
License:       GPLv2+
URL:           http://code.google.com/p/sopcast-player/
Source0:       http://sopcast-player.googlecode.com/files/%{name}-%{version}.tar.gz
Buildroot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gettext python-setuptools desktop-file-utils
Requires:      python >= 2.4.3 vlc >= 0.9.4 vlc-devel >= 0.9.4 sp-auth >= 3.0.1
Requires:      hicolor-icon-theme pygtk2-libglade

%description
SopCast Player is designed to be an easy to use Linux GUI front-end for the p2p
streaming technology developed by SopCast. SopCast Player features an 
integrated video player, a channel guide, and bookmarks. Once SopCast Player is
installed it simply "just works" with no required configuration. 

%prep
%setup -q -n %{name}

%build
make INSTALLDIR=%{_libdir}/%{name} %{?_smp_flags}

%install
rm -fr %{buildroot}
make install INSTALLDIR=%{_libdir}/%{name} DESTDIR=%{buildroot}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
%find_lang %{name}

%clean
rm -fr %{buildroot}

%post
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Sun Feb 17 2009 Orcan Ogetbil <oget [DOT] fedora [AT] gmail [DOT] com> - 0.3.1-1
- Initial build
