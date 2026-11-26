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
./mpeg2dec/src/mpeg2dec -o pgm videos/elementary/pendulum.m2v
```

3) Voici le fichier `encoded_images/pendulum/0.pgm`
```
P5 # cette ligne donne le type de la structure (c'est un magic number) et P5 indique que c'est un PGM
720 720 # (witdh) (3/2 * height)
255 # la valeur maximale pour encoder les couleurs (profondeur)
BINAIRE # chaque pixel est codé par 1 ou 2 octets selon que la valeur maximale soit strictement inférieure (1 octet), ou bien supérieure ou égale à 256 (2 octets) // source: https://fr.wikipedia.org/wiki/Portable_pixmap
```
Pour le sampling mode nous sommes en 4:2:0 (Y full res, U et V font la width/2 et height/2)

4)
Les flags `progressive_frame`, `top_field_first`, `repeat_first_field` correspondent respectivement aux flags dans le code `PIC_FLAG_PROGRESSIVE_FRAME`, `PIC_FLAG_TOP_FIELD_FIRST`, `PIC_FLAG_REPEAT_FIRST_FIELD` qui sont définis dans `include/mpeg2.h`. On a donc rajouté les logs dans un fichier `CSV` pour chaque images dans `src/mpeg2dec.c` au moment de la fin du traitement de chaque images.

5) L'une des premières version naïve (disponible [ici](https://github.com/Antrubtor/TVID-project/blob/17396d148d8f60ea6fd9c1c6ee8921330f19cde3/src/pgm_to_decoded_matrix.py)) fonctionnait (et fonctionne toujours pareil par principe) par :
* une fonction qui faisait une lecture en binaire du headeur, ainsi que mettre toutes les valeurs de pixel de l'image non décodés dans une matrice.
* une fonction qui permet de récupérer la valeur Y, U et V pour chaque pixels et en fait la conversion pour au final retourner une matrice décodée.
* une fonction pour écrire l'image au format P3 de PPM car le plus simple à gérer.
Pour faire l'application nous avons choisis d'utiliser Python pour sa simplicité, puis dans les versions futures nous avons utilisés Numpy car nous avions été confrontés à des problèmes d'optimisation...

6) Pour ajouter des options nous avons utilisé le package `argparse`, et pour l'affichage en séquence nous avons utilisé le package `cv2`.

7) Le flag `frame_period` correspond à un élément de la struct `mpeg2_sequence_s` étant elle même dans la struct `mpeg2_info_s`. Mais comme nous avions déjà choisi le format `CSV` nous l'avons log pour chaque frame même si la valeur est pour toute les frames de la vidéo.

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
Le pid du flux vidéo est `0x1422`

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
Le pid du flux de la 3ème vidéo est `0x3fd`

2) Notre `scripts/setup.sh` démultiplexe déjà ce stream avec:
```
./mpeg2dec/src/mpeg2dec -t 0x3fd -o pgm videos/ts/ctv.ts
```
Encore une fois `progressive_frame` alterne entre 0 et 1, par contre `progressive_sequence` est correcte. Donc `uv run main.py encoded_images/ctv3 --progressive_frame 0` corrige les problèmes.

3) Le jeu d'acteur est absolument incroyable mais quand les effets sur le gateau sont affichés et que l'on regarde frame par frame on a l'impression que la fille déplace d'avant en arrière une crèpe sur sa poele. En gros les images ne sont pas dans l'ordre, alors qu'il n'y a pas cet effet sur vlc. L'effet à du être rajouté en top field first alors que notre vidéo est en bottom field first, ce qui donne cet effet lorsque la séquence a été rajoutée.

4) Avec la question C)1) on peut voir que l'id du premier flux vidéo est `0x3e9`

5)
```
./mpeg2dec/src/mpeg2dec -t 0x3e9 -o pgm videos/ts/ctv.ts
```
Il ne faut pas trust `progressive_frame` ni `progressive_sequence`, car à vue d'oeil les images ne sont pas entrelassées. Donc `uv run main.py encoded_images/ctv1 --progressive_frame 1` a le bon rendu.

6) `progressive_sequence` est faux, les frames sont techhniquement toutes progressives MAIS avec des particularitées:

Si `top_field_first` = 0 et `repeat_first_field` = 0 et `progressive_frame` = 0 : on affiche l'image 1 fois (durée normale de 2 trames)
Si `top_field_first` = 1 et `repeat_first_field` = 1 et `progressive_frame` = 0 : on affiche l'image 1.5 fois (3 trames)
Si `top_field_first` = 0 et `repeat_first_field` = 0 et `progressive_frame` = 1 : on affiche l'image 1 fois (durée normale de 2 trames, en progressif)
Si `top_field_first` = 0 et `repeat_first_field` = 1 et `progressive_frame` = 1 : on affiche l'image 2 fois (4 trames)
Si `top_field_first` = 1 et `repeat_first_field` = 1 et `progressive_frame` = 1 : on affiche l'image 3 fois (6 trames)

### D:

1)

2)

3)
