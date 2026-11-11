# TVID

## Groupe:
- [talvin.ackbaraly](https://cri.epita.fr/users/talvin.ackbaraly/)
- [noah.civilise](https://cri.epita.fr/users/noah.civilise/)
- [antoine.mosimann](https://cri.epita.fr/users/antoine.mosimann/)

## Instructions (dossier scripts/):
* `setup.sh` permet de télécharger les vidéos, clone le repository de mpeg2dec, appliquer le patch, compiler et générer les pgm en utilisant l'exécutable crée
* `cleanup.sh` permet de remettre le dossier dans son état initial
* `generate_patch.sh` permet de créer le fichier `mpeg2dec.patch` qui contient toutes les modifications faites sur le repository de mpeg2dec
* `apply_patch.sh` permet d'appliquer le patch crée (donc d'appliquer toutes les modifications faites)

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
Pour le sampling mode nous sommes en 4:2:0 (Y full res, U et V font la width/2)

4)

5)

6)

7)

8)

9)

10)

### B:

1) `ffprobe cnn.ts` nous donne cette sortie:
```
Input #0, mpegts, from 'cnn.ts':
  Duration: 00:00:29.53, start: 44414.345322, bitrate: 3118 kb/s
  Program 1
  Stream #0:0[0x1422]: Video: mpeg2video (Main) ([2][0][0][0] / 0x0002), yuv420p(tv, progressive), 544x480 [SAR 20:17 DAR 4:3], 29.97 fps, 29.97 tbr, 90k tbn, 59.94 tbc
    Side data:
      cpb: bitrate max/min/avg: 15000000/0/0 buffer size: 1835008 vbv_delay: N/A
  Stream #0:1[0x1423]: Audio: mp2 ([4][0][0][0] / 0x0004), 48000 Hz, stereo, fltp, 160 kb/s
```
Le pid du flux vidéo est 0x1442

2) Dans le fichier `scripts/setup.sh` on a rajouté les commandes pour décoder le flux vidéo en utilisant le pid, un exemple de commande:
```

./mpeg2dec/src/mpeg2dec -t 0x1422 -o pgm videos/ts/cnn.ts
```
mais on a aussi ajouté les pids de `ctv.ts`.

3)

4)

5)

6)
