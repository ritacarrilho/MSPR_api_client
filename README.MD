## Kawa Products API 

## Participants 👥
- BILLARD Mélissa
- BRACCIALES-COMBAS Lola
- CARRILHO LAMEIRA Rita
- DIAGNE Sokhna

## Technologie 
- Api en [FastApi](https://fastapi.tiangolo.com/)

## Base de données
- [MySQL](https://www.mysql.com/fr/)

**Nom BDD** : ``customer_db``

### Création de la base de donnée
```python
## De la racine
py database/scripts/create_BDD.py
```
![](/assets/create_bdd-2.png)

### Mock initial
```
https://615f5fb4f7254d0017068109.mockapi.io/api/v1/customers
```
*Liste de données de tous les clients.*

![](./assets/mock_client.png)

### Modèle Conceptuel de Données (MCD)
![](./assets/BDD_client-2.png)

#### Modèle Logique de Données (MLD)
![](./assets/mld-2.png)


### Détails tables

#### Table ``customers``

id (INT, clé primaire) : Identifiant unique du client.

created_at (DATETIME) : Date de création du client.

name (VARCHAR) : Nom complet du client.

username (VARCHAR) : Nom d'utilisateur du client.

first_name (VARCHAR) : Prénom du client.

last_name (VARCHAR) : Nom de famille du client.

postal_code (VARCHAR) : Code postal de l'adresse.

city (VARCHAR) : Ville de l'adresse.

#### Table ``profiles``

id (INT, clé primaire) : Identifiant unique du profil.

customer_id (INT, clé étrangère) : Référence à l'identifiant du client.

first_name (VARCHAR) : Prénom du profil.

last_name (VARCHAR) : Nom de famille du profil.

#### Table ``companies``

id (INT, clé primaire) : Identifiant unique de l'entreprise.

customer_id (INT, clé étrangère) : Référence à l'identifiant du client.

company_name (VARCHAR) : Nom de l'entreprise.

#### Table ``orders``

id (INT, clé primaire) : Identifiant unique de la commande.

customer_id (INT, clé étrangère) : Référence à l'identifiant du client.

created_at (DATETIME) : Date de création de la commande.

## Endpoints de l'API
![](/assets/api-endpoint.png)

## Docker

1) Build container : ```docker-compose build```

2) Start container : ```docker-compose up```

## Commandes utiles
### Lancer l'api en local
```python
# Dans le fichier app
fastapi dev main.py
# ou
# À la racine
 uvicorn app.main:app --reload
```
### Effacer fichiers DS_Store
```java
find . -name .DS_Store -print0 | xargs -0 git rm -f --ignore-unmatch
```
