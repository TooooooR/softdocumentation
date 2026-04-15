import argparse

from di import build_import_service


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv", 
        default="posts.csv", 
        help="Path to CSV file",
    )
    parser.add_argument(
        "--mode",
        choices=["append", "replace"],
        default="append",
        help="append adds records, replace clears table before import",
    )
    parser.add_argument(
        "--db-url",
        default="sqlite:///app.db",
        help="SQLAlchemy database URL",
    )

    args = parser.parse_args()

    service = build_import_service(db_url=args.db_url)
    inserted = service.import_from_csv(file_path=args.csv, mode=args.mode)
    print(f"Imported rows: {inserted} (mode={args.mode})")


if __name__ == "__main__":
    main()
