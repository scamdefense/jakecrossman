#!/usr/bin/env python3
"""
SEO Testing and Validation Script for Jake Crossman Acting Portfolio
Tests all SEO implementations and provides recommendations
"""

import requests  # type: ignore[import-untyped]
import json
import time
import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


class SEOTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url.rstrip("/")
        self.results = {"passed": [], "failed": [], "warnings": [], "performance": {}}

    def test_page(self, path="/"):
        """Test a single page for SEO compliance."""
        url = urljoin(self.base_url, path)

        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            load_time = time.time() - start_time

            self.results["performance"][path] = {
                "load_time": round(load_time, 3),
                "status_code": response.status_code,
                "size": len(response.content),
            }

            if response.status_code != 200:
                self.results["failed"].append(f"❌ {path}: HTTP {response.status_code}")
                return False

            soup = BeautifulSoup(response.text, "html.parser")

            # Test title
            title = soup.find("title")
            if title and title.text.strip():
                if len(title.text) <= 60:
                    self.results["passed"].append(
                        f"✅ {path}: Title present and optimal length "
                        f"({len(title.text)} chars)"
                    )
                else:
                    self.results["warnings"].append(
                        f"⚠️ {path}: Title too long ({len(title.text)} chars)"
                    )
            else:
                self.results["failed"].append(f"❌ {path}: Missing or empty title")

            # Test meta description
            meta_desc = soup.find("meta", attrs={"name": "description"})
            if meta_desc and meta_desc.get("content"):
                desc_length = len(meta_desc["content"])
                if 120 <= desc_length <= 160:
                    self.results["passed"].append(
                        f"✅ {path}: Meta description optimal ({desc_length} chars)"
                    )
                elif desc_length < 120:
                    self.results["warnings"].append(
                        f"⚠️ {path}: Meta description too short ({desc_length} chars)"
                    )
                else:
                    self.results["warnings"].append(
                        f"⚠️ {path}: Meta description too long ({desc_length} chars)"
                    )
            else:
                self.results["failed"].append(f"❌ {path}: Missing meta description")

            # Test h1 tag
            h1_tags = soup.find_all("h1")
            if len(h1_tags) == 1:
                self.results["passed"].append(f"✅ {path}: Single H1 tag present")
            elif len(h1_tags) == 0:
                self.results["failed"].append(f"❌ {path}: No H1 tag found")
            else:
                self.results["warnings"].append(
                    f"⚠️ {path}: Multiple H1 tags ({len(h1_tags)})"
                )

            # Test canonical URL
            canonical = soup.find("link", attrs={"rel": "canonical"})
            if canonical and canonical.get("href"):
                self.results["passed"].append(f"✅ {path}: Canonical URL present")
            else:
                self.results["failed"].append(f"❌ {path}: Missing canonical URL")

            # Test Open Graph
            og_title = soup.find("meta", attrs={"property": "og:title"})
            og_desc = soup.find("meta", attrs={"property": "og:description"})
            og_image = soup.find("meta", attrs={"property": "og:image"})

            if og_title and og_desc and og_image:
                self.results["passed"].append(f"✅ {path}: Open Graph tags complete")
            else:
                missing = []
                if not og_title:
                    missing.append("og:title")
                if not og_desc:
                    missing.append("og:description")
                if not og_image:
                    missing.append("og:image")
                self.results["failed"].append(
                    f"❌ {path}: Missing Open Graph: {', '.join(missing)}"
                )

            # Test Twitter Cards
            twitter_card = soup.find("meta", attrs={"property": "twitter:card"})
            twitter_title = soup.find("meta", attrs={"property": "twitter:title"})

            if twitter_card and twitter_title:
                self.results["passed"].append(f"✅ {path}: Twitter Card tags present")
            else:
                self.results["failed"].append(f"❌ {path}: Missing Twitter Card tags")

            # Test structured data
            json_ld_scripts = soup.find_all(
                "script", attrs={"type": "application/ld+json"}
            )
            if json_ld_scripts:
                valid_schemas = 0
                for script in json_ld_scripts:
                    try:
                        json.loads(script.string)
                        valid_schemas += 1
                    except json.JSONDecodeError:
                        pass

                if valid_schemas > 0:
                    self.results["passed"].append(
                        f"✅ {path}: {valid_schemas} valid JSON-LD schema(s)"
                    )
                else:
                    self.results["failed"].append(f"❌ {path}: Invalid JSON-LD schemas")
            else:
                self.results["failed"].append(f"❌ {path}: No structured data found")

            # Test alt text for images
            images = soup.find_all("img")
            images_without_alt = [img for img in images if not img.get("alt")]

            if images:
                if not images_without_alt:
                    self.results["passed"].append(
                        f"✅ {path}: All {len(images)} images have alt text"
                    )
                else:
                    self.results["warnings"].append(
                        f"⚠️ {path}: {len(images_without_alt)}/"
                        f"{len(images)} images missing alt text"
                    )

            # Test page load time
            if load_time <= 2.0:
                self.results["passed"].append(
                    f"✅ {path}: Fast load time ({load_time:.2f}s)"
                )
            elif load_time <= 4.0:
                self.results["warnings"].append(
                    f"⚠️ {path}: Moderate load time ({load_time:.2f}s)"
                )
            else:
                self.results["failed"].append(
                    f"❌ {path}: Slow load time ({load_time:.2f}s)"
                )

            return True

        except requests.RequestException as e:
            self.results["failed"].append(f"❌ {path}: Request failed - {str(e)}")
            return False

    def test_sitemaps(self):
        """Test sitemap accessibility and validity."""
        sitemaps = [
            "/sitemap.xml",
            "/news-sitemap.xml",
            "/image-sitemap.xml",
            "/video-sitemap.xml",
        ]

        for sitemap_path in sitemaps:
            try:
                url = urljoin(self.base_url, sitemap_path)
                response = requests.get(url, timeout=10)

                if response.status_code == 200:
                    try:
                        ET.fromstring(response.text)
                        self.results["passed"].append(
                            f"✅ {sitemap_path}: Valid XML sitemap"
                        )
                    except ET.ParseError:
                        self.results["failed"].append(f"❌ {sitemap_path}: Invalid XML")
                else:
                    self.results["failed"].append(
                        f"❌ {sitemap_path}: HTTP {response.status_code}"
                    )

            except requests.RequestException as e:
                self.results["failed"].append(
                    f"❌ {sitemap_path}: Request failed - {str(e)}"
                )

    def test_robots_txt(self):
        """Test robots.txt file."""
        try:
            url = urljoin(self.base_url, "/robots.txt")
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                content = response.text
                if "User-agent:" in content and "Sitemap:" in content:
                    self.results["passed"].append(
                        "✅ /robots.txt: Valid and contains sitemap references"
                    )
                else:
                    self.results["warnings"].append(
                        "⚠️ /robots.txt: Missing required directives"
                    )
            else:
                self.results["failed"].append(
                    f"❌ /robots.txt: HTTP {response.status_code}"
                )

        except requests.RequestException as e:
            self.results["failed"].append(f"❌ /robots.txt: Request failed - {str(e)}")

    def test_favicon(self):
        """Test favicon accessibility."""
        favicon_paths = [
            "/favicon.ico",
            "/static/favicon/favicon.ico",
            "/static/favicon/apple-touch-icon.png",
            "/static/favicon/android-chrome-192x192.png",
        ]

        for favicon_path in favicon_paths:
            try:
                url = urljoin(self.base_url, favicon_path)
                response = requests.head(url, timeout=5)

                if response.status_code == 200:
                    self.results["passed"].append(f"✅ {favicon_path}: Accessible")
                else:
                    self.results["warnings"].append(
                        f"⚠️ {favicon_path}: HTTP {response.status_code}"
                    )

            except requests.RequestException:
                self.results["warnings"].append(f"⚠️ {favicon_path}: Not accessible")

    def run_all_tests(self):
        """Run comprehensive SEO test suite."""
        print("🚀 Starting SEO Test Suite for Jake Crossman Portfolio")
        print("=" * 60)

        # Test main pages
        pages = ["/", "/about", "/reel", "/resume", "/gallery", "/news", "/contact"]

        print("\n📄 Testing Pages...")
        for page in pages:
            print(f"Testing {page}...")
            self.test_page(page)

        print("\n🗺️ Testing Sitemaps...")
        self.test_sitemaps()

        print("\n🤖 Testing robots.txt...")
        self.test_robots_txt()

        print("\n🎨 Testing Favicons...")
        self.test_favicon()

        # Print results
        self.print_results()

    def print_results(self):
        """Print formatted test results."""
        print("\n" + "=" * 60)
        print("📊 SEO TEST RESULTS")
        print("=" * 60)

        print(f"\n✅ PASSED ({len(self.results['passed'])} tests)")
        for result in self.results["passed"]:
            print(f"  {result}")

        if self.results["warnings"]:
            print(f"\n⚠️ WARNINGS ({len(self.results['warnings'])} items)")
            for result in self.results["warnings"]:
                print(f"  {result}")

        if self.results["failed"]:
            print(f"\n❌ FAILED ({len(self.results['failed'])} tests)")
            for result in self.results["failed"]:
                print(f"  {result}")

        if self.results["performance"]:
            print("\n⚡ PERFORMANCE SUMMARY")
            total_time = sum(
                p["load_time"] for p in self.results["performance"].values()
            )
            avg_time = total_time / len(self.results["performance"])
            print(f"  Average load time: {avg_time:.2f}s")

            slowest = max(
                self.results["performance"].items(), key=lambda x: x[1]["load_time"]
            )
            print(f"  Slowest page: {slowest[0]} ({slowest[1]['load_time']:.2f}s)")

        # Calculate score
        total_tests = len(self.results["passed"]) + len(self.results["failed"])
        if total_tests > 0:
            score = (len(self.results["passed"]) / total_tests) * 100
            print(f"\n🎯 SEO SCORE: {score:.1f}%")

            if score >= 90:
                print("🌟 Excellent SEO implementation!")
            elif score >= 80:
                print("👍 Good SEO implementation with minor issues")
            elif score >= 70:
                print("⚠️ SEO needs improvement")
            else:
                print("❌ SEO implementation needs significant work")

        print("\n" + "=" * 60)

        return len(self.results["failed"]) == 0


def main():
    """Main function to run SEO tests."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Test SEO implementation for Jake Crossman portfolio"
    )
    parser.add_argument(
        "--url",
        default="http://localhost:5000",
        help="Base URL to test (default: http://localhost:5000)",
    )
    parser.add_argument("--page", help="Test specific page only")
    parser.add_argument(
        "--json-output",
        metavar="FILE",
        help="Write raw results to FILE in JSON format",
    )

    args = parser.parse_args()

    tester = SEOTester(args.url)

    if args.page:
        print(f"Testing single page: {args.page}")
        success = tester.test_page(args.page)
    else:
        success = tester.run_all_tests()

    tester.print_results()

    if args.json_output:
        try:
            with open(args.json_output, "w") as f:
                json.dump(tester.results, f, indent=2)
            print(f"Results written to {args.json_output}")
        except OSError as e:
            print(f"Failed to write results file: {e}", file=sys.stderr)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
