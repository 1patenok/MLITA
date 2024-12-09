"""Модуль: re (Regular Expressions)"""
import re


def id(token):
    """Проверка идентификатора функции."""
    return token in {'f', 'g', 'h', 'p', 'r'}


def arg(token):
    """Проверка переменной."""
    return token in {'x', 'y', 'z'}


def S(tokens):
    """Старт."""
    if not tokens:
        raise SyntaxError("Ожидалась функция")
    result = Func(tokens)
    if tokens:
        raise SyntaxError("Лишние токены после функции")
    return result


def Func(tokens):
    """Обрабатывает функцию с аргументами."""
    if not tokens or not id(tokens[0]):
        raise SyntaxError("Ожидался идентификатор функции")
    func_name = tokens.pop(0)
    if not tokens or tokens[0] != '(':
        raise SyntaxError("Ожидалась '(' после имени функции")
    tokens.pop(0)

    args = Args(tokens)

    if not tokens or tokens[0] != ')':
        raise SyntaxError("Ожидалась ')' в конце функции")
    tokens.pop(0)

    return f"{func_name}({args})"


def Arg(tokens):
    """Обрабатывает аргумент функции."""
    if not tokens:
        raise SyntaxError("Ожидался аргумент")
    if arg(tokens[0]):
        return tokens.pop(0)
    elif id(tokens[0]):
        return Func(tokens)
    else:
        raise SyntaxError("Ожидался аргумент или функция")


def Args(tokens):
    """Обрабатывает список из трех аргументов функции."""
    args = []
    for _ in range(3):
        arg_value = Arg(tokens)
        args.append(arg_value)
        if len(args) < 3:
            if not tokens or tokens[0] != ';':
                raise SyntaxError("Ожидался ';' между аргументами")
            tokens.pop(0)
    return ";".join(args)


def main():
    """Главная функция."""
    examples = [
        "f(x;g(y;y;h(x;x;x));f(z;y;x))",
        "f(x;f(y;z;x);z)",
        "h(f(x;y;z);y;g(z;x;y))",
        "f(x;x;g(y;h(x;x;y);z))",
        "f(x;y;z)",
        "f(x;y)",
        "f(x;;y)",
        "f(x;y;z;)",
        "f(x;y;h())",
        "f(x;y;z",
    ]
    for example in examples:
        tokens = re.findall(r'[a-zA-Z]+|[();]', example)
        try:
            S(tokens)
            print(f"{example} -> Корректный")
        except SyntaxError as e:
            print(f"{example} -> Ошибка: {e}")


if __name__ == "__main__":
    main()
