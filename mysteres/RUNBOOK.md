# Cerveau Minute — format « Mystères » (publication quotidienne)

Chaque exécution **prépare une seule** vidéo pour Instagram @nox.science (ex-@cerveauminute). **Mode semi-automatique** : la tâche ne publie PAS sur Instagram. Arno publie lui-même depuis l'application pour ajouter un son de la bibliothèque Instagram (« Interstellar slowed »). La tâche lui envoie une notification avec les liens et la légende.
Tout ce qui concerne ce format vit dans `mysteres/`. Ne jamais toucher à `disparaitre/` (autre compte).
Les fichiers à la racine (`RUNBOOK.md`, `journal.json`, `scripts/`, `outil/`) appartiennent à l'ancien format et ne servent plus.

## Constantes
- Dépôt : `shfyy8jvfy-lab/cerveauminute-videos` (public, branche `main`)
- URL publique d'une vidéo : `https://raw.githubusercontent.com/shfyy8jvfy-lab/cerveauminute-videos/main/mysteres/<fichier>`
- Voix ElevenLabs : **Zion Aquila - Deep, Aged, Warm**, `voice_id = t2969wgUwHbBoVCZNHRU`, modèle `eleven_v4` (indications de jeu entre crochets), `generations_count = 1`, flow à réutiliser `1etQVP5O9lEQcDAGVgzu`. Traitement obligatoire après téléchargement : `sh ../../moteur/voix.sh dl/voice_raw.mp3 voice.mp3` (≈ 2 demi-tons plus grave + coffre).
- Windsor.ai : NE PLUS PUBLIER par Windsor (mode semi-automatique). Compte `17841472152672061` (nox.science) pour mémoire.
- Moteur : `mysteres/moteur/` (`timing.py`, `render.py`, `music.py`, `assemble.py`). Dépendances : `numpy`, `opencv-python`, `scipy`, `ffmpeg` (sinon `pip install --break-system-packages numpy opencv-python-headless scipy`). Police des sous-titres : Inter (`fc-list | grep -i inter`) ; à défaut libass prend une police par défaut, ce n'est pas bloquant.

## Déroulé d'une exécution
0. Lire `mysteres/journal.json`. Si la date du jour (Europe/Brussels) est **avant** `debut` : ne rien faire, terminer.
   Si un élément de `prets` a déjà la date du jour : un épisode a déjà été préparé aujourd'hui → renvoyer la notification de l'étape 10 pour cet épisode, puis terminer.
1. (rien : en mode semi-automatique, on fabrique toujours un nouvel épisode)
2. **Fabriquer un épisode** : prendre le premier sujet de `banque_sujets`. Numéro = dernier numéro (publiées + prêts) + 1. Dossier `mysteres/episodes/epNN_<slug>/`.
3. **Recherche** (WebSearch / WebFetch) : chaque chiffre, date ou affirmation doit avoir au moins une source sérieuse (revue scientifique, institution, presse scientifique ou archéologique reconnue). Si un fait n'est pas confirmé : le retirer. Si le sujet ne tient pas : le déplacer en fin de banque et prendre le suivant. Pas de pseudo-science, pas d'extraterrestres « sérieux ».
4. **Écrire `plan.json`** sur le modèle de `episodes/ep01_grand_vide/plan.json` :
   - `sentences[]` : `text` (ce que la voix dit, nombres en lettres, sauf les années comme « 2017 »), `shots` (liste `[nom_du_plan, fraction]`, fractions qui somment à 1), `callouts` optionnels (`[texte court en MAJUSCULES, position 0-1 dans la phrase]`, un chiffre clé, ≤ 24 caractères).
   - **Structure obligatoire** : (1) **accroche choc** dès la 1re phrase, avec le fait le plus intrigant ; (2) **une phrase de contexte** (où, quand, qui) ; (3) développement avec 4 à 6 faits surprenants et précis, moins connus du grand public ; (4) fin qui **boucle sur l'accroche** et laisse un mystère ouvert. Ne jamais commencer sans contexte.
   - Ton : sensationnel, mystérieux, phrases courtes et rythmées, mais **aucune information faussée**.
   - Longueur : 200 à 240 mots (≈ 70 à 80 s avec cette voix).
   - `sources` : liste des sources (titre, revue/site, année).
   - `legende` : 1 phrase d'accroche + 1 emoji, une ligne « Sources : … » (revues/années), la ligne « 🎙️ Voix générée par IA. », puis 4 à 5 hashtags dont toujours `#noxscience`.
5. **Plans 3D** : réutiliser les plans du moteur si pertinents (`grep "^def sh_" mysteres/moteur/render.py`), et écrire les plans propres au sujet dans `epNN_<slug>/scenes.py` (fonctions `sh_<nom>(img, u, t, v, T)`, exécutées dans l'espace du moteur : `Scene` avec `box`, `seg`, `add`, `circle`, `pyramid`, `grid_plane` ; `look_at`, `orbit`, `draw`, `stars`, `ease`, `lerp` ; couleurs `GOLD`, `AMBER`, `WHITE`, `COPPER`, ou d'autres définies dans scenes.py, en BGR 0-1). Voir les exemples `sh_chisel_granite`, `sh_muons`, `sh_river_map` dans render.py.
   - Style : fil de fer lumineux sur fond noir, objet principal bien cadré et assez grand au centre de l'écran vertical, caméra qui bouge doucement (orbite ou travelling), un plan par idée.
   - `v` = numéro de l'angle quand un plan long est découpé : prévoir 2 ou 3 cadrages différents selon `v`.
   - Pas de personnage connu, pas de logo, pas de visage réaliste.
6. **Contrôle visuel avant la voix** (dans le dossier de l'épisode) :
   `python3 ../../moteur/timing.py && python3 ../../moteur/render.py x --preview`
   puis assembler les PNG de `previews/` en planche contact et **la regarder** (Read). Corriger les plans vides, trop petits, hors cadre ou illisibles. Supprimer `previews/` ensuite.
7. **Voix off** :
   - Dans `plan.json`, chaque phrase peut avoir un champ `jeu` (indication de jeu en anglais, ex. `"slow, commanding, deep voice"`, `"lower, mysterious"`, `"intense"`, `"slow, solemn"`, `"dramatic pause, low"`). En mettre sur l'accroche, la révélation et la fin (4 à 6 au total) pour une voix charismatique, lente et imposante.
   - `creative_generate_speech` : `prompt` = pour chaque phrase `[jeu] text` (ou juste `text` sans jeu), mis bout à bout avec un espace ; `voice_id`, `model_id = eleven_v4`, `flow_id` et `generations_count = 1` comme ci-dessus. Les crochets ne vont QUE dans le prompt, jamais dans `text`.
   - Attendre ~20 s, puis `creative_get_flow_run_status` (flow_id + session_ids) jusqu'à `all_completed` ; `curl -sSf -o dl/voice_raw.mp3 "<content_url>"`.
   - `creative_add_flow_asset_node` (flow_id, `generation_id` de la prise, `modality = audio`), puis `creative_transcribe_audio` (flow_id, `connect_from = [node_id]`, `model_id = eleven_scribe_v1`). Attendre ~15 s, `creative_get_flow_run_status` → `curl -sSf -o words.json "<words_download_url>"`.
   - Si ElevenLabs échoue : réessayer au plus 2 fois, à 2 minutes d'intervalle (`sleep 120`), jamais deux appels dans la même minute. Sinon, échec (étape 11).
   - Traitement de la voix : `sh ../../moteur/voix.sh dl/voice_raw.mp3 voice.mp3`
8. **Montage** (dans le dossier de l'épisode) :
   ```
   python3 ../../moteur/timing.py voice.mp3 words.json
   python3 ../../moteur/render.py visual.mp4          # ~4-6 min
   python3 ../../moteur/music.py music.wav
   python3 ../../moteur/assemble.py visual.mp4 final_sans_musique.mp4 voice.mp3
   python3 ../../moteur/assemble.py visual.mp4 final_orgue.mp4 voice.mp3 music.wav
   ffmpeg -y -i final_sans_musique.mp4 -c:v libx264 -preset veryfast -crf 23 -c:a copy -movflags +faststart ../../videos/epNN_<slug>_sans_musique.mp4
   ffmpeg -y -i final_orgue.mp4 -c:v libx264 -preset veryfast -crf 23 -c:a copy -movflags +faststart ../../videos/epNN_<slug>_orgue.mp4
   ```
   La version **sans musique** est celle qu'Arno publie (il ajoute le son dans l'application). La version **orgue** est une solution de secours, avec la musique originale.
   **Contrôle** : extraire 6 images (début, accroche, milieu, révélation, fin) et les regarder ; vérifier la durée (entre 45 et 90 s : les reels publiés par certains outils sont limités à 90 s), que les sous-titres suivent la voix et que le volume est proche de -14 LUFS (`ffmpeg -i ... -af ebur128 -f null -`). Corriger avant de continuer.
   Ne pas committer `visual.mp4`, `final*.mp4`, `music.wav`, `previews/` (dans le `.gitignore`). Committer `plan.json`, `scenes.py`, `timeline.json`, `words.json`, `voice.mp3` et les deux vidéos finales.
   Retirer le sujet de `banque_sujets` et l'ajouter à `sujets_traites`.
9. **Pousser** : `git add` + commit + `git push` (faire `git pull --rebase` avant si besoin). Vérifier `curl -sI` sur les deux URL raw → HTTP 200 (attendre 30 s et réessayer si 404).
10. **Prévenir Arno (pas de publication Instagram)** : ajouter l'épisode à `prets` dans le journal (n, sujet, dossier, date, `video_sans_musique` et `video_orgue` = URL raw, `legende`), `dernier_echec = null`, commit, push. Puis envoyer une notification push (outil `PushNotification`) **courte** : « Nox #NN prêt : <sujet>. Vidéo : <URL raw sans musique> ». Le message final de l'exécution reprend : le sujet, l'URL de la vidéo sans musique, l'URL de la version orgue, et la légende complète prête à copier-coller.
    **Ne jamais appeler `create_video_post` ni aucune action de publication Windsor ou Metricool.**
11. **En cas d'échec** (recherche, rendu, voix, push) : écrire dans `journal.json` → `dernier_echec = {date, episode, etape, erreur}`, commit, push, envoyer une notification push courte qui signale l'échec, et s'arrêter.

## Règles
- Un seul épisode préparé par exécution, jamais deux fois le même sujet.
- Si `banque_sujets` contient moins de 5 sujets : en ajouter 10 nouveaux (mystères historiques, archéologiques, scientifiques ou d'ingénierie, avec un fait vérifiable et surprenant), sans répéter `sujets_traites`.
- Pas de musique, d'images ou de voix appartenant à d'autres : la musique est générée par `music.py`, les visuels par `render.py`.
- Message final en français : l'épisode prêt (numéro, sujet, liens, légende) ou la raison de l'échec.
