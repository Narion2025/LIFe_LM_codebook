from .codebook_manager import check_consistency


def main() -> None:
    result = check_consistency()
    print("Konsistenzprüfung:")
    for section, messages in result.items():
        if messages:
            print(f"{section}:")
            for msg in messages:
                print(f"  {msg}")
        else:
            print(f"{section}: OK")


if __name__ == "__main__":
    main()
