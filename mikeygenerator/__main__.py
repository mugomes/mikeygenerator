"""Permite executar o aplicativo com: python -m mikeygenerator"""

from .main_window import MainWindow


def main() -> None:
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
