A PROPOS :
    Cette application a été réalisée dans le cadre d'un projet de SSII
(Son, Signal et Image pour l'Informaticien) à l'école d'ingénieurs
Polytech'Nice - Sophia Antipolis.

    Elle permet de trouver la fréquence de sous échantillonnage 
permettant d’écouter une version comprimée d’un signal haute fidélité 
sans le dégrader de manière excessive en 3 étapes :

    - analyse du contenu du spectre et du spectrogramme du signal 
      pour trouver la nouvelle fréquence d’échantillonnage ;
    - filtrage avec un filtre passe bas ;
    - ré-échantillonnage et reconstruction à la fréquence 
      d’échantillonnage initiale grâce au filtre passe-bas 
      utilisé comme filtre interpolateur.


AUTEURS :
    Guy CHAMPOLION (champoll@polytech.unice.fr)
    François CHAPUIS (fchapuis@polytech.unice.fr)


INSTALLATION :
    Pour que cette application fonctionne, vous devez 
avoir installé sur votre ordinateur la version 2.6
(ou 2.7) de Python ainsi que les bibliothèques suivantes
dont vous trouverez les installeurs dans le dossier "libs":

    - numpy (v 1.5.1)
    - scipy (v 0.8.0)
    - matplotlib (v 1.0.0)

  Vous trouverez des informations sur le rôle joué par ces
bibliothèques à cette adresse :
http://www.scipy.org/Getting_Started#head-29c5ff005c7f21eb9e5e19c850159cdfd80a39ed