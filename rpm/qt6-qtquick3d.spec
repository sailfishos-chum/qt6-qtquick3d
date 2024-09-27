%global  qt_version 6.7.2

Summary: Qt6 - Quick3D Libraries and utilities
Name:    qt6-qtquick3d
Version: 6.7.2
Release: 3%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
Source0: %{name}-%{version}.tar.bz2

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ninja
BuildRequires: qt6-rpm-macros >= %{qt_version}
BuildRequires: qt6-qtbase-static >= %{qt_version}
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel
BuildRequires: qt6-qtdeclarative-static
BuildRequires: qt6-qtquicktimeline-devel
BuildRequires: qt6-qtshadertools-devel


%description
The Qt 6 Quick3D library.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
Requires: qt6-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
# BuildRequires: qt6-qtquick3d-devel >= %{version}
%description examples
%{summary}.
%endif

%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
%if 0%{?rhel} >= 10
%ifarch x86_64
# The bundled embree attempts to limit optimization to SSE4.1 and disable AVX,
# but RHEL 10 defaults to -march=x86-64-v3 which includes AVX, resulting in
# build failures due to missing symbols from the AVX code which is not built.
CXXFLAGS="$CXXFLAGS -mno-avx"
%endif
%endif

# QT is known not to work properly with LTO at this point.  Some of the issues
# are being worked on upstream and disabling LTO should be re-evaluated as
# we update this change.  Until such time...
# Disable LTO
%define _lto_cflags %{nil}

%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF} \
  -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF}
#   -DQT_FEATURE_system_assimp=ON

%cmake_build


%install
%cmake_install

# hardlink files to %{_bindir}, add -qt6 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt6_bindir}
for i in * ; do
  case "${i}" in
    balsam|meshdebug|shadergen|balsamui|instancer|materialeditor|shapegen)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt6
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSES/GPL*
%{_qt6_libdir}/libQt6Quick3D.so.6*
%{_qt6_libdir}/libQt6Quick3DAssetImport.so.6*
%{_qt6_libdir}/libQt6Quick3DRuntimeRender.so.6*
%{_qt6_libdir}/libQt6Quick3DUtils.so.6*
%{_qt6_libdir}/libQt6Quick3DIblBaker.so.6*
%{_qt6_libdir}/libQt6Quick3DParticles.so.6*
%{_qt6_libdir}/libQt6Quick3DAssetUtils.so.6*
%{_qt6_libdir}/libQt6Quick3DEffects.so.6*
%{_qt6_libdir}/libQt6Quick3DHelpers.so.6*
%{_qt6_libdir}/libQt6Quick3DHelpersImpl.so*
%{_qt6_libdir}/libQt6Quick3DParticleEffects.so.6*
%{_qt6_libdir}/libQt6Quick3DGlslParser.so.6*
%dir %{_qt6_qmldir}/QtQuick3D/
%{_qt6_qmldir}/QtQuick3D/
%{_qt6_plugindir}/assetimporters/*.so

%files devel
%{_bindir}/balsam-qt6
%{_bindir}/meshdebug-qt6
%{_bindir}/shadergen-qt6
%{_bindir}/balsamui-qt6
%{_bindir}/instancer-qt6
%{_bindir}/materialeditor-qt6
%{_bindir}/shapegen-qt6
%{_qt6_bindir}/balsam
%{_qt6_bindir}/meshdebug
%{_qt6_bindir}/shadergen
%{_qt6_bindir}/balsamui
%{_qt6_bindir}/instancer
%{_qt6_bindir}/materialeditor
%{_qt6_bindir}/shapegen
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_includedir}/QtQuick3D
%{_qt6_includedir}/QtQuick3DAssetImport
%{_qt6_includedir}/QtQuick3DIblBaker
%{_qt6_includedir}/QtQuick3DParticles
%{_qt6_includedir}/QtQuick3DRuntimeRender
%{_qt6_includedir}/QtQuick3DUtils
%{_qt6_includedir}/QtQuick3DAssetUtils
%{_qt6_includedir}/QtQuick3DHelpers
%{_qt6_includedir}/QtQuick3DHelpersImpl
%{_qt6_includedir}/QtQuick3DGlslParser
%dir %{_qt6_libdir}/cmake/Qt6Quick3DIblBaker
%{_qt6_libdir}/cmake/Qt6Quick3DIblBaker/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Quick3DParticles
%{_qt6_libdir}/cmake/Qt6Quick3DParticles/*.cmake
%{_qt6_libdir}/cmake/Qt6/FindWrapQuick3DAssimp.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%ifarch x86_64 aarch64
%dir %{_qt6_libdir}/cmake/Qt6BundledEmbree/
%{_qt6_libdir}/cmake/Qt6/FindWrapBundledEmbreeConfigExtra.cmake
%{_qt6_libdir}/cmake/Qt6BundledEmbree/*.cmake
%endif
%dir %{_qt6_libdir}/cmake/Qt6Quick3D/
%{_qt6_libdir}/cmake/Qt6Quick3D/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Quick3DAssetImport/
%{_qt6_libdir}/cmake/Qt6Quick3DAssetImport/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Quick3DRuntimeRender/
%{_qt6_libdir}/cmake/Qt6Quick3DRuntimeRender/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Quick3DTools/
%{_qt6_libdir}/cmake/Qt6Quick3DTools/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Quick3DUtils/
%{_qt6_libdir}/cmake/Qt6Quick3DUtils/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Quick3DAssetUtils/
%{_qt6_libdir}/cmake/Qt6Quick3DAssetUtils/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Quick3DEffects/
%{_qt6_libdir}/cmake/Qt6Quick3DEffects/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Quick3DHelpers/
%{_qt6_libdir}/cmake/Qt6Quick3DHelpers/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Quick3DHelpersImpl/
%{_qt6_libdir}/cmake/Qt6Quick3DHelpersImpl/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Quick3DGlslParserPrivate
%{_qt6_libdir}/cmake/Qt6Quick3DGlslParserPrivate/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6Quick3DParticleEffects
%{_qt6_libdir}/cmake/Qt6Quick3DParticleEffects/*.cmake
%ifarch x86_64 aarch64
%{_qt6_libdir}/libQt6BundledEmbree.a
%endif
%{_qt6_libdir}/libQt6Quick3D.prl
%{_qt6_libdir}/libQt6Quick3D.so
%{_qt6_libdir}/libQt6Quick3DAssetImport.prl
%{_qt6_libdir}/libQt6Quick3DAssetImport.so
%{_qt6_libdir}/libQt6Quick3DRuntimeRender.prl
%{_qt6_libdir}/libQt6Quick3DRuntimeRender.so
%{_qt6_libdir}/libQt6Quick3DUtils.prl
%{_qt6_libdir}/libQt6Quick3DUtils.so
%{_qt6_libdir}/libQt6Quick3DIblBaker.prl
%{_qt6_libdir}/libQt6Quick3DIblBaker.so
%{_qt6_libdir}/libQt6Quick3DParticles.prl
%{_qt6_libdir}/libQt6Quick3DParticles.so
%{_qt6_libdir}/libQt6Quick3DAssetUtils.prl
%{_qt6_libdir}/libQt6Quick3DAssetUtils.so
%{_qt6_libdir}/libQt6Quick3DEffects.prl
%{_qt6_libdir}/libQt6Quick3DEffects.so
%{_qt6_libdir}/libQt6Quick3DHelpers.prl
%{_qt6_libdir}/libQt6Quick3DHelpers.so
%{_qt6_libdir}/libQt6Quick3DHelpersImpl.prl
%{_qt6_libdir}/libQt6Quick3DHelpersImpl.so
%{_qt6_libdir}/libQt6Quick3DGlslParser.prl
%{_qt6_libdir}/libQt6Quick3DGlslParser.so
%{_qt6_libdir}/libQt6Quick3DParticleEffects.prl
%{_qt6_libdir}/libQt6Quick3DParticleEffects.so
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_plugindir}/qmltooling/libqmldbg_quick3dprofiler.so
%{_qt6_libdir}/pkgconfig/*.pc


%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif

