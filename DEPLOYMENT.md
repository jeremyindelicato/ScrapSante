# Déploiement sur Streamlit Cloud

## Configuration des secrets

Pour déployer ce dashboard sur Streamlit Cloud, vous devez configurer les secrets.

### Étapes de déploiement

1. **Poussez votre code sur GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Dashboard Casemix"
   git branch -M main
   git remote add origin https://github.com/votre-username/votre-repo.git
   git push -u origin main
   ```

2. **Connectez-vous sur Streamlit Cloud**
   - Allez sur [share.streamlit.io](https://share.streamlit.io)
   - Connectez-vous avec votre compte GitHub
   - Cliquez sur "New app"

3. **Configurez l'application**
   - Sélectionnez votre repository GitHub
   - Sélectionnez la branche `main`
   - Spécifiez le fichier principal : `app_analyse_casemix.py`

4. **Configurez les secrets**
   - Cliquez sur "Advanced settings"
   - Dans la section "Secrets", ajoutez :
   ```toml
   DASHBOARD_PASSWORD = "votre_mot_de_passe_securise"
   ```

5. **Déployez**
   - Cliquez sur "Deploy!"
   - Attendez que l'application soit déployée

## Configuration locale avec .env

Pour le développement local :

1. Copiez le fichier `.env.example` vers `.env`
   ```bash
   cp .env.example .env
   ```

2. Modifiez le fichier `.env` avec votre mot de passe
   ```
   DASHBOARD_PASSWORD=votre_mot_de_passe
   ```

3. Lancez l'application
   ```bash
   streamlit run app_analyse_casemix.py
   ```

## Sécurité

- Le fichier `.env` est ignoré par git (voir `.gitignore`)
- Ne commitez jamais le fichier `.env` contenant des secrets
- Sur Streamlit Cloud, utilisez toujours la configuration des secrets intégrée
- Changez le mot de passe par défaut avant le déploiement

## Structure des fichiers

```
.
├── app_analyse_casemix.py          # Application principale
├── data_casemix_2022_2024.csv      # Données
├── etablissements_finess.csv       # Mapping FINESS
├── requirements.txt                # Dépendances Python
├── .env                           # Variables d'environnement (local)
├── .env.example                   # Exemple de configuration
├── .gitignore                     # Fichiers à ignorer par git
└── DEPLOYMENT.md                  # Ce fichier
```
