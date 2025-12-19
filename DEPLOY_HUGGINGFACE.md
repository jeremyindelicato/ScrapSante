# Guide de déploiement sur Hugging Face Spaces

## Étape 1 : Créer un compte et un Space

1. Va sur https://huggingface.co/join et crée un compte
2. Une fois connecté, clique sur ton profil → "New Space"
3. Configure :
   - **Space name** : `dashboard-casemix` (ou ton choix)
   - **License** : MIT
   - **Select SDK** : **Streamlit**
   - **Space hardware** : CPU basic (gratuit)
4. Clique sur **Create Space**
5. **IMPORTANT** : Note l'URL de ton Space (ex: `https://huggingface.co/spaces/ton-username/dashboard-casemix`)

## Étape 2 : Renommer le README pour Hugging Face

Dans ton terminal/PowerShell :

```bash
cd "c:\Users\JIndelic\OneDrive - Stryker\Bureau\Casemix extraction"

# Sauvegarder l'ancien README
mv README.md README_OLD.md

# Utiliser le nouveau README pour Hugging Face
mv README_HF.md README.md
```

## Étape 3 : Ajouter Hugging Face comme remote Git

```bash
# Remplace 'ton-username' et 'dashboard-casemix' par tes valeurs
git remote add huggingface https://huggingface.co/spaces/ton-username/dashboard-casemix

# Vérifier
git remote -v
```

## Étape 4 : Pousser le code vers Hugging Face

```bash
# Commiter le nouveau README
git add README.md README_HF.md
git commit -m "Prepare for Hugging Face Spaces deployment"

# Pousser vers Hugging Face (attention, Git LFS va uploader le Parquet)
git push huggingface main --force
```

**Note** : Le push peut prendre 2-3 minutes à cause de Git LFS (40 MB de Parquet).

## Étape 5 : Configurer les Secrets sur Hugging Face

1. Va sur ton Space : `https://huggingface.co/spaces/ton-username/dashboard-casemix`
2. Clique sur **Settings** (en haut à droite)
3. Scroll jusqu'à **Repository secrets**
4. Clique sur **New secret**
5. Ajoute :
   - **Name** : `DASHBOARD_PASSWORD`
   - **Value** : `1234` (ou ton mot de passe)
6. Clique sur **Save**

## Étape 6 : Attendre le déploiement

1. Retourne sur l'onglet **App** de ton Space
2. Le build va démarrer automatiquement
3. Attends 3-5 minutes (première fois)
4. L'app sera accessible à : `https://ton-username-dashboard-casemix.hf.space`

## Étape 7 : Tester l'application

1. Ouvre l'URL de ton Space
2. Entre ton mot de passe (1234)
3. Teste la navigation et les filtres
4. **Vérifie que c'est plus rapide qu'avant !** 🚀

## ⚠️ Troubleshooting

### Erreur "Git LFS" lors du push
```bash
# Installer Git LFS si pas déjà fait
git lfs install
git lfs track "*.parquet"
git add .gitattributes
git commit -m "Add Git LFS tracking"
git push huggingface main --force
```

### L'app ne démarre pas
1. Va dans l'onglet **Logs** de ton Space
2. Vérifie les erreurs
3. Souvent c'est un problème de secrets → vérifie que DASHBOARD_PASSWORD est bien configuré

### Mot de passe ne fonctionne pas
1. Settings → Repository secrets
2. Vérifie que DASHBOARD_PASSWORD = "1234" (avec guillemets)

## 🎉 C'est terminé !

Si tout fonctionne, ton dashboard est maintenant déployé sur Hugging Face avec 16 GB de RAM au lieu de 1 GB sur Streamlit Cloud. Les performances devraient être **beaucoup meilleures** !

## 📊 Comparaison

| | Streamlit Cloud | Hugging Face Spaces |
|---|---|---|
| RAM | 1 GB | 16 GB |
| CPU | Partagé | Dédié |
| Coût | Gratuit | Gratuit |
| Performance | ⭐⭐ | ⭐⭐⭐⭐⭐ |
