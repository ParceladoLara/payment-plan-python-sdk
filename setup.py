from setuptools import setup, find_packages

setup(
    name="payment-plan-python-sdk",
    version="1.0.1",
    description="A Python SDK for Lara Payment Plan, a wrapper around the Lara Payment Plan Rust library.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Parcelado Lara",
    author_email="	it-group@lara.app.br",
    url="https://github.com/ParceladoLara/payment-plan-python-sdk",
    packages=find_packages(include=["payment_plan", "payment_plan._internal"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Add your dependencies here
    ]
)