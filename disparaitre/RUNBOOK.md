# On va tous disparaître — chaîne automatique

Chaque exécution fabrique et publie **un** nouvel épisode sur Instagram @on.va.tous.disparaitre, sans intervention humaine.
Concept : chaque Reel raconte un scénario (réel, discuté ou farfelu) d'extinction de l'humanité, expliqué très simplement, avec une légère touche d'humour.

## Constantes
- Dépôt : `shfyy8jvfy-lab/cerveauminute-videos` (public, branche `main`), dossier `disparaitre/`
- Windsor.ai : connecteur `instagram`, compte `17841461678535981` (on.va.tous.disparaitre), action `create_video_post`
- URL publique d'une vidéo : `https://raw.githubusercontent.com/shfyy8jvfy-lab/cerveauminute-videos/main/disparaitre/videos/<fichier>.mp4`
- Voix off ElevenLabs (style « badass / bande-annonce ») qui lit tout le texte à l'écran, par-dessus la nappe sonore générée par `engine.py`. Musique de fond originale générée par `musique.py` (orgue spatial lent, « slowed + reverb », grille originale en ré mineur — jamais d'extrait d'une œuvre existante), mixée automatiquement par `engine.py` sous la voix. Désactivable par épisode avec `MUSIQUE = False` ; volume réglé par `MUSIC_LEVEL` dans `engine.py`.
  - Connecteur ElevenLabs, modèle `eleven_v4`, voix `dcbUcEjFfmgpM8W4YTRG` (Roland Lescalde – Epic Narrator), `generations_count = 1`.
  - Préfixe de chaque prompt : `[deep, powerful, cinematic trailer voice] `
  - Coût ≈ 1 800 crédits ElevenLabs par épisode.

## Étapes
1. Cloner le dépôt (`git clone --depth 1`), lire `disparaitre/journal.json`. Numéro du nouvel épisode = dernier numéro de `publiees` + 1. Sujet = premier élément de `banque_sujets`.
   - Si `banque_sujets` est vide : ajouter 10 nouveaux sujets (mélanger risques sérieux, hypothèses discutées et théories farfelues / mythes à démonter), puis continuer.
2. **Recherche** : vérifier chaque fait du sujet avec au moins deux sources fiables (WebSearch / WebFetch : revues, agences spatiales, universités, grands médias). Noter les sources dans la docstring de l'épisode. Si le sujet est un mythe (ex. Nibiru), le dire clairement dans la vidéo. En cas de doute sur un fait : le retirer.
3. **Écrire** `disparaitre/episodes/epNN.py` en prenant `ep02.py` comme modèle (structure, ton, longueur) :
   - 12 à 14 scènes, 2,2 à 5,4 s chacune, total 45 à 55 s.
   - Ordre : accroche (question) → titre (`scene_title`, 2 lignes de 9 caractères max en capitales) → explication en 4-6 scènes avec **une seule image qui sert de fil rouge** → le moment catastrophe (`BOOM_SCENE` = index de cette scène) → une blague légère du quotidien → ce que disent vraiment les scientifiques (probabilité / délai / consensus) → fin (`scene_end` avec une variante de « vous devrez quand même payer vos impôts »).
   - Phrases courtes, zéro jargon non expliqué. Un mot technique au maximum, entre parenthèses.
   - **Une couleur de fond différente à chaque scène**, dessins simples (cercles, lignes, rectangles arrondis) avec un petit mouvement. Pas de visage réaliste, pas de personnage, logo ou image connus.
   - Texte principal entre y = 1000 et 1450 ; illustration entre y = 300 et 950 ; rien sous y = 1550 (interface Instagram).
   - `VOIX` : liste de textes, **un par scène, dans l'ordre de `SCENES`** (même longueur), écrits pour être lus à voix haute : reprend le texte à l'écran ; nombres écrits en toutes lettres (« neuf pour cent », « quarante et un mille ») ; scène titre = « Scénario d'extinction numéro NN : … » ; scène de fin = la punchline + « Abonnez-vous. Tant qu'il y a un demain. ». Max ~150 caractères par scène.
   - Les durées de `SCENES` sont des minimums : `engine.py` allonge automatiquement chaque scène pour que sa voix tienne (vidéo finale ≈ 60-85 s).
   - `LEGENDE` : titre « Épisode NN : … » + 2-3 phrases (dont le fait clé et sa source si surprenant) + « On va tous disparaître… mais pas aujourd'hui. » + 6 à 9 hashtags dont `#findumonde`.
4. **Aperçu** : `cd disparaitre && python3 engine.py episodes/epNN.py --preview 0:2.5 1:1.5 ...` (une image par scène, au moment le plus chargé), assembler une planche et la regarder. Vérifier : texte lisible, rien qui déborde ou se chevauche, dessins compréhensibles. Corriger puis recommencer jusqu'à ce que ce soit propre.
5. **Voix off** (ElevenLabs) :
   - `creative_create_flow` (nom « On va tous disparaître — epNN voix »), puis pour chaque scène i un appel `creative_generate_speech` avec ce `flow_id`, `model_id = eleven_v4`, `voice_id = dcbUcEjFfmgpM8W4YTRG`, `generations_count = 1`, `prompt = "[deep, powerful, cinematic trailer voice] " + VOIX[i]`. Les 13-14 appels peuvent partir en même temps. **Ne jamais relancer un appel** (chaque appel est facturé).
   - Attendre ~5 s puis `creative_get_flow_run_status` avec toutes les `session_ids` jusqu'à `all_completed`. Associer chaque résultat à sa scène **par le texte du prompt** (pas par l'ordre).
   - Télécharger chaque `content_url` avec `curl` vers `voix/epNN/sII.mp3` (s00.mp3, s01.mp3…). Vérifier qu'il y a exactement un fichier par scène.
   - `python3 engine.py episodes/epNN.py --durees` : affiche les durées finales et le `thumb_offset`.
   - Si une génération échoue ou si le connecteur ElevenLabs est indisponible : noter `dernier_echec`, pousser, s'arrêter sans publier.
6. **Rendu** : `python3 engine.py episodes/epNN.py videos/epNN_<sujet>.mp4` (≈ 1-2 min). Contrôler 3 images extraites avec ffmpeg, la durée (55-90 s) et que la piste audio n'est pas muette (`ffmpeg -i … -af volumedetect -f null -` : mean_volume entre -30 et -12 dB).
7. `git add` épisode + `voix/epNN/` + vidéo, commit, `git fetch && git rebase origin/main`, `git push`. Vérifier que l'URL raw répond HTTP 200 (`curl -sI`).
8. **Publication** : Windsor `get_connectors` pour vérifier que le compte `17841461678535981` est bien listé (sinon : noter `dernier_echec` dans le journal, pousser, s'arrêter). Puis `execute_action` → `create_video_post` avec `video_url`, `caption` = `LEGENDE`, `share_to_feed = true`, `thumb_offset` = valeur donnée par `--durees`.
9. Mettre à jour `journal.json` : retirer le sujet de `banque_sujets`, ajouter à `publiees` (numero, sujet, fichier, date, media_id), commit, push.
