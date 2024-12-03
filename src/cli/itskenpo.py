from common.selenium_factory import NotReadyError, SeleniumFactory
from itskenpo.itskenpo import Itskenpo


def main() -> None:
    try:
        SeleniumFactory.validate()
    except NotReadyError:
        print("Seleniumのコンテナが起動していません")
        return
    Itskenpo().execute()


if __name__ == "__main__":
    # python -m src.cli.itskenpo
    main()
