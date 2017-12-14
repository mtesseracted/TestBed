import setuptools
"""
After making modules, to install run:
    %>pip install -e .
in the directory the module directory lives
"""

if __name__ == "__main__":
    setuptools.setup(
        name='pymodule',
        version="0.1.1",
        description='A starting template for Python programs',
        author='Aaron Mahler',
        author_email='alm100@duke.edu',
        url="https://github.com/mtesseracted/TestBed",
        license='BSD-3C',
        packages=setuptools.find_packages(),
        install_requires=[
            'numpy>=1.7',
        ],
        extras_require={
            'docs': [
                'sphinx==1.2.3',  # autodoc was broken in 1.3.1
                'sphinxcontrib-napoleon',
                'sphinx_rtd_theme',
                'numpydoc',
            ],
            'tests': [
                'pytest',
                'pytest-cov',
                'pytest-pep8',
                'tox',
            ],
        },

        tests_require=[
            'pytest',
            'pytest-cov',
            'pytest-pep8',
            'tox',
        ],

        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
        ],
        zip_safe=True,
    )
