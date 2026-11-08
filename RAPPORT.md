# TVID

## Groupe:
- [talvin.ackbaraly](https://cri.epita.fr/users/talvin.ackbaraly/)
- [noah.civilise](https://cri.epita.fr/users/noah.civilise/)
- [antoine.mosimann](https://cri.epita.fr/users/antoine.mosimann/)

## Setup:
Pour setup le projet il suffit de lancer `setup.sh`, celui-ci télécharge les vidéos ainsi que clone le repository de mpeg2dec, le compile et génères les pgm en utilisant son exécutable.
Inversement `cleanup.sh` remet le dossier dans son état initial.

## Questions:

### A:

1) Après avoir visualisé toutes les videos, s'il faut en choisir une nous utiliserons `pendulum.m2v`, vu que dans la visualisation avec VLC le K du OK ne s'affiche pas comme on l'a vu en cours, ainsi que du jaggies.
```
vlc -V x11 videos/elementary/pendulum.m2v
vlc -V xvideo videos/elementary/pendulum.m2v
```

2) Notre `setup.sh` fait déjà cette étape.
```
cd encoded_images/pendulum
../../mpeg2dec/src/mpeg2dec -o pgm ../../videos/elementary/pendulum.m2v
```

3) Voici le fichier `encoded_images/pendulum/0.pgm`
```
P5 # cette ligne donne le type de la structure (c'est un magic number) et P5 indique que c'est un PGM
720 720 # width heigh
255 # la valeur maximale pour encoder les couleurs
BINAIRE # chaque pixel est codé par 1 ou 2 octets selon que la valeur maximale soit strictement inférieure (1 octet), ou bien supérieure ou égale à 256 (2 octets) // source: https://fr.wikipedia.org/wiki/Portable_pixmap
```
TODO: dire pour le sampling mode
