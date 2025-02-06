from setuptools import setup, find_packages

setup(
    name='secure-share',
    version='1.0.0',
    description='A secure file-sharing program with AES encryption.',
    author='Willbara',
    packages=find_packages(),
    install_requires=[
        'cryptography'
    ],
    entry_points={
        'console_scripts': [
            'secure-share=secure_share.cli:main'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)