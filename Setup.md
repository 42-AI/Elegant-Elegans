# Installation de l'environnement

## Introduction
Comme mentionné dans le Readme à la racine du répertoire, ce projet s'appuie sur 2 outils utilisés dans le monde de la recherche en biologie:
* [CeleST](https://dcs-lcsr.github.io/CeleST/) qui est un programme développé en Matlab
* [WF\NTP](https://github.com/impact27/WF_NTP) qui est un programme développé en Python
À ce jour, ces 2 outils ne semblent plus être actif en terme de développement et maintenance mais restent tout de même utilisé par la communauté scientifique.

Dans les sections qui vont suivre sont détaillés les étapes d'installation pour **CeleST** et **WF\_NTP**.


## Installation d'Anaconda pour Python3.8
1. télécharger le script d'installation d'anaconda (`wget -P /tmp https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh`)
2. ajouter les droits d'exécution à l'utilisateur (`sudo chmod u+x Anaconda3-2020.02-Linux-x86_64.sh`) et exécuter le script d'installation
3. Ajouter le répertoire `anaconda3/bin` au `PATH` en exportant celui-ci au sein de votre `bashrc` ou `zshrc` (`PATH="$HOME/anaconda3/bin:$HOME/.local/bin:$PATH"`)
4. fermer et réouvrir votre shell et lancer la commande `conda init bash` (ou `conda init zsh` en fonction de votre shell)
5. fermer et réouvrir votre shell encore une fois

L'installation est complète.


## Installation de WF_NTP
1. Créer un environement conda virtuel avec la commande `conda create -n v_wf_ntp python=3.8` et activer le (`conda activate  v_wf_ntp`)
2. Installer la librairie `Numpy` via la commande `conda install -f conda_wf_ntp_requirements.txt`
3. Enfin copier le fichier `run_script/multiwormtracker_app` à la racine du répertoire `WF_NTP`

L'installation de `WF_NTP` est complète, vous pouvez lancer le programme en effectuant la commande `./multiwormtracker_app`.


## Installation de CeleST
Afin de pouvoir lancer CeleST, plusieurs étapes préliminaires sont nécessaires:
1. télécharger le code source à partir de http://celest.mbb.rutgers.edu/
2. *(en cours)* étape d'installation de matlab
3. essayer de voir si des étapes suppllémentaires sont nécessaire.


### Octave GNU à la place de Matlab
1. installer [Octave for GNU/Linux](https://wiki.octave.org/Octave_for_GNU/Linux#Distribution_independent). Utiliser la méthode avec `flatpak` qui consiste à exécuter la commande:
    ```bash
    flatpak install flathub org.octave.Octave
    ```
2. Problème pour lancer CeleST dans Octave.

