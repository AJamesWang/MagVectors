from cx_Freeze import setup, Executable

includes = []
excludes = []
pacakges = []
path = []


GUI2Exe_Target = Executable(
	script = "MagVectors.py",
	initScript = None,
	base = 'Win32GUI',
	)