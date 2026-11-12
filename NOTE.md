# Note pour dev

## Image progressive (progressive_frame = 1)
- C'est le fonctionnement actuel basique
- YUV:
    - Y : Luma (luminance) -> 2 premiers tiers de la hauteur
    - U (gauche) et V (droite) : Chroma (chrominance) -> dernier tier de la hauteur
- Ainsi pour construire l'image finale:
    - Pour 2 lignes Luma, on regarde une même ligne Chroma
    - Ex: Pour la ligne 0 et 1 de Luma, on regarde la ligne Y//2 = 0 de Chroma
    - Ex: Pour la ligne 2 et 3 de Luma, on regarde la ligne Y//2 = 1 de Chroma
    - etc
- Simple et efficace

## Image entrelacée (progressive_frame = 0)
- C'est le cas où une image même image à capturé 2 instants en même temps (par exemple à cause du mouvement)
- YUV (same) sauf que:
    - 1 ligne sur 2 correspond à une frame, et le reste des lignes à une autre frame (que ce soit pour la Luma ou la Chroma).
    - Comment ça fonctionne ?
    - Les lignes paires (0, 2, 4, ...) constituent le Top Field
    - Les lignes impaires (1, 3, 5, ...) le Bottom Field
- La construction des images:
    - Pour le Top Field par exemple (lignes paires):
    - Ces lignes là doivent garder les même données dans l'image résultante
    - Le reste des lignes doivent être interpolées
    - Pour la ligne paire actuelle (Luma) on regarde sa Chroma (mais qui elle aussi est entrelacée !):
    - Donc pour la ligne 0 de Luma, on regarde Y//2 = 0 de Chroma
    - Pour la ligne 2 de Luma, on regarde la même Chroma que pour la précédente (0)
    - Pour la ligne 4 de Luma, on regarde Y//2 = 2 de Chroma
    - Pour la ligne 6 de Luma, on regarde la même Chroma que pour la précédente (4)
    - etc...
    - Et c'est la même chose avec les lignes impaires pour le Bottom Field
- Ensuite la colonne (top_field_first) dans les logs nous permet de savoir quelle frame mettre en 1ère ou en 2ème
- Et la colonne (repeat_first_field) fait répéter la 1ère frame une fois de plus en 3ème position !
