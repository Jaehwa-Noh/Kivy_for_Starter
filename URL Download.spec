# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew

block_cipher = None

a = Analysis(['C:\\Users\\Jaehwa\\Github\\Kivy for Starter\\Start 11\\test.py'],
             pathex=['C:\\Users\\Jaehwa\\Github\\Kivy for Starter'],
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
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='URL Download',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )

coll = COLLECT(exe, Tree('C:\\Users\\Jaehwa\\Github\\Kivy for Starter\\Start 11\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='URL Download')
