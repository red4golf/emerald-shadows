"""PyInstaller entry point for the standalone Emerald Shadows executable.

Build (from the repo root):
    pyinstaller --onefile --name EmeraldShadows --console launcher.py

The result lands in dist/EmeraldShadows.exe — a single file players can
double-click, no Python required. Saves and logs are created next to
wherever the exe is run from.
"""

from emerald_shadows.main import main

if __name__ == "__main__":
    main()
