from rich import print


class Print:
    @staticmethod
    def success(message):
        print("=" * 20)
        print(f"[green]{message}")
        print("=" * 20)

    @staticmethod
    def error(message):
        print("=" * 20)
        print(f"[red]{message}")
        print("=" * 20)
