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
720 720 # (witdh) (2/3 * height)
255 # la valeur maximale pour encoder les couleurs (profondeur)
BINAIRE # chaque pixel est codé par 1 ou 2 octets selon que la valeur maximale soit strictement inférieure (1 octet), ou bien supérieure ou égale à 256 (2 octets) // source: https://fr.wikipedia.org/wiki/Portable_pixmap
```
Pour le sampling mode nous sommes en 4:2:0 (Y full res, U et V font la witdh/2)

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
Le pid du flux vidéo est 0x1422

2) Dans le fichier `scripts/setup.sh` on a rajouté les commandes pour décoder le flux vidéo en utilisant le pid, un exemple de commande:
```

./mpeg2dec/src/mpeg2dec -t 0x1422 -o pgm videos/ts/cnn.ts
```
mais on a aussi ajouté les pids de `ctv.ts`.

3) Quand progressive frame vaut:
* 1: L'image est "plus nette", sauf que de temps en temps on a des lignes comme si le fichier disait qu'il ne fallait pas désentrelasser alors que si, donc un effet de peigne.
* 0: L'image fait des sauts de haut en bas, mais est bien désentrelassée

4) `progressive_frame` dans `logs.csv` change par blocs de frames entre 0 et 1 et `top_field_first` est toujours égal à 1
Avec `vlc -V x11 --deinterlace-mode bob videos/ts/cnn.ts` on ne voit aucune différence entre les moments où `progressive_frame` est à 0 et 1, comme si elle était forcée à 1.

5) Dans aucune des vidéos le flag `progressive_sequence` est set à 1 mais on a quand même des progressive_frame a 1 dans la vidéo de cnn. Donc l'encodeur a renvoyé de mauvaises valeurs.

6) Nous avons implémenté `uv run main.py encoded_images/cnn --progressive_frame 0` pour forcer la valeur de progressive_frame, du coup toute la vidéo est bien désentrelassée !

### C:

1) `ffprobe cnn.ts` nous donne cette sortie:
```
Input #0, mpegts, from 'ctv.ts':
  Duration: 00:02:28.86, start: 43417.464456, bitrate: 9928 kb/s
  Program 100 
    Metadata:
      service_name    : 中視數位台
      service_provider: CTV
  Stream #0:6[0x3e9]: Video: mpeg2video (Main) ([2][0][0][0] / 0x0002), yuv420p(tv, progressive), 704x480 [SAR 10:11 DAR 4:3], 29.97 fps, 59.94 tbr, 90k tbn, start 43420.009967
    Side data:
      CPB properties: bitrate max/min/avg: 15000000/0/0 buffer size: 1835008 vbv_delay: N/A
  Stream #0:7[0x3ea]: Audio: mp2 ([4][0][0][0] / 0x0004), 48000 Hz, stereo, s16p, 128 kb/s, start 43419.410078
  Stream #0:5[0x3eb]: Audio: mp2 ([4][0][0][0] / 0x0004), 48000 Hz, mono, s16p, 128 kb/s, start 43419.350244
  Program 101 
    Metadata:
      service_name    : 中視新聞台
      service_provider: CTV
  Stream #0:3[0x3f3]: Video: mpeg2video (Main) ([2][0][0][0] / 0x0002), yuv420p(tv, bottom first), 704x480 [SAR 10:11 DAR 4:3], 29.97 fps, 29.97 tbr, 90k tbn, start 43418.224844
    Side data:
      CPB properties: bitrate max/min/avg: 15000000/0/0 buffer size: 1835008 vbv_delay: N/A
  Stream #0:4[0x3f4]: Audio: mp2 ([4][0][0][0] / 0x0004), 48000 Hz, stereo, s16p, 128 kb/s, start 43418.306222
  Program 102 
    Metadata:
      service_name    : 中視綜藝台
      service_provider: CTV
  Stream #0:1[0x3fd]: Video: mpeg2video (Main) ([2][0][0][0] / 0x0002), yuv420p(tv, bottom first), 704x480 [SAR 10:11 DAR 4:3], 29.97 fps, 29.97 tbr, 90k tbn, start 43417.590867
    Side data:
      CPB properties: bitrate max/min/avg: 15000000/0/0 buffer size: 1835008 vbv_delay: N/A
  Stream #0:2[0x3fe]: Audio: mp2 ([4][0][0][0] / 0x0004), 48000 Hz, stereo, s16p, 128 kb/s, start 43417.464456
  Program 150 
    Metadata:
      service_name    : Gemstar
      service_provider: CTV
  Stream #0:8[0x5dd]: Unknown: none ([13][0][0][0] / 0x000D), start 43417.464456
  Stream #0:9[0x5de]: Unknown: none ([13][0][0][0] / 0x000D), start 43417.464456
  No Program
  Stream #0:0[0x12]: Data: epg, start 43417.464456
```
Le pid du flux de la 3ème vidéo est 0x3fd

2) Notre `scripts/setup.sh` démultiplexe déjà ce stream avec:
```
mpeg2dec -t 0x3fd -o pgm ctv.ts
```
