###############################################################################
###############################################################################
##
##  Copyright (C) 2004-2018 Red Hat, Inc.  All rights reserved.
##
##  This copyrighted material is made available to anyone wishing to use,
##  modify, copy, or redistribute it subject to the terms and conditions
##  of the GNU General Public License v.2.
##
###############################################################################
###############################################################################

Name: gfs2-utils
Version: 3.2.0
Release: 11%{?dist}
License: GPLv2+ and LGPLv2+
Group: System Environment/Kernel
Summary: Utilities for managing the global file system (GFS2)
%ifnarch %{arm}
%{?fedora:Requires: kmod(gfs2.ko) kmod(dlm.ko)}
%endif
BuildRequires: ncurses-devel
BuildRequires: kernel-headers
BuildRequires: automake
BuildRequires: libtool
BuildRequires: zlib-devel
BuildRequires: gettext-devel
BuildRequires: bison
BuildRequires: flex
BuildRequires: libblkid-devel
BuildRequires: libuuid-devel
BuildRequires: check-devel
Requires: lvm2-lockd
Source: https://releases.pagure.org/gfs2-utils/gfs2-utils-%{version}.tar.gz
URL: https://pagure.io/gfs2-utils
Patch0: bz1622050-1-fsck_gfs2_Don_t_check_fs_formats_we_don_t_recognise.patch
Patch1: bz1622050-2-libgfs2_Fix_pointer_cast_byte_order_issue.patch
Patch2: bz1659490-gfs2_utils_Wrong_hash_value_used_to_clean_journals.patch
Patch3: bz1698858-mkfs_gfs2_Improve_alignment_of_first_resource_group.patch
Patch4: bz1757115-gfs2_5_General_updates_and_layout_improvements.patch
Patch5: bz1693000-fsck_gfs2_8_Manpage_updates.patch
Patch6: bz1839219-mkfs_gfs2_Don_t_use_i_o_limits_hints_4K_for_block_size.patch
Patch7: bz1833141-1-gfs2_jadd_Handle_out_of_space_issues.patch
Patch8: bz1833141-2-gfs2_jadd_error_handling_overhaul.patch
Patch9: bz1818983-gfs2_5_Update_some_mentions_of_gfs2_tool.patch
Patch10: bz1779806-mkfs_gfs2_Tighten_minimum_journal_size_checks.patch
Patch11: bz1942434-1-gfs2_jadd_Use_fallocate_to_preallocate_journals.patch
Patch12: bz1942434-2-gfs2_jadd_Don_t_fsync_after_each_block_written.patch


%prep
%setup -q -n gfs2-utils-%{version}
%patch0 -p1 -b .bz1622050-1-fsck_gfs2_Don_t_check_fs_formats_we_don_t_recognise
%patch1 -p1 -b .bz1622050-2-libgfs2_Fix_pointer_cast_byte_order_issue
%patch2 -p1 -b .bz1659490-gfs2_utils_Wrong_hash_value_used_to_clean_journals
%patch3 -p1 -b .bz1698858-mkfs_gfs2_Improve_alignment_of_first_resource_group
%patch4 -p1 -b .bz1757115-gfs2_5_General_updates_and_layout_improvements
%patch5 -p1 -b .bz1693000-fsck_gfs2_8_Manpage_updates
%patch6 -p1 -b .bz1839219-mkfs_gfs2_Don_t_use_i_o_limits_hints_4K_for_block_size
%patch7 -p1 -b .bz1833141-1-gfs2_jadd_Handle_out_of_space_issues
%patch8 -p1 -b .bz1833141-2-gfs2_jadd_error_handling_overhaul
%patch9 -p1 -b .bz1818983-gfs2_5_Update_some_mentions_of_gfs2_tool
%patch10 -p1 -b .bz1779806-mkfs_gfs2_Tighten_minimum_journal_size_checks
%patch11 -p1 -b .bz1942434-1-gfs2_jadd_Use_fallocate_to_preallocate_journals
%patch12 -p1 -b .bz1942434-2-gfs2_jadd_Don_t_fsync_after_each_block_written


%build
./autogen.sh
%configure
make %{_smp_mflags} V=1

%check
make check || { cat tests/testsuite.log; exit 1; }

%install
make -C gfs2 install DESTDIR=%{buildroot}
# Don't ship gfs2_{trace,lockcapture} in this package
rm -f %{buildroot}/usr/sbin/gfs2_trace
rm -f %{buildroot}/usr/sbin/gfs2_lockcapture
rm -f %{buildroot}%{_mandir}/man8/gfs2_trace.8
rm -f %{buildroot}%{_mandir}/man8/gfs2_lockcapture.8

%description
The gfs2-utils package contains a number of utilities for creating, checking,
modifying, and correcting inconsistencies in GFS2 file systems.

%files
%doc doc/COPYING.* doc/COPYRIGHT doc/*.txt
%doc doc/README.contributing doc/README.licence
%{_sbindir}/fsck.gfs2
%{_sbindir}/gfs2_grow
%{_sbindir}/gfs2_jadd
%{_sbindir}/mkfs.gfs2
%{_sbindir}/gfs2_convert
%{_sbindir}/gfs2_edit
%{_sbindir}/tunegfs2
%{_sbindir}/gfs2_withdraw_helper
%{_sbindir}/glocktop
%{_mandir}/man8/*gfs2*
%{_mandir}/man8/glocktop*
%{_mandir}/man5/*
%{_prefix}/lib/udev/rules.d/82-gfs2-withdraw.rules

%changelog
* Wed Mar 24 2021 Andrew Price <anprice@redhat.com> - 3.2.0-11
- gfs2_jadd: Use fallocate to preallocate journals
- gfs2_jadd: Don't fsync after each block written
  Resolves: rhbz#1942434

* Thu Nov 12 2020 Andrew Price <anprice@redhat.com> - 3.2.0-10
- mkfs.gfs2: Tighten minimum journal size checks
  Resolves: rhbz#1779806

* Tue Jun 09 2020 Andrew Price <anprice@redhat.com> - 3.2.0-9
- gfs2_jadd: Handle out-of-space issues
- gfs2_jadd: error handling overhaul
  Resolves: rhbz#1833141
- gfs2.5: Update some mentions of gfs2_tool
  Resolves: rhbz#1818983

* Tue Jun 02 2020 Andrew Price <anprice@redhat.com> - 3.2.0-8
- mkfs.gfs2: Don't use i/o limits hints <4K for block size
  Resolves: rhbz#1839219

* Fri Oct 18 2019 Andrew Price <anprice@redhat.com> - 3.2.0-7
- fsck.gfs2(8): Manpage updates
  Resolves: rhbz#1693000

* Wed Oct 16 2019 Andrew Price <anprice@redhat.com> - 3.2.0-6
- gfs2.5: General updates and layout improvements
  Resolves: rhbz#1757115

* Fri May 03 2019 Andrew Price <anprice@redhat.com> - 3.2.0-5
- mkfs.gfs2: Improve alignment of first resource group
  Resolves: rhbz#1698858

* Fri Dec 14 2018 Andrew Price <anprice@redhat.com> - 3.2.0-4
- gfs2-utils: Wrong hash value used to clean journals
  Resolves: rhbz#1659490

* Thu Nov 01 2018 Andrew Price <anprice@redhat.com> - 3.2.0-3
- Require lvm2-lockd
  Resolves: rhbz#1642272

* Mon Oct 01 2018 Andrew Price <anprice@redhat.com> - 3.2.0-2
- fsck.gfs2: Don't check fs formats we don't recognise
- libgfs2: Fix pointer cast byte order issue
  Resolves: rhbz#1622050

* Thu May 24 2018 Andrew Price <anprice@redhat.com> - 3.2.0-1
- New upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 13 2017 Andrew Price <anprice@redhat.com> - 3.1.10-4
- Update URL in spec file

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 28 2017 Andrew Price <anprice@redhat.com> - 3.1.10-1
- New upstream release
- Make dependency on libuuid explicit

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 07 2016 Andrew Price <anprice@redhat.com> - 3.1.9-1
- New upstream release
- Drop all patches
- Add glocktop to the package

* Mon Feb 15 2016 Andrew Price <anprice@redhat.com> - 3.1.8-7
- libgfs2: Add support for dirent.de_rahead
- gfs2_edit: Include dirent.de_rahead in directory listings
- gfs2-utils: Add a check for the de_rahead field
- libgfs2: Support the new dirent de_cookie field
  Resolves: bz#1307532

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 20 2015 Andrew Price <anprice@redhat.com> - 3.1.8-5
- Add patches to install the withdraw helper script properly:
  scripts_rename_gfs2_wd_udev_sh_to_gfs2_withdraw_helper.patch
  scripts_install_the_withdraw_helper_script.patch
  scripts_install_the_withdraw_udev_rules_script.patch
- Remove the obsolete udev script installation bits

* Tue Aug 11 2015 Andrew Price <anprice@redhat.com> - 3.1.8-4
- gfs2-utils: Fix hang on withdraw
- Install udev withdraw handler scripts

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Apr 18 2015 Andrew Price <anprice@redhat.com> - 3.1.8-2
- fsck.gfs2: replace recent i_goal fixes with simple logic

* Tue Apr 07 2015 Andrew Price <anprice@redhat.com> - 3.1.8-1
- New upstream release
- Remove perl dependency
- Update spec per the latest packaging guidelines

* Mon Sep 08 2014 Andrew Price <anprice@redhat.com> - 3.1.7-1
- New upstream release
- Drop all patches
- gfs2-utils tests: Build unit tests with consistent cpp flags

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Josh Boyer <jwboyer@fedoraproject.org> - 3.1.6-7
- Switch to using Requires on individual kernel modules
  Resolves: bz#1056191

* Fri Mar 21 2014 Andrew Price <anprice@redhat.com> - 3.1.6-6
- gfs2_grow: Don't try to open an empty string
- libgfs2: Add lgfs2 open mnt functions
- Switch is pathname mounted callers to lgfs2 open mnt
- libgfs2 Remove is pathname mounted
  Resolves: bz#1079286

* Fri Oct 04 2013 Andrew Price <anprice@redhat.com> - 3.1.6-5
- Suppress req on kernel-modules-extra for ARM arches.

* Tue Sep 17 2013 Andrew Price <anprice@redhat.com> - 3.1.6-4
- Don't use README.* for docs (it can pick up some patch files)

* Wed Aug 21 2013 Andrew Price <anprice@redhat.com> - 3.1.6-3
- Install utils into /usr/sbin instead of /sbin
  Resolves: rhbz#996539

* Mon Jul 29 2013 Andrew Price <anprice@redhat.com> - 3.1.6-2
- Don't install gfs2_lockcapture and gfs2_trace
  Resolves: rhbz#987019
- Run test suite after build (requires check-devel build req)
- Install both of the READMEs into doc/

* Wed Jul 24 2013 Andrew Price <anprice@redhat.com> - 3.1.6-1
- New upstream release
- Drop 'file' requirement - mkfs.gfs2 now uses libblkid instead
- Drop 'ncurses' requirement - dependency is added automatically
- Drop requires chkconfig and initscripts - no longer installs daemons
- Drop fix_build_on_rawhide.patch - upstream
- Add build req on libblkid-devel

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Andrew Price <anprice@redhat.com> - 3.1.5-1
- New upstream release
  Removes mount.gfs2, gfs2_tool, gfs2_quota
- Remove rawhide_transition.patch - now obsolete
- Update BuildRequires:
  Change glibc-kernheaders to kernel-headers
  Add bison and flex
- Provide a valid url for Source0
- Add fix_build_on_rawhide.patch to fix a circular dep introduced in
  bison 2.6, and a make -j race between libgfs2 and gfs2l

* Tue Aug 14 2012 Andrew Price <anprice@redhat.com> - 3.1.4-6
- Make the kernel-modules-extra requirement Fedora-specific
  Resolves bz#847955

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 17 2012 Andrew Price <anprice@redhat.com> - 3.1.4-4
- Remove commented-out sections
- Clean up some lintian warnings
- Add dependency on kernel-modules-extra as per bz#811547

* Wed Mar 07 2012 Andrew Price <anprice@redhat.com> - 3.1.4-3
- Remove redundant postinstall scriptlet

* Thu Feb  2 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.4-2
- make sure to Obsolete gfs2-cluster

* Wed Feb 01 2012 Andrew Price <anprice@redhat.com> - 3.1.4-1
- New upstream release
  Adds gfs2_lockgather script
- Remove gfs2-cluster (commented out for now)
- Remove dependency on corosynclib-devel and systemd-units
- Add rawhide_transition.patch to stop gfs_controld from building

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Andrew Price <anprice@redhat.com> - 3.1.3-1
- New upstream release
  Bugfixes and improvements to fsck.gfs2
  Fixes various other bugs
  Improve strings and translation support
- Adds gfs2-cluster systemd unit
- Removes gfs2* init scripts

* Wed Jul 06 2011 Andrew Price <anprice@redhat.com> - 3.1.2-1
- New upstream release
  Fixes several bugs
  Improves translation support
  Adds savemeta compression
- Add zlib-devel to BuildRequires
- Add gettext-devel to BuildRequires

* Wed May 25 2011 Steven Whitehouse <swhiteho@redhat.com> - 3.1.1-3
- Update wiki URL
- Remove gfs2_tool and gfs2_quota from package

* Fri Feb 25 2011 Bob Peterson <rpeterso@redhat.com> - 3.1.1-2
- Bumping release number to keep upgrades consistent.

* Wed Feb 23 2011 Bob Peterson <rpeterso@redhat.com> - 3.1.1-1
- gfs2_edit savemeta doesn't save all leafs for big directories
- gfs2_edit improvements
- fsck.gfs2: can't repair rgrps resulting from gfs_grow->gfs2_convert
- fsck.gfs2: reports master/root dinodes as unused and fixes bitmap

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Steven Whitehouse <swhiteho@redhat.com> - 3.1.0-4
- Drop mount.gfs2 and its man page
- Only list gfs2_tool once in the files list

* Wed Dec  8 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.0-3
- Drop circular dependency on cman

* Fri Dec  3 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 3.1.0-2
- gfs2-cluster should Obsoletes/Provides gfs-pcmk

* Tue Sep 30 2010 Steven Whitehouse <swhiteho@redhat.com> - 3.1.0-1
- Bringing this package back for upstream GFS2
  Addition of gfs2tune to the utils
  Merge of gfs_controld from cman

* Thu Jan 22 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.03.11-1
- New upstream release
  Fix several bugs and drastically improve startup errors.

* Wed Dec 10 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.03.10-1
- New upstream release
  Fix several bugs and port gfs1 code to match 2.6.27 kernel.

* Fri Oct 31 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.03.09-1
- New upstream release
  Fix rhbz#468966
  Addresses several security issues similar to CVE-2008-4192 and
  CVE-2008-4579 after deep code audit from upstream
- cleanup patches to match 2.6.26 kernel in F-9

* Tue Oct 21 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.03.08-1
- New upstream release
  Fix rhbz#460376 CVE-2008-4192
  Fix rhbz#467386 CVE-2008-4579
- cleanup/update patches to match 2.6.26 kernel in F-9

* Thu Aug 14 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.03.07-1
- New upstream release
- Fix rgmanager startup locking issues
- Apply patch to include kernel headers from 2.6.26 required to build
  userland. Userland will run in 2.6.25 compatibility mode
- Apply patch to keep kernel modules at 2.6.25 (upstream is at 2.6.26)
  (this patch is purely cosmetic since we don't build kernel modules
  but keep the source in sync is Good (tm))
- Cleanup packaging for installed docs and file permissions

* Mon Jul 14 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.03.05-1
- New upstream release
- Cleanup installed doc after upstream

* Wed Jun 11 2008 Fabio M. Di Nitto <fdinitto@redhat.com> 2.03.04-1
- New upstream release
- Resolves: #446995 #318271 #447378 #445662
- Update license tags after major upstream cleanup
- Include COPYRIGHT file

* Fri May 30 2008 Fabio M. Di Nitto <fdinitto@redhat.com> 2.03.03-1
- New upstream release
- Fix several build warnings
- Update spec files to use macros
- Update Requires to use packages rather than pointing at files
- Drop BR on kernel-devel since it's not required anymore
- Update build section to use proper _sysconfdir, libdir and sbindir
- Avoid abusing cd when we can ask make to do the work for us
- Remove /usr/sbin from file section. We don't have any file there
  and we can avoid shipping stuff by mistake

* Mon Apr 14 2008 Steven Whitehouse <swhiteho@redhat.com> 2.03.00-3
- Fabbione saves the day. We can get rid of the sed stuff after all

* Mon Apr 14 2008 Steven Whitehouse <swhiteho@redhat.com> 2.03.00-1
- New upstream sources
- Eric Sandeen's solution to kernel version dep

* Wed Apr 09 2008 Steven Whitehouse <swhiteho@redhat.com> 0.1.25.2.02.01-15
- Remove obsolete chkconfig patch for initscript
- Enable parallel make
- Remove obsolete copy of gfs2_ondisk.h (this should be in glibc-kernheaders)

* Wed Apr 09 2008 Steven Whitehouse <swhiteho@redhat.com> 0.1.25.2.02.01-14
- Update URL
- Fix license spec

* Fri Mar 14 2008 Chris Feist <cfeist@redhat.com> 0.1.25.2.02.00-2
- New upstream sources.

* Tue Jan 16 2007 Chris Feist <cfeist@redhat.com> 0.1.24-1
- New upstream sources.
- Resolves: rhbz#222747

* Wed Jan 03 2007 Chris Feist <cfeist@redhat.com> 0.1.24-1
- Updated sources
- Resolves: rhbz#218560

* Thu Dec 21 2006 Chris Feist <cfeist@redhat.com> 0.1.23-1
- Updated sources
- Resolves: rhbz#218560

* Tue Dec 19 2006 Chris Feist <cfeist@redhat.com> 0.1.22-1
- New upstream sources.
- Resolves: rhbz#219878

* Tue Dec 04 2006 Chris Feist <cfeist@redhat.com> 0.1.21-1
- New upstream sources.
- Resolves: rhbz#218134 rhbz#215962

* Thu Nov 30 2006 Chris Feist <cfeist@redhat.com> 0.1.19-1
- New upstream sources.
- Resolves: rhbz#217798

* Wed Nov 29 2006 Chris Feist <cfeist@redhat.com> 0.1.18-1
- New upstream sources.
- Resolves: rhbz#217460

* Thu Oct 26 2006 Chris Feist <cfeist@redhat.com> 0.1.14-1
- New upstream sources.

* Fri Oct 13 2006 Chris Feist <cfeist@redhat.com> 0.1.12-1
- New Upstream sources.

* Fri Oct 13 2006 Chris Feist <cfeist@redhat.com> 0.1.10-1
- New Upstream sources.

* Mon Oct 09 2006 Chris Feist <cfeist@redhat.com> 0.1.9-1
- New Upstream sources.

* Mon Sep 25 2006 Chris Feist <cfeist@redhat.com> 0.1.8-1
- New Upstream sources.

* Wed Sep 13 2006 Chris Feist <cfeist@redhat.com> 0.1.7-1
- New Upstream sources.

* Thu Sep 07 2006 Chris Feist <cfeist@redhat.com> 0.1.6-2
- Fix typo in uninstall script (turn off gfs2 instead of gfs)

* Mon Aug 28 2006 Chris Feist <cfeist@redhat.com> 0.1.6-1
- New Upstream sources.

* Tue Aug 22 2006 Chris Feist <cfeist@redhat.com> 0.1.5-1
- New Upstream sources.

* Mon Aug 14 2006 Chris Feist <cfeist@redhat.com> 0.1.3-0
- New Upstream sources, use dist tag.

* Fri Jul 14 2006 Chris Feist <cfeist@redhat.com>
- Rebuild with updated sources

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Tue Jun 27 2006 Florian La Roche <laroche@redhat.com>
- fix typo in preun script

* Fri Jun 09 2006 Chris Feist <cfeist@redhat.com> - 0.1.0-1.fc6.3
- Initial build of gfs-utils.
