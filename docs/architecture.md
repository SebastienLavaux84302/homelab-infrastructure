# Architecture : vue fonctionnelle

Le lab personnel permet de manipuler des machines virtuelles sous Proxmox et d'expérimenter l'administration et les déploiements automatisés. Les composants et les relations ci-dessous sont une représentation pédagogique : les services, les réseaux et les flux varient selon les essais.

| Élément | Rôle dans les expérimentations |
| --- | --- |
| Proxmox | Héberger les machines virtuelles utilisées pour les tests. |
| Machine d'administration | Préparer les configurations et lancer Ansible. |
| Machines de lab | Accueillir des systèmes et des services à installer ou examiner. |
| Réseau personnel UniFi | Fournir un environnement pour expérimenter le réseau et ses équipements. |

## Principes de conception à adapter

1. Définir une zone de test distincte des équipements usuels et n'autoriser que les communications nécessaires.
2. Séparer, lorsque l'exercice le permet, l'administration, les services et les machines volontairement vulnérables.
3. Prévoir une méthode de retour arrière avant une modification : sauvegarde testée, snapshot adapté au contexte ou reconstruction.
4. Réduire les privilèges et éviter d'exposer directement des services de lab à Internet.
5. Documenter les versions, prérequis et résultats réels d'un essai au moment où il est effectué.

Ces points décrivent une démarche de conception, pas un audit ni une affirmation que chaque mesure est en place dans l'installation personnelle.

## Ce qui n'est pas publié

Pas d'adresses ou de noms d'hôtes réels, de plan réseau détaillé, de clés, d'identifiants, de sauvegardes ni d'images de machines. Les exemples utilisent des noms fictifs et doivent être adaptés à un environnement autorisé.
