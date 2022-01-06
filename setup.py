import setuptools
setuptools.setup(
    name="panda_module_sample",
    version="0.0.1",
    options={
        'build_apps': {
            'platforms': ["manylinux2014_x86_64"],
            'include_patterns': [
                "assets/*",
            ],
            'include_modules': {
                '*': [
                    "packaging.version",
                    "packaging.specifiers",
                    "packaging.requirements",
                ]
            },
            'console_apps': {
                'sample': "sample.py",
            },
        }
    }
)
