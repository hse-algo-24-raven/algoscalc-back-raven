from src.internal.errors import AlgorithmValueError


def find_count_string(text: str, findtext: str) -> int:
    if not isinstance(text, str) or not isinstance(findtext, str):
        raise AlgorithmValueError("Значения не строковые")

    count = 0

    if len(findtext) == 1:
        return text.lower().count(findtext)
    find_text_split = findtext.lower().split(" ")
    text_split = text.lower().split(" ")

    num = 0

    for i in range(len(text_split)):
        num = 0
        for j in range(len(find_text_split)):
            if find_text_split[j] in text_split[i]:
                num += 1
                i += 1
        if num == len(find_text_split):
            count += 1

    return count


def main(text, findtext):
    return {"num_count": find_count_string(text, findtext)}


if __name__ == "__main__":
    cnt = find_count_string("text is very long", "text is very long")
    print(f"Num_count = {cnt}")
