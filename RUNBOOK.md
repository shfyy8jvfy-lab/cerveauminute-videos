# Cerveau Minute — chaîne automatique

Chaque exécution publie **une** vidéo sur Instagram @cerveauminute, sans intervention humaine.

## Constantes
- Dépôt : `shfyy8jvfy-lab/cerveauminute-videos` (public, branche `main`)
- Voix ElevenLabs : **Anatole – Convincing, Dynamic and Clear**, `voice_id = Jrq4GqCKqYpigdQsZRkP`, modèle `eleven_v4`, `generations_count = 1` (offre gratuite : économiser les crédits)
- Flow ElevenLabs à réutiliser : `VDaHz7E3opElVyf9pODw`
- Windsor.ai : connecteur `instagram`, compte `17841472152672061` (cerveauminute), action `create_video_post`
- URL publique d'une vidéo : `https://raw.githubusercontent.com/shfyy8jvfy-lab/cerveauminute-videos/main/videos/<fichier>.mp4`

## Étapes
1. Cloner le dépôt, lire `journal.json`. Prendre le premier élément de `file_attente` (un fichier de `scripts/`).
   - Si `file_attente` est vide : écrire 4 nouveaux scripts (voir « Écrire un script ») à partir de `banque_sujets`, les ajouter à `file_attente`, retirer les sujets de la banque, puis continuer.
2. **Voix off** : `creative_generate_speech` avec le champ `tts` du script, la voix et le flow ci-dessus.
   - Si ElevenLabs répond « Free generations are busy » : ne pas relancer dans le même tour. Attendre ~2 minutes (ex. `sleep 120` dans Bash) et réessayer, **3 essais maximum** au total. Si les 3 échouent : noter l'échec dans `journal.json` (`dernier_echec`) et s'arrêter ; le script reste en tête de file pour la prochaine exécution.
3. Récupérer l'URL du MP3 avec `creative_get_flow_run_status` (attendre `status = completed`), puis `curl -o voix.mp3 "<content_url>"`.
4. **Sous-titres** : `python3 outil/timing.py scripts/<nn>.json voix.mp3 specs/<nn>.json`
5. **Montage** : `python3 outil/render.py specs/<nn>.json videos/cerveau_minute_<nn>.mp4` (police Poppins Bold déjà installée ; sinon `pip install --break-system-packages pillow`).
6. **Contrôle** : extraire 3 images (début, milieu, fin) avec ffmpeg et les regarder. Le texte doit être lisible et en phase avec la voix ; la durée entre 20 et 60 s. Si c'est raté, corriger le script JSON ou le rendu avant de publier.
7. `git add` vidéo + spec, commit, `git push`. Vérifier que l'URL raw répond (HTTP 200) avec `curl -sI`.
8. **Publication** : Windsor `execute_action` → `create_video_post` avec `video_url` (URL raw), `caption` = champ `legende` du script, `share_to_feed = true`.
9. Mettre à jour `journal.json` : déplacer le script de `file_attente` vers `publiees` (numéro, sujet, fichier, date, media_id si fourni), commit, push.

## Écrire un script
- 30 à 40 secondes à l'oral (environ 90 à 110 mots), structure : accroche (question ou fait surprenant) → contexte → explication en 2-3 idées → révélation → question finale pour les commentaires.
- Phrases de moins de 12 mots, pas d'introduction.
- **Vérifier chaque fait** avec au moins une source fiable (WebSearch/WebFetch) ; en cas de doute, changer de sujet. Citer la source dans la légende si un chiffre est surprenant.
- Champ `tts` : le texte lu, nombres écrits en toutes lettres. Champ `segments[].chunks` : le même texte affiché (chiffres autorisés), découpé à chaque pause audible (point, deux-points, points de suspension, virgule forte).
- `key` : 1 à 3 mots en majuscules ; `icon` parmi `door`, `coin`, `ticket`, `plane`, `question`, `none` ; `hl` : 1 ou 2 mots du chunk à surligner (écrits exactement comme dans le texte, ponctuation comprise).
- Légende : 1 phrase + 3 à 5 hashtags, toujours `#cerveauminute`.
- Pas de visage humain réaliste, pas d'imitation de voix réelle, pas de musique ni d'images d'autrui.
