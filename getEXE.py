import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "main.py",
        "--onedir",
        "--noconfirm",
        "-i",
        "server/favicon.ico",
        "--add-data",
        "server;server",
        "--add-data",
        "utils/adb;adb",
        "--name",
        "WFHelper",
    ]
)
