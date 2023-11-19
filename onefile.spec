# -*- mode: python ; coding: utf-8 -*-

added_data = [
	( 'texture', 'texture' ), 
	( 'texture/guns', 'texture/guns' ), 
	( 'texture/items', 'texture/items' ), 
	( 'texture/maps', 'texture/maps' ), 
	( 'sound', 'sound' ), 
	( 'sound/item_sounds', 'sound/item_sounds' ), 
	( 'sound/radio_chatter', 'sound/radio_chatter' ), 
	( 'sound/scrollbarclicks', 'sound/scrollbarclicks' ), 	
	( 'sound/sfx', 'sound/sfx' ), 
	( 'sound/songs', 'sound/songs' ), 
	( 'bended', 'bended' ), 
	( 'anim/expl_blood', 'anim/expl_blood' ), 
	( 'anim/expl1', 'anim/expl1' ), 
	( 'anim/glitch', 'anim/glitch' ), 
	( 'anim/intro1', 'anim/intro1' ), 
	( 'anim/intro2', 'anim/intro2' ), 
	( 'anim/intro3', 'anim/intro3' ), 
	( 'anim/intro4', 'anim/intro4' ), 
	( 'anim/intro5', 'anim/intro5' ), 
	( 'anim/intro6', 'anim/intro6' ), 
	( 'anim/intro7', 'anim/intro7' ), 
	( 'anim/intro8', 'anim/intro8' ), 
	( 'anim/vs', 'anim/vs' ), 
]

block_cipher = None


a = Analysis(
    ['C:\\Users\\Reset\\Documents\\GitHub\\OVRDOZE\\RUN.py'],
    pathex=[],
    binaries=[],
    datas=added_data,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OVRDOZE',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='texture/icon.png',
)
