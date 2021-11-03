import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "main.py",
        "--onefile",
        "--noconfirm",
        "--add-data",
        "configs;configs",
        "--add-data",
        "utils/adb;adb",
        "--add-data",
        "server/templates;server/templates",
        "--name",
        "WFHelper",
    ]
)
