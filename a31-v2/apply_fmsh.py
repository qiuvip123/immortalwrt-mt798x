# -*- coding: utf-8 -*-
"""A31 FM25S01A injection: core.c manufacturer entry + spinand.h extern + Makefile objs; write fmsh.c from external file."""
import os, sys
ROOT = sys.argv[1]          # kernel source root
FM = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "fmsh.c")

# 1) core.c: insert fmsh manufacturer after winbond
core = os.path.join(ROOT, "drivers", "mtd", "nand", "spi", "core.c")
s = open(core, encoding="utf-8").read()
anchor = "\t&winbond_spinand_manufacturer,\n"
add = "\t&fmsh_spinand_manufacturer,\n"
assert anchor in s, "core.c winbond anchor missing"
assert "fmsh_spinand_manufacturer" not in s, "core.c fmsh already present"
s = s.replace(anchor, anchor + add, 1)
open(core, "w", encoding="utf-8", newline="\n").write(s)
print("core.c: fmsh manufacturer injected")

# 2) spinand.h: extern after winbond extern
h = os.path.join(ROOT, "include", "linux", "mtd", "spinand.h")
s = open(h, encoding="utf-8").read()
anchor = "extern const struct spinand_manufacturer winbond_spinand_manufacturer;\n"
add = "extern const struct spinand_manufacturer fmsh_spinand_manufacturer;\n"
assert anchor in s, "spinand.h winbond extern missing"
assert "fmsh_spinand_manufacturer" not in s, "spinand.h fmsh already present"
s = s.replace(anchor, anchor + add, 1)
open(h, "w", encoding="utf-8", newline="\n").write(s)
print("spinand.h: fmsh extern injected")

# 3) Makefile: append fmsh.o
mk = os.path.join(ROOT, "drivers", "mtd", "nand", "spi", "Makefile")
s = open(mk, encoding="utf-8").read()
old = "spinand-objs := core.o gigadevice.o macronix.o micron.o paragon.o toshiba.o winbond.o"
new = old + " fmsh.o"
assert old in s, "Makefile objs line missing"
assert "fmsh.o" not in s.split(old,1)[1].split("\n",1)[0], "fmsh.o already present"
s = s.replace(old, new, 1)
open(mk, "w", encoding="utf-8", newline="\n").write(s)
print("Makefile: fmsh.o appended")

# 4) fmsh.c
dst = os.path.join(ROOT, "drivers", "mtd", "nand", "spi", "fmsh.c")
open(dst, "w", encoding="utf-8", newline="\n").write(open(FM, encoding="utf-8").read())
print("fmsh.c written:", len(open(FM, encoding="utf-8").read().encode()), "bytes")
