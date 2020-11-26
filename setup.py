from setuptools import setup, find_packages

setup(
  name='connect_four',
  version='0.0.1',
  description='OpenAI Gym environment for the Connect Four game',
  install_requires=['gym', 'tensorflow'],  # Dependencies connect_four needs
  license='MIT',
  packages=find_packages(),
)
