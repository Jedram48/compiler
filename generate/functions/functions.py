register = ('a', 'b', 'c', 'd', 'e' 'f', 'g', 'h')

def recreate_value(value: int, r: str) -> tuple:
    if r not in register:
        raise ValueError("Register must one of {a, b, c, d, e, f, g, h}")
    if value == 0:
        return tuple([f"RST {r}"])
    lines = []
    while value > 1:
        if value % 2 == 1:
            lines.append(f"INC {r}")
            value -= 1
        else:
            lines.append(f"SHL {r}")
            value /= 2
    lines.append(f"INC {r}")
    lines.append(f"RST {r}")
    return tuple(lines[::-1])