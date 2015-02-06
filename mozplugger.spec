%define _mozillapath    %{_libdir}/mozilla/plugins

%define build_debug 0
%{?_with_debug: %{expand: %%global build_debug 1}}
%{?_without_debug: %{expand: %%global build_debug 0}}

Name:           mozplugger
Version:        1.14.6
Release:        3
Summary:        Generic mozilla plug-in 
License:        GPLv2+
Group:          Networking/WWW
Source0:        http://mozplugger.mozdev.org/files/mozplugger-%{version}.tar.gz
Source1:        http://umn.dl.sourceforge.net/sourceforge/mplayerplug-in/mini.tar.bz2
Source2:        mozmimetypes-1.4.1.tar.bz2
Patch1:		mozplugger-1.14.6-pulseaudio.patch
Patch2:		mozplugger-1.14.6-gqview.patch
URL:            http://mozplugger.mozdev.org/
Obsoletes:      plugger
Provides:       plugger
Requires:       mikmod
Requires:       mpg123
Requires:       sox
Requires:       imagemagick
Requires:       geeqie
Requires:       mplayer >= 0.90-0.rc4
Requires:       perl-base
Requires:       TiMidity++
Requires:       gv >= 3.6.1
Requires:       xpdf
Requires:       m4
BuildRequires:  pkgconfig(x11)

%description
MozPlugger is a generic Mozilla plug-in that allows the use of standard Linux
programs as plug-ins for media types on the Internet.

%prep
%setup -q -a 1 -a 2
%patch1 -p1 -b .pulse
%patch2 -p1 -b .gqview

%build
%configure
%make

%install
%{__mkdir_p} %{buildroot}%{_mozillapath}/plugins \
        %{buildroot}%{_libdir}/netscape/plugins \
        %{buildroot}%{_bindir} \
        %{buildroot}%{_sysconfdir} \
        %{buildroot}%{_mandir}/man7 \
        %{buildroot}%{_datadir}/mplayer/Skin/mini

%{__install} -p -m 755 mozplugger-helper %{buildroot}%{_bindir}
%{__install} -p -m 755 mozplugger-controller %{buildroot}%{_bindir}
%{__install} -p -m 755 mozplugger-linker %{buildroot}%{_bindir}
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
%{_bindir}/mozplugger-linker
%{_bindir}/mozplugger-controller
%{_datadir}/mplayer/Skin/mini
%{_libdir}/netscape/plugins/mozplugger.so
%{_mozillapath}/mozplugger.so
%{_mandir}/man7/mozplugger.7*
%config(noreplace) %{_sysconfdir}/mozpluggerrc
%config(noreplace) %{_sysconfdir}/mozpluggerrc.default



%changelog
* Thu May 31 2012 Guilherme Moro <guilherme@mandriva.com> 1.14.5-1
+ Revision: 801451
- Updated to version 1.14.5
  dropped useless patches

* Wed Jul 06 2011 Per Ã˜yvind Karlsen <peroyvind@mandriva.org> 1.13.3-4
+ Revision: 688931
- rebuild to get proper definition of %%__grep macro in scriptlet

* Sat Feb 05 2011 Funda Wang <fwang@mandriva.org> 1.13.3-3
+ Revision: 636132
- tighten BR

* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 1.13.3-2mdv2011.0
+ Revision: 612940
- the mass rebuild of 2010.1 packages

* Wed Apr 21 2010 Lev Givon <lev@mandriva.org> 1.13.3-1mdv2010.1
+ Revision: 537752
- Update to 1.13.3.

* Wed Jan 27 2010 Frederik Himpe <fhimpe@mandriva.org> 1.13.1-1mdv2010.1
+ Revision: 497415
- update to new version 1.13.1

* Thu Aug 27 2009 Frederik Himpe <fhimpe@mandriva.org> 1.13.0-1mdv2010.0
+ Revision: 421719
- update to new version 1.13.0

* Sun May 03 2009 Frederik Himpe <fhimpe@mandriva.org> 1.12.1-1mdv2010.0
+ Revision: 370956
- update to new version 1.12.1

* Fri Mar 06 2009 Giuseppe GhibÃ² <ghibo@mandriva.com> 1.12.0-2mdv2009.1
+ Revision: 349919
- Add missed mozplugger-linker to binaries.

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Wed Nov 19 2008 Funda Wang <fwang@mandriva.org> 1.12.0-1mdv2009.1
+ Revision: 304386
- New version 1.12.0
- compile mozplugin as module

* Fri Sep 12 2008 Funda Wang <fwang@mandriva.org> 1.11.0-1mdv2009.0
+ Revision: 284061
- New version 1.11.0

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sat Mar 29 2008 Giuseppe GhibÃ² <ghibo@mandriva.com> 1.10.2-1mdv2008.1
+ Revision: 191104
- Fix mozpluggerrc for working openoffice-2.4.
- Fix memory leak (1.10.2).

* Mon Feb 04 2008 Giuseppe GhibÃ² <ghibo@mandriva.com> 1.10.1-1mdv2008.1
+ Revision: 162383
- Update to release 1.10.1.
- Add support for pulseaudio in mplayer (first in list).

* Sun Feb 03 2008 Funda Wang <fwang@mandriva.org> 1.10.0-1mdv2008.1
+ Revision: 161658
- New version 1.10.0

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 1.8.1-2mdv2008.1
+ Revision: 153220
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sat Jun 30 2007 Funda Wang <fwang@mandriva.org> 1.8.1-1mdv2008.0
+ Revision: 46050
- New version


* Fri Mar 02 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 1.8.0-1mdv2007.0
+ Revision: 130873
- Release 1.8.0.

* Thu Jan 18 2007 Giuseppe GhibÃ² <ghibo@mandriva.com> 1.7.4-2mdv2007.1
+ Revision: 110078
- Added new Patch0 for using 64bit native OOo with higher priority

  + David Walluck <walluck@mandriva.org>
    - remove Patch0 (merged upstream)
      use parallel make
      add macros
    - 1.7.4
    - Import mozplugger

* Wed Nov 02 2005 Giuseppe Ghibò <ghibo@mandriva.com> 1.7.3-1mdk
- Release: 1.7.3.
- Merged Patches into Patch0.

* Tue Aug 30 2005 Giuseppe Ghibò <ghibo@mandriva.com> 1.7.2-3mdk
- Rebuilt Patch2 (gv).
- Added Patch1 for kdvi call.

* Tue Aug 23 2005 Giuseppe Ghibò <ghibo@mandriva.com> 1.7.2-2mdk
- mozmimetypes 1.4 (thanks to Pixel).

* Fri Apr 29 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.7.2-1mdk
- Release: 1.7.2.

* Tue Mar 29 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.7.1-7mdk
- Added support for Acrobat Reader 7.

* Mon Feb 14 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.7.1-6mdk
- Added m4 to Requires.

* Sat Jan 29 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.7.1-5mdk
- Disabled debug.

* Fri Jan 07 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.7.1-4mdk
- Added missed mozpluggerrc.default.

* Thu Jan 06 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.7.1-3mdk
- mozmimetypes-1.3.

* Thu Jan 06 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.7.1-2mdk
- Build with DEBUG enabled, for now.
- Added Patch0 for gv >= 3.6.1 (fix big #12911, from Michael Reinsch).
- mozmimetypes-1.2: added mozpluggerrc-sanitize script to
  allow sanitizing an out of sync mozpluggerrc config file with
  packages installed.

* Wed Jan 05 2005 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.7.1-1mdk
- Release: 1.7.1.
- Removed Patch1-4, merged upstream.

* Thu Dec 30 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.7.0-2mdk
- Added CVS patches for correctly resizing acrobat windows.
- Added hxplay to RealPlayer mime-types.

* Mon Dec 27 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.7.0-1mdk
- Release: 1.7.0.
- Removed Patch1->7: merged upstream.

* Wed Dec 22 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.6.1-8mdk
- Backported patch from CVS for mozplugger-helper.c to
  have windows correctly maximized.

* Mon Dec 20 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.6.1-7mdk
- Backported patch from CVS to terminate the
  process with SIGTERM instead of SIGKILL.

* Sat Dec 18 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.6.1-6mdk
- Backported patch from CVS to fix flashing window problems during
  window swallowing.

* Fri Oct 15 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.6.1-5mdk
- Fixed bug #12082 for correctly swallowing Xpdf.

* Tue Oct 05 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.6.1-4mdk
- Added Patch2, backporting patches from 1.6.2 (return
  NPPERR_GENERIC_ERROR in NPP_NewStream() when streaming; removed
  unnecessary calls to XSync and XMapWindow(); more reliable
  OpenOffice swallowing).

* Tue Oct 05 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.6.1-3mdk
- Use -ao esd,alsa,oss,arts,sdl,null and -vo xv,x11
  in mozzpluggerrc for mplayer.

* Sun Sep 19 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.6.1-2mdk
- updated enable_mozmimetypes to 1.1 (thanks to Pixel), so to avoid
  commeting/uncommenting of wrong blocks in triggers.
- added some mimetype to mozpluggerrc and fixed swallowing
  of gnumeric.

* Fri Aug 20 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.6.1-1mdk
- 1.6.1.

* Mon Jul 26 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.6.0-1mdk
- 1.6.0
- cosmetics

* Thu Apr 22 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.5.2-3mdk
- Fixed image/x-macpaint mime types in triggers.

* Fri Apr 09 2004 Giuseppe Ghibò <ghibo@mandrakesoft.com> 1.5.2-2mdk
- Added Pixel's script to add/remove mimetypes from mozpluggerrc.

* Sat Apr 03 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.5.2-1mdk
- 1.5.2
- drop P1

