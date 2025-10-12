
# THE VIPER COMPILER

Viper is a lightweight compiler for the Viper programming language — a statically typed language
built for safety, clarity, and convenience. It emphasizes clean syntax, precise semantics, and
strict type safety with well-defined scope isolation.  

The compiler enforces explicit state changes, preventing hidden side effects and reducing the
likelihood of subtle bugs.  

Viper is currently implemented entirely in Python and will use the `llvmlite` library to generate
machine code.

## GOALS

The compiler may be modified later to include extensions in C for enhancing performance, if it
becomes a bottleneck. There are also plans to rewrite the entire compiler in C if the rewrite
featuring C extensions does not fulfill its purpose.

## PRE-BUILT BINARIES

The pre-built binaries for Windows can be found in [the Releases page](http://google.com). For
Linux, pre-built binaries are not available.

## BUILDING

The compiler can be built successfully for Windows. The compiler cannot be built on Linux (at the
moment due to issues with Nuitka).

The compiler can be built with the build script `src/vbuild.py`. This script uses Nuitka to
compile to native machine code.  

Navigate to the directory `src/`, which contains `main.py`, the entry point of the program. Then,
run the following command:

```powershell
python.exe -B -OO ./vbuild.py -nass -nwarn -ndoc -nextrafl -q -op -i=<iconfl> ./main.py
```

Replace `<iconfl>` with the icon file path. If you are debugging, you might want to not specify or
remove the flags `-nass`, `-nwarn`, `-ndoc`, `-nextrafl` and `-q`.  

Execute `python.exe -B -OO ./vbuild.py -h` for help on the build script. The compiler uses
[Nuitka](http://nuitka.net) to compile Python to binaries. Make sure Nuitka is installed in the
Python environment being used. Make sure to activate the proper Python environment before
building.

## RUNNING

To run from source directly, navigate to the directory `src/` containing
`main.py`, the entry-point of the program, and run:

```powershell
python.exe -B -OO ./main.py <vifl>
```

`<vifl>` is the path of the Viper source file (`.vi`). A development source file named `main.vi`
will be present in the directory `src/dev/`.

## CONTRIBUTING

All contributions are welcome. Please contact me via GitHub if you want to contribute.

