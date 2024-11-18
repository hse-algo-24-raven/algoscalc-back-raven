def fibonacci(n: str) -> str:
    pass


def main(n: int):
    return {"result": fibonacci(n)}


if __name__ == "__main__":
    num = "1000"
    print(f"n = {num}, n-е число Фибоначчи = {fibonacci(num)}")
