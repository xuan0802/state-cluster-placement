from setuptools import setup, find_packages

setup(
    name='state-cluster-placement',
    version='1.1',
    packages=find_packages(),
    url='',
    license='',
    author='xuan',
    author_email='xuan@dcn.ssu.ac.kr',
    description='placement algorithms for state management functions',
    entry_points={
        'console_scripts': [
            'test_script = state_cluster_placement.main:main'
        ]
    }
)
