from abc import ABC, abstractmethod


class Printer(ABC):
    @abstractmethod
    def print(self, message: str) -> None:
        """メッセージを出力する"""


class CliPrinter(Printer):
    def print(self, message: str) -> None:
        print(message)


class NullPrinter(Printer):
    def print(self, message: str) -> None:
        pass  # なにもしない
