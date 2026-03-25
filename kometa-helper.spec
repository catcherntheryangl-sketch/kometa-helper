# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Kometa Helper
# Run: pyinstaller kometa-helper.spec

import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[str(Path('.').resolve())],
    binaries=[],
    datas=[
        ('assets', 'assets'),
    ],
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
    console=False,           # No console window — GUI app
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=none # Windows taskbar/exe icon
    version='version_info.txt',
)
