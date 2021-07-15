# connect4
Connect Four Game environment and agents that play it

## Installation

I created this project using the anaconda distribution. You can install it [here](https://docs.anaconda.com/anaconda/install/). If you prefer a lightweight version, you can [install Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/) instead.


Create a conda environment with:

    $ conda create --name connect4 python=3

Activate the conda environment with:

    $ conda activate connect4

Install the necessary dependencies with:

    $ pip install -e .
    
Download the `connect_four.db` file from [this .zip file](https://drive.google.com/file/d/1NOuFxv5T2Z2YsOZzoiaLZUYKRYl5nNT4/view?usp=sharing) or [this .tgz file](https://drive.google.com/file/d/1XvgOu1ofMhTYj63ThcbIla3NAaINdWqE/view?usp=sharing) and place it in the same directory as `play.py`.

Play against one of the DFPN agent:

    $ python play.py
