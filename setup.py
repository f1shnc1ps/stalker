from setuptools import setup, find_packages

setup(
    name='phantom-osint',
    version='1.0.0',
    description='Unified OSINT reconnaissance tool: usernames, emails, phones, IPs',
    author='OSINT Team',
    url='https://github.com/yourusername/phantom',
    packages=find_packages(),
    install_requires=[
        'requests>=2.28.0',
        'httpx>=0.23.0',
        'pydantic>=1.10.0',
        'click>=8.1.0',
        'colorama>=0.4.6',
        'tabulate>=0.9.0',
        'pyyaml>=6.0',
    ],
    entry_points={
        'console_scripts': [
            'phantom=phantom.cli:main',
        ],
    },
    python_requires='>=3.11',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],
)
