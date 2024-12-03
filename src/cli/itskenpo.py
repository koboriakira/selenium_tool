from common.printer import CliPrinter
from common.selenium_factory import NotReadyError, SeleniumFactory
from itskenpo.check_reservation_usecase import CheckReservationUseCase
from itskenpo.visitor import Visitor


def main() -> None:
    try:
        SeleniumFactory.validate()
    except NotReadyError:
        print("Seleniumのコンテナが起動していません")
        return
    usecase = CheckReservationUseCase(visitor=Visitor(), printer=CliPrinter())
    usecase.execute()


if __name__ == "__main__":
    # python -m src.cli.itskenpo
    main()
