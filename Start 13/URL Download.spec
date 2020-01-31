# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew

block_cipher = None

a = Analysis(['C:\\Users\\Jaehwa\\Github\\Kivy for Starter\\Start 11\\test.py'],
             pathex=['C:\\Users\\Jaehwa\\Github\\Kivy for Starter\\Start 13'],
             binaries=[],
             datas=[],
             hiddenimports=[('win32timezone')],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz, Tree('C:\\Users\\Jaehwa\\Github\\Kivy for Starter\\Start 11\\'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          [],
          name='URL Download',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
