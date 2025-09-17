# 📊 Rapport de Performance Mila Assist

## ⚙️ Configuration

- Temps de chargement : **14.0 ms**

- Configuration valide : **Oui**


## ⚡ Temps de réponse & Précision

*Tests basés sur les données réelles de la base de données (comme train.py)*

- Temps moyen combiné (3 modes) : **383.6 ms**

- Précision combinée (3 modes) : **94.6%**


### 🧠 Mode Local Intelligent (Fallback complet)

- Temps moyen : **417.9 ms**

- Précision : **94.9%** (94/99)


### 🤖 Mode Local Brut (Keras seulement)

- Temps moyen : **113.6 ms**

- Précision : **89.9%** (89/99)


### 🌐 Mode API (Serveur externe)

- Temps moyen : **619.5 ms**

- Précision : **99.0%** (98/99)


### 📋 Détails des tests de précision

| Question | Tag attendu | Mots-clés | Réponse | Temps (ms) | Mode | Précis |

|---|---|---|---|---|---|---|

| bonjour | greetings | vous, merci, être | Hello ! Bonjour, merci de vous être conn... | 137.7 | local_smart | ✅ |

| salut | greetings | vous, merci, être | Bonjour, merci de vous être connecté ! C... | 837.7 | local_smart | ✅ |

| coucou | greetings | vous, merci, être | Voici ce que je sais : Bonjour, merci de... | 365.4 | local_smart | ✅ |

| Bonjour comment vous appeler vous ? | bonjour_comment_vous_appeler_v | virtuel, assistant, votre | Hello ! Je m'appelle Julie, votre assist... | 116.5 | local_smart | ✅ |

| au revoir | goodbye | revenez, passez, bonne | Passez une bonne journée, revenez quand ... | 303.8 | local_smart | ✅ |

| à bientôt | goodbye | revenez, passez, bonne | Passez une bonne journée, revenez quand ... | 307.6 | local_smart | ✅ |

| à plus tard | goodbye | revenez, passez, bonne | Voici ce que je sais : Passez une bonne ... | 351.3 | local_smart | ✅ |

| merci | thanks | heureux | Heureux d'aider !... | 610.9 | local_smart | ✅ |

| merci beaucoup | thanks | heureux | Je vous en prie ! Heureux d'aider !... | 349.5 | local_smart | ✅ |

| super, merci | thanks | heureux | Heureux d'aider ! C'est avec plaisir !... | 523.0 | local_smart | ✅ |

| Ajouter mon Twitch au canal content ? | twitch | ajoutez, stream, titre | Voici ce que je sais : Ajoutez @ai_licia... | 407.0 | local_smart | ✅ |

| Voir les événements passés au-delà des récents ? | past_events | restent, faites | Faites défiler, ils restent jusqu'au ref... | 526.4 | local_smart | ✅ |

| On peut pas lui changer sont texte quand elle me réponds quand je l'appel  par example quand je l'appel elle me répond 'hum hum' pour me dire qu'elle m'etend et j'aurais voulu qu'elle me réponde par 'oui mon_nom' ou juste 'oui!!' au lieu de 'hum hum' | humhum | modifiable, pour, peux | Oui le hum hum n'est pas modifiable pour... | 545.3 | local_smart | ✅ |

| comment tu t'appel | name1 | programme, julie, artificielle | Je m'appelle Julie un programme d'intell... | 491.2 | local_smart | ✅ |

| comment t'appelles tu | name1 | programme, julie, artificielle | Je suis là pour ça ! Je m'appelle Julie ... | 385.2 | local_smart | ✅ |

| comment vous appelez vous | name1 | programme, julie, artificielle | Je m'appelle Julie un programme d'intell... | 512.2 | local_smart | ✅ |

| Comment Obtenir ai_licia ? | comment_obtenir_ai_licia_? | simple, très, choisis | Désolé, je ne comprends pas votre questi... | 10.0 | local_smart | ❌ |

| Comment obtenir ai_licia ? | signup | simple, très, récupérez | Désolé, je ne comprends pas votre questi... | 11.0 | local_smart | ❌ |

| Comment configurer mon stream | stream_setup | pour, votre, configurer | Je suis là pour ça ! Pour configurer vot... | 610.6 | local_smart | ✅ |

| Comment démarrer un stream | stream_setup | pour, votre, configurer | Je suis là pour ça ! Pour configurer vot... | 394.6 | local_smart | ✅ |

| Quels sont les réglages pour un stream | stream_setup | pour, votre, configurer | Voici ce que je sais : Pour configurer v... | 299.0 | local_smart | ✅ |

| Comment monétiser mon stream | monetize_stream | pour, votre, monétiser | Bien sûr, je peux vous aider ! Pour moné... | 338.4 | local_smart | ✅ |

| Comment gagner de l'argent avec le streaming | monetize_stream | pour, votre, monétiser | Bien sûr, je peux vous aider ! Pour moné... | 299.6 | local_smart | ✅ |

| Quels sont les moyens de monétiser un stream | monetize_stream | pour, votre, monétiser | Pour monétiser votre stream, vous pouvez... | 493.5 | local_smart | ✅ |

| Comment promouvoir mon stream | stream_promotion | promouvoir, pour, votre | Bien sûr, je peux vous aider ! Pour prom... | 370.9 | local_smart | ✅ |

| Comment attirer plus de spectateurs à mon stream | stream_promotion | promouvoir, pour, votre | Je suis là pour ça ! Pour promouvoir vot... | 349.8 | local_smart | ✅ |

| Quels sont les meilleurs moyens de promouvoir mon stream | stream_promotion | promouvoir, pour, votre | Pour promouvoir votre stream, utilisez l... | 390.9 | local_smart | ✅ |

| Comment planifier mon stream | stream_schedule | pour, votre, planifier | Voici comment je peux vous assister : Po... | 486.0 | local_smart | ✅ |

| Comment créer un calendrier de streaming | stream_schedule | pour, votre, planifier | Voici comment je peux vous assister : Po... | 369.0 | local_smart | ✅ |

| Comment la retirer de mon stream ? | remove | retirez, temporaire, retrait | Bien sûr, je peux vous aider ! Retrait t... | 393.1 | local_smart | ✅ |

| Comment engager mon audience | engage_audience | pour, engager, votre | Pour engager votre audience, interagisse... | 378.3 | local_smart | ✅ |

| Comment rendre mon stream plus interactif | engage_audience | pour, engager, votre | Pour engager votre audience, interagisse... | 255.7 | local_smart | ✅ |

| Comment réinitialiser le bot ? | reset | navigateur, source, ouvrez | Je suis là pour ça ! Ouvrez la source na... | 333.5 | local_smart | ✅ |

| Comment résoudre les problèmes de streaming | stream_troubleshoot | pour, résoudre, problèmes | Voici comment je peux vous assister : Po... | 389.4 | local_smart | ✅ |

| Comment corriger les problèmes de latence dans mon stream | stream_troubleshoot | pour, résoudre, problèmes | Voici comment je peux vous assister : Po... | 452.5 | local_smart | ✅ |

| Pourquoi mon stream lag | stream_troubleshoot | pour, résoudre, problèmes | Pour résoudre les problèmes de streaming... | 327.0 | local_smart | ✅ |

| Comment améliorer la qualité de mon stream | stream_quality | pour, améliorer, qualité | Bien sûr, je peux vous aider ! Pour amél... | 364.7 | local_smart | ✅ |

| Comment obtenir une meilleure qualité de stream | stream_quality | pour, améliorer, qualité | Je suis là pour ça ! Pour améliorer la q... | 332.7 | local_smart | ✅ |

| Pourquoi mon stream est il de mauvaise qualité | stream_quality | pour, améliorer, qualité | Pour améliorer la qualité de votre strea... | 338.7 | local_smart | ✅ |

| Comment définir le nom de mon bot ? | names | mettez, dans, jour | Voici comment je peux vous assister : Me... | 554.2 | local_smart | ✅ |

| Comment donner un nom personnalisé à ai_licia ? | nickname | dans, onglet, changez | Bien sûr, je peux vous aider ! Changez s... | 367.9 | local_smart | ✅ |

| Comment utiliser un code cadeau ? | code | comme, code, promo | Utilisez-le comme code promo au checkout... | 360.2 | local_smart | ✅ |

| Comment la faire réagir à ma voix ? | voice | speak, page, vous, choisissez, | Bien sûr, je peux vous aider ! Page Spea... | 531.6 | local_smart | ✅ |

| ai_licia a-t-elle une voix ? | voice | speak, page, vous, choisissez, | Voici ce que je sais : Oui ! Vous pouvez... | 547.1 | local_smart | ✅ |

| Comment faire parler l'IA via TTS ? | talk | customise, générez, source | Bien sûr, je peux vous aider ! Customise... | 461.5 | local_smart | ✅ |

| Comment tirer le meilleur parti de ai_licia ? | comment_tirer_le_meilleur_part | avons, rédigé, nous | Voici comment je peux vous assister : No... | 364.7 | local_smart | ✅ |

| Comment puis-je recommander AI_licia à mes amis ? | comment_puis-je_recommander_ai | vous, pouvez, recommander | Je suis là pour ça ! Vous pouvez recomma... | 328.6 | local_smart | ✅ |

| Comment savoir si ai_licia fonctionnerait dans mon stream | comment_savoir_si_ai_licia_fon | dans, utilisée, plus | Jusqu'à présent, ai_licia a été utilisée... | 317.8 | local_smart | ✅ |

| Comment puis-je définir la personnalité de base d'AI_licia ? | comment_puis-je_définir_la_per | vous, définir, pouvez | Voici comment je peux vous assister : Vo... | 310.3 | local_smart | ✅ |

| Je ne comprends pas comment entendre ai_licia (TTS). | text_to_speech | customise, text, speech | Voici comment je peux vous assister : Cu... | 490.1 | local_smart | ✅ |

| Comment puis-je être informé des nouveautés sur AI_licia ? | comment_puis-je_être_informé_d | vous, tient, section | Je suis là pour ça ! La section "Nouveau... | 400.1 | local_smart | ✅ |

| Comment voir ai_licia en action chez d'autres streamers ? | stream | pour, voir, gardez | Je suis là pour ça ! Gardez un œil sur #... | 308.2 | local_smart | ✅ |

| J'aimerais suggérer une fonctionnalité pour ai_licia, comment puis-je faire cela ? | j'aimerais_suggérer_une_foncti | entendre, nous, adorerions | Bien sûr, je peux vous aider ! Nous ador... | 335.7 | local_smart | ✅ |

| Comment stopper ses messages sur mes pubs et demandes d'abos ? | talking | customise, choisissez, setting | Customise ai_licia -> Settings : choisis... | 333.5 | local_smart | ✅ |

| La commande Shoutout marche mal avec certains pseudos. Comment écrire les descriptions ? | commands | comme, décrivez, pour | Voici comment je peux vous assister : Dé... | 588.3 | local_smart | ✅ |

| Elle marche en test mais pas en continu en live, comment l'appeler vocalement ? | speak | live, speak, ouvrez, hors, cli | Voici comment je peux vous assister : Cl... | 868.6 | local_smart | ✅ |

| Je parle dans 'Speak to ai_licia' mais elle ne rejoint pas le chat. | speak | live, speak, ouvrez, hors, cli | Hors live : cliquez sur Test ai_licia pu... | 263.0 | local_smart | ✅ |

| Comment changer alicia de compte tiktok car j'ai été ban 3 jours de mon compte principal ? | ban | simple, pour, plus | Bien sûr, je peux vous aider ! Pour un b... | 333.2 | local_smart | ✅ |

| Je veux donner un visage vtuber/png à AiLicia mais les programmes n'acceptent que l'entrée micro. Comment faire accepter une source navigateur comme micro ? | vtuber | avons, carte, nous | Nous avons une carte sur la roadmap pour... | 586.6 | local_smart | ✅ |

| qui t'a programmé | creator | samuel, créé, développeurs | J'ai été créé par Samuel un développeurs... | 317.1 | local_smart | ✅ |

| qui t'a créé | creator | samuel, créé, développeurs | Voici ce que je sais : J'ai été créé par... | 292.2 | local_smart | ✅ |

| qui est ton créateur | creator | samuel, créé, développeurs | Voici ce que je sais : J'ai été créé par... | 288.2 | local_smart | ✅ |

| Reconnaît-elle qui est mod ? | mod |  | Non.... | 303.2 | local_smart | ❌ |

| es tu vieux | age | suis, donc, programme | Voici ce que je sais : Je suis un progra... | 533.6 | local_smart | ✅ |

| es tu recent | age | suis, donc, programme | Je suis un programme informatique, donc ... | 401.1 | local_smart | ✅ |

| es tu ancien | age | suis, donc, programme | Voici ce que je sais : Je suis un progra... | 334.0 | local_smart | ✅ |

| es tu sage | es_tu_sage | implique, sagesse, compréhensi | La sagesse implique une compréhension pr... | 305.0 | local_smart | ✅ |

| j'ai besoin d'aide pour configurer AI_licia | j'ai_besoin_d'aide_pour_config | vous, besoin, avez | Voici comment je peux vous assister : Si... | 336.6 | local_smart | ✅ |

| Changer le nom d'Ai_licia ? | name | instructions, nouveau, créez,  | Voici ce que je sais : Créez un nouveau ... | 347.0 | local_smart | ✅ |

| Puis-je changer le nom d'ai_licia sur Twitch ? | name | instructions, nouveau, créez,  | Voici ce que je sais : Oui ! Guide ici :... | 578.8 | local_smart | ✅ |

| Changer le display name d'Ai_licia sur Twitch ? | name | instructions, nouveau, créez,  | Voici ce que je sais : Page : https://st... | 538.6 | local_smart | ✅ |

| Puis je tester ai_licia ? | puis_je_tester_ai_licia_? | avoir, bien, peux | Bien sûr ! Tu peux avoir un premier aper... | 378.7 | local_smart | ✅ |

| Qu'est ce que ai_licia? | Ai_licia | pour, compagnon, premier | ai_licia est le premier compagnon IA pou... | 333.6 | local_smart | ✅ |

| Qu'est-ce que ai_licia ? | Ai_licia | pour, compagnon, premier | Voici ce que je sais : ai_licia est le p... | 606.1 | local_smart | ✅ |

| Qu'est-ce que ailicia ? | Ai_licia | pour, compagnon, premier | Voici ce que je sais : ai_licia est le p... | 536.5 | local_smart | ✅ |

| ai_licia est elle uniquement pour Twitch ? | ai_licia_est_elle_uniquement_p | moment, pour, mais | Voici ce que je sais : Pour le moment ou... | 323.0 | local_smart | ✅ |

| Plusieurs ai_licia en même temps ? | multiple | botting, comme, risque | Désolé, je ne comprends pas votre questi... | 11.9 | local_smart | ❌ |

| Puis-je donner un surnom à AI_licia ? | puis-je_donner_un_surnom_à_ai_ | vous, choisir, pouvez | Oui, vous pouvez choisir un petit surnom... | 341.1 | local_smart | ✅ |

| Peut-on désactiver ai_licia temporairement ? | disable | bouton, haut, droite | Voici ce que je sais : Il y a un bouton ... | 360.4 | local_smart | ✅ |

| Qu'est-ce qu'ai_licia ? | ai_licia | votre | ai_licia est le premier compagnon IA pou... | 553.7 | local_smart | ❌ |

| ai_licia est-elle disponible sur Discord ? | discord | rejoignez, nous, travaillons | Nous y travaillons ! Rejoignez la liste ... | 537.8 | local_smart | ✅ |

| Puis-je personnaliser le comportement d'AI_licia ? | puis-je_personnaliser_le_compo | vous, absolument, avez | Absolument ! Vous avez le contrôle total... | 428.9 | local_smart | ✅ |

| Puis-je intégrer AI_licia à mes outils de streaming ? | puis-je_intégrer_ai_licia_à_me | peut, intégrée, être | Oui, AI_licia peut être intégrée à diver... | 861.0 | local_smart | ✅ |

| Quels paramètres d'interaction puis-je ajuster pour AI_licia ? | quels_paramètres_d'interaction | vous, pouvez, ajuster | Voici ce que je sais : Vous pouvez ajust... | 558.9 | local_smart | ✅ |

| À quoi sert la section "Tes Personnages" dans AI_licia ? | à_quoi_sert_la_section_"tes_pe | vous, section, permet | Voici ce que je sais : La section "Tes P... | 335.5 | local_smart | ✅ |

| Je viens d'ajouter ai_licia à mon stream, par où commencer ? | start | vous, avons, nous | Voici ce que je sais : Nous avons ce qu'... | 569.7 | local_smart | ✅ |

| mode Blanc/Light/Dark sur le site AI_licia ? | mode_blanc/light/dark_sur_le_s | changer, mode, permet | Voici ce que je sais : Le mode Light/Dar... | 664.6 | local_smart | ✅ |

| Configurer un compte alt Twitch pour ai_licia lié à mon principal ? | account | token, lien, ouvrez | Ouvrez le lien de token en navigation pr... | 775.2 | local_smart | ✅ |

| Je parle à ai_licia pendant mon stream, mais elle ne semble pas répondre ? | je_parle_à_ai_licia_pendant_mo | toujours, dois, garder | Tu dois toujours garder ouverte la page ... | 395.3 | local_smart | ✅ |

| Pour que ai_licia puisse écouter et me répondre quand je suis en live le bouton 'écouter' de l'application doit être toujours activé ? | écouter | faut, page, être | Voici ce que je sais : Oui. Il faut être... | 446.9 | local_smart | ✅ |

| Associer la voix TTS à une mascotte (PNG bouche animée) ? | mascot | avec, dans, plugin | Oui dans OBS avec le plugin Move (Exceld... | 392.2 | local_smart | ✅ |

| Est il possible de désactiver le TTS pour certains stream et le réactiver pour d'autres ? | TTS | dois, pouvoir, faire | Voici ce que je sais : Tu dois pouvoir l... | 530.9 | local_smart | ✅ |

| Peut-on lui faire ignorer les récompenses de points, surtout les requêtes TTS ? Ça se chevauche. | points | encore, nous, cette | Nous n'avons pas encore cette option et ... | 324.4 | local_smart | ✅ |

| Pour les voix doit-on garder le site ouvert ou ajouter à OBS ? | voices | personnage, dans, onglet | Oui via OBS : dans le personnage onglet ... | 571.0 | local_smart | ✅ |

| Elle connaît la catégorie du stream ? | categories | elle, catégorie | Voici ce que je sais : Oui elle a l'info... | 485.8 | local_smart | ✅ |

| La faire 'voir' le stream avec Streamlabs ? | see | virtual, streamlabs, utilisez | Voici ce que je sais : Utilisez Streamla... | 662.0 | local_smart | ✅ |

| Event mode masque la stream knowledge. Est-elle perdue ? | event | ignorée, simplement, mode | Non, simplement ignorée en mode event. R... | 344.2 | local_smart | ✅ |

| Configurer l'outil multi-action avec le plugin Stream Deck ? | stream_deck | request, plugin, installez | Voici ce que je sais : Installez le plug... | 662.3 | local_smart | ✅ |

| Si je lui donne un autre nom dans 'roles' réagira-t-elle à celui-ci ? | roles | après, fonctionnalité, carte | Oui via la fonctionnalité 'surnoms d'ai_... | 394.7 | local_smart | ✅ |

| bonjour | greetings | vous, merci, être | Bonjour, merci de vous être connecté ! C... | 3329.2 | local_raw | ✅ |

| salut | greetings | vous, merci, être | Bonjour, merci de vous être connecté ! C... | 78.7 | local_raw | ✅ |

| coucou | greetings | vous, merci, être | Bonjour, merci de vous être connecté ! C... | 137.4 | local_raw | ✅ |

| Bonjour comment vous appeler vous ? | bonjour_comment_vous_appeler_v | virtuel, assistant, votre | Je m'appelle Julie, votre assistant virt... | 76.4 | local_raw | ✅ |

| au revoir | goodbye | revenez, passez, bonne | Passez une bonne journée, revenez quand ... | 69.7 | local_raw | ✅ |

| à bientôt | goodbye | revenez, passez, bonne | Bonjour, merci de vous être connecté ! C... | 77.7 | local_raw | ❌ |

| à plus tard | goodbye | revenez, passez, bonne | Passez une bonne journée, revenez quand ... | 117.6 | local_raw | ✅ |

| merci | thanks | heureux | Heureux d'aider !... | 72.4 | local_raw | ✅ |

| merci beaucoup | thanks | heureux | Heureux d'aider !... | 82.7 | local_raw | ✅ |

| super, merci | thanks | heureux | Heureux d'aider !... | 67.2 | local_raw | ✅ |

| Ajouter mon Twitch au canal content ? | twitch | ajoutez, stream, titre | Ajoutez @ai_licia au titre de stream au ... | 80.9 | local_raw | ✅ |

| Voir les événements passés au-delà des récents ? | past_events | restent, faites | Faites défiler, ils restent jusqu'au ref... | 70.5 | local_raw | ✅ |

| On peut pas lui changer sont texte quand elle me réponds quand je l'appel  par example quand je l'appel elle me répond 'hum hum' pour me dire qu'elle m'etend et j'aurais voulu qu'elle me réponde par 'oui mon_nom' ou juste 'oui!!' au lieu de 'hum hum' | humhum | modifiable, pour, peux | Pas encore. Nous prévoyons une base de c... | 95.3 | local_raw | ❌ |

| comment tu t'appel | name1 | programme, julie, artificielle | Je m'appelle Julie un programme d'intell... | 85.4 | local_raw | ✅ |

| comment t'appelles tu | name1 | programme, julie, artificielle | Je m'appelle Julie un programme d'intell... | 159.4 | local_raw | ✅ |

| comment vous appelez vous | name1 | programme, julie, artificielle | Je m'appelle Julie un programme d'intell... | 75.7 | local_raw | ✅ |

| Comment Obtenir ai_licia ? | comment_obtenir_ai_licia_? | simple, très, choisis | Très simple ! Rends-toi sur https://stre... | 66.0 | local_raw | ✅ |

| Comment obtenir ai_licia ? | signup | simple, très, récupérez | Très simple ! Rends-toi sur https://stre... | 0.0 | local_raw | ✅ |

| Comment configurer mon stream | stream_setup | pour, votre, configurer | Pour configurer votre stream, vous devez... | 68.6 | local_raw | ✅ |

| Comment démarrer un stream | stream_setup | pour, votre, configurer | Pour configurer votre stream, vous devez... | 66.7 | local_raw | ✅ |

| Quels sont les réglages pour un stream | stream_setup | pour, votre, configurer | Les outils populaires pour le streaming ... | 75.0 | local_raw | ✅ |

| Comment monétiser mon stream | monetize_stream | pour, votre, monétiser | Pour monétiser votre stream, vous pouvez... | 71.4 | local_raw | ✅ |

| Comment gagner de l'argent avec le streaming | monetize_stream | pour, votre, monétiser | Pour monétiser votre stream, vous pouvez... | 85.9 | local_raw | ✅ |

| Quels sont les moyens de monétiser un stream | monetize_stream | pour, votre, monétiser | Pour monétiser votre stream, vous pouvez... | 70.7 | local_raw | ✅ |

| Comment promouvoir mon stream | stream_promotion | promouvoir, pour, votre | Pour promouvoir votre stream, utilisez l... | 135.1 | local_raw | ✅ |

| Comment attirer plus de spectateurs à mon stream | stream_promotion | promouvoir, pour, votre | Pour promouvoir votre stream, utilisez l... | 89.6 | local_raw | ✅ |

| Quels sont les meilleurs moyens de promouvoir mon stream | stream_promotion | promouvoir, pour, votre | Pour promouvoir votre stream, utilisez l... | 68.6 | local_raw | ✅ |

| Comment planifier mon stream | stream_schedule | pour, votre, planifier | Pour planifier votre stream, choisissez ... | 71.1 | local_raw | ✅ |

| Comment créer un calendrier de streaming | stream_schedule | pour, votre, planifier | Pour planifier votre stream, choisissez ... | 76.0 | local_raw | ✅ |

| Comment la retirer de mon stream ? | remove | retirez, temporaire, retrait | Le bouton apparaît quelques minutes aprè... | 89.6 | local_raw | ❌ |

| Comment engager mon audience | engage_audience | pour, engager, votre | Pour engager votre audience, interagisse... | 80.5 | local_raw | ✅ |

| Comment rendre mon stream plus interactif | engage_audience | pour, engager, votre | Pour engager votre audience, interagisse... | 67.8 | local_raw | ✅ |

| Comment réinitialiser le bot ? | reset | navigateur, source, ouvrez | Ouvrez la source navigateur dans un nouv... | 72.5 | local_raw | ✅ |

| Comment résoudre les problèmes de streaming | stream_troubleshoot | pour, résoudre, problèmes | Pour résoudre les problèmes de streaming... | 67.8 | local_raw | ✅ |

| Comment corriger les problèmes de latence dans mon stream | stream_troubleshoot | pour, résoudre, problèmes | Pour résoudre les problèmes de streaming... | 85.3 | local_raw | ✅ |

| Pourquoi mon stream lag | stream_troubleshoot | pour, résoudre, problèmes | Pour résoudre les problèmes de streaming... | 86.3 | local_raw | ✅ |

| Comment améliorer la qualité de mon stream | stream_quality | pour, améliorer, qualité | Pour améliorer la qualité de votre strea... | 69.4 | local_raw | ✅ |

| Comment obtenir une meilleure qualité de stream | stream_quality | pour, améliorer, qualité | Pour améliorer la qualité de votre strea... | 71.4 | local_raw | ✅ |

| Pourquoi mon stream est il de mauvaise qualité | stream_quality | pour, améliorer, qualité | Pour améliorer la qualité de votre strea... | 70.8 | local_raw | ✅ |

| Comment définir le nom de mon bot ? | names | mettez, dans, jour | Mettez à jour le nom dans la page Charac... | 86.5 | local_raw | ✅ |

| Comment donner un nom personnalisé à ai_licia ? | nickname | dans, onglet, changez | Pour un nom personnalisé : compte séparé... | 70.9 | local_raw | ❌ |

| Comment utiliser un code cadeau ? | code | comme, code, promo | Utilisez-le comme code promo au checkout... | 72.9 | local_raw | ✅ |

| Comment la faire réagir à ma voix ? | voice | speak, page, vous, choisissez, | Dans la configuration TTS, section varia... | 74.6 | local_raw | ❌ |

| ai_licia a-t-elle une voix ? | voice | speak, page, vous, choisissez, | Oui ! Vous pouvez faire parler ai_licia ... | 93.7 | local_raw | ✅ |

| Comment faire parler l'IA via TTS ? | talk | customise, générez, source | Customise ai_licia -> TTS, générez la so... | 82.4 | local_raw | ✅ |

| Comment tirer le meilleur parti de ai_licia ? | comment_tirer_le_meilleur_part | avons, rédigé, nous | Nous avons rédigé un article de blog pou... | 91.1 | local_raw | ✅ |

| Comment puis-je recommander AI_licia à mes amis ? | comment_puis-je_recommander_ai | vous, pouvez, recommander | Vous pouvez recommander AI_licia à vos a... | 69.4 | local_raw | ✅ |

| Comment savoir si ai_licia fonctionnerait dans mon stream | comment_savoir_si_ai_licia_fon | dans, utilisée, plus | Jusqu'à présent, ai_licia a été utilisée... | 88.6 | local_raw | ✅ |

| Comment puis-je définir la personnalité de base d'AI_licia ? | comment_puis-je_définir_la_per | vous, définir, pouvez | Vous pouvez définir la personnalité de b... | 74.4 | local_raw | ✅ |

| Je ne comprends pas comment entendre ai_licia (TTS). | text_to_speech | customise, text, speech | Ajoutez les pseudos, ajoutez les infos, ... | 70.8 | local_raw | ❌ |

| Comment puis-je être informé des nouveautés sur AI_licia ? | comment_puis-je_être_informé_d | vous, tient, section | La section "Nouveautés" https://headway-... | 92.3 | local_raw | ✅ |

| Comment voir ai_licia en action chez d'autres streamers ? | stream | pour, voir, gardez | Pour l'instant non, c'est l'un ou l'autr... | 67.6 | local_raw | ✅ |

| J'aimerais suggérer une fonctionnalité pour ai_licia, comment puis-je faire cela ? | j'aimerais_suggérer_une_foncti | entendre, nous, adorerions | Nous adorerions entendre tes idées pour ... | 72.2 | local_raw | ✅ |

| Comment stopper ses messages sur mes pubs et demandes d'abos ? | talking | customise, choisissez, setting | Customise ai_licia -> Settings : choisis... | 69.6 | local_raw | ✅ |

| La commande Shoutout marche mal avec certains pseudos. Comment écrire les descriptions ? | commands | comme, décrivez, pour | Les descriptions disent quand les utilis... | 86.3 | local_raw | ✅ |

| Elle marche en test mais pas en continu en live, comment l'appeler vocalement ? | speak | live, speak, ouvrez, hors, cli | Hors live : cliquez sur Test ai_licia pu... | 79.4 | local_raw | ✅ |

| Je parle dans 'Speak to ai_licia' mais elle ne rejoint pas le chat. | speak | live, speak, ouvrez, hors, cli | Cliquez Speak to AI_licia, ouvrez le mic... | 71.4 | local_raw | ✅ |

| Comment changer alicia de compte tiktok car j'ai été ban 3 jours de mon compte principal ? | ban | simple, pour, plus | Pour un ban de 3 jours, le plus simple s... | 67.4 | local_raw | ✅ |

| Je veux donner un visage vtuber/png à AiLicia mais les programmes n'acceptent que l'entrée micro. Comment faire accepter une source navigateur comme micro ? | vtuber | avons, carte, nous | Nous avons une carte sur la roadmap pour... | 71.7 | local_raw | ✅ |

| qui t'a programmé | creator | samuel, créé, développeurs | J'ai été créé par Samuel un développeurs... | 75.9 | local_raw | ✅ |

| qui t'a créé | creator | samuel, créé, développeurs | J'ai été créé par Samuel un développeurs... | 91.6 | local_raw | ✅ |

| qui est ton créateur | creator | samuel, créé, développeurs | J'ai été créé par Samuel un développeurs... | 72.2 | local_raw | ✅ |

| Reconnaît-elle qui est mod ? | mod |  | J'ai été créé par Samuel un développeurs... | 68.5 | local_raw | ❌ |

| es tu vieux | age | suis, donc, programme | La sagesse implique une compréhension pr... | 66.2 | local_raw | ❌ |

| es tu recent | age | suis, donc, programme | La sagesse implique une compréhension pr... | 70.5 | local_raw | ❌ |

| es tu ancien | age | suis, donc, programme | La sagesse implique une compréhension pr... | 69.0 | local_raw | ❌ |

| es tu sage | es_tu_sage | implique, sagesse, compréhensi | La sagesse implique une compréhension pr... | 70.6 | local_raw | ✅ |

| j'ai besoin d'aide pour configurer AI_licia | j'ai_besoin_d'aide_pour_config | vous, besoin, avez | Si vous avez besoin d'aide pour configur... | 68.1 | local_raw | ✅ |

| Changer le nom d'Ai_licia ? | name | instructions, nouveau, créez,  | Créez un nouveau compte avec ce nom puis... | 95.3 | local_raw | ✅ |

| Puis-je changer le nom d'ai_licia sur Twitch ? | name | instructions, nouveau, créez,  | Créez un nouveau compte avec ce nom puis... | 91.4 | local_raw | ✅ |

| Changer le display name d'Ai_licia sur Twitch ? | name | instructions, nouveau, créez,  | Oui ! Guide ici : https://www.getailicia... | 80.2 | local_raw | ✅ |

| Puis je tester ai_licia ? | puis_je_tester_ai_licia_? | avoir, bien, peux | Bien sûr ! Tu peux avoir un premier aper... | 68.8 | local_raw | ✅ |

| Qu'est ce que ai_licia? | Ai_licia | pour, compagnon, premier | ai_licia est votre compagnon, votre co-a... | 68.0 | local_raw | ✅ |

| Qu'est-ce que ai_licia ? | Ai_licia | pour, compagnon, premier | ai_licia est votre compagnon, votre co-a... | 96.9 | local_raw | ✅ |

| Qu'est-ce que ailicia ? | Ai_licia | pour, compagnon, premier | ai_licia est votre compagnon, votre co-a... | 67.2 | local_raw | ✅ |

| ai_licia est elle uniquement pour Twitch ? | ai_licia_est_elle_uniquement_p | moment, pour, mais | Pour le moment oui, mais nous prévoyons ... | 87.4 | local_raw | ✅ |

| Plusieurs ai_licia en même temps ? | multiple | botting, comme, risque | Non, risque d'être vu comme botting par ... | 95.1 | local_raw | ✅ |

| Puis-je donner un surnom à AI_licia ? | puis-je_donner_un_surnom_à_ai_ | vous, choisir, pouvez | Oui, vous pouvez choisir un petit surnom... | 98.3 | local_raw | ✅ |

| Peut-on désactiver ai_licia temporairement ? | disable | bouton, haut, droite | Il y a un bouton en haut à droite du das... | 86.5 | local_raw | ✅ |

| Qu'est-ce qu'ai_licia ? | ai_licia | votre | ai_licia est votre compagnon, votre co-a... | 76.0 | local_raw | ✅ |

| ai_licia est-elle disponible sur Discord ? | discord | rejoignez, nous, travaillons | Nous y travaillons ! Rejoignez la liste ... | 70.4 | local_raw | ✅ |

| Puis-je personnaliser le comportement d'AI_licia ? | puis-je_personnaliser_le_compo | vous, absolument, avez | Absolument ! Vous avez le contrôle total... | 75.8 | local_raw | ✅ |

| Puis-je intégrer AI_licia à mes outils de streaming ? | puis-je_intégrer_ai_licia_à_me | peut, intégrée, être | Oui, AI_licia peut être intégrée à diver... | 87.3 | local_raw | ✅ |

| Quels paramètres d'interaction puis-je ajuster pour AI_licia ? | quels_paramètres_d'interaction | vous, pouvez, ajuster | Vous pouvez ajuster plusieurs paramètres... | 71.7 | local_raw | ✅ |

| À quoi sert la section "Tes Personnages" dans AI_licia ? | à_quoi_sert_la_section_"tes_pe | vous, section, permet | La section "Tes Personnages" https://str... | 68.5 | local_raw | ✅ |

| Je viens d'ajouter ai_licia à mon stream, par où commencer ? | start | vous, avons, nous | Nous avons ce qu'il vous faut ! Regardez... | 68.2 | local_raw | ✅ |

| mode Blanc/Light/Dark sur le site AI_licia ? | mode_blanc/light/dark_sur_le_s | changer, mode, permet | Le mode Light/Dark permet de changer l'a... | 70.1 | local_raw | ✅ |

| Configurer un compte alt Twitch pour ai_licia lié à mon principal ? | account | token, lien, ouvrez | Ouvrez le lien de token en navigation pr... | 64.5 | local_raw | ✅ |

| Je parle à ai_licia pendant mon stream, mais elle ne semble pas répondre ? | je_parle_à_ai_licia_pendant_mo | toujours, dois, garder | Tu dois toujours garder ouverte la page ... | 69.5 | local_raw | ✅ |

| Pour que ai_licia puisse écouter et me répondre quand je suis en live le bouton 'écouter' de l'application doit être toujours activé ? | écouter | faut, page, être | Oui. Il faut être sur la page et que éco... | 78.6 | local_raw | ✅ |

| Associer la voix TTS à une mascotte (PNG bouche animée) ? | mascot | avec, dans, plugin | Dans la configuration TTS, section varia... | 88.9 | local_raw | ✅ |

| Est il possible de désactiver le TTS pour certains stream et le réactiver pour d'autres ? | TTS | dois, pouvoir, faire | Tu dois pouvoir le faire depuis OBS, si ... | 70.9 | local_raw | ✅ |

| Peut-on lui faire ignorer les récompenses de points, surtout les requêtes TTS ? Ça se chevauche. | points | encore, nous, cette | Nous n'avons pas encore cette option et ... | 76.0 | local_raw | ✅ |

| Pour les voix doit-on garder le site ouvert ou ajouter à OBS ? | voices | personnage, dans, onglet | Oui via OBS : dans le personnage onglet ... | 104.8 | local_raw | ✅ |

| Elle connaît la catégorie du stream ? | categories | elle, catégorie | Oui elle a l'info de catégorie 😊.... | 101.3 | local_raw | ✅ |

| La faire 'voir' le stream avec Streamlabs ? | see | virtual, streamlabs, utilisez | Utilisez Streamlabs Virtual Camera. Tuto... | 109.0 | local_raw | ✅ |

| Event mode masque la stream knowledge. Est-elle perdue ? | event | ignorée, simplement, mode | Non, simplement ignorée en mode event. R... | 146.5 | local_raw | ✅ |

| Configurer l'outil multi-action avec le plugin Stream Deck ? | stream_deck | request, plugin, installez | Installez le plugin API Request : https:... | 86.7 | local_raw | ✅ |

| Si je lui donne un autre nom dans 'roles' réagira-t-elle à celui-ci ? | roles | après, fonctionnalité, carte | Oui via la fonctionnalité 'surnoms d'ai_... | 134.3 | local_raw | ✅ |

| bonjour | greetings | vous, merci, être | Bonjour ! Bonjour, merci de vous être co... | 661.2 | api | ✅ |

| salut | greetings | vous, merci, être | Bonjour ! Bonjour, merci de vous être co... | 678.8 | api | ✅ |

| coucou | greetings | vous, merci, être | Bonjour, merci de vous être connecté ! C... | 545.6 | api | ✅ |

| Bonjour comment vous appeler vous ? | bonjour_comment_vous_appeler_v | virtuel, assistant, votre | Hello ! Je m'appelle Julie, votre assist... | 1401.0 | api | ✅ |

| au revoir | goodbye | revenez, passez, bonne | Passez une bonne journée, revenez quand ... | 766.0 | api | ✅ |

| à bientôt | goodbye | revenez, passez, bonne | Passez une bonne journée, revenez quand ... | 2506.5 | api | ✅ |

| à plus tard | goodbye | revenez, passez, bonne | Voici ce que je sais : Passez une bonne ... | 778.1 | api | ✅ |

| merci | thanks | heureux | Pas de problème ! Heureux d'aider !... | 1078.0 | api | ✅ |

| merci beaucoup | thanks | heureux | Je vous en prie ! Heureux d'aider !... | 761.4 | api | ✅ |

| super, merci | thanks | heureux | Pas de problème ! Heureux d'aider !... | 326.9 | api | ✅ |

| Ajouter mon Twitch au canal content ? | twitch | ajoutez, stream, titre | Voici ce que je sais : Ajoutez @ai_licia... | 572.8 | api | ✅ |

| Voir les événements passés au-delà des récents ? | past_events | restent, faites | Voici ce que je sais : Faites défiler, i... | 455.1 | api | ✅ |

| On peut pas lui changer sont texte quand elle me réponds quand je l'appel  par example quand je l'appel elle me répond 'hum hum' pour me dire qu'elle m'etend et j'aurais voulu qu'elle me réponde par 'oui mon_nom' ou juste 'oui!!' au lieu de 'hum hum' | humhum | modifiable, pour, peux | Oui le hum hum n'est pas modifiable pour... | 600.9 | api | ✅ |

| comment tu t'appel | name1 | programme, julie, artificielle | Je suis là pour ça ! Je m'appelle Julie ... | 513.2 | api | ✅ |

| comment t'appelles tu | name1 | programme, julie, artificielle | Je m'appelle Julie un programme d'intell... | 725.2 | api | ✅ |

| comment vous appelez vous | name1 | programme, julie, artificielle | Voici comment je peux vous assister : Je... | 494.2 | api | ✅ |

| Comment Obtenir ai_licia ? | comment_obtenir_ai_licia_? | simple, très, choisis | Très simple ! Rends-toi sur https://stre... | 606.3 | api | ✅ |

| Comment obtenir ai_licia ? | signup | simple, très, récupérez | Voici comment je peux vous assister : Tr... | 742.3 | api | ✅ |

| Comment configurer mon stream | stream_setup | pour, votre, configurer | Bien sûr, je peux vous aider ! Pour conf... | 569.7 | api | ✅ |

| Comment démarrer un stream | stream_setup | pour, votre, configurer | Bien sûr, je peux vous aider ! Pour conf... | 948.0 | api | ✅ |

| Quels sont les réglages pour un stream | stream_setup | pour, votre, configurer | Voici ce que je sais : Pour configurer v... | 675.0 | api | ✅ |

| Comment monétiser mon stream | monetize_stream | pour, votre, monétiser | Pour monétiser votre stream, vous pouvez... | 564.9 | api | ✅ |

| Comment gagner de l'argent avec le streaming | monetize_stream | pour, votre, monétiser | Je suis là pour ça ! Pour monétiser votr... | 525.3 | api | ✅ |

| Quels sont les moyens de monétiser un stream | monetize_stream | pour, votre, monétiser | Voici ce que je sais : Pour monétiser vo... | 659.2 | api | ✅ |

| Comment promouvoir mon stream | stream_promotion | promouvoir, pour, votre | Je suis là pour ça ! Pour promouvoir vot... | 508.0 | api | ✅ |

| Comment attirer plus de spectateurs à mon stream | stream_promotion | promouvoir, pour, votre | Bien sûr, je peux vous aider ! Pour prom... | 446.0 | api | ✅ |

| Quels sont les meilleurs moyens de promouvoir mon stream | stream_promotion | promouvoir, pour, votre | Pour promouvoir votre stream, utilisez l... | 634.3 | api | ✅ |

| Comment planifier mon stream | stream_schedule | pour, votre, planifier | Bien sûr, je peux vous aider ! Pour plan... | 714.5 | api | ✅ |

| Comment créer un calendrier de streaming | stream_schedule | pour, votre, planifier | Pour planifier votre stream, choisissez ... | 502.6 | api | ✅ |

| Comment la retirer de mon stream ? | remove | retirez, temporaire, retrait | Retrait temporaire : retirez mod/vip. Po... | 391.1 | api | ✅ |

| Comment engager mon audience | engage_audience | pour, engager, votre | Voici comment je peux vous assister : Po... | 452.9 | api | ✅ |

| Comment rendre mon stream plus interactif | engage_audience | pour, engager, votre | Bien sûr, je peux vous aider ! Pour enga... | 555.4 | api | ✅ |

| Comment réinitialiser le bot ? | reset | navigateur, source, ouvrez | Je suis là pour ça ! Ouvrez la source na... | 437.9 | api | ✅ |

| Comment résoudre les problèmes de streaming | stream_troubleshoot | pour, résoudre, problèmes | Pour résoudre les problèmes de streaming... | 388.7 | api | ✅ |

| Comment corriger les problèmes de latence dans mon stream | stream_troubleshoot | pour, résoudre, problèmes | Bien sûr, je peux vous aider ! Pour réso... | 341.4 | api | ✅ |

| Pourquoi mon stream lag | stream_troubleshoot | pour, résoudre, problèmes | Voici ce que je sais : Pour résoudre les... | 571.4 | api | ✅ |

| Comment améliorer la qualité de mon stream | stream_quality | pour, améliorer, qualité | Je suis là pour ça ! Pour améliorer la q... | 486.2 | api | ✅ |

| Comment obtenir une meilleure qualité de stream | stream_quality | pour, améliorer, qualité | Bien sûr, je peux vous aider ! Pour amél... | 859.2 | api | ✅ |

| Pourquoi mon stream est il de mauvaise qualité | stream_quality | pour, améliorer, qualité | Pour améliorer la qualité de votre strea... | 830.4 | api | ✅ |

| Comment définir le nom de mon bot ? | names | mettez, dans, jour | Mettez à jour le nom dans la page Charac... | 464.2 | api | ✅ |

| Comment donner un nom personnalisé à ai_licia ? | nickname | dans, onglet, changez | Je suis là pour ça ! Changez son nom dan... | 581.4 | api | ✅ |

| Comment utiliser un code cadeau ? | code | comme, code, promo | Utilisez-le comme code promo au checkout... | 343.2 | api | ✅ |

| Comment la faire réagir à ma voix ? | voice | speak, page, vous, choisissez, | Bien sûr, je peux vous aider ! Page Spea... | 601.8 | api | ✅ |

| ai_licia a-t-elle une voix ? | voice | speak, page, vous, choisissez, | Voici ce que je sais : Oui ! Vous pouvez... | 1268.3 | api | ✅ |

| Comment faire parler l'IA via TTS ? | talk | customise, générez, source | Bien sûr, je peux vous aider ! Customise... | 1201.6 | api | ✅ |

| Comment tirer le meilleur parti de ai_licia ? | comment_tirer_le_meilleur_part | avons, rédigé, nous | Voici comment je peux vous assister : No... | 466.5 | api | ✅ |

| Comment puis-je recommander AI_licia à mes amis ? | comment_puis-je_recommander_ai | vous, pouvez, recommander | Bien sûr, je peux vous aider ! Vous pouv... | 373.4 | api | ✅ |

| Comment savoir si ai_licia fonctionnerait dans mon stream | comment_savoir_si_ai_licia_fon | dans, utilisée, plus | Voici comment je peux vous assister : Ju... | 696.8 | api | ✅ |

| Comment puis-je définir la personnalité de base d'AI_licia ? | comment_puis-je_définir_la_per | vous, définir, pouvez | Je suis là pour ça ! Vous pouvez définir... | 502.1 | api | ✅ |

| Je ne comprends pas comment entendre ai_licia (TTS). | text_to_speech | customise, text, speech | Bien sûr, je peux vous aider ! Customise... | 544.1 | api | ✅ |

| Comment puis-je être informé des nouveautés sur AI_licia ? | comment_puis-je_être_informé_d | vous, tient, section | La section "Nouveautés" https://headway-... | 566.2 | api | ✅ |

| Comment voir ai_licia en action chez d'autres streamers ? | stream | pour, voir, gardez | Voici comment je peux vous assister : Ga... | 791.2 | api | ✅ |

| J'aimerais suggérer une fonctionnalité pour ai_licia, comment puis-je faire cela ? | j'aimerais_suggérer_une_foncti | entendre, nous, adorerions | Nous adorerions entendre tes idées pour ... | 459.3 | api | ✅ |

| Comment stopper ses messages sur mes pubs et demandes d'abos ? | talking | customise, choisissez, setting | Voici comment je peux vous assister : Cu... | 375.6 | api | ✅ |

| La commande Shoutout marche mal avec certains pseudos. Comment écrire les descriptions ? | commands | comme, décrivez, pour | Je suis là pour ça ! Décrivez les comme ... | 1997.8 | api | ✅ |

| Elle marche en test mais pas en continu en live, comment l'appeler vocalement ? | speak | live, speak, ouvrez, hors, cli | Je suis là pour ça ! Cliquez Speak to AI... | 683.0 | api | ✅ |

| Je parle dans 'Speak to ai_licia' mais elle ne rejoint pas le chat. | speak | live, speak, ouvrez, hors, cli | Hors live : cliquez sur Test ai_licia pu... | 531.2 | api | ✅ |

| Comment changer alicia de compte tiktok car j'ai été ban 3 jours de mon compte principal ? | ban | simple, pour, plus | Je suis là pour ça ! Pour un ban de 3 jo... | 739.2 | api | ✅ |

| Je veux donner un visage vtuber/png à AiLicia mais les programmes n'acceptent que l'entrée micro. Comment faire accepter une source navigateur comme micro ? | vtuber | avons, carte, nous | Voici comment je peux vous assister : No... | 471.0 | api | ✅ |

| qui t'a programmé | creator | samuel, créé, développeurs | J'ai été créé par Samuel un développeurs... | 377.4 | api | ✅ |

| qui t'a créé | creator | samuel, créé, développeurs | J'ai été créé par Samuel un développeurs... | 358.1 | api | ✅ |

| qui est ton créateur | creator | samuel, créé, développeurs | J'ai été créé par Samuel un développeurs... | 516.4 | api | ✅ |

| Reconnaît-elle qui est mod ? | mod |  | Voici ce que je sais : Non.... | 344.5 | api | ❌ |

| es tu vieux | age | suis, donc, programme | Je suis un programme informatique, donc ... | 714.1 | api | ✅ |

| es tu recent | age | suis, donc, programme | Voici ce que je sais : Je suis un progra... | 590.5 | api | ✅ |

| es tu ancien | age | suis, donc, programme | Voici ce que je sais : Je suis un progra... | 595.6 | api | ✅ |

| es tu sage | es_tu_sage | implique, sagesse, compréhensi | Voici ce que je sais : La sagesse impliq... | 549.8 | api | ✅ |

| j'ai besoin d'aide pour configurer AI_licia | j'ai_besoin_d'aide_pour_config | vous, besoin, avez | Je suis là pour ça ! Si vous avez besoin... | 425.4 | api | ✅ |

| Changer le nom d'Ai_licia ? | name | instructions, nouveau, créez,  | Créez un nouveau compte avec ce nom puis... | 388.5 | api | ✅ |

| Puis-je changer le nom d'ai_licia sur Twitch ? | name | instructions, nouveau, créez,  | Voici ce que je sais : Oui ! Guide ici :... | 603.2 | api | ✅ |

| Changer le display name d'Ai_licia sur Twitch ? | name | instructions, nouveau, créez,  | Page : https://streamer-dashboard.ailici... | 446.0 | api | ✅ |

| Puis je tester ai_licia ? | puis_je_tester_ai_licia_? | avoir, bien, peux | Voici ce que je sais : Bien sûr ! Tu peu... | 555.3 | api | ✅ |

| Qu'est ce que ai_licia? | Ai_licia | pour, compagnon, premier | ai_licia est le premier compagnon IA pou... | 443.5 | api | ✅ |

| Qu'est-ce que ai_licia ? | Ai_licia | pour, compagnon, premier | Voici ce que je sais : ai_licia est le p... | 635.3 | api | ✅ |

| Qu'est-ce que ailicia ? | Ai_licia | pour, compagnon, premier | ai_licia est le premier compagnon IA pou... | 1040.5 | api | ✅ |

| ai_licia est elle uniquement pour Twitch ? | ai_licia_est_elle_uniquement_p | moment, pour, mais | Voici ce que je sais : Pour le moment ou... | 529.5 | api | ✅ |

| Plusieurs ai_licia en même temps ? | multiple | botting, comme, risque | Voici ce que je sais : Non, risque d'êtr... | 370.3 | api | ✅ |

| Puis-je donner un surnom à AI_licia ? | puis-je_donner_un_surnom_à_ai_ | vous, choisir, pouvez | Oui, vous pouvez choisir un petit surnom... | 328.9 | api | ✅ |

| Peut-on désactiver ai_licia temporairement ? | disable | bouton, haut, droite | Voici ce que je sais : Il y a un bouton ... | 762.1 | api | ✅ |

| Qu'est-ce qu'ai_licia ? | ai_licia | votre | ai_licia est votre compagnon, votre co-a... | 662.7 | api | ✅ |

| ai_licia est-elle disponible sur Discord ? | discord | rejoignez, nous, travaillons | Voici ce que je sais : Nous y travaillon... | 382.5 | api | ✅ |

| Puis-je personnaliser le comportement d'AI_licia ? | puis-je_personnaliser_le_compo | vous, absolument, avez | Voici ce que je sais : Absolument ! Vous... | 654.6 | api | ✅ |

| Puis-je intégrer AI_licia à mes outils de streaming ? | puis-je_intégrer_ai_licia_à_me | peut, intégrée, être | Oui, AI_licia peut être intégrée à diver... | 490.5 | api | ✅ |

| Quels paramètres d'interaction puis-je ajuster pour AI_licia ? | quels_paramètres_d'interaction | vous, pouvez, ajuster | Voici ce que je sais : Vous pouvez ajust... | 582.5 | api | ✅ |

| À quoi sert la section "Tes Personnages" dans AI_licia ? | à_quoi_sert_la_section_"tes_pe | vous, section, permet | La section "Tes Personnages" https://str... | 422.6 | api | ✅ |

| Je viens d'ajouter ai_licia à mon stream, par où commencer ? | start | vous, avons, nous | Nous avons ce qu'il vous faut ! Regardez... | 652.3 | api | ✅ |

| mode Blanc/Light/Dark sur le site AI_licia ? | mode_blanc/light/dark_sur_le_s | changer, mode, permet | Le mode Light/Dark permet de changer l'a... | 405.1 | api | ✅ |

| Configurer un compte alt Twitch pour ai_licia lié à mon principal ? | account | token, lien, ouvrez | Voici ce que je sais : Ouvrez le lien de... | 1009.0 | api | ✅ |

| Je parle à ai_licia pendant mon stream, mais elle ne semble pas répondre ? | je_parle_à_ai_licia_pendant_mo | toujours, dois, garder | Voici ce que je sais : Tu dois toujours ... | 624.3 | api | ✅ |

| Pour que ai_licia puisse écouter et me répondre quand je suis en live le bouton 'écouter' de l'application doit être toujours activé ? | écouter | faut, page, être | Voici ce que je sais : Oui. Il faut être... | 478.4 | api | ✅ |

| Associer la voix TTS à une mascotte (PNG bouche animée) ? | mascot | avec, dans, plugin | Oui dans OBS avec le plugin Move (Exceld... | 454.4 | api | ✅ |

| Est il possible de désactiver le TTS pour certains stream et le réactiver pour d'autres ? | TTS | dois, pouvoir, faire | Voici ce que je sais : Tu dois pouvoir l... | 316.4 | api | ✅ |

| Peut-on lui faire ignorer les récompenses de points, surtout les requêtes TTS ? Ça se chevauche. | points | encore, nous, cette | Nous n'avons pas encore cette option et ... | 742.0 | api | ✅ |

| Pour les voix doit-on garder le site ouvert ou ajouter à OBS ? | voices | personnage, dans, onglet | Oui via OBS : dans le personnage onglet ... | 552.7 | api | ✅ |

| Elle connaît la catégorie du stream ? | categories | elle, catégorie | Oui elle a l'info de catégorie 😊.... | 403.7 | api | ✅ |

| La faire 'voir' le stream avec Streamlabs ? | see | virtual, streamlabs, utilisez | Voici ce que je sais : Utilisez Streamla... | 303.5 | api | ✅ |

| Event mode masque la stream knowledge. Est-elle perdue ? | event | ignorée, simplement, mode | Voici ce que je sais : Non, simplement i... | 815.0 | api | ✅ |

| Configurer l'outil multi-action avec le plugin Stream Deck ? | stream_deck | request, plugin, installez | Installez le plugin API Request : https:... | 527.3 | api | ✅ |

| Si je lui donne un autre nom dans 'roles' réagira-t-elle à celui-ci ? | roles | après, fonctionnalité, carte | Voici ce que je sais : Oui via la foncti... | 339.8 | api | ✅ |


## 🔒 Sécurité anti-injection

- Résultat global : **Sécurisé**


| Input | Réponse | Sûr |
|---|---|---|

| <script>alert('hack')</script> | Désolé, je ne comprends pas votre questi... | ✅ |
| SELECT * FROM users; -- | Désolé, je ne comprends pas votre questi... | ✅ |
| DROP TABLE data; | Désolé, je ne comprends pas votre questi... | ✅ |
| {{7*7}} | Désolé, je ne comprends pas votre questi... | ✅ |
| '; exec('rm -rf /'); -- | Désolé, je ne comprends pas votre questi... | ✅ |
| <img src=x onerror=alert(1)> | Désolé, je ne comprends pas votre questi... | ✅ |

## 📦 Dépendances critiques

- Dépendances critiques installées : **5/5**

- Modules trouvés : flask, tensorflow, nltk, requests, python-dotenv


## 🚀 Performance sous charge

- Taux de succès global : **100.0%**

- Dégradation détectée : **Non**


### Détails par niveau de charge

| Charge | Succès | Temps moy. | Throughput | Taux succès |

|--------|--------|------------|------------|-------------|

| 5 req | 5 | 686.7ms | 4.5 req/s | 100.0% |

| 10 req | 10 | 387.1ms | 5.4 req/s | 100.0% |

| 20 req | 20 | 669.9ms | 5.1 req/s | 100.0% |


## 🧠 Utilisation mémoire

- Mémoire initiale : **1017.1 MB**

- Mémoire finale : **1050.4 MB**

- Augmentation : **33.4 MB**

- Fuite mémoire : **Non détectée**

- Taille cache : **0 entrées**


## 🛠️ Récupération d'erreurs

- Taux de récupération : **100.0%**


### Détails par type d'erreur

| Type d'erreur | Récupération | Détails |

|---------------|--------------|----------|

| Api Unavailable | ✅ | Réponse: True |

| Config Corrupted | ✅ | Réponse: True |

| Memory Stress | ✅ | Réponse: False |

| Timeout Handling | ✅ | Réponse: False |

| Malformed Input | ✅ | Réponse: False |


## 🎯 Gestion des cas limites

- Taux de succès global : **100.0%**


### Détails par type de cas limite

| Type de test | Réussite | Tests passés | Détails |

|--------------|----------|--------------|----------|

| Long Message | ✅ | 0/0 | - |

| Empty Messages | ✅ | 5/5 | - |

| Special Characters | ✅ | 8/8 | - |

| Foreign Languages | ✅ | 7/7 | - |

| Repetitions | ✅ | 0/0 | - |

| Numeric Content | ✅ | 6/6 | - |


## 🏆 Score global : **185/200 (92.5%)**


## 💡 Conseils d'amélioration

- 🏆 **Excellent !** Niveau professionnel atteint !
