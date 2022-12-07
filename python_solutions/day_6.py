from pathlib import Path


INPUT_FILE_PATH = Path("../inputs/day_6.txt")


def get_signal() -> str:
    with open(INPUT_FILE_PATH, "r") as f:
        return f.read()


def search_for_marker(signal: str, marker_size: int) -> int:
    for i in range(len(signal) - (len(signal) % marker_size) - marker_size):
        if len(set(signal[i : i + marker_size])) == marker_size:
            return i + (marker_size - 1)
    raise RuntimeError("No marker found")


def main():

    signal = get_signal()
    part_1 = search_for_marker(signal, marker_size=4)
    part_2 = search_for_marker(signal, marker_size=14)

    print(f"Packet received at character {part_1 + 1}")
    print(f"Message received at character {part_2 + 1}")


if __name__ == "__main__":
    main()
