from pathlib import Path

from setuptools import find_packages, setup


BASE_DIR = Path(__file__).parent
README_PATH = BASE_DIR / "README.md"
REQUIREMENTS_PATH = BASE_DIR / "requirements.txt"


def read_requirements() -> list[str]:
    if not REQUIREMENTS_PATH.exists():
        return []

    requirements: list[str] = []
    for line in REQUIREMENTS_PATH.read_text(encoding="utf-8").splitlines():
        cleaned = line.strip()
        if not cleaned or cleaned.startswith("#"):
            continue
        requirements.append(cleaned)
    return requirements


setup(
    name="zomato-chatbot",
    version="0.1.0",
    author="Tamaghna",
    author_email="tamaghna51@gmail.com",
    description="A Chainlit-based food discovery assistant with OpenAI-compatible LLM support.",
    long_description=README_PATH.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    python_requires=">=3.10",
)

