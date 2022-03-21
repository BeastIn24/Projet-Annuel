
La commande pour exécuter le code est :
python3 main.py <type de chargement des données> saved_matchup_tables/filename <point de vue> <marge epsilon>

Le chargement des données peut être fait depuis le site web directement avec l'argument "save",
dans ce cas les données seront sauvegardées dans le répertoire saved_matchup_tables avec le nom de fichier choisi.
L'url utilisée par le parser est celle écrite dans la classe "parser.py", elle doit être changée selon la table de données voulue.
Il peut être fait en chargeant un fichier json en utilisant l'argument "load", le fichier choisi est celui indiqué par filename.

On peut exécuter les algorithmes du point de vue déterministe en utilisant l'argument "d", et probabiliste
en utilisant "p".

L'argument epsilon est un entier correspondant au pourcentage de marge.
