import gdb
import gdbutils

#from luajit21 import *

typ = gdbutils.typ


def is_gc64():
	t_MRef = gdb.lookup_type('MRef')
	t_GCRef = gdb.lookup_type('GCRef')
	try:
		fld_m = t_MRef['ptr64']
		fld_gc = t_GCRef['gcptr64']
		return True
	except KeyError:
		return False


if is_gc64():
	print("welcome to the brave new world!")

	LJ_GCVMASK = 2**47 - 1

	def mref(r, t):
		return r['ptr64'].cast(typ(t + "*"))

	def gcrefp(r, t):
		return r['gcptr64'].cast(typ(t + "*"))

	def gcref(r):
		return gcrefp(r, 'GCobj')

	def gcval(o):
		return (o['gcr']['gcptr64'] & LJ_GCVMASK).cast(typ('GCobj*'))

	def itype(o):
		return (o['it64'] >> 47).cast(typ('uint32_t'))

	def frame_gc(f):
		return gcval(f-1)

	def frame_ftsz(f):
		return f['ftsz']

	def frame_pc(f):
		return f['ftsz'].cast(typ('BCIns *'))
		#return mref(f['ftsz'], 'BCIns')

	def frame_contpc(f):
		return frame_pc(f - 2)

	def frame_prevl(f):
		return f - (2 + bc_a(frame_pc(f)[-1]))

else:
	print("nothing new here")
