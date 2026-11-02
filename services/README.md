# Jenkins et SonarQube avec Ansible

Deux rôles expérimentaux pour un **laboratoire RHEL 9 ou compatible**, avec des sources logicielles déjà disponibles. Ils ont été créés pour ce portfolio avec l'assistance de **Codex (OpenAI)** et ne correspondent pas à une copie des déploiements personnels d'origine.

| Rôle | Actions | Source logicielle |
| --- | --- | --- |
| `lab_jenkins` | Installe Java, les dépendances et le paquet Jenkins, puis démarre son service systemd. | Dépôts DNF déjà configurés, par exemple synchronisés via Satellite. |
| `lab_sonarqube` | Vérifie une archive, installe une version, configure l'accès PostgreSQL et un service systemd dédié. | Archive officielle fournie sur le contrôleur Ansible et dépendances présentes dans les dépôts DNF. |

Ces rôles concernent une **installation de test**. Ils ne configurent pas de plugins, de pipelines, de TLS, de proxy inverse ou de règles de pare-feu et ne créent pas la base PostgreSQL. Vérifier les licences, versions, ressources et conditions d'utilisation de chaque produit.

## Prérequis

- Un contrôleur avec `ansible-core` 2.16, un accès SSH aux cibles et les privilèges nécessaires ; Python et le support DNF doivent être disponibles sur les cibles.
- Deux groupes d'inventaire : `jenkins` et `sonarqube`, sur des machines de test de la famille Red Hat 9.
- Les paquets et leurs dépendances déjà présents dans les dépôts autorisés. En environnement Satellite déconnecté, synchroniser et publier préalablement les contenus nécessaires, dont le RPM Jenkins et sa clé de signature approuvée si le dépôt l'exige.
- Pour SonarQube : une base PostgreSQL compatible, créée et accessible, avec un compte dédié ; une archive officielle au format ZIP, sa version exacte et son SHA-256 vérifié auprès de la source de confiance ; un JDK compatible avec cette version. Les valeurs fournies ici prévoient Java 21, à adapter selon la version choisie. Si plusieurs versions de Java sont installées, vérifier le binaire sélectionné par défaut et adapter `lab_sonarqube_java_path`.
- Sur la cible SonarQube, vérifier notamment `vm.max_map_count` (valeur par défaut contrôlée : au moins 524288) et l'accès à `/tmp`. Le rôle ne modifie pas les paramètres du noyau. L'unité systemd fixe les limites de fichiers et de processus.

Les cibles n'ont pas besoin d'un accès direct à Internet si les sources et dépendances ont été préparées. Le rôle SonarQube copie l'archive depuis le contrôleur ; il ne la télécharge pas.

## Préparer les variables

Depuis ce répertoire :

```bash
cp inventories/services.example.yml inventories/services.local.yml
cp vars.example.yml vars.local.yml
# Modifier l'inventaire et les variables locales.
ansible-vault create secrets.local.yml
```

Dans le fichier chiffré `secrets.local.yml`, définir `vault_sonarqube_db_password` avec le mot de passe du compte PostgreSQL. Le fichier `vars.local.yml` l'utilise sans le révéler en clair. Conserver ces fichiers et le mot de passe Vault hors du dépôt ; ils sont ignorés par `.gitignore`.

L'exemple utilise des noms en `.invalid` et un SHA-256 à remplacer : il ne représente aucune machine réelle. Les listes `*_enablerepo` et `*_disablerepo` sont facultatives et s'appliquent aux transactions DNF des rôles ; elles ne remplacent pas la préparation et l'activation des dépôts Satellite nécessaires sur la cible.

## Vérifier et déployer

```bash
# Vérification syntaxique, sans connexion aux cibles.
ansible-playbook -i inventories/services.local.yml playbooks/lab-services.yml --syntax-check

# Jenkins : mode simulation, puis déploiement après lecture du résultat.
ansible-playbook -i inventories/services.local.yml playbooks/jenkins.yml --check
ansible-playbook -i inventories/services.local.yml playbooks/jenkins.yml

# SonarQube : prérequis, puis déploiement après vérification.
ansible-playbook -i inventories/services.local.yml playbooks/sonarqube.yml --check --extra-vars @vars.local.yml --extra-vars @secrets.local.yml --ask-vault-pass
ansible-playbook -i inventories/services.local.yml playbooks/sonarqube.yml --extra-vars @vars.local.yml --extra-vars @secrets.local.yml --ask-vault-pass
```

Pour SonarQube, `--check` contrôle seulement les prérequis, le SHA-256 du fichier sur le contrôleur et `vm.max_map_count` : il ne simule ni l'extraction, ni la configuration, ni le démarrage. Pour Jenkins, DNF estime les changements mais le démarrage systemd n'est pas vérifié en mode simulation. Les métadonnées des dépôts peuvent être consultées pendant la vérification DNF.

Le rôle SonarQube écoute par défaut sur `127.0.0.1:9000` et n'ouvre pas de port dans le pare-feu. Adapter l'accès à son lab ; par exemple, utiliser un tunnel SSH. La configuration et les journaux peuvent contenir des données sensibles : ne pas les publier.

## Contrôles locaux

Depuis ce répertoire, avec Ansible installé sur le contrôleur :

```bash
ansible-playbook -i localhost, tests/validate-roles.yml
python3 -m unittest discover -s tests -v
```

Le premier test utilise une archive fictive et une limite mémoire volontairement réduite pour vérifier les contrôles, y compris le rejet d'un mauvais SHA-256. Il ne déploie aucun service. Le second vérifie l'échappement des propriétés Java.

## Limites et diagnostic

- Vérifier l'état des services avec `systemctl status jenkins` et `systemctl status lab-sonarqube`, puis leurs journaux avec `journalctl -u jenkins` ou `journalctl -u lab-sonarqube` sur la cible.
- Jenkins peut nécessiter une configuration initiale et des plugins obtenus depuis des sources autorisées. Ne pas publier le mot de passe initial ni les secrets d'administration.
- Le rôle SonarQube attend une archive officielle dont le répertoire et le JAR contiennent la version indiquée. Il considère chaque version extraite comme immuable : remplacer le contenu d'une archive pour la même version ne déclenche pas une nouvelle extraction.
- Les paramètres PostgreSQL sont écrits dans `sonar.properties` en mode `0640`. Les tâches qui les manipulent masquent leur sortie et désactivent le diff, mais l'hôte et ses sauvegardes doivent rester protégés.
- La syntaxe et les contrôles locaux sont testés ; aucun déploiement complet sur RHEL 9, Satellite, PostgreSQL ou un vrai SonarQube n'est revendiqué ici. Tester les versions choisies sur des machines jetables avant tout autre usage.

Références : [installation Jenkins sur Linux](https://www.jenkins.io/doc/book/installing/linux/), [préparation Linux SonarQube Community Build](https://docs.sonarsource.com/sonarqube-community-build/server-installation/pre-installation/linux), [SonarQube en tant que service](https://docs.sonarsource.com/sonarqube-server/server-installation/from-zip-file/starting-stopping-server/running-as-a-service).
