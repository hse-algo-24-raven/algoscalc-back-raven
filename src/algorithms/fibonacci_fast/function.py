def fibonacci(n: str) -> str:
    if not n.isdigit():
        raise ValueError("Переданное значение не является целым числом")

    n = int(n)

    if n == 0:
        return "0"
    if n == 1:
        return "1"

    def matrix_multiply(a, b):
        return [
            [
                a[0][0] * b[0][0] + a[0][1] * b[1][0],
                a[0][0] * b[0][1] + a[0][1] * b[1][1],
            ],
            [
                a[1][0] * b[0][0] + a[1][1] * b[1][0],
                a[1][0] * b[0][1] + a[1][1] * b[1][1],
            ],
        ]

    def matrix_power(matrix, power):
        result = [[1, 0], [0, 1]]
        base = matrix

        while power > 0:
            if power % 2 == 1:
                result = matrix_multiply(result, base)
            base = matrix_multiply(base, base)
            power //= 2

        return result

    fibonacci_matrix = [[1, 1], [1, 0]]

    result_matrix = matrix_power(fibonacci_matrix, n - 1)
    return str(result_matrix[0][0])


def main(n: str):
    return {"result": fibonacci(str(n))}


if __name__ == "__main__":
    num = "1000"
    print(f"n = {num}, n-е число Фибоначчи = {fibonacci(num)}")
