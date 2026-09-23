# Complete evaluation review

All 192 original cases remain here and in the original JSON/CSV folders. Choice correctness and free-text quality are different. Empty continuations are retained. This is a public development benchmark.

## starter / untrained

| Case | Category | Status | Expected | Picked | Score | Missing prompt words | Missing choices | Actual free continuation |
|---|---|---|---|---|---:|---|---|---|
| lang_01 | domain_context | scored | service | juice | 0 | none | none | pear professor item doctor course harvest team physician journey checking buyer delivery our report the lecturer item offering and system <UNK> taste recommended payment |
| lang_02 | domain_context | scored | quality | lesson | 0 | none | none | interest with credit traffic bank brand journey consumer risk bond us kitchen juice system in was care patient station patient mango offering discussed banana |
| lang_03 | domain_context | scored | payment | harvest | 0 | none | none | review review compared item during item banana us doctor quality juice code credit pear lecturer we |
| lang_04 | domain_context | scored | juice | juice | 1 | none | none | new was learning software taste discussion report package . design patient review learned instructor deposit design taste traffic program today student shopper recommended mentioned |
| lang_05 | domain_context | scored | journey | journey | 1 | none | none | bicycle discussion learned dentist orange professor instructor and about orange shopper client has treatment new about credit another journey after |
| lang_06 | domain_context | scored | security | student | 0 | none | none | we deposit design train return support buyer lesson question office focused support support learning compared about course they mentioned tutor of treatment therapist fruit |
| lang_07 | domain_context | scored | patient | patient | 1 | none | none | learned during health in interest route report professor ordered important a banana price investment purchase harvest the buyer investment on and compared taste harvest |
| lang_08 | domain_context | scored | lesson | journey | 0 | none | none | teacher report software store recommended banana about apple our yesterday mortgage a and our our student deposit today today <UNK> investment reviewed different treatment |
| lang_09 | domain_place | scored | store | store | 1 | none | none | route tutor helped they care recommended peach health today market product juice train learned car local instructor today credit risk service customer security peach |
| lang_10 | domain_place | scored | market | station | 0 | none | none | important student new learning data office fruit instructor different bank nurse care payment was and juice another juice merchandise a market discussion order offering |
| lang_11 | domain_place | scored | bank | station | 0 | none | none | was program instructor the data question new doctor system yesterday brand payment merchandise mortgage update different truck package return website merchandise care interest school |
| lang_12 | domain_place | scored | kitchen | hospital | 0 | none | none | bus peach about package design selected hospital lesson focused yesterday detail journey local peach learned program returned service traffic station important train bicycle focused |
| lang_13 | domain_place | scored | station | school | 0 | none | none | professor bus product product discussed a understand selected taste course truck journey payment store doctor software bicycle and loan on selected explains update delivery |
| lang_14 | domain_place | scored | office | store | 0 | none | none | harvest focused order course detail lecturer selected reviewed student and lesson a local understand doctor reviewed they report explains detail we today dentist kitchen |
| lang_15 | domain_place | scored | hospital | hospital | 1 | none | none | yesterday different our school review review buyer item team student we focused discussion store apple product detail compared with fruit update patient yesterday was |
| lang_16 | domain_place | scored | school | school | 1 | none | none | customer journey checking application selected peach orange doctor professor credit payment station quality customer care reviewed with brand question discussed discussed truck different risk |
| lang_17 | new_wording | scored | health | health | 1 | none | none | customer order bank taste |
| lang_18 | new_wording | scored | student | risk | 0 | none | none | during brand understand school station merchandise code credit taxi deposit local was program detail yesterday detail apple reviewed understand doctor banana apple learned risk |
| lang_19 | new_wording | scored | return | taste | 0 | none | none | car brand price service software taxi question during we about market merchandise platform bicycle banana with travel return lesson after teacher after after health |
| lang_20 | new_wording | scored | fruit | fruit | 1 | none | none | learned instructor hospital support |
| lang_21 | new_wording | scored | route | lesson | 0 | none | none | customer after dentist ordered bond software they team order bond design about design journey in office office investment helped helped website hospital update juice |
| lang_22 | new_wording | scored | update | update | 1 | none | none | educator website tutor dentist traffic platform store offering offering shopper focused during hospital course in route pear the investment bank peach instructor discussed merchandise |
| lang_23 | new_wording | scored | support | health | 0 | none | none | design update update another pear offering design station bus office car subscriber truck student focused the the care pear the course order us order |
| lang_24 | new_wording | scored | delivery | student | 0 | none | none | tutor doctor today pear focused brand instructor discussion delivery question understand our focused route discussion after bond bank care traffic data report the teacher |
| lang_25 | grammar | out_of_vocabulary | is | None | 0 | bird, one | is, are, were, am | deposit a office car new client we quality selected mango harvest about about student team hospital merchandise client helped harvest discussion professor after discussed |
| lang_26 | grammar | out_of_vocabulary | are | None | 0 | dogs | is, am, are | different on educator peach travel local buyer security design route route peach interest bond helped customer market and taxi report bank code report question |
| lang_27 | grammar | out_of_vocabulary | walked | None | 0 | she | walking, walk, walked, walks | update support buyer nurse offering client quality bank school journey mango truck . website school new store store payment nurse juice apple package taxi |
| lang_28 | opposites | out_of_vocabulary | cold | None | 0 | hot, is, opposite | fast, cold, warm, heavy | return orange detail doctor |
| lang_29 | opposites | out_of_vocabulary | full | None | 0 | empty, is, opposite | full, quiet, early, soft | learning treatment the hospital price a item code we offering report report checking tutor data website lesson system juice a teacher data application purchase |
| lang_30 | opposites | out_of_vocabulary | quiet | None | 0 | is, noisy, opposite | loud, round, late, quiet | journey they detail team teacher return tutor nurse system another harvest about investment mortgage team website taste returned subscriber travel loan kitchen office website |
| lang_31 | negation | out_of_vocabulary | blue | None | 0 | blue, box, is, it, not, red | green, yellow, blue, red | brand payment station surgeon risk bicycle orange brand train bicycle doctor reviewed bond student us important design design another pear review returned patient market |
| lang_32 | negation | out_of_vocabulary | milk | None | 0 | ava, bought, buy, did, milk, not, she, tea | rice, milk, tea, bread | support course client taxi return different travel report explains reviewed train store detail subscriber team <UNK> selected us buyer website return lesson nurse educator |
| lang_33 | negation | out_of_vocabulary | closed | None | 0 | closed, door, is, it, not, open | closed, open, wide, missing | helped tutor customer tutor juice data harvest of item deposit security system with update code at after report selected subscriber investment another hospital question |
| lang_34 | reference | out_of_vocabulary | maya | None | 0 | book, lent, leo, maya, thanked, to | leo, nora, omar, maya | checking review after harvest investment customer travel question mortgage course merchandise yesterday mango of design brand program price our course taste dentist new train |
| lang_35 | reference | out_of_vocabulary | finn | None | 0 | ella, finn, gave, pencil, person, received, who | sara, noah, finn, ella | route another of product mango at detail course station train local instructor return ordered product juice quality support team we team delivery treatment today |
| lang_36 | reference | out_of_vocabulary | omar | None | 0 | answered, call, called, from, nina, omar | emma, omar, nina, luca | care loan taste bicycle surgeon product course surgeon educator of mentioned platform kitchen physician bank today quality bank recommended delivery of dentist apple subscriber |
| lang_37 | sequence | out_of_vocabulary | dry | None | 0 | action, cup, dry, first, is, it, last, then, wash | dry, wash, buy, fill | brand delivery ordered in package after local dentist product client selected system buyer understand today quality learned risk student of traffic car selected platform |
| lang_38 | sequence | out_of_vocabulary | breakfast | None | 0 | breakfast, earlier, happens, is, lunch, meal | lunch, dinner, supper, breakfast | apple package physician understand hospital during nurse platform deposit detail harvest car another dentist treatment was professor bus mentioned after data learned school doctor |
| lang_39 | sequence | out_of_vocabulary | bus | None | 0 | arrived, before, later, that, vehicle | none | merchandise educator care student system kitchen us brand delivery order new about package program code office bond a <UNK> station data system juice local |
| lang_40 | spatial_relations | out_of_vocabulary | book | None | 0 | bag, book, contains, inside, is | lamp, book, shelf, desk | price loan about application physician lesson recommended mortgage bond order on teacher learning shopper shopper . program fruit travel package student application we return |
| lang_41 | spatial_relations | out_of_vocabulary | below | None | 0 | above, desk, is, lamp | below, above, inside, beside | at bank service bank juice selected harvest mango yesterday about loan different during the the hospital has checking recommended they recommended kitchen lecturer journey |
| lang_42 | spatial_relations | out_of_vocabulary | right | None | 0 | ball, box, is, left, to | left, north, south, right | data checking understand lecturer kitchen truck detail bus review credit therapist physician after therapist at educator journey pear journey helped professor route at after |
| lang_43 | everyday_knowledge | out_of_vocabulary | ice | None | 0 | freezes, into, water | sand, wood, ice, steam | bicycle software the on client bus us reviewed compared update us new in local physician update |
| lang_44 | everyday_knowledge | out_of_vocabulary | dry | None | 0 | an, person, stay, to, umbrella, uses | asleep, dry, wet, hungry | recommended mortgage package brand station detail dentist team loan patient doctor checking educator during mango learned taxi important report focused route route security after |
| lang_45 | everyday_knowledge | out_of_vocabulary | light | None | 0 | dark, room, see, to, turn | light, pillow, spoon, shoe | service during tutor yesterday on today client instructor software offering teacher quality juice brand review in was teacher buyer teacher truck mango of mortgage |
| lang_46 | categories_and_analogies | out_of_vocabulary | fish | None | 0 | bird, is, robin, salmon | bird, tree, tool, fish | returned pear credit ordered application dentist harvest mango store train ordered reviewed treatment bus office service ordered juice deposit return tutor |
| lang_47 | categories_and_analogies | out_of_vocabulary | cat | None | 0 | dog, grows, into, kitten, puppy | duck, goat, cat, horse | offering yesterday security on returned application customer train discussed taste they detail |
| lang_48 | categories_and_analogies | out_of_vocabulary | fruit | None | 0 | an, carrot, is, vegetable | fabric, metal, vehicle | detail detail learned car market subscriber mango on of harvest peach apple bond doctor today selected hospital traffic us offering different offering discussion apple |

Failed case IDs: lang_01, lang_02, lang_03, lang_06, lang_08, lang_10, lang_11, lang_12, lang_13, lang_14, lang_18, lang_19, lang_21, lang_23, lang_24, lang_25, lang_26, lang_27, lang_28, lang_29, lang_30, lang_31, lang_32, lang_33, lang_34, lang_35, lang_36, lang_37, lang_38, lang_39, lang_40, lang_41, lang_42, lang_43, lang_44, lang_45, lang_46, lang_47, lang_48.

## starter / final

| Case | Category | Status | Expected | Picked | Score | Missing prompt words | Missing choices | Actual free continuation |
|---|---|---|---|---|---:|---|---|---|
| lang_01 | domain_context | scored | service | service | 1 | none | none | service in detail . |
| lang_02 | domain_context | scored | quality | quality | 1 | none | none | quality in detail . |
| lang_03 | domain_context | scored | payment | payment | 1 | none | none | return in detail . |
| lang_04 | domain_context | scored | juice | juice | 1 | none | none | fruit in detail . |
| lang_05 | domain_context | scored | journey | journey | 1 | none | none | journey in detail . |
| lang_06 | domain_context | scored | security | security | 1 | none | none | security in detail . |
| lang_07 | domain_context | scored | patient | patient | 1 | none | none | treatment in detail . |
| lang_08 | domain_context | scored | lesson | lesson | 1 | none | none | lesson in detail . |
| lang_09 | domain_place | scored | store | store | 1 | none | none | store . |
| lang_10 | domain_place | scored | market | market | 1 | none | none | market . |
| lang_11 | domain_place | scored | bank | bank | 1 | none | none | bank . |
| lang_12 | domain_place | scored | kitchen | kitchen | 1 | none | none | kitchen . |
| lang_13 | domain_place | scored | station | station | 1 | none | none | station . |
| lang_14 | domain_place | scored | office | office | 1 | none | none | office . |
| lang_15 | domain_place | scored | hospital | hospital | 1 | none | none | hospital . |
| lang_16 | domain_place | scored | school | school | 1 | none | none | school . |
| lang_17 | new_wording | scored | health | health | 1 | none | none | health at the hospital . |
| lang_18 | new_wording | scored | student | harvest | 0 | none | none | local lecturer . |
| lang_19 | new_wording | scored | return | care | 0 | none | none | new investment . |
| lang_20 | new_wording | scored | fruit | fruit | 1 | none | none | different pear . |
| lang_21 | new_wording | scored | route | route | 1 | none | none | important taxi . |
| lang_22 | new_wording | scored | update | treatment | 0 | none | none | local website . |
| lang_23 | new_wording | scored | support | health | 0 | none | none | important item . |
| lang_24 | new_wording | scored | delivery | delivery | 1 | none | none | local merchandise . |
| lang_25 | grammar | out_of_vocabulary | is | None | 0 | bird, one | is, are, were, am | the new customer with another client at the store . |
| lang_26 | grammar | out_of_vocabulary | are | None | 0 | dogs | is, am, are | the new educator with another educator at the school . |
| lang_27 | grammar | out_of_vocabulary | walked | None | 0 | she | walking, walk, walked, walks | the new buyer with another client at the store . |
| lang_28 | opposites | out_of_vocabulary | cold | None | 0 | hot, is, opposite | fast, cold, warm, heavy | **[empty response]** |
| lang_29 | opposites | out_of_vocabulary | full | None | 0 | empty, is, opposite | full, quiet, early, soft | **[empty response]** |
| lang_30 | opposites | out_of_vocabulary | quiet | None | 0 | is, noisy, opposite | loud, round, late, quiet | **[empty response]** |
| lang_31 | negation | out_of_vocabulary | blue | None | 0 | blue, box, is, it, not, red | green, yellow, blue, red | **[empty response]** |
| lang_32 | negation | out_of_vocabulary | milk | None | 0 | ava, bought, buy, did, milk, not, she, tea | rice, milk, tea, bread | **[empty response]** |
| lang_33 | negation | out_of_vocabulary | closed | None | 0 | closed, door, is, it, not, open | closed, open, wide, missing | **[empty response]** |
| lang_34 | reference | out_of_vocabulary | maya | None | 0 | book, lent, leo, maya, thanked, to | leo, nora, omar, maya | the station . |
| lang_35 | reference | out_of_vocabulary | finn | None | 0 | ella, finn, gave, pencil, person, received, who | sara, noah, finn, ella | mentioned in the different mango yesterday . |
| lang_36 | reference | out_of_vocabulary | omar | None | 0 | answered, call, called, from, nina, omar | emma, omar, nina, luca | the bank . |
| lang_37 | sequence | out_of_vocabulary | dry | None | 0 | action, cup, dry, first, is, it, last, then, wash | dry, wash, buy, fill | **[empty response]** |
| lang_38 | sequence | out_of_vocabulary | breakfast | None | 0 | breakfast, earlier, happens, is, lunch, meal | lunch, dinner, supper, breakfast | **[empty response]** |
| lang_39 | sequence | out_of_vocabulary | bus | None | 0 | arrived, before, later, that, vehicle | none | new bicycle focused on journey report yesterday . |
| lang_40 | spatial_relations | out_of_vocabulary | book | None | 0 | bag, book, contains, inside, is | lamp, book, shelf, desk | new loan report yesterday . |
| lang_41 | spatial_relations | out_of_vocabulary | below | None | 0 | above, desk, is, lamp | below, above, inside, beside | **[empty response]** |
| lang_42 | spatial_relations | out_of_vocabulary | right | None | 0 | ball, box, is, left, to | left, north, south, right | new banana focused on harvest at the different peach focused on fruit . |
| lang_43 | everyday_knowledge | out_of_vocabulary | ice | None | 0 | freezes, into, water | sand, wood, ice, steam | the new program focused on data and security . |
| lang_44 | everyday_knowledge | out_of_vocabulary | dry | None | 0 | an, person, stay, to, umbrella, uses | asleep, dry, wet, hungry | **[empty response]** |
| lang_45 | everyday_knowledge | out_of_vocabulary | light | None | 0 | dark, room, see, to, turn | light, pillow, spoon, shoe | kitchen . |
| lang_46 | categories_and_analogies | out_of_vocabulary | fish | None | 0 | bird, is, robin, salmon | bird, tree, tool, fish | office . |
| lang_47 | categories_and_analogies | out_of_vocabulary | cat | None | 0 | dog, grows, into, kitten, puppy | duck, goat, cat, horse | bank station focused on traffic helped us understand the different bicycle focused on traffic helped us understand the journey . |
| lang_48 | categories_and_analogies | out_of_vocabulary | fruit | None | 0 | an, carrot, is, vegetable | fabric, metal, vehicle | kitchen . |

Failed case IDs: lang_18, lang_19, lang_22, lang_23, lang_25, lang_26, lang_27, lang_28, lang_29, lang_30, lang_31, lang_32, lang_33, lang_34, lang_35, lang_36, lang_37, lang_38, lang_39, lang_40, lang_41, lang_42, lang_43, lang_44, lang_45, lang_46, lang_47, lang_48.

## expanded / untrained

| Case | Category | Status | Expected | Picked | Score | Missing prompt words | Missing choices | Actual free continuation |
|---|---|---|---|---|---:|---|---|---|
| lang_01 | domain_context | scored | service | traffic | 0 | none | none | harvest garden patient two requires accepted afternoon circle travel incomplete cleaned program food teacher price sell leaf on detail smooth likes hard dirty easily |
| lang_02 | domain_context | scored | quality | quality | 1 | none | none | learned people give other did harvest bridge have class school satisfied its form lamp cleaned local surface full brush opens points visit belong blanket |
| lang_03 | domain_context | scored | payment | route | 0 | none | none | choosing brought warm security return store day cancel doctor item found detail tastes need go helps used brand chose enjoys send its programs satisfied |
| lang_04 | domain_context | scored | juice | code | 0 | none | none | bright form accepted blanket appeared design mean easily strong it print form requires shop ordered blue lecturer longer hour good important last mentioned cars |
| lang_05 | domain_context | scored | journey | journey | 1 | none | none | enter soft visit without does during checks brush carry shopper around box credit purchases one cup blocks interest sell bright to know buy keeps |
| lang_06 | domain_context | scored | security | security | 1 | none | none | plates website prove receive quiet dirty circle days clearly new wet card price accepted program marked releasing ordered delivery closed board bed understand smooth |
| lang_07 | domain_context | scored | patient | traffic | 0 | none | none | needs care truck explains list never needs washing they exchanges report report deposit learning fit its strong soft account loses closed feel long agreed |
| lang_08 | domain_context | scored | lesson | journey | 0 | none | none | helped correct time bought drop team through checks hall larger connection bridge print selected sell adds rejected ended noisy large among hall consumer comes |
| lang_09 | domain_place | scored | store | kitchen | 0 | none | none | neither two around guarantee school large through route places hall accepted explanation cool checking afternoon pear into reading checked blocks bed of time sweet |
| lang_10 | domain_place | scored | market | kitchen | 0 | none | none | bed instead us place becomes has still until application us movement afternoon slow furniture go sheet appointment gives sour correct completed only morning near |
| lang_11 | domain_place | scored | bank | kitchen | 0 | none | none | has know passes washing order draws draws sells accepted already customer condition remains ones holds was dentist interest blue refreshing read patient narrow hard |
| lang_12 | domain_place | scored | kitchen | kitchen | 1 | none | none | understand passes client schedule cannot reports while chair during list question carry hall long enjoys brand classroom checked give bends program mean code class |
| lang_13 | domain_place | scored | station | school | 0 | none | none | discussion sells takes product learning blocks neither arrives taste data only must kitchen need agreed receive nurse mark final when hour sells sour later |
| lang_14 | domain_place | scored | office | bank | 0 | none | none | leaves heat rejected physician chair room short accepted card hall of enter fits service feel question remain print for print hand night early to |
| lang_15 | domain_place | scored | hospital | bank | 0 | none | none | without larger explain damaged during lose beside bicycle carry clearly to alone hall explain bench shelf pears taste misses cups remains larger dark bright |
| lang_16 | domain_place | scored | school | school | 1 | none | none | our larger truck read label satisfied hospital forget offering website line about pear nurse treatment high accepted avoided blocks update picture clearly delete reached |
| lang_17 | new_wording | scored | health | traffic | 0 | none | none | review address tastes day difficult wet system shelf pear belong physician says remain hall apple avoids discussion separate <UNK> taste learned holds sweet lamp |
| lang_18 | new_wording | scored | student | student | 1 | none | none | remained hospital examples far apple misses price accepted explanation paper today just passes orange bag doctor package health classroom print reviewed they dirty smooth |
| lang_19 | new_wording | scored | return | code | 0 | none | none | among took appear purchases table around check wind bond used never examples checking mortgage enough likes contains schedule signal reports keeps failed before paper |
| lang_20 | new_wording | scored | fruit | order | 0 | none | none | never last mentioned reports wind holiday credit says . ends another today gates likes recorded water brush package reviews enjoys belong on than enough |
| lang_21 | new_wording | scored | route | route | 1 | none | none | dentist saves give rooms loses lowers through saves next printed make took complete does empty pears printed nor passes kept client hour fits sweet |
| lang_22 | new_wording | scored | update | journey | 0 | none | none | leaf review day rooms furniture outside outside people station bus examples two different gates damaged recommended school driver other outside agreed credit clean surgeon |
| lang_23 | new_wording | scored | support | traffic | 0 | none | none | releasing completed cannot hangs code surface before new sheet music signal cook days left traffic understand receive <UNK> saved train therapist wind adds soft |
| lang_24 | new_wording | scored | delivery | code | 0 | none | none | entered to tastes of lift desk finished tutor until below reached purchase near office checked sweet agreed outside morning |
| lang_25 | grammar | out_of_vocabulary | is | None | 0 | bird | are, were, am | school file to adds long shop never clearly merchandise dentist appeared health brought avoids bench slow price quality before remain did allows taste far |
| lang_26 | grammar | out_of_vocabulary | are | None | 0 | dogs | am, are | full helps around is find enter did circle sell tastes selected fill visit comes route go error taste us shelf cleans taxi account signal |
| lang_27 | grammar | out_of_vocabulary | walked | None | 0 | she | walking, walk, walked, walks | crowded cleans remained carries bond gives gates asks wind sour continued checks bright give reviewed order appear sweet instead easy make because requested leaf |
| lang_28 | opposites | out_of_vocabulary | cold | None | 0 | hot, opposite | cold | missing asks clearly bench rejected discussed did brought banana discussion payment holiday accepts prove error report purchases sell asks educator tutor purchases rooms path |
| lang_29 | opposites | out_of_vocabulary | full | None | 0 | opposite | none | support consumer fit bends feels noisy rest rest forget hangs sweet local passes decides therapist decides market know blocks platform order hand complete smooth |
| lang_30 | opposites | out_of_vocabulary | quiet | None | 0 | opposite | loud, round | missing lamp purchases market as wide nurse health enters bends mango surgeon already exchanges cool discussion receive empty complete delivery teacher shelf pears farm |
| lang_31 | negation | out_of_vocabulary | blue | None | 0 | red | green, yellow, red | allows explains one comes rest closed places consumer cup strong away rooms until bench client beside compares replace exchanges rough path alone becomes avoids |
| lang_32 | negation | out_of_vocabulary | milk | None | 0 | ava, milk, she, tea | rice, milk, tea, bread | harvest security angry orange helps application interrupts when application review payment ended explain receive mentioned jars rough as one receive practice arrived final contain |
| lang_33 | negation | scored | closed | wide | 0 | none | none | market over consumer picture . miss interrupts furniture feel from night bus compares wind station allows food should health understand change delete loses releasing |
| lang_34 | reference | out_of_vocabulary | maya | None | 0 | lent, leo, maya, thanked | leo, nora, omar, maya | and fit have merchandise today nor examples good good gates high printed lecturer cannot describes investment visit cleaned took sweet lose apple credit instructor |
| lang_35 | reference | out_of_vocabulary | finn | None | 0 | ella, finn, gave, pencil, person, received, who | sara, noah, finn, ella | order chooses night subscriber becomes noon us fast examples surface removed bicycle travel job without final wide wide reached opens angry checked error requested |
| lang_36 | reference | out_of_vocabulary | omar | None | 0 | answered, call, called, nina, omar | emma, omar, nina, luca | reached juice learning puts lift should route orange crowded takes below refreshing holiday rooms high recorded so hand farm empty among bed during drips |
| lang_37 | sequence | out_of_vocabulary | dry | None | 0 | action, first, then, wash | wash | allows therapist shopper unpaid farm exchanges working clean chooses banana care morning day go sells high us bag yesterday contains of adds heat subscriber |
| lang_38 | sequence | out_of_vocabulary | breakfast | None | 0 | breakfast, earlier, happens, lunch, meal | lunch, dinner, supper, breakfast | account appear purchases lamp line strong today there need desk enters floor until change in package requires feels yesterday and nurse wide physician box |
| lang_39 | sequence | out_of_vocabulary | bus | None | 0 | vehicle | none | low has to receipt remained cups replace tastes feels damaged misses cloth decides larger with points decides discussion a website accepted sour journey long |
| lang_40 | spatial_relations | scored | book | shelf | 0 | none | none | floor with returned buyer truck cleaned dirty remained drips calls discussion merchandise above appointment inside blue crowded receipt printed course marked is different ends |
| lang_41 | spatial_relations | scored | below | beside | 0 | none | none | adds while window page used us calls window afternoon bicycle available angry unfinished code nor so strong reaches larger says water |
| lang_42 | spatial_relations | out_of_vocabulary | right | None | 0 | ball | north, south, right | draws ones subscriber barely outside refused helped bridge hour just today go security about cart quality noon remained classroom discussion longer delivery window difficult |
| lang_43 | everyday_knowledge | out_of_vocabulary | ice | None | 0 | freezes | sand, wood, ice, steam | ready bends apple makes contains station follows requires tutor was print bright holds releasing therapist cars into away label noisy forget left every cloth |
| lang_44 | everyday_knowledge | out_of_vocabulary | dry | None | 0 | person, stay, umbrella, uses | asleep, hungry | checked so likes sells interest know final avoided prove focused mango angry loses buyer narrow error bed receive correct complete unfinished hangs drop narrow |
| lang_45 | everyday_knowledge | out_of_vocabulary | light | None | 0 | see, turn | spoon, shoe | remain lose store taxi purchases delete last cleans contained therapist juice software lecturer wet and card appear followed apples draws narrow lose time ones |
| lang_46 | categories_and_analogies | out_of_vocabulary | fish | None | 0 | bird, robin, salmon | bird, tree, tool, fish | chooses over reviewed blocks never mark outside low quality juice that of subscriber entered room should long miss other moving delete morning payment exchanges |
| lang_47 | categories_and_analogies | out_of_vocabulary | cat | None | 0 | dog, grows, kitten, puppy | duck, goat, cat, horse | brush strong class chose subscriber comes closed is leave health train likes treatment explains wind return box same path below soft arrived pears followed |
| lang_48 | categories_and_analogies | out_of_vocabulary | fruit | None | 0 | carrot, vegetable | fabric, metal, vehicle | nurse choosing rooms comes error finishes sells outside next purchase is choosing object receipt team nor at empty long purchase lose cart drop enough |

Failed case IDs: lang_01, lang_03, lang_04, lang_07, lang_08, lang_09, lang_10, lang_11, lang_13, lang_14, lang_15, lang_17, lang_19, lang_20, lang_22, lang_23, lang_24, lang_25, lang_26, lang_27, lang_28, lang_29, lang_30, lang_31, lang_32, lang_33, lang_34, lang_35, lang_36, lang_37, lang_38, lang_39, lang_40, lang_41, lang_42, lang_43, lang_44, lang_45, lang_46, lang_47, lang_48.

## expanded / final

| Case | Category | Status | Expected | Picked | Score | Missing prompt words | Missing choices | Actual free continuation |
|---|---|---|---|---|---:|---|---|---|
| lang_01 | domain_context | scored | service | service | 1 | none | none | purchase in detail . |
| lang_02 | domain_context | scored | quality | quality | 1 | none | none | delivery in detail . |
| lang_03 | domain_context | scored | payment | payment | 1 | none | none | interest in detail . |
| lang_04 | domain_context | scored | juice | juice | 1 | none | none | fruit in detail . |
| lang_05 | domain_context | scored | journey | journey | 1 | none | none | journey in detail . |
| lang_06 | domain_context | scored | security | security | 1 | none | none | code in detail . |
| lang_07 | domain_context | scored | patient | patient | 1 | none | none | health in detail . |
| lang_08 | domain_context | scored | lesson | lesson | 1 | none | none | lesson in detail . |
| lang_09 | domain_place | scored | store | store | 1 | none | none | store . |
| lang_10 | domain_place | scored | market | market | 1 | none | none | market . |
| lang_11 | domain_place | scored | bank | bank | 1 | none | none | bank . |
| lang_12 | domain_place | scored | kitchen | kitchen | 1 | none | none | kitchen . |
| lang_13 | domain_place | scored | station | station | 1 | none | none | station . |
| lang_14 | domain_place | scored | office | office | 1 | none | none | office . |
| lang_15 | domain_place | scored | hospital | hospital | 1 | none | none | hospital . |
| lang_16 | domain_place | scored | school | school | 1 | none | none | school . |
| lang_17 | new_wording | scored | health | health | 1 | none | none | patient at the hospital . |
| lang_18 | new_wording | scored | student | student | 1 | none | none | student hospital has far . |
| lang_19 | new_wording | scored | return | return | 1 | none | none | payment . |
| lang_20 | new_wording | scored | fruit | fruit | 1 | none | none | new pear . |
| lang_21 | new_wording | scored | route | route | 1 | none | none | dentist to a nurse with two . |
| lang_22 | new_wording | scored | update | update | 1 | none | none | small office has kept . |
| lang_23 | new_wording | scored | support | support | 1 | none | none | support treatment . |
| lang_24 | new_wording | scored | delivery | delivery | 1 | none | none | price . |
| lang_25 | grammar | out_of_vocabulary | is | None | 0 | bird | are, were, am | bag does not understand the shop never <UNK> the dirty cup . |
| lang_26 | grammar | out_of_vocabulary | are | None | 0 | dogs | am, are | full signal appointment to an . |
| lang_27 | grammar | out_of_vocabulary | walked | None | 0 | she | walking, walk, walked, walks | is not remained while the hard price is on the update . |
| lang_28 | opposites | out_of_vocabulary | cold | None | 0 | hot, opposite | cold | missing when the new platform . |
| lang_29 | opposites | out_of_vocabulary | full | None | 0 | opposite | none | ready taste but the new application rest . |
| lang_30 | opposites | out_of_vocabulary | quiet | None | 0 | opposite | loud, round | missing security from the working update . |
| lang_31 | negation | out_of_vocabulary | blue | None | 0 | red | green, yellow, red | allows . |
| lang_32 | negation | out_of_vocabulary | milk | None | 0 | ava, milk, she, tea | rice, milk, tea, bread | . |
| lang_33 | negation | scored | closed | closed | 1 | none | none | market . |
| lang_34 | reference | out_of_vocabulary | maya | None | 0 | lent, leo, maya, thanked | leo, nora, omar, maya | for the station . |
| lang_35 | reference | out_of_vocabulary | finn | None | 0 | ella, finn, gave, pencil, person, received, who | sara, noah, finn, ella | class . |
| lang_36 | reference | out_of_vocabulary | omar | None | 0 | answered, call, called, nina, omar | emma, omar, nina, luca | an early bag . |
| lang_37 | sequence | out_of_vocabulary | dry | None | 0 | action, first, then, wash | wash | easy . |
| lang_38 | sequence | out_of_vocabulary | breakfast | None | 0 | breakfast, earlier, happens, lunch, meal | lunch, dinner, supper, breakfast | dirty fruit . |
| lang_39 | sequence | out_of_vocabulary | bus | None | 0 | vehicle | none | station . |
| lang_40 | spatial_relations | scored | book | book | 1 | none | none | table . |
| lang_41 | spatial_relations | scored | below | inside | 0 | none | none | bag . |
| lang_42 | spatial_relations | out_of_vocabulary | right | None | 0 | ball | north, south, right | different peach . |
| lang_43 | everyday_knowledge | out_of_vocabulary | ice | None | 0 | freezes | sand, wood, ice, steam | the far apple while the station two requires inside . |
| lang_44 | everyday_knowledge | out_of_vocabulary | dry | None | 0 | person, stay, umbrella, uses | asleep, hungry | while the basket . |
| lang_45 | everyday_knowledge | out_of_vocabulary | light | None | 0 | see, turn | spoon, shoe | narrow lose . |
| lang_46 | categories_and_analogies | out_of_vocabulary | fish | None | 0 | bird, robin, salmon | bird, tree, tool, fish | review . |
| lang_47 | categories_and_analogies | out_of_vocabulary | cat | None | 0 | dog, grows, kitten, puppy | duck, goat, cat, horse | wide . |
| lang_48 | categories_and_analogies | out_of_vocabulary | fruit | None | 0 | carrot, vegetable | fabric, metal, vehicle | review . |

Failed case IDs: lang_25, lang_26, lang_27, lang_28, lang_29, lang_30, lang_31, lang_32, lang_34, lang_35, lang_36, lang_37, lang_38, lang_39, lang_41, lang_42, lang_43, lang_44, lang_45, lang_46, lang_47, lang_48.
