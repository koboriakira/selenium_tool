from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def print(self, *values: object) -> None:
        """メッセージを出力する"""


class CliPrinter(Printer):
    def print(self, *values: object) -> None:
        print(*values)


class NullPrinter(Printer):
    def print(self, *values: object) -> None:
        pass  # なにもしない
