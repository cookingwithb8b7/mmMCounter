# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for mmMCounter
Builds a single-file executable with all dependencies bundled
"""

block_cipher = None

a = Analysis(
    ['../src/main.py'],
    pathex=['e:\\mmmcounter'],
    binaries=[],
    datas=[
        ('../assets/sounds', 'assets/sounds'),
        ('../assets/fonts', 'assets/fonts'),
        ('../configs/profiles/default.json', 'configs/profiles'),
    ],
    hiddenimports=[
        'pynput.keyboard._win32',
        'pynput.mouse._win32',
        'pygame',
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
    name='mmMCounter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress for smaller file size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI app)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='../assets/icon.ico'  # Uncomment when icon is created
)
