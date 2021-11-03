import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "main.py",
        "--onefile",
        "--noconfirm",
        "--add-data",
        "configs;configs",
        "--add-data",
        "adb;adb",
        "--name",
        "WFHelper-emulator1440x810",
    ]
)
