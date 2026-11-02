# Exemple : diagnostic d'une machine Linux

Ce petit playbook pédagogique vérifie la connexion Ansible et affiche la distribution, sa version et le gestionnaire de services. Il ne configure pas de service et ne nécessite pas d'élévation de privilèges. Ansible utilise toutefois un répertoire temporaire sur la cible pour exécuter ses modules et collecte des faits système.

## Prérequis

- Ansible sur le contrôleur et Python sur la cible ;
- une machine de test Linux, accessible en SSH avec un compte autorisé ;
- un inventaire adapté à cette cible.

```bash
cp inventory.example.yml inventory.local.yml
# Modifier le nom d'hôte, l'adresse et l'utilisateur dans inventory.local.yml.
ansible-playbook -i inventory.local.yml diagnostic.yml --syntax-check
ansible-playbook -i inventory.local.yml diagnostic.yml
```

Le domaine `.invalid` de l'exemple est fictif : il faut le remplacer avant la seconde commande. `--syntax-check` vérifie la syntaxe du playbook sans établir la connexion ; la seconde commande se connecte à la cible. Adapter la configuration SSH sans stocker de mot de passe ou de clé privée dans le dépôt.

Le YAML de cet exemple a été vérifié. Son exécution avec Ansible et sur une cible distante reste à valider.

Le rapport réel dépend de la machine et de sa configuration. Ne pas publier de sortie contenant des informations propres à une infrastructure privée.
