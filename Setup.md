*(english below ([here](#introduction-english-version)))*
# Installation de l'environnement / overall Setup

---

- [Introduction](#introduction)
- [Installation d'Anaconda pour Python3.8](#installation-danaconda-pour-python38)
- [Installation de WF_NTP](#installation-de-wf_ntp)
- [Installation de CeleST](#installation-de-celest)

---
## Introduction
Le projet Elegant-Elegans s'appuie à ce jour sur 2 outils utilisés dans le monde de la recherche en biologie:
* [CeleST](https://dcs-lcsr.github.io/CeleST/) (version MacOS) qui est un programme développé en Matlab.
* [WF\_NTP](https://github.com/impact27/WF_NTP) qui est un programme développé en Python.
À ce jour, ces 2 outils ne semblent plus être actif en terme de développement et maintenance mais semblent encore utilisés par la communauté scientifique.

Dans les sections qui vont suivre sont détaillés les étapes d'installation pour **CeleST** et **WF\_NTP**.

## Installation d'Anaconda pour Python3.8
La documentation détaillée d'anaconda se trouve [ici](https://docs.anaconda.com/anaconda/install/).
### Linux
1. télécharger le script d'installation d'anaconda (`wget -P /tmp https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh`)
   > À noter que l'exécutable télécharger par la commande wget est pour un système dont l'architecture est x86 (pour vérifier tapper `arch` ou `uname -m` dans votre terminal)
2. ajouter les droits d'exécution à l'utilisateur (`sudo chmod u+x Anaconda3-2020.02-Linux-x86_64.sh`) et exécuter le script d'installation
3. Ajouter le répertoire `anaconda3/bin` au `PATH` en exportant celui-ci au sein de votre `bashrc` ou `zshrc` (`PATH="$HOME/anaconda3/bin:$HOME/.local/bin:$PATH"`)
4. fermer et réouvrir votre shell et lancer la commande `conda init bash` (ou `conda init zsh` en fonction de votre shell)
5. fermer et réouvrir votre shell encore une fois

L'installation est complète.

### Windows
1. Télécharger l'exécutable d'installation [Anaconda](https://www.anaconda.com/products/distribution) ou [Miniconda](https://docs.conda.io/en/latest/miniconda.html) pour Python 3.8.
2. Lancer l'exécutable et suivre les instructions jusqu'à ce que l'installation soit complète.

## Installation de WF_NTP

### Linux
1. Créer un environement conda virtuel avec la commande:
   ```bash
   conda create -n v_wf_ntp python=3.8
   ```
2. Activer l'environnement:
   ```bash
   conda activate  v_wf_ntp
   ```
> **Note**
>
> Si vous utilisez miniconda a la place d'anaconda pensez a ajouter le channel conda-forge grâce à la commande:
> ```bash
> conda config --append channels conda-forge
  ```

3. Installer les différentes librairies rassemblées dans le fichier `conda_wf_ntp_requirements.txt` via la commande:
   ```bash
   conda install --file conda_wf_ntp_requirements.txt
   ```
3. Copier le fichier `run_script/multiwormtracker_app` à la racine du répertoire `WF_NTP/`

L'installation de `WF_NTP` est complète, vous pouvez lancer le programme avec la commande `./multiwormtracker_app` ou bien double cliquer dessus.

### Windows
#### Création de l'environnement conda
1. Ouvrir l'Anaconda Prompt et se placer dans le répertoire `Elegant-Elegans`
   ```bash
   cd path\to\Elegant-Elegans
   ```
2. Créer un environnement conda virtuel `v_wf_ntp`, puis l'activer :
   ```bash
   conda env create -f env_wf_ntp.yml
   conda activate v_wf_ntp
   ```
   > L'environnement est bien activé si `v_wf_ntp` apparaît entre parenthèses au début de la ligne de commande.

#### Exécution
1. Dans l'Anaconda Prompt, se placer dans le répertoire `WF_NTP`
   ```bash
   cd path\to\Elegant-Elegans\WF_NTP
   ```
2. Vérifier que l'environnement `v_wf_ntp` est bien activé et lancer le programme de `WF_NTP` avec la commande :
   ```bash
   python multiwormtracker_app
   ```

## Installation de CeleST
### Étapes préliminaires
Afin de pouvoir lancer CeleST, plusieurs étapes préliminaires sont nécessaires:
1. télécharger le code source à partir de http://celest.mbb.rutgers.edu/
2. installer le logiciel **Octave** ([ici](https://wiki.octave.org/Octave_for_GNU/Linux) pour les systèmes Linux ou encore [là](https://wiki.octave.org/Octave_for_macOS) pour MacOS)

### Octave
L'installation du logiciel Octave est simple.
Si vous êtes *root* et sous un système *Ubuntu*, vous avez simplement à effectuer les commandes:
```bash
apt install octave
apt install liboctave-dev  # development files
```
Pour un système Linux différent, vous trouverez la démarche sur la page [wiki d'Octave](https://wiki.octave.org/Octave_for_GNU/Linux)

Dans le cas où vous n'êtes pas *root*, il est possible d'installer Octave en tant que distribution indépendante au sein d'Anaconda.
Dans ce cas vous pouvez l'ajouter à l'environnement conda `v_wf_ntp`  (de sorte à avoir un environnement unique) où bien dans un second environnement conda.
Une fois l'environnement activé, effectué la commande:
```bash
conda install -c conda-forge octave
```
Il est également possible d'installer Octave avec `flatpak`:
```bash
flatpak install flathub org.octave.Octave
```

L'installation d'Octave est complète. Vous pouvez le lancer via votre centre d'applications.

## Installation et exécution de CeleST

Le code source de CeleST est présent au sein du répertoire pour des raisons de comodités car il a été nécesaire de faire quelques modifications pour le faire fonctionner sur une version récente d'Octave ou Matlab. La version fournie est prête à être lancée avec Octave directement.


Si vous désirez exécuter CeleST à partir du code source original, voici les étapes à suivre:
1. décompresser l'archive `'source code.zip'`:
   ```bash
   unzip 'source code.zip' -d /path/to/the/desired/directory/celest
   ```
2. Le code de `CeleST` est en Matlab, de plus il a été rédigé il y a quelques années et ne semble pas être maintenu. Deux répertoires sont présents dans l'archive `CeleST`:
   *  `__MACOSX` (code source pour MacOS)
   *  `source code` (code source pour Linux)
   1. **Installation Linux**: Dans le répertoire contenant le code source (`source code`) effectué la modification suivante:
      ```bash
      # fichier CeleST.m ligne 174
      tableVideos = uitable(...,'ColumnEditable',[],...);
      # remplacer les crochets par:
      tableVideos = uitable(...,'ColumnEditable',false,...);
      ```
   2. **Installation MacOS**: #TODO: cela devrait être sensiblement les mêmes étapes que sous Linux.

`CeleST` est prêt à être lancer avec `Octave`.

### Exécution

#### Interface graphique

1. Lancer `Octave`
2. Modifier le répertoire courant afin que celui-ci soit le répertoire contenant le code source (voir image).
![octave change directory](.assets/octave_change_directory.png)
3. clique-droit sur le fichier `CeleST.m` et sélectionner `Run`:
![CeleST run selection](.assets/CeleST_m_run_selection.png)

L'interface de `CeleST` s'ouvre, vous pouvez alors utiliser le programme.

#### interface ligne de commande

1. `cd source_code`
2. `octave --eval "run(CeleST.m)"`

*Note: Les différentes étapes ont été réalisées sur un système Ubuntu22.04, a priori cela devrait être identique sur Ubuntu21.04*

---
---

- [Introduction](#introduction-english-version)
- [Anaconda for Python3.8](#anaconda-for-python38)
- [WF_NTP setup](#wf_ntp-setup)
- [CeleST setup](#celest-setup)

## Introduction (english version)

Elegant-Elegans is based on 2 tools used by the academic biological community:
* [CeleST](https://dcs-lcsr.github.io/CeleST/) (MacOS version) written in Matlab.
* [WF\_NTP](https://github.com/impact27/WF_NTP) written in Python.

There are no recent activities on the respective github repository, but it seems that these tools are still used by some scientist.

In the following section, we described the different steps to setup a working environment for **CeleST** and **WF\_NTP**.

### Anaconda for Python3.8 
Anaconda documentation can be found [here](https://docs.anaconda.com/anaconda/install/) (*installation is more detailled there*)
#### Linux
1. Download installation script of anaconda (`wget -P /tmp https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh`).
   > **info**
   >
   > Note that the downloaded executable with the command above is for a x86 architecture system.
   > To check your architecture, you can look at the output of:
   > ```bash
   > arch
   > # or
   > uname -m
   >```
2. Add the executable permission (`sudo chmod u+x Anaconda3-2020.02-Linux-x86_64.sh`) and execute the script (```./Anaconda3-2020.02-Linux-x86_64.sh```)
3. Add the repository `anaconda3/bin` at your `PATH` variable environment by writing the export in your `~/.bashrc` ou `~/.zshrc` (`export PATH="$HOME/anaconda3/bin:$HOME/.local/bin:$PATH"` at the end of `~/.bashrc` ou `~/.zshrc`).
4. Now you can close and reopen your terminal and execute the command `conda init bash` (ou `conda init zsh` depending on the shell you are using).
5. Close and reopen your terminal one more time.

The installation should be complete.

#### Windows
1. Download the installation executable [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) for Python 3.8.
2. Execute the script and follow the instructions until the installation is completed.

### WF_NTP setup

#### Linux
1. Create an virtual conda environment with the command:
   ```bash
   conda create -n v_wf_ntp python=3.8
   ```
2. activate the venv:
   ```bash
   conda activate  v_wf_ntp
   ```
> **Note**
>
> If you are using Minicondat instead of Anaconda, you need to add the `conda-forge` channel:
> ```bash
> conda config --append channels conda-forge
  ```
3. Install the libraries gather in `conda_wf_ntp_requirements.txt` with the command:
   ```bash
   conda install --file conda_wf_ntp_requirements.txt
   ```
4. Copy the file `run_script/multiwormtracker_app` at the root of the repository `WF_NTP/`

Installation of `WF_NTP` should be complete, you can run the program with the command `./multiwormtracker_app` or double click on it.

#### Windows
##### Conda environment
1. Open the Anaconda pompt and go to `Elegant-Elegans` folder.
   ```bash
   cd path\to\Elegant-Elegans
   ```
2. Create a conda virtual environment named `v_wf_ntp`, and activate it:
   ```bash
   conda env create -f env_wf_ntp.yml
   conda activate v_wf_ntp
   ```
   > Virtual environment is correctly created if `v_wf_ntp` appears between parentheses at the beginning of the line in the prompt.

##### Execution
1. In the Anaconda Prompt, go to the folder `WF_NTP`
   ```bash
   cd path\to\Elegant-Elegans\WF_NTP
   ```
2. Verify `v_wf_ntp` is activated and run the program `WF_NTP` with the command:
   ```bash
   python multiwormtracker_app
   ```

### CeleST setup
### Preliminaries steps (if not using the CeleST code given)
To run `CeleST`, several steps are needed:
1. Download the source code from  http://celest.mbb.rutgers.edu/
2. Install **Octave** ([here](https://wiki.octave.org/Octave_for_GNU/Linux) Linux system or [there](https://wiki.octave.org/Octave_for_macOS) for MacOS)

### Octave
Installation step are prety simple.

If you are *root* user and on *Ubuntu* system, you only need to run the following commands:
```bash
apt install octave
apt install liboctave-dev  # development files
```
For a different system than Linux, one can find the steps on the wiki of Octave ([wiki d'Octave](https://wiki.octave.org/Octave_for_GNU/Linux)).

If you are not a *root* user, it is possible to install Octave as an independante distribution within Anaconda.
In that case, you can either add it to your conda virtual environment `v_wf_ntp` or create a new virtual environment.

After you choose in which virtual environment you want to add octave, activate it and write the command:
```bash
conda install -c conda-forge octave
```

Last option listed here, you can install Octave with `flatpak`:
```bash
flatpak install flathub org.octave.Octave
```

Octave installation should be complete. You can run it from your application center.

### CeleST modification

CeleST source code can be found in the repository Elegant-Elegans for simplicity. It has been slighly modified to work with recent version of Octave or Matlab. Thus it should work directly.

!!! warning
   `CeleST` code is in Matlab and has been written few years ago. So the code is obsolete.

If one want to use CeleST from the orignal source code, here are the steps you have to follow to make it work:
1. unzip the file `'source code.zip'`:
   ```bash
   unzip 'source code.zip' -d /path/to/the/desired/directory/celest
   ```
2. You will find 2 folders within `CeleST`:
   *  `__MACOSX` (code source for MacOS)
   *  `source code` (code source for Linux)
   1. **Linux Installation**: In the folder (`source code`) one have to make the following modification::
      ```bash
      # CeleST.m file - line 174
      tableVideos = uitable(...,'ColumnEditable',[],...);
      # replacing the square bracket by:
      tableVideos = uitable(...,'ColumnEditable',false,...);
      ```
   2. **MacOS Installation**: #TODO: should be quite similar to Linux.

`CeleST` should be ready to be execute with `Octave`.

#### Execution
##### Graphical interface

1. Launch `Octave`
2. Modify the `current folder` to be the folder containing the source code (see picture).
![octave change directory](.assets/octave_change_directory.png)
3. right click on the file `CeleST.m` and select `Run`:
![CeleST run selection](.assets/CeleST_m_run_selection.png)

`CeleST` interface should be opening, you can use `CelesT` with Octave.

##### Command Line Interface (CLI)

1. `cd source_code`
2. `octave --eval "run(CeleST.m)"`

*Note: The different steps has been realised with Ubuntu22.04, a priori this should be identical on Ubuntu21.04*


---
---

## Contribution

Contributors must used black formatter, used isort and flake8 to check their code.
Thus before doing a pull request, you have to setup your local repository to install the pre-commit hooks.


Here are the steps to setup the pre-commit hooks:

* Install pre-commit
   ```sh
   pip install pre-commit
   ```
* Install the hooks with:
   ```sh
   pre-commit install
   ```
* run the hooks with
   ```sh
   pre-commit run -a
   ```
