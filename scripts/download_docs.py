from pathlib import Path
import httpx

DOCS = {
    "Amazon-2024-Annual-Report.pdf": "https://s2.q4cdn.com/299287126/files/doc_financials/2025/ar/Amazon-2024-Annual-Report.pdf",
    "AMZN-Q3-2025-Earnings-Release.pdf": "https://s2.q4cdn.com/299287126/files/doc_financials/2025/q3/AMZN-Q3-2025-Earnings-Release.pdf",
    "AMZN-Q2-2025-Earnings-Release.pdf": "https://s2.q4cdn.com/299287126/files/doc_financials/2025/q2/AMZN-Q2-2025-Earnings-Release.pdf",
}


def main():
    target_dir = Path("./data/docs")
    target_dir.mkdir(parents=True, exist_ok=True)

    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        for filename, url in DOCS.items():
            output_path = target_dir / filename
            response = client.get(url)
            response.raise_for_status()
            output_path.write_bytes(response.content)
            print(f"Downloaded {filename}")


if __name__ == "__main__":
    main()