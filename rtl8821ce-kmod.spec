%global RepoName rtl8821ce_linux

%global buildforkernels akmod
%global debug_package %{nil}

Name:		    rtl8821ce-kmod
Version:	    4.3.14
Release:	    2%{?dist}
Summary:	    Realtek 8821ce driver

Group:		    System Environment/Kernel
License:	    GPLv2
URL:		    https://github.com/francescomasala/rtl8821ce_linux
Source0:	    https://github.com/francescomasala/%{RepoName}/archive/master.zip
Source11:       rtl8821ce-kmod-kmodtool-excludekernel-filterfile

%global AkmodsBuildRequires %{_bindir}/kmodtool
#, elfutils-libelf-devel
BuildRequires:  %{AkmodsBuildRequires}

%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} --obsolete-name rtl8812ce --obsolete-version "%{?epoch}:%{version}" %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Realtek 8821ce USB WiFi driver.

%prep
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null
%setup -q -c -T
mkdir %{name}-%{version}-src
pushd %{name}-%{version}-src
tar xzf %{SOURCE0}
popd

for kernel_version in %{?kernel_versions} ; do
 cp -a %{name}-%{version}-src _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}/%{RepoName}-master
 make -C ${kernel_version##*___} M=`pwd` modules
 popd
done

%install
rm -rf ${RPM_BUILD_ROOT}
for kernel_version in %{?kernel_versions}; do
 pushd _kmod_build_${kernel_version%%___*}/%{RepoName}-master
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 install -m 0755 *.ko ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}${kernel_version%%___*}%{kmodinstdir_postfix}
 popd
done

chmod 0755 $RPM_BUILD_ROOT%{kmodinstdir_prefix}*%{kmodinstdir_postfix}/* || :
%{?akmod_install}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue May 30 2017 Alexei Panov <me AT elemc DOT name> 4.3.14-2
-  Fixed obsolete-name parameter

* Tue May 30 2017 Alexei Panov <me AT elemc DOT name> 4.3.14-1
-  Initial build

