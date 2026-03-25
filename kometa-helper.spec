# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

block_cipher = None
base_path = Path('.').resolve()

a = Analysis(
    ['main.py'],
    pathex=[str(base_path)], # This ensures PyInstaller looks in the root for 'src'
    binaries=[],
    datas=[], 
    hiddenimports=[
        'customtkinter',
        'PIL',
        'PIL._tkinter_finder',
        'yaml',
        'requests',
        'psutil',
        'packaging',
        'plyer',
        'plyer.platforms.win.notification',
    ],
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
    name='KometaHelper',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None, # Fixed: Must be capital 'None'
)
