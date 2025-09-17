# 📊 Rapport de Performance Mila Assist

## ⚙️ Configuration

- Temps de chargement : **28.0 ms**

- Configuration valide : **Oui**


## ⚡ Temps de réponse & Précision

*Tests basés sur les données réelles de la base de données (comme train.py)*

- Temps moyen combiné (3 modes) : **415.1 ms**

- Précision combinée (3 modes) : **94.6%**


### 🧠 Mode Local Intelligent (Fallback complet)

- Temps moyen : **485.5 ms**

- Précision : **94.9%** (94/99)


### 🤖 Mode Local Brut (Keras seulement)

- Temps moyen : **145.2 ms**

- Précision : **89.9%** (89/99)


### 🌐 Mode API (Serveur externe)

- Temps moyen : **614.5 ms**

- Précision : **99.0%** (98/99)


### 📋 Détails des tests de précision

| Question | Tag attendu | Mots-clés | Réponse | Temps (ms) | Mode | Précis |

|---|---|---|---|---|---|---|

| bonjour | greetings | vous, être, merci | Bonjour, merci de vous être connecté ! C... | 7925.9 | local_smart | ✅ |

| salut | greetings | vous, être, merci | Salut ! Bonjour, merci de vous être conn... | 560.5 | local_smart | ✅ |

| coucou | greetings | vous, être, merci | Bonjour, merci de vous être connecté ! C... | 531.6 | local_smart | ✅ |

| Bonjour comment vous appeler vous ? | bonjour_comment_vous_appeler_v | assistant, virtuel, votre | Hello ! Je m'appelle Julie, votre assist... | 284.0 | local_smart | ✅ |

| au revoir | goodbye | passez, bonne, revenez | Passez une bonne journée, revenez quand ... | 276.1 | local_smart | ✅ |

| à bientôt | goodbye | passez, bonne, revenez | Passez une bonne journée, revenez quand ... | 389.6 | local_smart | ✅ |

| à plus tard | goodbye | passez, bonne, revenez | Passez une bonne journée, revenez quand ... | 1170.0 | local_smart | ✅ |

| merci | thanks | heureux | Je vous en prie ! Heureux d'aider !... | 547.1 | local_smart | ✅ |

| merci beaucoup | thanks | heureux | Heureux d'aider !... | 586.5 | local_smart | ✅ |

| super, merci | thanks | heureux | Heureux d'aider !... | 502.8 | local_smart | ✅ |

| Ajouter mon Twitch au canal content ? | twitch | ajoutez, titre, stream | Voici ce que je sais : Ajoutez @ai_licia... | 488.0 | local_smart | ✅ |

| Voir les événements passés au-delà des récents ? | past_events | faites, restent | Voici ce que je sais : Faites défiler, i... | 328.1 | local_smart | ✅ |

| On peut pas lui changer sont texte quand elle me réponds quand je l'appel  par example quand je l'appel elle me répond 'hum hum' pour me dire qu'elle m'etend et j'aurais voulu qu'elle me réponde par 'oui mon_nom' ou juste 'oui!!' au lieu de 'hum hum' | humhum | modifiable, peux, pour | Oui le hum hum n'est pas modifiable pour... | 598.4 | local_smart | ✅ |

| comment tu t'appel | name1 | programme, julie, artificielle | Je suis là pour ça ! Je m'appelle Julie ... | 493.3 | local_smart | ✅ |

| comment t'appelles tu | name1 | programme, julie, artificielle | Bien sûr, je peux vous aider ! Je m'appe... | 527.0 | local_smart | ✅ |

| comment vous appelez vous | name1 | programme, julie, artificielle | Voici comment je peux vous assister : Je... | 374.3 | local_smart | ✅ |

| Comment Obtenir ai_licia ? | comment_obtenir_ai_licia_? | choisis, très, simple | Désolé, je ne comprends pas votre questi... | 14.7 | local_smart | ❌ |

| Comment obtenir ai_licia ? | signup | très, récupérez, simple | Désolé, je ne comprends pas votre questi... | 10.2 | local_smart | ❌ |

| Comment configurer mon stream | stream_setup | configurer, votre, pour | Bien sûr, je peux vous aider ! Pour conf... | 283.6 | local_smart | ✅ |

| Comment démarrer un stream | stream_setup | configurer, votre, pour | Voici comment je peux vous assister : Po... | 288.6 | local_smart | ✅ |

| Quels sont les réglages pour un stream | stream_setup | configurer, votre, pour | Voici ce que je sais : Pour configurer v... | 778.2 | local_smart | ✅ |

| Comment monétiser mon stream | monetize_stream | votre, monétiser, pour | Bien sûr, je peux vous aider ! Pour moné... | 294.9 | local_smart | ✅ |

| Comment gagner de l'argent avec le streaming | monetize_stream | votre, monétiser, pour | Voici comment je peux vous assister : Po... | 316.5 | local_smart | ✅ |

| Quels sont les moyens de monétiser un stream | monetize_stream | votre, monétiser, pour | Voici ce que je sais : Pour monétiser vo... | 299.9 | local_smart | ✅ |

| Comment promouvoir mon stream | stream_promotion | votre, promouvoir, pour | Bien sûr, je peux vous aider ! Pour prom... | 288.5 | local_smart | ✅ |

| Comment attirer plus de spectateurs à mon stream | stream_promotion | votre, promouvoir, pour | Pour promouvoir votre stream, utilisez l... | 259.8 | local_smart | ✅ |

| Quels sont les meilleurs moyens de promouvoir mon stream | stream_promotion | votre, promouvoir, pour | Voici ce que je sais : Pour promouvoir v... | 604.9 | local_smart | ✅ |

| Comment planifier mon stream | stream_schedule | votre, planifier, pour | Voici comment je peux vous assister : Po... | 298.8 | local_smart | ✅ |

| Comment créer un calendrier de streaming | stream_schedule | votre, planifier, pour | Bien sûr, je peux vous aider ! Pour plan... | 259.9 | local_smart | ✅ |

| Comment la retirer de mon stream ? | remove | retrait, temporaire, retirez | Je suis là pour ça ! Retrait temporaire ... | 326.5 | local_smart | ✅ |

| Comment engager mon audience | engage_audience | engager, votre, pour | Je suis là pour ça ! Pour engager votre ... | 261.1 | local_smart | ✅ |

| Comment rendre mon stream plus interactif | engage_audience | engager, votre, pour | Bien sûr, je peux vous aider ! Pour enga... | 616.4 | local_smart | ✅ |

| Comment réinitialiser le bot ? | reset | ouvrez, source, navigateur | Voici comment je peux vous assister : Ou... | 387.9 | local_smart | ✅ |

| Comment résoudre les problèmes de streaming | stream_troubleshoot | résoudre, problèmes, pour | Pour résoudre les problèmes de streaming... | 309.9 | local_smart | ✅ |

| Comment corriger les problèmes de latence dans mon stream | stream_troubleshoot | résoudre, problèmes, pour | Je suis là pour ça ! Pour résoudre les p... | 289.9 | local_smart | ✅ |

| Pourquoi mon stream lag | stream_troubleshoot | résoudre, problèmes, pour | Pour résoudre les problèmes de streaming... | 259.6 | local_smart | ✅ |

| Comment améliorer la qualité de mon stream | stream_quality | améliorer, qualité, pour | Bien sûr, je peux vous aider ! Pour amél... | 732.5 | local_smart | ✅ |

| Comment obtenir une meilleure qualité de stream | stream_quality | améliorer, qualité, pour | Voici comment je peux vous assister : Po... | 484.3 | local_smart | ✅ |

| Pourquoi mon stream est il de mauvaise qualité | stream_quality | améliorer, qualité, pour | Voici ce que je sais : Pour améliorer la... | 280.6 | local_smart | ✅ |

| Comment définir le nom de mon bot ? | names | dans, mettez, jour | Je suis là pour ça ! Mettez à jour le no... | 265.2 | local_smart | ✅ |

| Comment donner un nom personnalisé à ai_licia ? | nickname | onglet, dans, changez | Je suis là pour ça ! Changez son nom dan... | 374.3 | local_smart | ✅ |

| Comment utiliser un code cadeau ? | code | promo, comme, code | Utilisez-le comme code promo au checkout... | 500.3 | local_smart | ✅ |

| Comment la faire réagir à ma voix ? | voice | faire, vous, page, pouvez, spe | Page Speak to ai_licia, choisissez la la... | 303.4 | local_smart | ✅ |

| ai_licia a-t-elle une voix ? | voice | faire, vous, page, pouvez, spe | Oui ! Vous pouvez faire parler ai_licia ... | -100.6 | local_smart | ✅ |

| Comment faire parler l'IA via TTS ? | talk | générez, source, customise | Voici comment je peux vous assister : Cu... | 323.8 | local_smart | ✅ |

| Comment tirer le meilleur parti de ai_licia ? | comment_tirer_le_meilleur_part | nous, rédigé, avons | Nous avons rédigé un article de blog pou... | 331.6 | local_smart | ✅ |

| Comment puis-je recommander AI_licia à mes amis ? | comment_puis-je_recommander_ai | pouvez, vous, recommander | Je suis là pour ça ! Vous pouvez recomma... | 271.8 | local_smart | ✅ |

| Comment savoir si ai_licia fonctionnerait dans mon stream | comment_savoir_si_ai_licia_fon | plus, dans, utilisée | Bien sûr, je peux vous aider ! Jusqu'à p... | 562.7 | local_smart | ✅ |

| Comment puis-je définir la personnalité de base d'AI_licia ? | comment_puis-je_définir_la_per | définir, pouvez, vous | Je suis là pour ça ! Vous pouvez définir... | 345.7 | local_smart | ✅ |

| Je ne comprends pas comment entendre ai_licia (TTS). | text_to_speech | speech, text, customise | Bien sûr, je peux vous aider ! Customise... | 523.4 | local_smart | ✅ |

| Comment puis-je être informé des nouveautés sur AI_licia ? | comment_puis-je_être_informé_d | tient, vous, section | Voici comment je peux vous assister : La... | 337.7 | local_smart | ✅ |

| Comment voir ai_licia en action chez d'autres streamers ? | stream | gardez, voir, pour | Gardez un œil sur #your-content pour voi... | 406.8 | local_smart | ✅ |

| J'aimerais suggérer une fonctionnalité pour ai_licia, comment puis-je faire cela ? | j'aimerais_suggérer_une_foncti | nous, adorerions, entendre | Bien sûr, je peux vous aider ! Nous ador... | 358.3 | local_smart | ✅ |

| Comment stopper ses messages sur mes pubs et demandes d'abos ? | talking | choisissez, settings, customis | Je suis là pour ça ! Customise ai_licia ... | 316.8 | local_smart | ✅ |

| La commande Shoutout marche mal avec certains pseudos. Comment écrire les descriptions ? | commands | décrivez, comme, pour | Bien sûr, je peux vous aider ! Décrivez ... | 319.2 | local_smart | ✅ |

| Elle marche en test mais pas en continu en live, comment l'appeler vocalement ? | speak | live, cliquez, speak, ouvrez,  | Bien sûr, je peux vous aider ! Cliquez S... | 321.3 | local_smart | ✅ |

| Je parle dans 'Speak to ai_licia' mais elle ne rejoint pas le chat. | speak | live, cliquez, speak, ouvrez,  | Hors live : cliquez sur Test ai_licia pu... | 288.9 | local_smart | ✅ |

| Comment changer alicia de compte tiktok car j'ai été ban 3 jours de mon compte principal ? | ban | plus, simple, pour | Bien sûr, je peux vous aider ! Pour un b... | 315.0 | local_smart | ✅ |

| Je veux donner un visage vtuber/png à AiLicia mais les programmes n'acceptent que l'entrée micro. Comment faire accepter une source navigateur comme micro ? | vtuber | nous, carte, avons | Bien sûr, je peux vous aider ! Nous avon... | 439.3 | local_smart | ✅ |

| qui t'a programmé | creator | samuel, créé, développeurs | J'ai été créé par Samuel un développeurs... | 293.0 | local_smart | ✅ |

| qui t'a créé | creator | samuel, créé, développeurs | J'ai été créé par Samuel un développeurs... | 317.0 | local_smart | ✅ |

| qui est ton créateur | creator | samuel, créé, développeurs | Voici ce que je sais : J'ai été créé par... | 314.7 | local_smart | ✅ |

| Reconnaît-elle qui est mod ? | mod |  | Non.... | 259.9 | local_smart | ❌ |

| es tu vieux | age | programme, suis, donc | Voici ce que je sais : Je suis un progra... | 372.1 | local_smart | ✅ |

| es tu recent | age | programme, suis, donc | Voici ce que je sais : Je suis un progra... | 349.4 | local_smart | ✅ |

| es tu ancien | age | programme, suis, donc | Voici ce que je sais : Je suis un progra... | 434.5 | local_smart | ✅ |

| es tu sage | es_tu_sage | compréhension, implique, sages | La sagesse implique une compréhension pr... | 371.8 | local_smart | ✅ |

| j'ai besoin d'aide pour configurer AI_licia | j'ai_besoin_d'aide_pour_config | avez, besoin, vous | Je suis là pour ça ! Si vous avez besoin... | 337.4 | local_smart | ✅ |

| Changer le nom d'Ai_licia ? | name | guide, instructions, compte, c | Voici ce que je sais : Créez un nouveau ... | 494.7 | local_smart | ✅ |

| Puis-je changer le nom d'ai_licia sur Twitch ? | name | guide, instructions, compte, c | Voici ce que je sais : Oui ! Guide ici :... | 392.2 | local_smart | ✅ |

| Changer le display name d'Ai_licia sur Twitch ? | name | guide, instructions, compte, c | Voici ce que je sais : Page : https://st... | 573.4 | local_smart | ✅ |

| Puis je tester ai_licia ? | puis_je_tester_ai_licia_? | avoir, bien, peux | Voici ce que je sais : Bien sûr ! Tu peu... | 306.6 | local_smart | ✅ |

| Qu'est ce que ai_licia? | Ai_licia | premier, compagnon, pour | Voici ce que je sais : ai_licia est le p... | 750.6 | local_smart | ✅ |

| Qu'est-ce que ai_licia ? | Ai_licia | premier, compagnon, pour | Voici ce que je sais : ai_licia est le p... | 773.1 | local_smart | ✅ |

| Qu'est-ce que ailicia ? | Ai_licia | premier, compagnon, pour | Voici ce que je sais : ai_licia est le p... | 512.8 | local_smart | ✅ |

| ai_licia est elle uniquement pour Twitch ? | ai_licia_est_elle_uniquement_p | mais, moment, pour | Voici ce que je sais : Pour le moment ou... | 603.5 | local_smart | ✅ |

| Plusieurs ai_licia en même temps ? | multiple | risque, comme, botting | Désolé, je ne comprends pas votre questi... | 11.2 | local_smart | ❌ |

| Puis-je donner un surnom à AI_licia ? | puis-je_donner_un_surnom_à_ai_ | pouvez, choisir, vous | Voici ce que je sais : Oui, vous pouvez ... | 652.6 | local_smart | ✅ |

| Peut-on désactiver ai_licia temporairement ? | disable | haut, bouton, droite | Voici ce que je sais : Il y a un bouton ... | 398.6 | local_smart | ✅ |

| Qu'est-ce qu'ai_licia ? | ai_licia | votre | Voici ce que je sais : ai_licia est le p... | 245.1 | local_smart | ❌ |

| ai_licia est-elle disponible sur Discord ? | discord | nous, rejoignez, travaillons | Nous y travaillons ! Rejoignez la liste ... | 356.4 | local_smart | ✅ |

| Puis-je personnaliser le comportement d'AI_licia ? | puis-je_personnaliser_le_compo | absolument, avez, vous | Voici ce que je sais : Absolument ! Vous... | 470.0 | local_smart | ✅ |

| Puis-je intégrer AI_licia à mes outils de streaming ? | puis-je_intégrer_ai_licia_à_me | être, peut, intégrée | Oui, AI_licia peut être intégrée à diver... | 478.8 | local_smart | ✅ |

| Quels paramètres d'interaction puis-je ajuster pour AI_licia ? | quels_paramètres_d'interaction | pouvez, vous, ajuster | Vous pouvez ajuster plusieurs paramètres... | 556.7 | local_smart | ✅ |

| À quoi sert la section "Tes Personnages" dans AI_licia ? | à_quoi_sert_la_section_"tes_pe | permet, vous, section | La section "Tes Personnages" https://str... | 300.5 | local_smart | ✅ |

| Je viens d'ajouter ai_licia à mon stream, par où commencer ? | start | nous, avons, vous | Nous avons ce qu'il vous faut ! Regardez... | 546.0 | local_smart | ✅ |

| mode Blanc/Light/Dark sur le site AI_licia ? | mode_blanc/light/dark_sur_le_s | mode, changer, permet | Voici ce que je sais : Le mode Light/Dar... | 665.3 | local_smart | ✅ |

| Configurer un compte alt Twitch pour ai_licia lié à mon principal ? | account | ouvrez, lien, token | Voici ce que je sais : Ouvrez le lien de... | 412.1 | local_smart | ✅ |

| Je parle à ai_licia pendant mon stream, mais elle ne semble pas répondre ? | je_parle_à_ai_licia_pendant_mo | toujours, dois, garder | Voici ce que je sais : Tu dois toujours ... | 322.4 | local_smart | ✅ |

| Pour que ai_licia puisse écouter et me répondre quand je suis en live le bouton 'écouter' de l'application doit être toujours activé ? | écouter | page, être, faut | Voici ce que je sais : Oui. Il faut être... | 535.5 | local_smart | ✅ |

| Associer la voix TTS à une mascotte (PNG bouche animée) ? | mascot | dans, avec, plugin | Voici ce que je sais : Oui dans OBS avec... | 532.1 | local_smart | ✅ |

| Est il possible de désactiver le TTS pour certains stream et le réactiver pour d'autres ? | TTS | faire, dois, pouvoir | Voici ce que je sais : Tu dois pouvoir l... | 492.4 | local_smart | ✅ |

| Peut-on lui faire ignorer les récompenses de points, surtout les requêtes TTS ? Ça se chevauche. | points | nous, encore, cette | Voici ce que je sais : Nous n'avons pas ... | 386.7 | local_smart | ✅ |

| Pour les voix doit-on garder le site ouvert ou ajouter à OBS ? | voices | personnage, onglet, dans | Voici ce que je sais : Oui via OBS : dan... | 326.1 | local_smart | ✅ |

| Elle connaît la catégorie du stream ? | categories | elle, catégorie | Oui elle a l'info de catégorie 😊.... | 607.3 | local_smart | ✅ |

| La faire 'voir' le stream avec Streamlabs ? | see | streamlabs, virtual, utilisez | Utilisez Streamlabs Virtual Camera. Tuto... | 403.5 | local_smart | ✅ |

| Event mode masque la stream knowledge. Est-elle perdue ? | event | mode, simplement, ignorée | Non, simplement ignorée en mode event. R... | 494.5 | local_smart | ✅ |

| Configurer l'outil multi-action avec le plugin Stream Deck ? | stream_deck | installez, plugin, request | Installez le plugin API Request : https:... | 461.9 | local_smart | ✅ |

| Si je lui donne un autre nom dans 'roles' réagira-t-elle à celui-ci ? | roles | carte, fonctionnalité, après | Oui via la fonctionnalité 'surnoms d'ai_... | 620.1 | local_smart | ✅ |

| bonjour | greetings | vous, être, merci | Bonjour, merci de vous être connecté ! C... | 187.0 | local_raw | ✅ |

| salut | greetings | vous, être, merci | Bonjour, merci de vous être connecté ! C... | 142.8 | local_raw | ✅ |

| coucou | greetings | vous, être, merci | Bonjour, merci de vous être connecté ! C... | 183.0 | local_raw | ✅ |

| Bonjour comment vous appeler vous ? | bonjour_comment_vous_appeler_v | assistant, virtuel, votre | Je m'appelle Julie, votre assistant virt... | 147.1 | local_raw | ✅ |

| au revoir | goodbye | passez, bonne, revenez | Passez une bonne journée, revenez quand ... | 169.3 | local_raw | ✅ |

| à bientôt | goodbye | passez, bonne, revenez | Bonjour, merci de vous être connecté ! C... | 208.7 | local_raw | ❌ |

| à plus tard | goodbye | passez, bonne, revenez | Passez une bonne journée, revenez quand ... | 135.6 | local_raw | ✅ |

| merci | thanks | heureux | Heureux d'aider !... | 182.2 | local_raw | ✅ |

| merci beaucoup | thanks | heureux | Heureux d'aider !... | 188.9 | local_raw | ✅ |

| super, merci | thanks | heureux | Heureux d'aider !... | 181.9 | local_raw | ✅ |

| Ajouter mon Twitch au canal content ? | twitch | ajoutez, titre, stream | Ajoutez @ai_licia au titre de stream au ... | 134.6 | local_raw | ✅ |

| Voir les événements passés au-delà des récents ? | past_events | faites, restent | Faites défiler, ils restent jusqu'au ref... | 176.4 | local_raw | ✅ |

| On peut pas lui changer sont texte quand elle me réponds quand je l'appel  par example quand je l'appel elle me répond 'hum hum' pour me dire qu'elle m'etend et j'aurais voulu qu'elle me réponde par 'oui mon_nom' ou juste 'oui!!' au lieu de 'hum hum' | humhum | modifiable, peux, pour | Pas encore. Nous prévoyons une base de c... | 155.3 | local_raw | ❌ |

| comment tu t'appel | name1 | programme, julie, artificielle | Je m'appelle Julie un programme d'intell... | 159.0 | local_raw | ✅ |

| comment t'appelles tu | name1 | programme, julie, artificielle | Je m'appelle Julie un programme d'intell... | 161.8 | local_raw | ✅ |

| comment vous appelez vous | name1 | programme, julie, artificielle | Je m'appelle Julie un programme d'intell... | 155.9 | local_raw | ✅ |

| Comment Obtenir ai_licia ? | comment_obtenir_ai_licia_? | choisis, très, simple | Très simple ! Rends-toi sur https://stre... | 153.0 | local_raw | ✅ |

| Comment obtenir ai_licia ? | signup | très, récupérez, simple | Très simple ! Rends-toi sur https://stre... | 0.1 | local_raw | ✅ |

| Comment configurer mon stream | stream_setup | configurer, votre, pour | Pour configurer votre stream, vous devez... | 172.8 | local_raw | ✅ |

| Comment démarrer un stream | stream_setup | configurer, votre, pour | Pour configurer votre stream, vous devez... | 198.3 | local_raw | ✅ |

| Quels sont les réglages pour un stream | stream_setup | configurer, votre, pour | Les outils populaires pour le streaming ... | 162.4 | local_raw | ✅ |

| Comment monétiser mon stream | monetize_stream | votre, monétiser, pour | Pour monétiser votre stream, vous pouvez... | 141.5 | local_raw | ✅ |

| Comment gagner de l'argent avec le streaming | monetize_stream | votre, monétiser, pour | Pour monétiser votre stream, vous pouvez... | 151.6 | local_raw | ✅ |

| Quels sont les moyens de monétiser un stream | monetize_stream | votre, monétiser, pour | Pour monétiser votre stream, vous pouvez... | 180.1 | local_raw | ✅ |

| Comment promouvoir mon stream | stream_promotion | votre, promouvoir, pour | Pour promouvoir votre stream, utilisez l... | 79.3 | local_raw | ✅ |

| Comment attirer plus de spectateurs à mon stream | stream_promotion | votre, promouvoir, pour | Pour promouvoir votre stream, utilisez l... | 106.2 | local_raw | ✅ |

| Quels sont les meilleurs moyens de promouvoir mon stream | stream_promotion | votre, promouvoir, pour | Pour promouvoir votre stream, utilisez l... | 166.1 | local_raw | ✅ |

| Comment planifier mon stream | stream_schedule | votre, planifier, pour | Pour planifier votre stream, choisissez ... | 145.2 | local_raw | ✅ |

| Comment créer un calendrier de streaming | stream_schedule | votre, planifier, pour | Pour planifier votre stream, choisissez ... | 113.6 | local_raw | ✅ |

| Comment la retirer de mon stream ? | remove | retrait, temporaire, retirez | Le bouton apparaît quelques minutes aprè... | 164.8 | local_raw | ❌ |

| Comment engager mon audience | engage_audience | engager, votre, pour | Pour engager votre audience, interagisse... | 164.1 | local_raw | ✅ |

| Comment rendre mon stream plus interactif | engage_audience | engager, votre, pour | Pour engager votre audience, interagisse... | 127.9 | local_raw | ✅ |

| Comment réinitialiser le bot ? | reset | ouvrez, source, navigateur | Ouvrez la source navigateur dans un nouv... | 93.4 | local_raw | ✅ |

| Comment résoudre les problèmes de streaming | stream_troubleshoot | résoudre, problèmes, pour | Pour résoudre les problèmes de streaming... | 150.1 | local_raw | ✅ |

| Comment corriger les problèmes de latence dans mon stream | stream_troubleshoot | résoudre, problèmes, pour | Pour résoudre les problèmes de streaming... | 150.7 | local_raw | ✅ |

| Pourquoi mon stream lag | stream_troubleshoot | résoudre, problèmes, pour | Pour résoudre les problèmes de streaming... | 124.0 | local_raw | ✅ |

| Comment améliorer la qualité de mon stream | stream_quality | améliorer, qualité, pour | Pour améliorer la qualité de votre strea... | 164.7 | local_raw | ✅ |

| Comment obtenir une meilleure qualité de stream | stream_quality | améliorer, qualité, pour | Pour améliorer la qualité de votre strea... | 151.6 | local_raw | ✅ |

| Pourquoi mon stream est il de mauvaise qualité | stream_quality | améliorer, qualité, pour | Pour améliorer la qualité de votre strea... | 183.4 | local_raw | ✅ |

| Comment définir le nom de mon bot ? | names | dans, mettez, jour | Mettez à jour le nom dans la page Charac... | 172.8 | local_raw | ✅ |

| Comment donner un nom personnalisé à ai_licia ? | nickname | onglet, dans, changez | Interaction timing en bas de Voice setti... | 128.1 | local_raw | ❌ |

| Comment utiliser un code cadeau ? | code | promo, comme, code | Utilisez-le comme code promo au checkout... | 172.2 | local_raw | ✅ |

| Comment la faire réagir à ma voix ? | voice | faire, vous, page, pouvez, spe | Oui, vous pouvez faire les deux ! D'abor... | 176.0 | local_raw | ✅ |

| ai_licia a-t-elle une voix ? | voice | faire, vous, page, pouvez, spe | Vous pouvez avoir les deux en même temps... | 161.5 | local_raw | ✅ |

| Comment faire parler l'IA via TTS ? | talk | générez, source, customise | Réglez chattiness dans interaction setti... | 125.6 | local_raw | ❌ |

| Comment tirer le meilleur parti de ai_licia ? | comment_tirer_le_meilleur_part | nous, rédigé, avons | Nous avons rédigé un article de blog pou... | 100.1 | local_raw | ✅ |

| Comment puis-je recommander AI_licia à mes amis ? | comment_puis-je_recommander_ai | pouvez, vous, recommander | Vous pouvez recommander AI_licia à vos a... | 163.0 | local_raw | ✅ |

| Comment savoir si ai_licia fonctionnerait dans mon stream | comment_savoir_si_ai_licia_fon | plus, dans, utilisée | Jusqu'à présent, ai_licia a été utilisée... | 97.9 | local_raw | ✅ |

| Comment puis-je définir la personnalité de base d'AI_licia ? | comment_puis-je_définir_la_per | définir, pouvez, vous | Vous pouvez définir la personnalité de b... | 150.0 | local_raw | ✅ |

| Je ne comprends pas comment entendre ai_licia (TTS). | text_to_speech | speech, text, customise | Customise ai_licia -> Text to Speech : c... | 164.7 | local_raw | ✅ |

| Comment puis-je être informé des nouveautés sur AI_licia ? | comment_puis-je_être_informé_d | tient, vous, section | La section "Nouveautés" https://headway-... | 158.9 | local_raw | ✅ |

| Comment voir ai_licia en action chez d'autres streamers ? | stream | gardez, voir, pour | Gardez un œil sur #your-content pour voi... | 152.6 | local_raw | ✅ |

| J'aimerais suggérer une fonctionnalité pour ai_licia, comment puis-je faire cela ? | j'aimerais_suggérer_une_foncti | nous, adorerions, entendre | Nous adorerions entendre tes idées pour ... | 131.6 | local_raw | ✅ |

| Comment stopper ses messages sur mes pubs et demandes d'abos ? | talking | choisissez, settings, customis | Customise ai_licia -> Settings : choisis... | 100.2 | local_raw | ✅ |

| La commande Shoutout marche mal avec certains pseudos. Comment écrire les descriptions ? | commands | décrivez, comme, pour | Les descriptions disent quand les utilis... | 135.9 | local_raw | ✅ |

| Elle marche en test mais pas en continu en live, comment l'appeler vocalement ? | speak | live, cliquez, speak, ouvrez,  | Hors live : cliquez sur Test ai_licia pu... | 165.0 | local_raw | ✅ |

| Je parle dans 'Speak to ai_licia' mais elle ne rejoint pas le chat. | speak | live, cliquez, speak, ouvrez,  | Hors live : cliquez sur Test ai_licia pu... | 170.9 | local_raw | ✅ |

| Comment changer alicia de compte tiktok car j'ai été ban 3 jours de mon compte principal ? | ban | plus, simple, pour | Pour un ban de 3 jours, le plus simple s... | 141.2 | local_raw | ✅ |

| Je veux donner un visage vtuber/png à AiLicia mais les programmes n'acceptent que l'entrée micro. Comment faire accepter une source navigateur comme micro ? | vtuber | nous, carte, avons | Nous avons une carte sur la roadmap pour... | -263.0 | local_raw | ✅ |

| qui t'a programmé | creator | samuel, créé, développeurs | J'ai été créé par Samuel un développeurs... | 109.4 | local_raw | ✅ |

| qui t'a créé | creator | samuel, créé, développeurs | J'ai été créé par Samuel un développeurs... | 72.9 | local_raw | ✅ |

| qui est ton créateur | creator | samuel, créé, développeurs | J'ai été créé par Samuel un développeurs... | 81.8 | local_raw | ✅ |

| Reconnaît-elle qui est mod ? | mod |  | J'ai été créé par Samuel un développeurs... | 96.8 | local_raw | ❌ |

| es tu vieux | age | programme, suis, donc | La sagesse implique une compréhension pr... | 129.4 | local_raw | ❌ |

| es tu recent | age | programme, suis, donc | La sagesse implique une compréhension pr... | 182.2 | local_raw | ❌ |

| es tu ancien | age | programme, suis, donc | La sagesse implique une compréhension pr... | 161.0 | local_raw | ❌ |

| es tu sage | es_tu_sage | compréhension, implique, sages | La sagesse implique une compréhension pr... | 191.6 | local_raw | ✅ |

| j'ai besoin d'aide pour configurer AI_licia | j'ai_besoin_d'aide_pour_config | avez, besoin, vous | Si vous avez besoin d'aide pour configur... | 178.7 | local_raw | ✅ |

| Changer le nom d'Ai_licia ? | name | guide, instructions, compte, c | Enchanté de vous rencontrer {n}. Comment... | 173.5 | local_raw | ❌ |

| Puis-je changer le nom d'ai_licia sur Twitch ? | name | guide, instructions, compte, c | Page : https://streamer-dashboard.ailici... | 192.0 | local_raw | ✅ |

| Changer le display name d'Ai_licia sur Twitch ? | name | guide, instructions, compte, c | Page : https://streamer-dashboard.ailici... | 89.2 | local_raw | ✅ |

| Puis je tester ai_licia ? | puis_je_tester_ai_licia_? | avoir, bien, peux | Bien sûr ! Tu peux avoir un premier aper... | 137.6 | local_raw | ✅ |

| Qu'est ce que ai_licia? | Ai_licia | premier, compagnon, pour | ai_licia est votre compagnon, votre co-a... | 88.1 | local_raw | ✅ |

| Qu'est-ce que ai_licia ? | Ai_licia | premier, compagnon, pour | ai_licia est votre compagnon, votre co-a... | 86.0 | local_raw | ✅ |

| Qu'est-ce que ailicia ? | Ai_licia | premier, compagnon, pour | ai_licia est votre compagnon, votre co-a... | 120.1 | local_raw | ✅ |

| ai_licia est elle uniquement pour Twitch ? | ai_licia_est_elle_uniquement_p | mais, moment, pour | Pour le moment oui, mais nous prévoyons ... | 186.1 | local_raw | ✅ |

| Plusieurs ai_licia en même temps ? | multiple | risque, comme, botting | Non, risque d'être vu comme botting par ... | 196.9 | local_raw | ✅ |

| Puis-je donner un surnom à AI_licia ? | puis-je_donner_un_surnom_à_ai_ | pouvez, choisir, vous | Oui, vous pouvez choisir un petit surnom... | 230.7 | local_raw | ✅ |

| Peut-on désactiver ai_licia temporairement ? | disable | haut, bouton, droite | Il y a un bouton en haut à droite du das... | 223.7 | local_raw | ✅ |

| Qu'est-ce qu'ai_licia ? | ai_licia | votre | ai_licia est votre compagnon, votre co-a... | 199.3 | local_raw | ✅ |

| ai_licia est-elle disponible sur Discord ? | discord | nous, rejoignez, travaillons | Nous y travaillons ! Rejoignez la liste ... | 211.1 | local_raw | ✅ |

| Puis-je personnaliser le comportement d'AI_licia ? | puis-je_personnaliser_le_compo | absolument, avez, vous | Absolument ! Vous avez le contrôle total... | 168.8 | local_raw | ✅ |

| Puis-je intégrer AI_licia à mes outils de streaming ? | puis-je_intégrer_ai_licia_à_me | être, peut, intégrée | Oui, AI_licia peut être intégrée à diver... | 131.9 | local_raw | ✅ |

| Quels paramètres d'interaction puis-je ajuster pour AI_licia ? | quels_paramètres_d'interaction | pouvez, vous, ajuster | Vous pouvez ajuster plusieurs paramètres... | 145.6 | local_raw | ✅ |

| À quoi sert la section "Tes Personnages" dans AI_licia ? | à_quoi_sert_la_section_"tes_pe | permet, vous, section | La section "Tes Personnages" https://str... | 191.2 | local_raw | ✅ |

| Je viens d'ajouter ai_licia à mon stream, par où commencer ? | start | nous, avons, vous | Nous avons ce qu'il vous faut ! Regardez... | 134.8 | local_raw | ✅ |

| mode Blanc/Light/Dark sur le site AI_licia ? | mode_blanc/light/dark_sur_le_s | mode, changer, permet | Le mode Light/Dark permet de changer l'a... | 163.4 | local_raw | ✅ |

| Configurer un compte alt Twitch pour ai_licia lié à mon principal ? | account | ouvrez, lien, token | Ouvrez le lien de token en navigation pr... | 119.6 | local_raw | ✅ |

| Je parle à ai_licia pendant mon stream, mais elle ne semble pas répondre ? | je_parle_à_ai_licia_pendant_mo | toujours, dois, garder | Tu dois toujours garder ouverte la page ... | 101.1 | local_raw | ✅ |

| Pour que ai_licia puisse écouter et me répondre quand je suis en live le bouton 'écouter' de l'application doit être toujours activé ? | écouter | page, être, faut | Oui. Il faut être sur la page et que éco... | 120.6 | local_raw | ✅ |

| Associer la voix TTS à une mascotte (PNG bouche animée) ? | mascot | dans, avec, plugin | Ajustez dans Character -> Voices (Genera... | 157.4 | local_raw | ✅ |

| Est il possible de désactiver le TTS pour certains stream et le réactiver pour d'autres ? | TTS | faire, dois, pouvoir | Tu dois pouvoir le faire depuis OBS, si ... | 120.1 | local_raw | ✅ |

| Peut-on lui faire ignorer les récompenses de points, surtout les requêtes TTS ? Ça se chevauche. | points | nous, encore, cette | Nous n'avons pas encore cette option et ... | 98.1 | local_raw | ✅ |

| Pour les voix doit-on garder le site ouvert ou ajouter à OBS ? | voices | personnage, onglet, dans | Oui via OBS : dans le personnage onglet ... | 147.0 | local_raw | ✅ |

| Elle connaît la catégorie du stream ? | categories | elle, catégorie | Oui elle a l'info de catégorie 😊.... | 101.5 | local_raw | ✅ |

| La faire 'voir' le stream avec Streamlabs ? | see | streamlabs, virtual, utilisez | Utilisez Streamlabs Virtual Camera. Tuto... | 182.5 | local_raw | ✅ |

| Event mode masque la stream knowledge. Est-elle perdue ? | event | mode, simplement, ignorée | Non, simplement ignorée en mode event. R... | 125.2 | local_raw | ✅ |

| Configurer l'outil multi-action avec le plugin Stream Deck ? | stream_deck | installez, plugin, request | Installez le plugin API Request : https:... | 258.0 | local_raw | ✅ |

| Si je lui donne un autre nom dans 'roles' réagira-t-elle à celui-ci ? | roles | carte, fonctionnalité, après | Oui via la fonctionnalité 'surnoms d'ai_... | 148.3 | local_raw | ✅ |

| bonjour | greetings | vous, être, merci | Bonjour ! Bonjour, merci de vous être co... | 300.1 | api | ✅ |

| salut | greetings | vous, être, merci | Salut ! Bonjour, merci de vous être conn... | 544.0 | api | ✅ |

| coucou | greetings | vous, être, merci | Bonjour, merci de vous être connecté ! C... | 723.5 | api | ✅ |

| Bonjour comment vous appeler vous ? | bonjour_comment_vous_appeler_v | assistant, virtuel, votre | Hello ! Je m'appelle Julie, votre assist... | 1028.5 | api | ✅ |

| au revoir | goodbye | passez, bonne, revenez | Passez une bonne journée, revenez quand ... | 825.2 | api | ✅ |

| à bientôt | goodbye | passez, bonne, revenez | Passez une bonne journée, revenez quand ... | 1240.0 | api | ✅ |

| à plus tard | goodbye | passez, bonne, revenez | Voici ce que je sais : Passez une bonne ... | 1074.7 | api | ✅ |

| merci | thanks | heureux | Je vous en prie ! Heureux d'aider !... | 512.0 | api | ✅ |

| merci beaucoup | thanks | heureux | Pas de problème ! Heureux d'aider !... | 477.8 | api | ✅ |

| super, merci | thanks | heureux | Pas de problème ! Heureux d'aider !... | 773.7 | api | ✅ |

| Ajouter mon Twitch au canal content ? | twitch | ajoutez, titre, stream | Ajoutez @ai_licia au titre de stream au ... | 1070.0 | api | ✅ |

| Voir les événements passés au-delà des récents ? | past_events | faites, restent | Faites défiler, ils restent jusqu'au ref... | 789.6 | api | ✅ |

| On peut pas lui changer sont texte quand elle me réponds quand je l'appel  par example quand je l'appel elle me répond 'hum hum' pour me dire qu'elle m'etend et j'aurais voulu qu'elle me réponde par 'oui mon_nom' ou juste 'oui!!' au lieu de 'hum hum' | humhum | modifiable, peux, pour | Voici ce que je sais : Oui le hum hum n'... | 531.9 | api | ✅ |

| comment tu t'appel | name1 | programme, julie, artificielle | Voici comment je peux vous assister : Je... | 430.1 | api | ✅ |

| comment t'appelles tu | name1 | programme, julie, artificielle | Bien sûr, je peux vous aider ! Je m'appe... | 337.9 | api | ✅ |

| comment vous appelez vous | name1 | programme, julie, artificielle | Je suis là pour ça ! Je m'appelle Julie ... | 758.5 | api | ✅ |

| Comment Obtenir ai_licia ? | comment_obtenir_ai_licia_? | choisis, très, simple | Bien sûr, je peux vous aider ! Très simp... | 641.4 | api | ✅ |

| Comment obtenir ai_licia ? | signup | très, récupérez, simple | Bien sûr, je peux vous aider ! Très simp... | 436.7 | api | ✅ |

| Comment configurer mon stream | stream_setup | configurer, votre, pour | Pour configurer votre stream, vous devez... | 484.3 | api | ✅ |

| Comment démarrer un stream | stream_setup | configurer, votre, pour | Voici comment je peux vous assister : Po... | 581.3 | api | ✅ |

| Quels sont les réglages pour un stream | stream_setup | configurer, votre, pour | Pour configurer votre stream, vous devez... | 575.6 | api | ✅ |

| Comment monétiser mon stream | monetize_stream | votre, monétiser, pour | Je suis là pour ça ! Pour monétiser votr... | 429.8 | api | ✅ |

| Comment gagner de l'argent avec le streaming | monetize_stream | votre, monétiser, pour | Voici comment je peux vous assister : Po... | 522.8 | api | ✅ |

| Quels sont les moyens de monétiser un stream | monetize_stream | votre, monétiser, pour | Voici ce que je sais : Pour monétiser vo... | 710.1 | api | ✅ |

| Comment promouvoir mon stream | stream_promotion | votre, promouvoir, pour | Pour promouvoir votre stream, utilisez l... | 417.3 | api | ✅ |

| Comment attirer plus de spectateurs à mon stream | stream_promotion | votre, promouvoir, pour | Je suis là pour ça ! Pour promouvoir vot... | 356.8 | api | ✅ |

| Quels sont les meilleurs moyens de promouvoir mon stream | stream_promotion | votre, promouvoir, pour | Voici ce que je sais : Pour promouvoir v... | 525.1 | api | ✅ |

| Comment planifier mon stream | stream_schedule | votre, planifier, pour | Voici comment je peux vous assister : Po... | 711.5 | api | ✅ |

| Comment créer un calendrier de streaming | stream_schedule | votre, planifier, pour | Pour planifier votre stream, choisissez ... | 480.2 | api | ✅ |

| Comment la retirer de mon stream ? | remove | retrait, temporaire, retirez | Bien sûr, je peux vous aider ! Retrait t... | 330.7 | api | ✅ |

| Comment engager mon audience | engage_audience | engager, votre, pour | Bien sûr, je peux vous aider ! Pour enga... | 620.1 | api | ✅ |

| Comment rendre mon stream plus interactif | engage_audience | engager, votre, pour | Voici comment je peux vous assister : Po... | 608.4 | api | ✅ |

| Comment réinitialiser le bot ? | reset | ouvrez, source, navigateur | Ouvrez la source navigateur dans un nouv... | 598.3 | api | ✅ |

| Comment résoudre les problèmes de streaming | stream_troubleshoot | résoudre, problèmes, pour | Voici comment je peux vous assister : Po... | 730.8 | api | ✅ |

| Comment corriger les problèmes de latence dans mon stream | stream_troubleshoot | résoudre, problèmes, pour | Je suis là pour ça ! Pour résoudre les p... | 555.5 | api | ✅ |

| Pourquoi mon stream lag | stream_troubleshoot | résoudre, problèmes, pour | Pour résoudre les problèmes de streaming... | 399.3 | api | ✅ |

| Comment améliorer la qualité de mon stream | stream_quality | améliorer, qualité, pour | Je suis là pour ça ! Pour améliorer la q... | 382.1 | api | ✅ |

| Comment obtenir une meilleure qualité de stream | stream_quality | améliorer, qualité, pour | Bien sûr, je peux vous aider ! Pour amél... | 300.2 | api | ✅ |

| Pourquoi mon stream est il de mauvaise qualité | stream_quality | améliorer, qualité, pour | Voici ce que je sais : Pour améliorer la... | 621.0 | api | ✅ |

| Comment définir le nom de mon bot ? | names | dans, mettez, jour | Je suis là pour ça ! Mettez à jour le no... | 448.6 | api | ✅ |

| Comment donner un nom personnalisé à ai_licia ? | nickname | onglet, dans, changez | Bien sûr, je peux vous aider ! Changez s... | 512.5 | api | ✅ |

| Comment utiliser un code cadeau ? | code | promo, comme, code | Voici comment je peux vous assister : Ut... | 421.9 | api | ✅ |

| Comment la faire réagir à ma voix ? | voice | faire, vous, page, pouvez, spe | Page Speak to ai_licia, choisissez la la... | 774.1 | api | ✅ |

| ai_licia a-t-elle une voix ? | voice | faire, vous, page, pouvez, spe | Voici ce que je sais : Oui ! Vous pouvez... | 139.4 | api | ✅ |

| Comment faire parler l'IA via TTS ? | talk | générez, source, customise | Je suis là pour ça ! Customise ai_licia ... | 418.9 | api | ✅ |

| Comment tirer le meilleur parti de ai_licia ? | comment_tirer_le_meilleur_part | nous, rédigé, avons | Je suis là pour ça ! Nous avons rédigé u... | 412.0 | api | ✅ |

| Comment puis-je recommander AI_licia à mes amis ? | comment_puis-je_recommander_ai | pouvez, vous, recommander | Je suis là pour ça ! Vous pouvez recomma... | 581.2 | api | ✅ |

| Comment savoir si ai_licia fonctionnerait dans mon stream | comment_savoir_si_ai_licia_fon | plus, dans, utilisée | Jusqu'à présent, ai_licia a été utilisée... | 584.7 | api | ✅ |

| Comment puis-je définir la personnalité de base d'AI_licia ? | comment_puis-je_définir_la_per | définir, pouvez, vous | Bien sûr, je peux vous aider ! Vous pouv... | 383.3 | api | ✅ |

| Je ne comprends pas comment entendre ai_licia (TTS). | text_to_speech | speech, text, customise | Voici comment je peux vous assister : Cu... | 559.9 | api | ✅ |

| Comment puis-je être informé des nouveautés sur AI_licia ? | comment_puis-je_être_informé_d | tient, vous, section | Bien sûr, je peux vous aider ! La sectio... | 680.4 | api | ✅ |

| Comment voir ai_licia en action chez d'autres streamers ? | stream | gardez, voir, pour | Je suis là pour ça ! Gardez un œil sur #... | 939.6 | api | ✅ |

| J'aimerais suggérer une fonctionnalité pour ai_licia, comment puis-je faire cela ? | j'aimerais_suggérer_une_foncti | nous, adorerions, entendre | Voici comment je peux vous assister : No... | 986.9 | api | ✅ |

| Comment stopper ses messages sur mes pubs et demandes d'abos ? | talking | choisissez, settings, customis | Customise ai_licia -> Settings : choisis... | 554.0 | api | ✅ |

| La commande Shoutout marche mal avec certains pseudos. Comment écrire les descriptions ? | commands | décrivez, comme, pour | Bien sûr, je peux vous aider ! Décrivez ... | 310.7 | api | ✅ |

| Elle marche en test mais pas en continu en live, comment l'appeler vocalement ? | speak | live, cliquez, speak, ouvrez,  | Bien sûr, je peux vous aider ! Cliquez S... | 335.7 | api | ✅ |

| Je parle dans 'Speak to ai_licia' mais elle ne rejoint pas le chat. | speak | live, cliquez, speak, ouvrez,  | Voici ce que je sais : Hors live : cliqu... | 536.5 | api | ✅ |

| Comment changer alicia de compte tiktok car j'ai été ban 3 jours de mon compte principal ? | ban | plus, simple, pour | Pour un ban de 3 jours, le plus simple s... | 388.2 | api | ✅ |

| Je veux donner un visage vtuber/png à AiLicia mais les programmes n'acceptent que l'entrée micro. Comment faire accepter une source navigateur comme micro ? | vtuber | nous, carte, avons | Bien sûr, je peux vous aider ! Nous avon... | 763.0 | api | ✅ |

| qui t'a programmé | creator | samuel, créé, développeurs | Voici ce que je sais : J'ai été créé par... | 509.7 | api | ✅ |

| qui t'a créé | creator | samuel, créé, développeurs | Voici ce que je sais : J'ai été créé par... | 649.9 | api | ✅ |

| qui est ton créateur | creator | samuel, créé, développeurs | Voici ce que je sais : J'ai été créé par... | 614.3 | api | ✅ |

| Reconnaît-elle qui est mod ? | mod |  | Non.... | 435.2 | api | ❌ |

| es tu vieux | age | programme, suis, donc | Voici ce que je sais : Je suis un progra... | 774.3 | api | ✅ |

| es tu recent | age | programme, suis, donc | Voici ce que je sais : Je suis un progra... | 502.4 | api | ✅ |

| es tu ancien | age | programme, suis, donc | Voici ce que je sais : Je suis un progra... | 481.8 | api | ✅ |

| es tu sage | es_tu_sage | compréhension, implique, sages | Voici ce que je sais : La sagesse impliq... | 696.7 | api | ✅ |

| j'ai besoin d'aide pour configurer AI_licia | j'ai_besoin_d'aide_pour_config | avez, besoin, vous | Bien sûr, je peux vous aider ! Si vous a... | 594.0 | api | ✅ |

| Changer le nom d'Ai_licia ? | name | guide, instructions, compte, c | Créez un nouveau compte avec ce nom puis... | 668.5 | api | ✅ |

| Puis-je changer le nom d'ai_licia sur Twitch ? | name | guide, instructions, compte, c | Voici ce que je sais : Oui ! Guide ici :... | 483.4 | api | ✅ |

| Changer le display name d'Ai_licia sur Twitch ? | name | guide, instructions, compte, c | Page : https://streamer-dashboard.ailici... | 759.5 | api | ✅ |

| Puis je tester ai_licia ? | puis_je_tester_ai_licia_? | avoir, bien, peux | Voici ce que je sais : Bien sûr ! Tu peu... | 559.2 | api | ✅ |

| Qu'est ce que ai_licia? | Ai_licia | premier, compagnon, pour | ai_licia est le premier compagnon IA pou... | 959.0 | api | ✅ |

| Qu'est-ce que ai_licia ? | Ai_licia | premier, compagnon, pour | Voici ce que je sais : ai_licia est le p... | 437.7 | api | ✅ |

| Qu'est-ce que ailicia ? | Ai_licia | premier, compagnon, pour | Voici ce que je sais : ai_licia est le p... | 399.2 | api | ✅ |

| ai_licia est elle uniquement pour Twitch ? | ai_licia_est_elle_uniquement_p | mais, moment, pour | Voici ce que je sais : Pour le moment ou... | 660.6 | api | ✅ |

| Plusieurs ai_licia en même temps ? | multiple | risque, comme, botting | Voici ce que je sais : Non, risque d'êtr... | 529.5 | api | ✅ |

| Puis-je donner un surnom à AI_licia ? | puis-je_donner_un_surnom_à_ai_ | pouvez, choisir, vous | Voici ce que je sais : Oui, vous pouvez ... | 887.7 | api | ✅ |

| Peut-on désactiver ai_licia temporairement ? | disable | haut, bouton, droite | Voici ce que je sais : Il y a un bouton ... | 639.6 | api | ✅ |

| Qu'est-ce qu'ai_licia ? | ai_licia | votre | Voici ce que je sais : ai_licia est votr... | 792.6 | api | ✅ |

| ai_licia est-elle disponible sur Discord ? | discord | nous, rejoignez, travaillons | Nous y travaillons ! Rejoignez la liste ... | 543.4 | api | ✅ |

| Puis-je personnaliser le comportement d'AI_licia ? | puis-je_personnaliser_le_compo | absolument, avez, vous | Absolument ! Vous avez le contrôle total... | 726.4 | api | ✅ |

| Puis-je intégrer AI_licia à mes outils de streaming ? | puis-je_intégrer_ai_licia_à_me | être, peut, intégrée | Voici ce que je sais : Oui, AI_licia peu... | 687.4 | api | ✅ |

| Quels paramètres d'interaction puis-je ajuster pour AI_licia ? | quels_paramètres_d'interaction | pouvez, vous, ajuster | Voici ce que je sais : Vous pouvez ajust... | 1760.7 | api | ✅ |

| À quoi sert la section "Tes Personnages" dans AI_licia ? | à_quoi_sert_la_section_"tes_pe | permet, vous, section | Voici ce que je sais : La section "Tes P... | 887.1 | api | ✅ |

| Je viens d'ajouter ai_licia à mon stream, par où commencer ? | start | nous, avons, vous | Voici ce que je sais : Nous avons ce qu'... | 805.1 | api | ✅ |

| mode Blanc/Light/Dark sur le site AI_licia ? | mode_blanc/light/dark_sur_le_s | mode, changer, permet | Voici ce que je sais : Le mode Light/Dar... | 787.0 | api | ✅ |

| Configurer un compte alt Twitch pour ai_licia lié à mon principal ? | account | ouvrez, lien, token | Voici ce que je sais : Ouvrez le lien de... | 460.4 | api | ✅ |

| Je parle à ai_licia pendant mon stream, mais elle ne semble pas répondre ? | je_parle_à_ai_licia_pendant_mo | toujours, dois, garder | Voici ce que je sais : Tu dois toujours ... | 807.9 | api | ✅ |

| Pour que ai_licia puisse écouter et me répondre quand je suis en live le bouton 'écouter' de l'application doit être toujours activé ? | écouter | page, être, faut | Voici ce que je sais : Oui. Il faut être... | 589.6 | api | ✅ |

| Associer la voix TTS à une mascotte (PNG bouche animée) ? | mascot | dans, avec, plugin | Voici ce que je sais : Oui dans OBS avec... | 720.9 | api | ✅ |

| Est il possible de désactiver le TTS pour certains stream et le réactiver pour d'autres ? | TTS | faire, dois, pouvoir | Voici ce que je sais : Tu dois pouvoir l... | 593.5 | api | ✅ |

| Peut-on lui faire ignorer les récompenses de points, surtout les requêtes TTS ? Ça se chevauche. | points | nous, encore, cette | Voici ce que je sais : Nous n'avons pas ... | 475.6 | api | ✅ |

| Pour les voix doit-on garder le site ouvert ou ajouter à OBS ? | voices | personnage, onglet, dans | Oui via OBS : dans le personnage onglet ... | 70.4 | api | ✅ |

| Elle connaît la catégorie du stream ? | categories | elle, catégorie | Oui elle a l'info de catégorie 😊.... | 979.6 | api | ✅ |

| La faire 'voir' le stream avec Streamlabs ? | see | streamlabs, virtual, utilisez | Voici ce que je sais : Utilisez Streamla... | 1015.6 | api | ✅ |

| Event mode masque la stream knowledge. Est-elle perdue ? | event | mode, simplement, ignorée | Non, simplement ignorée en mode event. R... | 558.1 | api | ✅ |

| Configurer l'outil multi-action avec le plugin Stream Deck ? | stream_deck | installez, plugin, request | Voici ce que je sais : Installez le plug... | 463.0 | api | ✅ |

| Si je lui donne un autre nom dans 'roles' réagira-t-elle à celui-ci ? | roles | carte, fonctionnalité, après | Oui via la fonctionnalité 'surnoms d'ai_... | 700.8 | api | ✅ |


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

- Dégradation détectée : **Oui**


### Détails par niveau de charge

| Charge | Succès | Temps moy. | Throughput | Taux succès |

|--------|--------|------------|------------|-------------|

| 5 req | 5 | 228.1ms | 4.2 req/s | 100.0% |

| 10 req | 10 | 208.8ms | 5.9 req/s | 100.0% |

| 20 req | 20 | 463.1ms | 4.2 req/s | 100.0% |


## 🧠 Utilisation mémoire

- Mémoire initiale : **706.2 MB**

- Mémoire finale : **803.8 MB**

- Augmentation : **97.6 MB**

- Fuite mémoire : **Détectée**

- Taille cache : **2 entrées**


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


## 🏆 Score global : **170/200 (85.0%)**


## 💡 Conseils d'amélioration

- 📈 Optimiser les performances sous charge

- 🧠 Corriger les fuites mémoire détectées

- 🥈 **Très bien !** Qualité production avec quelques améliorations possibles
