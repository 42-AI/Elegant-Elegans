# Elegant-Elegans

*(english below)*

## Cloner le répertoire et sous modules
Ce répertoire contient un sous-module `WF_NTP`. Afin de cloner ce répertoire et les sous-modules, taper la commande:
```bash
git clone --recurse-submodules git@github.com:42-AI/Elegant-Elegans.git
```

---

## Cloning the repository and submodules
The present repository include a submodule named `WF_NTP`. To clone this repository and the submodules, one should enter:
```bash
git clone --recurse-submodules git@github.com:42-AI/Elegant-Elegans.git
```

## Conversion d'images .tiff en vidéo
Ce répertoire contient un module `converter`, qui convertit des images .tiff en vidéo.
Entrer la commande: 
```bash
python -m converter --path PATH --output OUTPUT -f FORMAT
```
Ou:
```bash
python3 -m converter --path PATH --output OUTPUT -f FORMAT
```
PATH représente le chemin d'accès au répertoire contenant au moins 100 images .tiff et un fichier metadata.txt.
OUTPUT est le nom de la sortie vidéo.
FORMAT est le format de sortie souhaité : .mp4 ou .avi.
Exemple :
```bash
python -m converter --path img/ --output video01 -f mp4
```

## Converting .tiff images to video
The present repository include a `converter` module. One can use it to convert .tiff images to a video.
Enter the command:
```bash
python -m converter --path PATH --output OUTPUT -f FORMAT
```
Or:
```bash
python3 -m converter --path PATH --output OUTPUT -f FORMAT
```
PATH represents the path to the directory containing at least 100 .tiff images and a metadata.txt file.
OUTPUT is the name of the video output.
FORMAT is the desired output format : .mp4 or .avi. 
Exemple:
```bash
python -m converter --path img/ --output video01 -f mp4
```


## Contributors
* Roberto Catini [rcatini](https://github.com/rcatini)
* Colomban Scully [SOTHSC](https://github.com/COTHSC)
* Jee Hyun Park [jhparkkkk](https://github.com/jhparkkkk)
* Shellen Dorlin [shell02](https://github.com/shell02)
* Constant Alle [cnstll](https://github.com/cnstll)
* Perrine Gros [p-lg-ux](https://github.com/p-lg-ux)
