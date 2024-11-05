Coucou bienvenue sur le github de ALLERLEFOOT Analytics

Raw data : https://github.com/statsbomb/open-data

Pour télécharger les modifications depuis le repo distant vers la machine locale :

git status

Vérifier qu'on est bien dans le bon repo

git pull

Ca devrait afficher un téléchargement de toutes les modifs récentes (ou rien si pas de modifs)

Puis modifications en local

Puis commit grâce aux extensions git sur vscode (barre de gauche)

competition : competition_id + season_id

matches/competition_id/season_id/ liste des match_id

events/match_id/liste des events

Ligue 1 2015/2016 : competition_id 7, season_id 27

shot : id 16 dans event

## Import des données brutes

Mettre le repo de données brutes au même niveau que ce repo : 

dir
|
|->al-lefoot
|->open-data