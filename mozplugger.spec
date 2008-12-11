%define _mozillapath    %{_libdir}/mozilla/plugins

%define build_debug 0
%{?_with_debug: %{expand: %%global build_debug 1}}
%{?_without_debug: %{expand: %%global build_debug 0}}

Name:           mozplugger
Version:        1.12.0
Release:        %mkrel 1
Summary:        Generic mozilla plug-in 
License:        GPLv2+
Group:          Networking/WWW
Source0:        http://mozplugger.mozdev.org/files/mozplugger-%{version}.tar.gz
Source1:        http://umn.dl.sourceforge.net/sourceforge/mplayerplug-in/mini.tar.bz2
Source2:        mozmimetypes-1.4.1.tar.bz2
Patch0:		mozplugger-1.7.4-ooo64native.patch
Patch1:		mozplugger-1.10.1-pulseaudio.patch
Patch2:		mozplugger-1.12.0-add-extra-libs.patch
URL:            http://mozplugger.mozdev.org/
Obsoletes:      plugger
Provides:       plugger
Requires:       mikmod
Requires:       mpg123
Requires:       sox
Requires:       imagemagick
Requires:       gqview
Requires:       mplayer >= 0.90-0.rc4
Requires:       perl-base
Requires:       TiMidity++
%if %mdkversion >= 1020
Requires:       gv >= 3.6.1
%else
Requires:       gv
%endif
Requires:       xpdf
Requires:       m4
BuildRequires:  X11-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
MozPlugger is a generic Mozilla plug-in that allows the use of standard Linux
programs as plug-ins for media types on the Internet.

%prep
%setup -q -a 1 -a 2
%ifarch x86_64
%patch0 -p1 -b .64
%endif
%if %{mdkversion} >= 200810
%patch1 -p1 -b .pulse
%endif
%patch2 -p0 -b .module

%build
%if %{build_debug}
%{make} RPM_OPT_FLAGS="%{optflags} -DDEBUG" XLIBDIR="%{_usr}/X11R6/%{_lib}" linux
%else
%{make} RPM_OPT_FLAGS="%{optflags}" XLIBDIR="%{_usr}/X11R6/%{_lib}" linux
%endif

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_mozillapath}/plugins \
        %{buildroot}%{_libdir}/netscape/plugins \
        %{buildroot}%{_bindir} \
        %{buildroot}%{_sysconfdir} \
        %{buildroot}%{_mandir}/man7 \
        %{buildroot}%{_datadir}/mplayer/Skin/mini

%{__install} -p -m 755 mozplugger-helper %{buildroot}%{_bindir}
%{__install} -p -m 755 mozplugger-controller %{buildroot}%{_bindir}
%{__install} -p -m 755 mozplugger.so %{buildroot}%{_mozillapath}
%{__install} -p -m 644 mozpluggerrc %{buildroot}%{_sysconfdir}/mozpluggerrc
%{__install} -p -m 644 mozpluggerrc %{buildroot}%{_sysconfdir}/mozpluggerrc.default
%{__install} -p -m 644 mozplugger.7 %{buildroot}%{_mandir}/man7

%{__mkdir_p} %{buildroot}%{_mozillapath}
%{__ln_s} %{_mozillapath}/mozplugger.so \
         %{buildroot}%{_libdir}/netscape/plugins/mozplugger.so
%{__install} -p -m 644 mini/*.png mini/skin mini/VERSION mini/README \
        %{buildroot}%{_datadir}/mplayer/Skin/mini/

%{__install} -p -m 755 enable_mozmimetypes %{buildroot}%{_bindir}
%{__ln_s} ./enable_mozmimetypes %{buildroot}%{_bindir}/disable_mozmimetypes

%{__install} -p -m 755 mozpluggerrc-sanitize %{buildroot}%{_bindir}
%{__perl} -pi -e \
        "s|\@LIBDIR\@|%{_libdir}|g;\
         s|\@SYSCONFDIR\@|%{_sysconfdir}|g;\
         s|\@PLUGINDIR\@|%{_mozillapath}|g;\
         s|\@BINDIR\@|%{_bindir}|g;" \
                %{buildroot}%{_bindir}/mozpluggerrc-sanitize

%if %{mdkversion} >= 200900
perl -pi -e 's@ooffice2.1@ooffice3.0@g' \
%{buildroot}%{_sysconfdir}/mozpluggerrc \
       %{buildroot}%{_sysconfdir}/mozpluggerrc.default
%elseif %{mdkversion} >= 200810
perl -pi -e 's@ooffice2.1@ooffice2.4@g' \
%{buildroot}%{_sysconfdir}/mozpluggerrc \
	%{buildroot}%{_sysconfdir}/mozpluggerrc.default
%endif

%if %build_debug
export DONT_STRIP=1
%endif

%clean
%{__rm} -rf %{buildroot}


%triggerin -- acroread-nppdf
[ "$2" -ge 1 ] || exit 0
if [ -r %{_sysconfdir}/mozpluggerrc ]; then
        if [ -x %{_bindir}/disable_mozmimetypes ]; then
                %{_bindir}/disable_mozmimetypes %{_sysconfdir}/mozpluggerrc \
                        application/pdf application/x-pdf
                touch %{_mozillapath}/mozplugger.so
        fi
fi

%triggerun -- acroread-nppdf
[ "$2" = "0" ] || exit 0
if [ -r %{_sysconfdir}/mozpluggerrc ]; then
        if [ -x %{_bindir}/enable_mozmimetypes ]; then
                %{_bindir}/enable_mozmimetypes %{_sysconfdir}/mozpluggerrc \
                        application/pdf application/x-pdf
                touch %{_mozillapath}/mozplugger.so
        fi
fi

%triggerpostun -- acroread-nppdf
[ "$2" = "0" ] || exit 0
if [ -r %{_sysconfdir}/mozpluggerrc ]; then
        if [ -x %{_bindir}/enable_mozmimetypes ]; then
                %{_bindir}/enable_mozmimetypes %{_sysconfdir}/mozpluggerrc \
                        application/pdf application/x-pdf
                touch %{_mozillapath}/mozplugger.so
        fi
fi

%triggerin -- RealPlayer-rpnp
[ "$2" -ge 1 ] || exit 0
if [ -r %{_sysconfdir}/mozpluggerrc ]; then
        if [ -x %{_bindir}/disable_mozmimetypes ]; then
                %{_bindir}/disable_mozmimetypes %{_sysconfdir}/mozpluggerrc \
                        audio/x-pn-realaudio-plugin
                touch %{_mozillapath}/mozplugger.so
        fi
fi

%triggerun -- RealPlayer-rpnp
[ "$2" = "0" ] || exit 0
if [ -r %{_sysconfdir}/mozpluggerrc ]; then
        if [ -x %{_bindir}/enable_mozmimetypes ]; then
                %{_bindir}/enable_mozmimetypes %{_sysconfdir}/mozpluggerrc \
                        audio/x-pn-realaudio-plugin
                touch %{_mozillapath}/mozplugger.so
        fi
fi

%triggerpostun -- RealPlayer-rpnp
[ "$2" = "0" ] || exit 0
if [ -r %{_sysconfdir}/mozpluggerrc ]; then
        if [ -x %{_bindir}/enable_mozmimetypes ]; then
                %{_bindir}/enable_mozmimetypes %{_sysconfdir}/mozpluggerrc \
                        audio/x-pn-realaudio-plugin
                touch %{_mozillapath}/mozplugger.so
        fi
fi

%triggerin -- mplayerplugin
[ "$2" -ge 1 ] || exit 0
if [ -r %{_sysconfdir}/mozpluggerrc ]; then
        if [ -x %{_bindir}/disable_mozmimetypes ]; then
                %{_bindir}/disable_mozmimetypes %{_sysconfdir}/mozpluggerrc \
                        application/x-drm-v2 \
                        application/x-mplayer2 \
                        application/x-ogg \
                        application/x-quicktimeplayer \
                        application/x-ms-wmw \
                        application/x-nsv-vp3-mp3 \
                        audio/ogg \
                        audio/wav \
                        audio/x-ms-wax \
                        audio/x-ms-wma \
                        audio/x-wav \
                        video/anim \
                        video/dl \
                        video/fli \
                        video/mp4 \
                        video/mpeg \
                        video/msvideo \
                        video/quicktime \
                        video/sgi-movie \
                        video/x-anim \
                        video/x-dl \
                        video/x-fli \
                        video/x-mpeg \
                        video/x-mpeg2 \
                        video/x-ms-asf \
                        video/x-ms-asf-plugin \
                        video/x-msvideo \
                        video/x-ms-wm \
                        video/x-ms-wmv \
                        video/x-ms-wvx \
                        image/x-macpaint \
                        video/x-quicktime \
                        video/x-sgi-movie
                touch %{_mozillapath}/mozplugger.so
        fi
fi

%triggerun -- mplayerplugin
[ "$2" = "0" ] || exit 0
if [ -r %{_sysconfdir}/mozpluggerrc ]; then
        if [ -x %{_bindir}/enable_mozmimetypes ]; then
                %{_bindir}/enable_mozmimetypes %{_sysconfdir}/mozpluggerrc \
                        application/x-drm-v2 \
                        application/x-mplayer2 \
                        application/x-ogg \
                        application/x-quicktimeplayer \
                        application/x-ms-wmv \
                        application/x-nsv-vp3-mp3 \
                        audio/ogg \
                        audio/wav \
                        audio/x-ms-wax \
                        audio/x-ms-wma \
                        audio/x-wav \
                        video/anim \
                        video/dl \
                        video/fli \
                        video/mp4 \
                        video/mpeg \
                        video/msvideo \
                        video/quicktime \
                        video/sgi-movie \
                        video/x-anim \
                        video/x-dl \
                        video/x-fli \
                        video/x-mpeg \
                        video/x-mpeg2 \
                        video/x-ms-asf \
                        video/x-ms-asf-plugin \
                        video/x-msvideo \
                        video/x-ms-wm \
                        video/x-ms-wmv \
                        video/x-ms-wvx \
                        image/x-macpaint \
                        video/x-quicktime \
                        video/x-sgi-movie
                touch %{_mozillapath}/mozplugger.so
        fi
fi

%triggerpostun -- mplayerplugin
[ "$2" = "0" ] || exit 0
if [ -r %{_sysconfdir}/mozpluggerrc ]; then
        if [ -x %{_bindir}/enable_mozmimetypes ]; then
                %{_bindir}/enable_mozmimetypes %{_sysconfdir}/mozpluggerrc \
                        application/x-drm-v2 \
                        application/x-mplayer2 \
                        application/x-ogg \
                        application/x-quicktimeplayer \
                        application/x-ms-wmv \
                        application/x-nsv-vmp3-mp3 \
                        audio/ogg \
                        audio/wav \
                        audio/x-ms-wax \
                        audio/x-ms-wma \
                        audio/x-wav \
                        video/anim \
                        video/dl \
                        video/fli \
                        video/mp4 \
                        video/mpeg \
                        video/msvideo \
                        video/quicktime \
                        video/sgi-movie \
                        video/x-anim \
                        video/x-dl \
                        video/x-fli \
                        video/x-mpeg \
                        video/x-mpeg2 \
                        video/x-ms-asf \
                        video/x-ms-asf-plugin \
                        video/x-msvideo \
                        video/x-ms-wm \
                        video/x-ms-wmv \
                        video/x-ms-wvx \
                        image/x-macpaint \
                        video/x-quicktime \
                        video/x-sgi-movie
                touch %{_mozillapath}/mozplugger.so
        fi
fi

%triggerin -- gv >= 3.6.1
if %{__grep} -q  "gv -safer -quiet -antialias" %{_sysconfdir}/mozpluggerrc; then
        %{__perl} -pi -e "s/gv -safer -quiet -antialias/gv --safer --quiet --antialias/g" %{_sysconfdir}/mozpluggerrc
fi

%triggerin -- gv < 3.6.1
if %{__grep} "gv --safer --quiet --antialias" %{_sysconfdir}/mozpluggerrc; then
        %{__perl} -pi -e "s/gv --safer --quiet --antialias/gv -safer -quiet -antialias/g" %{_sysconfdir}/mozpluggerrc
fi

%files
%defattr(-,root,root)
%doc README COPYING
%{_bindir}/enable_mozmimetypes
%{_bindir}/disable_mozmimetypes
%{_bindir}/mozpluggerrc-sanitize
%{_bindir}/mozplugger-helper
%{_bindir}/mozplugger-controller
%{_datadir}/mplayer/Skin/mini
%{_libdir}/netscape/plugins/mozplugger.so
%{_mozillapath}/mozplugger.so
%{_mandir}/man7/mozplugger.7*
%config(noreplace) %{_sysconfdir}/mozpluggerrc
%config(noreplace) %{_sysconfdir}/mozpluggerrc.default


