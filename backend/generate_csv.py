import argparse
import csv
import random

USERNAMES = [
    "taras_dev",
    "olena_writer",
    "andrii_code",
    "marta_ui",
    "ivan_backend",
    "nazar_ops",
    "sofia_pm",
    "dmytro_qa",
    "iryna_marketing",
    "yurii_admin",
]

EMAIL_DOMAINS = ["example.com", "mail.com", "site.org", "wp.local", "demo.net"]

TITLE_WORDS = [
    "WordPress",
    "Plugin",
    "Theme",
    "Guide",
    "Tips",
    "Performance",
    "Security",
    "SEO",
    "Update",
    "Tutorial",
]

TAGS = ["news", "tech", "wordpress", "plugins", "themes", "seo", "hosting", "dev"]

CONTENT_WORDS = [
    "fast",
    "reliable",
    "scalable",
    "simple",
    "clean",
    "modern",
    "secure",
    "plugin",
    "theme",
    "content",
    "dashboard",
    "editor",
    "settings",
    "optimize",
    "publish",
    "article",
]


def random_email(username: str) -> str:
    domain = random.choice(EMAIL_DOMAINS)
    number = random.randint(1, 9999)
    return f"{username}{number}@{domain}"


def random_title() -> str:
    words_count = random.randint(2, 5)
    return " ".join(random.choices(TITLE_WORDS, k=words_count))


def random_content() -> str:
    words_count = random.randint(3, 10)
    return " ".join(random.choices(CONTENT_WORDS, k=words_count))


def generate_csv(output_path: str, rows_count: int) -> None:
    fields = ["username", "email", "post_title", "post_tag", "post_content"]

    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for _ in range(rows_count):
            username = random.choice(USERNAMES)
            writer.writerow(
                {
                    "username": username,
                    "email": random_email(username),
                    "post_title": random_title(),
                    "post_tag": random.choice(TAGS),
                    "post_content": random_content(),
                }
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate CSV with random WordPress-like posts")
    parser.add_argument("--output", default="posts.csv", help="Output CSV path")
    parser.add_argument("--rows", type=int, default=1000, help="Number of rows to generate")

    args = parser.parse_args()

    if args.rows < 1000:
        raise ValueError("rows must be at least 1000")

    generate_csv(output_path=args.output, rows_count=args.rows)
    print(f"Created {args.rows} rows in {args.output}")


if __name__ == "__main__":
    main()
