# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import os.path
import re
import sys

import llnl.util.tty as tty

import spack.build_environment
import spack.util.executable


class Llvm(CMakePackage, CudaPackage):
    """The LLVM Project is a collection of modular and reusable compiler and
       toolchain technologies. Despite its name, LLVM has little to do
       with traditional virtual machines, though it does provide helpful
       libraries that can be used to build them. The name "LLVM" itself
       is not an acronym; it is the full name of the project.
    """

    homepage = "https://llvm.org/"
    url = "https://github.com/llvm/llvm-project/archive/llvmorg-7.1.0.tar.gz"
    list_url = "https://releases.llvm.org/download.html"
    git = "https://github.com/llvm/llvm-project"
    maintainers = ['trws', 'haampie']

    tags = ['e4s']

    generator = 'Ninja'

    family = "compiler"  # Used by lmod

    # fmt: off
    version('main', branch='main')
    version('13.0.0', sha256='a1131358f1f9f819df73fa6bff505f2c49d176e9eef0a3aedd1fdbce3b4630e8')
    version('12.0.1', sha256='66b64aa301244975a4aea489f402f205cde2f53dd722dad9e7b77a0459b4c8df')
    version('12.0.0', sha256='8e6c99e482bb16a450165176c2d881804976a2d770e0445af4375e78a1fbf19c')
    version('11.1.0', sha256='53a0719f3f4b0388013cfffd7b10c7d5682eece1929a9553c722348d1f866e79')
    version('11.0.1', sha256='9c7ad8e8ec77c5bde8eb4afa105a318fd1ded7dff3747d14f012758719d7171b')
    version('11.0.0', sha256='8ad4ddbafac4f2c8f2ea523c2c4196f940e8e16f9e635210537582a48622a5d5')
    version('10.0.1', sha256='c7ccb735c37b4ec470f66a6c35fbae4f029c0f88038f6977180b1a8ddc255637')
    version('10.0.0', sha256='b81c96d2f8f40dc61b14a167513d87c0d813aae0251e06e11ae8a4384ca15451')
    version('9.0.1', sha256='be7b034641a5fda51ffca7f5d840b1a768737779f75f7c4fd18fe2d37820289a')
    version('9.0.0', sha256='7807fac25330e24e9955ca46cd855dd34bbc9cc4fdba8322366206654d1036f2')
    version('8.0.1', sha256='5b18f6111c7aee7c0933c355877d4abcfe6cb40c1a64178f28821849c725c841')
    version('8.0.0', sha256='d81238b4a69e93e29f74ce56f8107cbfcf0c7d7b40510b7879e98cc031e25167')
    version('7.1.0', sha256='71c93979f20e01f1a1cc839a247945f556fa5e63abf2084e8468b238080fd839')
    version('7.0.1', sha256='f17a6cd401e8fd8f811fbfbb36dcb4f455f898c9d03af4044807ad005df9f3c0')
    version('6.0.1', sha256='aefadceb231f4c195fe6d6cd3b1a010b269c8a22410f339b5a089c2e902aa177')
    version('6.0.0', sha256='1946ec629c88d30122afa072d3c6a89cc5d5e4e2bb28dc63b2f9ebcc7917ee64')
    version('5.0.2', sha256='fe87aa11558c08856739bfd9bd971263a28657663cb0c3a0af01b94f03b0b795')
    version('5.0.1', sha256='84ca454abf262579814a2a2b846569f6e0cb3e16dc33ca3642b4f1dff6fbafd3')
    version('5.0.0', sha256='1f1843315657a4371d8ca37f01265fa9aae17dbcf46d2d0a95c1fdb3c6a4bab6')
    version('4.0.1', sha256='cd664fb3eec3208c08fb61189c00c9118c290b3be5adb3215a97b24255618be5')
    version('4.0.0', sha256='28ca4b2fc434cb1f558e8865386c233c2a6134437249b8b3765ae745ffa56a34')
    version('3.9.1', sha256='f5b6922a5c65f9232f83d89831191f2c3ccf4f41fdd8c63e6645bbf578c4ab92')
    version('3.9.0', sha256='9c6563a72c8b5b79941c773937d997dd2b1b5b3f640136d02719ec19f35e0333')
    version('3.8.1', sha256='69360f0648fde0dc3d3c4b339624613f3bc2a89c4858933bc3871a250ad02826')
    version('3.8.0', sha256='b5cc5974cc2fd4e9e49e1bbd0700f872501a8678bd9694fa2b36c65c026df1d1')
    version('3.7.1', sha256='d2cb0eb9b8eb21e07605bfe5e7a5c6c5f5f8c2efdac01ec1da6ffacaabe4195a')
    version('3.7.0', sha256='dc00bc230be2006fb87b84f6fe4800ca28bc98e6692811a98195da53c9cb28c6')
    version('3.6.2', sha256='f75d703a388ba01d607f9cf96180863a5e4a106827ade17b221d43e6db20778a')
    version('3.5.1', sha256='5d739684170d5b2b304e4fb521532d5c8281492f71e1a8568187bfa38eb5909d')
    # fmt: on

    # NOTE: The debug version of LLVM is an order of magnitude larger than
    # the release version, and may take up 20-30 GB of space. If you want
    # to save space, build with `build_type=Release`.

    variant(
        "clang",
        default=True,
        description="Build the LLVM C/C++/Objective-C compiler frontend",
    )
    variant(
        "flang",
        default=False,
        description="Build the LLVM Fortran compiler frontend "
        "(experimental - parser only, needs GCC)",
    )
    variant(
        "omp_debug",
        default=False,
        description="Include debugging code in OpenMP runtime libraries",
    )
    variant("lldb", default=True, description="Build the LLVM debugger")
    variant("lld", default=True, description="Build the LLVM linker")
    variant("mlir", default=False, description="Build with MLIR support")
    variant(
        "internal_unwind",
        default=True,
        description="Build the libcxxabi libunwind",
    )
    variant(
        "polly",
        default=True,
        description="Build the LLVM polyhedral optimization plugin, "
        "only builds for 3.7.0+",
    )
    variant(
        "libcxx",
        default=True,
        description="Build the LLVM C++ standard library",
    )
    variant(
        "compiler-rt",
        default=True,
        description="Build LLVM compiler runtime, including sanitizers",
    )
    variant(
        "gold",
        default=(sys.platform != "darwin"),
        description="Add support for LTO with the gold linker plugin",
    )
    variant(
        "split_dwarf",
        default=False,
        description="Build with split dwarf information",
    )
    variant(
        "shared_libs",
        default=False,
        description="Build all components as shared libraries, faster, "
        "less memory to build, less stable",
    )
    variant(
        "build_llvm_dylib",
        default=False,
        description="Build LLVM shared library, containing all "
        "components in a single shared library",
    )
    variant(
        "link_llvm_dylib",
        default=False,
        description="Link LLVM tools against the LLVM shared library",
    )
    variant(
        "all_targets",
        default=False,
        description="Build all supported targets, default targets "
        "<current arch>,NVPTX,AMDGPU,CppBackend",
    )
    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )
    variant(
        "omp_tsan",
        default=False,
        description="Build with OpenMP capable thread sanitizer",
    )
    variant(
        "omp_as_runtime",
        default=True,
        description="Build OpenMP runtime via ENABLE_RUNTIME by just-built Clang",
    )
    variant('code_signing', default=False,
            description="Enable code-signing on macOS")
    variant("python", default=False, description="Install python bindings")

    variant('version_suffix', default='none', description="Add a symbol suffix")
    variant('z3', default=False, description='Use Z3 for the clang static analyzer')

    extends("python", when="+python")

    # Build dependency
    depends_on("cmake@3.4.3:", type="build")
    depends_on('cmake@3.13.4:', type='build', when='@12:')
    depends_on("ninja", type="build")
    depends_on("python@2.7:2.8", when="@:4 ~python", type="build")
    depends_on("python", when="@5: ~python", type="build")
    depends_on("pkgconfig", type="build")

    # Universal dependency
    depends_on("python@2.7:2.8", when="@:4+python")
    depends_on("python", when="@5:+python")
    depends_on('z3', when='@8:+clang+z3')

    # openmp dependencies
    depends_on("perl-data-dumper", type=("build"))
    depends_on("hwloc")
    depends_on("libelf", when="+cuda")  # libomptarget
    depends_on("libffi", when="+cuda")  # libomptarget

    # ncurses dependency
    depends_on("ncurses+termlib")

    # lldb dependencies
    depends_on("swig", when="+lldb")
    depends_on("libedit", when="+lldb")
    depends_on("py-six", when="@5.0.0: +lldb +python")

    # gold support, required for some features
    depends_on("binutils+gold+ld+plugins", when="+gold")

    # polly plugin
    depends_on("gmp", when="@:3.6 +polly")
    depends_on("isl", when="@:3.6 +polly")

    conflicts("+build_llvm_dylib", when="+shared_libs")
    conflicts("+link_llvm_dylib", when="~build_llvm_dylib")
    conflicts("+lldb", when="~clang")
    conflicts("+libcxx", when="~clang")
    conflicts("+internal_unwind", when="~clang")
    conflicts("+compiler-rt", when="~clang")
    conflicts("+flang", when="~clang")
    # Introduced in version 11 as a part of LLVM and not a separate package.
    conflicts("+flang", when="@:10")

    conflicts('~mlir', when='+flang', msg='Flang requires MLIR')

    # Older LLVM do not build with newer compilers, and vice versa
    conflicts("%gcc@8:", when="@:5")
    conflicts("%gcc@:5.0", when="@8:")
    # clang/lib: a lambda parameter cannot shadow an explicitly captured entity
    conflicts("%clang@8:", when="@:4")

    # When these versions are concretized, but not explicitly with +libcxx, these
    # conflicts will enable clingo to set ~libcxx, making the build successful:

    # libc++ of LLVM13, see https://libcxx.llvm.org/#platform-and-compiler-support
    # @13 does not support %gcc@:10 https://bugs.llvm.org/show_bug.cgi?id=51359#c1
    # GCC    11     - latest stable release per GCC release page
    # Clang: 11, 12 - latest two stable releases per LLVM release page
    # AppleClang 12 - latest stable release per Xcode release page
    conflicts("%gcc@:10",         when="@13:+libcxx")
    conflicts("%clang@:10",       when="@13:+libcxx")
    conflicts("%apple-clang@:11", when="@13:+libcxx")

    # libcxx-4 and compiler-rt-4 fail to build with "newer" clang and gcc versions:
    conflicts('%gcc@7:',         when='@:4+libcxx')
    conflicts('%clang@6:',       when='@:4+libcxx')
    conflicts('%apple-clang@6:', when='@:4+libcxx')
    conflicts('%gcc@7:',         when='@:4+compiler-rt')
    conflicts('%clang@6:',       when='@:4+compiler-rt')
    conflicts('%apple-clang@6:', when='@:4+compiler-rt')

    # OMP TSAN exists in > 5.x
    conflicts("+omp_tsan", when="@:5")

    # OpenMP via ENABLE_RUNTIME restrictions
    conflicts("+omp_as_runtime", when="~clang", msg="omp_as_runtime requires clang being built.")
    conflicts("+omp_as_runtime", when="@:11.1", msg="omp_as_runtime works since LLVM 12.")

    # cuda_arch value must be specified
    conflicts("cuda_arch=none", when="+cuda", msg="A value for cuda_arch must be specified.")

    # MLIR exists in > 10.x
    conflicts("+mlir", when="@:9")

    # code signing is only necessary on macOS",
    conflicts('+code_signing', when='platform=linux')
    conflicts('+code_signing', when='platform=cray')

    conflicts(
        '+code_signing',
        when='~lldb platform=darwin',
        msg="code signing is only necessary for building the "
            "in-tree debug server on macOS. Turning this variant "
            "off enables a build of llvm with lldb that uses the "
            "system debug server",
    )

    # LLVM bug https://bugs.llvm.org/show_bug.cgi?id=48234
    # CMake bug: https://gitlab.kitware.com/cmake/cmake/-/issues/21469
    # Fixed in upstream versions of both
    conflicts('^cmake@3.19.0', when='@6.0.0:11.0.0')

    # Github issue #4986
    patch("llvm_gcc7.patch", when="@4.0.0:4.0.1+lldb %gcc@7.0:")

    # sys/ustat.h has been removed in favour of statfs from glibc-2.28. Use fixed sizes:
    patch('llvm5-sanitizer-ustat.patch', when="@4:6+compiler-rt")

    # Fix lld templates: https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=230463
    patch('llvm4-lld-ELF-Symbols.patch', when="@4+lld%clang@6:")
    patch('llvm5-lld-ELF-Symbols.patch', when="@5+lld%clang@7:")

    # Fix missing std:size_t in 'llvm@4:5' when built with '%clang@7:'
    patch('xray_buffer_queue-cstddef.patch', when="@4:5+compiler-rt%clang@7:")

    # https://github.com/llvm/llvm-project/commit/947f9692440836dcb8d88b74b69dd379d85974ce
    patch('sanitizer-ipc_perm_mode.patch', when="@5:7+compiler-rt%clang@11:")
    patch('sanitizer-ipc_perm_mode.patch', when="@5:9+compiler-rt%gcc@9:")

    # github.com/spack/spack/issues/24270 and MicrosoftDemangle: %gcc@10: and %clang@13:
    patch('missing-includes.patch', when='@8:11')

    # Backport from llvm master + additional fix
    # see  https://bugs.llvm.org/show_bug.cgi?id=39696
    # for a bug report about this problem in llvm master.
    patch("constexpr_longdouble.patch", when="@6:8+libcxx")
    patch("constexpr_longdouble_9.0.patch", when="@9:10.0.0+libcxx")

    # Backport from llvm master; see
    # https://bugs.llvm.org/show_bug.cgi?id=38233
    # for a bug report about this problem in llvm master.
    patch("llvm_py37.patch", when="@4:6 ^python@3.7:")

    # https://bugs.llvm.org/show_bug.cgi?id=39696
    patch("thread-p9.patch", when="@develop+libcxx")

    # https://github.com/spack/spack/issues/19625,
    # merged in llvm-11.0.0_rc2, but not found in 11.0.1
    patch("lldb_external_ncurses-10.patch", when="@10.0.0:11.0.1+lldb")

    # https://github.com/spack/spack/issues/19908
    # merged in llvm main prior to 12.0.0
    patch("llvm_python_path.patch", when="@11.0.0")

    # Workaround for issue https://github.com/spack/spack/issues/18197
    patch('llvm7_intel.patch', when='@7 %intel@18.0.2,19.0.4')

    # Remove cyclades support to build against newer kernel headers
    # https://reviews.llvm.org/D102059
    patch('no_cyclades.patch', when='@10:12.0.0')
    patch('no_cyclades9.patch', when='@6:9')

    # The functions and attributes below implement external package
    # detection for LLVM. See:
    #
    # https://spack.readthedocs.io/en/latest/packaging_guide.html#making-a-package-discoverable-with-spack-external-find
    executables = ['clang', 'flang', 'ld.lld', 'lldb']

    @classmethod
    def filter_detected_exes(cls, prefix, exes_in_prefix):
        result = []
        for exe in exes_in_prefix:
            # Executables like lldb-vscode-X are daemon listening
            # on some port and would hang Spack during detection.
            # clang-cl and clang-cpp are dev tools that we don't
            # need to test
            if any(x in exe for x in ('vscode', 'cpp', '-cl', '-gpu')):
                continue
            result.append(exe)
        return result

    @classmethod
    def determine_version(cls, exe):
        version_regex = re.compile(
            # Normal clang compiler versions are left as-is
            r'clang version ([^ )\n]+)-svn[~.\w\d-]*|'
            # Don't include hyphenated patch numbers in the version
            # (see https://github.com/spack/spack/pull/14365 for details)
            r'clang version ([^ )\n]+?)-[~.\w\d-]*|'
            r'clang version ([^ )\n]+)|'
            # LLDB
            r'lldb version ([^ )\n]+)|'
            # LLD
            r'LLD ([^ )\n]+) \(compatible with GNU linkers\)'
        )
        try:
            compiler = Executable(exe)
            output = compiler('--version', output=str, error=str)
            if 'Apple' in output:
                return None
            match = version_regex.search(output)
            if match:
                return match.group(match.lastindex)
        except spack.util.executable.ProcessError:
            pass
        except Exception as e:
            tty.debug(e)

        return None

    @classmethod
    def determine_variants(cls, exes, version_str):
        variants, compilers = ['+clang'], {}
        lld_found, lldb_found = False, False
        for exe in exes:
            if 'clang++' in exe:
                compilers['cxx'] = exe
            elif 'clang' in exe:
                compilers['c'] = exe
            elif 'flang' in exe:
                variants.append('+flang')
                compilers['fc'] = exe
                compilers['f77'] = exe
            elif 'ld.lld' in exe:
                lld_found = True
                compilers['ld'] = exe
            elif 'lldb' in exe:
                lldb_found = True
                compilers['lldb'] = exe

        variants.append('+lld' if lld_found else '~lld')
        variants.append('+lldb' if lldb_found else '~lldb')

        return ''.join(variants), {'compilers': compilers}

    @classmethod
    def validate_detected_spec(cls, spec, extra_attributes):
        # For LLVM 'compilers' is a mandatory attribute
        msg = ('the extra attribute "compilers" must be set for '
               'the detected spec "{0}"'.format(spec))
        assert 'compilers' in extra_attributes, msg
        compilers = extra_attributes['compilers']
        for key in ('c', 'cxx'):
            msg = '{0} compiler not found for {1}'
            assert key in compilers, msg.format(key, spec)

    @property
    def cc(self):
        msg = "cannot retrieve C compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('c', None)
        result = None
        if '+clang' in self.spec:
            result = os.path.join(self.spec.prefix.bin, 'clang')
        return result

    @property
    def cxx(self):
        msg = "cannot retrieve C++ compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('cxx', None)
        result = None
        if '+clang' in self.spec:
            result = os.path.join(self.spec.prefix.bin, 'clang++')
        return result

    @property
    def fc(self):
        msg = "cannot retrieve Fortran compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('fc', None)
        result = None
        if '+flang' in self.spec:
            result = os.path.join(self.spec.prefix.bin, 'flang')
        return result

    @property
    def f77(self):
        msg = "cannot retrieve Fortran 77 compiler [spec is not concrete]"
        assert self.spec.concrete, msg
        if self.spec.external:
            return self.spec.extra_attributes['compilers'].get('f77', None)
        result = None
        if '+flang' in self.spec:
            result = os.path.join(self.spec.prefix.bin, 'flang')
        return result

    @run_before('cmake')
    def codesign_check(self):
        if self.spec.satisfies("+code_signing"):
            codesign = which('codesign')
            mkdir('tmp')
            llvm_check_file = join_path('tmp', 'llvm_check')
            copy('/usr/bin/false', llvm_check_file)
            try:
                codesign('-f', '-s', 'lldb_codesign', '--dryrun',
                         llvm_check_file)

            except ProcessError:
                # Newer LLVM versions have a simple script that sets up
                # automatically when run with sudo priviliges
                setup = Executable("./lldb/scripts/macos-setup-codesign.sh")
                try:
                    setup()
                except Exception:
                    raise RuntimeError(
                        'spack was unable to either find or set up'
                        'code-signing on your system. Please refer to'
                        'https://lldb.llvm.org/resources/build.html#'
                        'code-signing-on-macos for details on how to'
                        'create this identity.'
                    )

    def flag_handler(self, name, flags):
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
            return(None, flags, None)
        elif name == 'ldflags' and self.spec.satisfies('%intel'):
            flags.append('-shared-intel')
            return(None, flags, None)
        return(flags, None, None)

    def setup_build_environment(self, env):
        """When using %clang, add only its ld.lld-$ver and/or ld.lld to our PATH"""
        if self.compiler.name in ['clang', 'apple-clang']:
            for lld in 'ld.lld-{0}'.format(self.compiler.version.version[0]), 'ld.lld':
                bin = os.path.join(os.path.dirname(self.compiler.cc), lld)
                sym = os.path.join(self.stage.path, 'ld.lld')
                if os.path.exists(bin) and not os.path.exists(sym):
                    mkdirp(self.stage.path)
                    os.symlink(bin, sym)
            env.prepend_path('PATH', self.stage.path)

    def setup_run_environment(self, env):
        if "+clang" in self.spec:
            env.set("CC", join_path(self.spec.prefix.bin, "clang"))
            env.set("CXX", join_path(self.spec.prefix.bin, "clang++"))
        if "+flang" in self.spec:
            env.set("FC", join_path(self.spec.prefix.bin, "flang"))
            env.set("F77", join_path(self.spec.prefix.bin, "flang"))

    root_cmakelists_dir = "llvm"

    def cmake_args(self):
        spec = self.spec
        define = CMakePackage.define
        from_variant = self.define_from_variant

        python = spec['python']
        cmake_args = [
            define("LLVM_REQUIRES_RTTI", True),
            define("LLVM_ENABLE_RTTI", True),
            define("LLVM_ENABLE_EH", True),
            define("CLANG_DEFAULT_OPENMP_RUNTIME", "libomp"),
            define("PYTHON_EXECUTABLE", python.command.path),
            define("LIBOMP_USE_HWLOC", True),
            define("LIBOMP_HWLOC_INSTALL_DIR", spec["hwloc"].prefix),
        ]

        version_suffix = spec.variants['version_suffix'].value
        if version_suffix != 'none':
            cmake_args.append(define('LLVM_VERSION_SUFFIX', version_suffix))

        if python.version >= Version("3"):
            cmake_args.append(define("Python3_EXECUTABLE", python.command.path))
        else:
            cmake_args.append(define("Python2_EXECUTABLE", python.command.path))

        projects = []
        runtimes = []

        if "+cuda" in spec:
            cmake_args.extend([
                define("CUDA_TOOLKIT_ROOT_DIR", spec["cuda"].prefix),
                define("LIBOMPTARGET_NVPTX_COMPUTE_CAPABILITIES",
                       ",".join(spec.variants["cuda_arch"].value)),
                define("CLANG_OPENMP_NVPTX_DEFAULT_ARCH",
                       "sm_{0}".format(spec.variants["cuda_arch"].value[-1])),
            ])
            if "+omp_as_runtime" in spec:
                cmake_args.extend([
                    define("LIBOMPTARGET_NVPTX_ENABLE_BCLIB", True),
                    # work around bad libelf detection in libomptarget
                    define("LIBOMPTARGET_DEP_LIBELF_INCLUDE_DIR",
                           spec["libelf"].prefix.include),
                ])
        else:
            # still build libomptarget but disable cuda
            cmake_args.extend([
                define("CUDA_TOOLKIT_ROOT_DIR", "IGNORE"),
                define("CUDA_SDK_ROOT_DIR", "IGNORE"),
                define("CUDA_NVCC_EXECUTABLE", "IGNORE"),
                define("LIBOMPTARGET_DEP_CUDA_DRIVER_LIBRARIES", "IGNORE"),
            ])

        cmake_args.append(from_variant("LIBOMPTARGET_ENABLE_DEBUG", "omp_debug"))

        if "+lldb" in spec:
            if spec.version >= Version('10'):
                cmake_args.append(from_variant("LLDB_ENABLE_PYTHON", 'python'))
            else:
                cmake_args.append(define("LLDB_DISABLE_PYTHON",
                                         '~python' in spec))
            if spec.satisfies("@5.0.0: +python"):
                cmake_args.append(define("LLDB_USE_SYSTEM_SIX", True))

        if "+gold" in spec:
            cmake_args.append(
                define("LLVM_BINUTILS_INCDIR", spec["binutils"].prefix.include)
            )

        if "+clang" in spec:
            projects.append("clang")
            projects.append("clang-tools-extra")
            if "+omp_as_runtime" in spec:
                runtimes.append("openmp")
            else:
                projects.append("openmp")

            if self.spec.satisfies("@8"):
                cmake_args.append(define('CLANG_ANALYZER_ENABLE_Z3_SOLVER',
                                         self.spec.satisfies('@8+z3')))
            if self.spec.satisfies("@9:"):
                cmake_args.append(define('LLVM_ENABLE_Z3_SOLVER',
                                         self.spec.satisfies('@9:+z3')))

        if "+flang" in spec:
            projects.append("flang")
        if "+lldb" in spec:
            projects.append("lldb")
        if "+lld" in spec:
            projects.append("lld")
        if "+compiler-rt" in spec:
            projects.append("compiler-rt")
        if "+libcxx" in spec:
            projects.append("libcxx")
            projects.append("libcxxabi")
        if "+mlir" in spec:
            projects.append("mlir")
        if "+internal_unwind" in spec:
            projects.append("libunwind")
        if "+polly" in spec:
            projects.append("polly")
            cmake_args.append(define("LINK_POLLY_INTO_TOOLS", True))

        cmake_args.extend([
            from_variant("BUILD_SHARED_LIBS", "shared_libs"),
            from_variant("LLVM_BUILD_LLVM_DYLIB", "build_llvm_dylib"),
            from_variant("LLVM_LINK_LLVM_DYLIB", "link_llvm_dylib"),
            from_variant("LLVM_USE_SPLIT_DWARF", "split_dwarf"),
            # By default on Linux, libc++.so is a ldscript. CMake fails to add
            # CMAKE_INSTALL_RPATH to it, which fails. Statically link libc++abi.a
            # into libc++.so, linking with -lc++ or -stdlib=libc++ is enough.
            define('LIBCXX_ENABLE_STATIC_ABI_LIBRARY', True)
        ])

        if "+all_targets" not in spec:  # all is default on cmake

            targets = ["NVPTX", "AMDGPU"]
            if spec.version < Version("3.9.0"):
                # Starting in 3.9.0 CppBackend is no longer a target (see
                # LLVM_ALL_TARGETS in llvm's top-level CMakeLists.txt for
                # the complete list of targets)
                targets.append("CppBackend")

            if spec.target.family in ("x86", "x86_64"):
                targets.append("X86")
            elif spec.target.family == "arm":
                targets.append("ARM")
            elif spec.target.family == "aarch64":
                targets.append("AArch64")
            elif spec.target.family in ("sparc", "sparc64"):
                targets.append("Sparc")
            elif spec.target.family in ("ppc64", "ppc64le", "ppc", "ppcle"):
                targets.append("PowerPC")

            cmake_args.append(define("LLVM_TARGETS_TO_BUILD", targets))

        cmake_args.append(from_variant("LIBOMP_TSAN_SUPPORT", "omp_tsan"))

        if self.compiler.name == "gcc":
            compiler = Executable(self.compiler.cc)
            gcc_output = compiler('-print-search-dirs', output=str, error=str)

            for line in gcc_output.splitlines():
                if line.startswith("install:"):
                    # Get path and strip any whitespace
                    # (causes oddity with ancestor)
                    gcc_prefix = line.split(":")[1].strip()
                    gcc_prefix = ancestor(gcc_prefix, 4)
                    break
            cmake_args.append(define("GCC_INSTALL_PREFIX", gcc_prefix))

        if self.spec.satisfies("~code_signing platform=darwin"):
            cmake_args.append(define('LLDB_USE_SYSTEM_DEBUGSERVER', True))

        # Semicolon seperated list of projects to enable
        cmake_args.append(define("LLVM_ENABLE_PROJECTS", projects))

        # Semicolon seperated list of runtimes to enable
        if runtimes:
            cmake_args.append(define("LLVM_ENABLE_RUNTIMES", runtimes))

        return cmake_args

    @run_after("install")
    def post_install(self):
        spec = self.spec
        define = CMakePackage.define

        # unnecessary if we build openmp via LLVM_ENABLE_RUNTIMES
        if "+cuda ~omp_as_runtime" in self.spec:
            ompdir = "build-bootstrapped-omp"
            prefix_paths = spack.build_environment.get_cmake_prefix_path(self)
            prefix_paths.append(str(spec.prefix))
            # rebuild libomptarget to get bytecode runtime library files
            with working_dir(ompdir, create=True):
                cmake_args = [
                    '-G', 'Ninja',
                    define('CMAKE_BUILD_TYPE', spec.variants['build_type'].value),
                    define("CMAKE_C_COMPILER", spec.prefix.bin + "/clang"),
                    define("CMAKE_CXX_COMPILER", spec.prefix.bin + "/clang++"),
                    define("CMAKE_INSTALL_PREFIX", spec.prefix),
                    define('CMAKE_PREFIX_PATH', prefix_paths)
                ]
                cmake_args.extend(self.cmake_args())
                cmake_args.extend([
                    define("LIBOMPTARGET_NVPTX_ENABLE_BCLIB", True),
                    define("LIBOMPTARGET_DEP_LIBELF_INCLUDE_DIR",
                           spec["libelf"].prefix.include),
                    self.stage.source_path + "/openmp",
                ])

                cmake(*cmake_args)
                ninja()
                ninja("install")
        if "+python" in self.spec:
            install_tree("llvm/bindings/python", site_packages_dir)

            if "+clang" in self.spec:
                install_tree("clang/bindings/python", site_packages_dir)

        with working_dir(self.build_directory):
            install_tree("bin", join_path(self.prefix, "libexec", "llvm"))
