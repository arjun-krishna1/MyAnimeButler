from flask import *
import os
import cluster

app = Flask(__name__)

with open("anime_name_key_anime_id_value1.json") as f:
    anime_names = json.loads(f.read())

with open("anime_id_key_anime_name_value.json") as f:
    anime_id_to_names = json.loads(f.read())
history = []
anime_choices = ['Cowboy Bebop', 'Trigun', 'Witch Hunter Robin', 'Beet the Vandel Buster', 'Eyeshield 21',
                 'Hachimitsu to Clover', 'Hungry Heart: Wild Striker', 'Initial D Fourth Stage', 'Monster', 'Naruto',
                 'One Piece', 'Prince of Tennis', 'Ring ni Kakero 1', 'School Rumble', 'Sunabouzu', 'Texhnolyze',
                 'Trinity Blood', 'Yakitate!! Japan', 'Zipang', 'Neon Genesis Evangelion', 'Berserk',
                 'Rurouni Kenshin: Meiji Kenkaku Romantan', '.hack//Sign', 'Aa! Megami-sama! (TV)',
                 'Kidou Tenshi Angelic Layer', 'Ai Yori Aoshi', 'Arc the Lad', 'Avenger', 'Beck', 'Blue Gender',
                 'Chobits', 'Chrno Crusade', 'D.N.Angel', 'D.C.: Da Capo', 'DearS', 'Rozen Maiden',
                 'Rozen Maiden: Träumend', 'Azumanga Daioh', 'Basilisk: Kouga Ninpou Chou', 'Black Cat', 'Cluster Edge',
                 'Full Metal Panic!', 'Full Metal Panic? Fumoffu', 'Full Metal Panic! The Second Raid', 'Gakuen Alice',
                 'Soukyuu no Fafner: Dead Aggressor', 'Mahou Shoujo Lyrical Nanoha',
                 'Mahou Shoujo Lyrical Nanoha A&#039;s', 'Shuffle!', 'Mobile Suit Gundam', 'Mobile Suit Zeta Gundam',
                 'Mobile Suit Gundam ZZ', 'Mobile Suit Victory Gundam', 'Mobile Suit Gundam Wing', 'After War Gundam X',
                 'Mobile Suit Gundam Seed', 'Mobile Suit Gundam Seed Destiny', 'Turn A Gundam',
                 'Mobile Fighter G Gundam', 'Last Exile', 'Mai-HiME', 'Mai-Otome',
                 'Shin Shirayuki-hime Densetsu Prétear', 'Air', 'Aishiteruze Baby★★', 'Akazukin Chacha',
                 'Ayashi no Ceres', 'Boys Be...', 'Hana yori Dango', 'Ou Dorobou Jing', 'Bakuretsu Tenshi',
                 'Chuuka Ichiban!', 'Corrector Yui', 'Chou Henshin Cosprayers', 'Uchuu no Stellvia',
                 'Sakigake!! Cromartie Koukou', 'El Hazard: The Alternative World', 'El Hazard: The Wanderers',
                 'Final Approach', 'Fruits Basket', 'Fullmetal Alchemist', 'Full Moon wo Sagashite', 'Fushigi Yuugi',
                 'Futakoi', 'Futakoi Alternative', 'Gate Keepers', 'Gensoumaden Saiyuuki', 'Saiyuuki Reload',
                 'Saiyuuki Reload Gunlock', 'GetBackers', 'Green Green', 'Gunslinger Girl', 'Hikaru no Go',
                 'Hunter x Hunter', 'Jinki:Extend', 'Kamikaze Kaitou Jeanne', 'Kannazuki no Miko', 'Kanon',
                 'Kareshi Kanojo no Jijou', 'Kono Minikuku mo Utsukushii Sekai', 'Kimi ga Nozomu Eien',
                 'Kita e.: Diamond Dust Drops', 'Loveless', 'Blood+', 'Solty Rei', 'Juuni Kokuki', 'Shaman King', 'X',
                 'Mahou Sensei Negima!', 'Maria-sama ga Miteru', 'Boukyaku no Senritsu', 'Ima, Soko ni Iru Boku',
                 'Peace Maker Kurogane', 'Pita Ten', 'Power Stone', 'RahXephon', 'Samurai 7', 'Scrapped Princess',
                 's.CRY.ed', 'Shingetsutan Tsukihime', 'Slam Dunk', 'Strange Dawn', 'Tactics', 'Tenjou Tenge',
                 'Tokyo Underground', 'Tsubasa Chronicle', 'Ultra Maniac', 'Vandread', 'Vandread: The Second Stage',
                 'Tenkuu no Escaflowne', 'Whistle!', 'Xenosaga The Animation', 'Initial D First Stage',
                 'Initial D Second Stage', 'Love Hina', 'Maburaho', 'Onegai☆Teacher', 'Onegai☆Twins', 'Rizelmine',
                 'Speed Grapher', 'Tenshi na Konamaiki', 'Wolf&#039;s Rain', 'Yumeria', 'Samurai Champloo',
                 'Lodoss-tou Senki: Eiyuu Kishi Den', 'R.O.D the TV', 'Ranma ½', 'Kidou Senkan Nadesico', 'Mezzo DSA',
                 'Dragon Ball', 'Dragon Ball GT', 'Elfen Lied', 'Jigoku Shoujo', 'Ninin ga Shinobuden', 'Air Master',
                 'Asagiri no Miko', 'Cardcaptor Sakura', 'Daa! Daa! Daa!', 'Dan Doh!!', 'Detective Conan',
                 'E&#039;s Otherwise', 'Eureka Seven', 'Rekka no Honoo', 'Gankutsuou', 'Genshiken',
                 'Girls Bravo: First Season', 'Gokusen', 'Gravitation', 'Agatha Christie no Meitantei Poirot to Marple',
                 'Great Teacher Onizuka', 'Groove Adventure Rave', 'Harukanaru Toki no Naka de: Hachiyou Shou',
                 'Ichigo 100%', 'InuYasha', 'Konjiki no Gash Bell!!', 'Kyou kara Maou!', 'Madlax',
                 'Jungle wa Itsumo Hare nochi Guu', 'Ikkitousen', 'Happy☆Lesson (TV)', 'Happy☆Lesson: Advance',
                 'Hajime no Ippo', 'Gunparade March: Arata Naru Kougunka', 'Gungrave', 'Bleach', 'Hellsing',
                 'Gad Guard', 'Noir', 'Mahoutsukai ni Taisetsu na Koto', 'Kiddy Grade', 'Love♥Love?',
                 'Mahoromatic: Automatic Maiden', 'Mahoromatic 2', 'Viewtiful Joe',
                 'Kyougoku Natsuhiko: Kousetsu Hyaku Monogatari', 'Animal Yokochou', 'Angel Heart', 'Akage no Anne',
                 'Area 88 (TV)', 'Argento Soma', 'B&#039;T X', 'Grappler Baki (TV)', 'Bakuten Shoot Beyblade',
                 'Comic Party', 'Seikai no Monshou', 'D.C.S.S: Da Capo Second Season', 'Dear Boys', 'Di Gi Charat',
                 'Divergence Eve', 'Divergence Eve 2: Misaki Chronicles', 'Dragon Drive',
                 'Grenadier: Hohoemi no Senshi', '.hack//Tasogare no Udewa Densetsu', 'Cinderella Boy',
                 'Mirai Shounen Conan', 'Aa! Megami-sama!: Chichaitte Koto wa Benri da ne',
                 'Abenobashi Mahou☆Shoutengai', 'Kerokko Demetan', 'Zettai Shounen', 'Akahori Gedou Hour Rabuge',
                 'Chiisana Obake Acchi, Kocchi, Socchi', 'Ace wo Nerae!', 'Hand Maid May', 'Najica Dengeki Sakusen',
                 'Paradise Kiss', 'Mousou Dairinin', 'Mobile Police Patlabor: On Television', 'Peach Girl',
                 'Petshop of Horrors', 'Puchi Puri Yuushi', 'Piano', 'Planetes', 'Midori no Hibi', 'Mahoujin Guru Guru',
                 'Dokidoki Densetsu: Mahoujin Guru Guru', 'Mama wa Shougaku 4 Nensei', 'Marmalade Boy',
                 'Matantei Loki Ragnarok', 'Ginyuu Mokushiroku Meine Liebe', 'Psychic Academy', 'Rose of Versailles',
                 'Serial Experiments Lain', 'Mutsu Enmei Ryuu Gaiden: Shura no Toki', 'Spiral: Suiri no Kizuna',
                 'Starship Operators', 'Tsukuyomi: Moon Phase', 'Futatsu no Spica', 'Eikoku Koi Monogatari Emma',
                 'W: Wish', 'Wild Arms: Twilight Venom', 'Binzume Yousei', 'Magical Canan', 'Ojamajo Doremi',
                 'Ojamajo Doremi Sharp', 'Motto! Ojamajo Doremi', 'Ojamajo Doremi Dokkaan!', 'UG☆Ultimate Girls',
                 'Shakugan no Shana', 'Fate/stay night', 'Himiko-den', 'Gallery Fake',
                 'Boogiepop wa Warawanai: Boogiepop Phantom', 'Burn Up Excess', 'Bannou Bunka Neko-Musume (1998)',
                 'Heppoko Jikken Animation Excel♥Saga', 'Galaxy Angel', 'Gantz', 'Gilgamesh', 'H2', 'Haibane Renmei',
                 'Capeta', 'Suzuka', 'Yuu☆Yuu☆Hakusho', 'Ai Yori Aoshi: Enishi', 'Gantz 2nd Stage', 'Seikai no Senki',
                 'Seikai no Senki II', 'Seihou Bukyou Outlaw Star', 'Hanaukyou Maid-tai', 'Buzzer Beater',
                 'Tantei Gakuen Q', 'Gun x Sword', 'Kore ga Watashi no Goshujinsama', 'Ragnarök the Animation',
                 'Samurai Deeper Kyou', 'Stratos 4', 'Dirty Pair', 'Kaleido Star', 'Magic Knight Rayearth',
                 'Shoujo Kakumei Utena', 'Maria-sama ga Miteru: Haru', 'Tales of Eternia The Animation',
                 'Weiß Kreuz Glühen', 'Weiß Kreuz', 'Fantastic Children', 'Gokujou Seitokai', 'Mushishi',
                 'Ghost in the Shell: Stand Alone Complex', 'Karin', 'Okusama wa Joshikousei (TV)', 'To Heart 2',
                 'To Heart', 'Tide-Line Blue', 'Ginban Kaleidoscope', 'Aria The Animation', 'Sousei no Aquarion',
                 'The Law of Ueki', 'Yu☆Gi☆Oh! Duel Monsters', 'Yu☆Gi☆Oh!: Duel Monsters GX', 'Kurau Phantom Memory',
                 'Damekko Doubutsu', 'Kino no Tabi: The Beautiful World', 'Girls Bravo: Second Season',
                 'Ichigo Mashimaro', 'Kamichu!', 'Paniponi Dash!', 'Bakuretsu Hunters',
                 'Yami to Boushi to Hon no Tabibito', 'Doraemon', 'Fushigiboshi no☆Futagohime', 'Glass no Kamen',
                 'Tottoko Hamtarou', 'I My Me! Strawberry Eggs', 'Kakyuusei 2: Hitomi no Naka no Shoujo-tachi',
                 'Kidou Shinsengumi Moeyo Ken TV', 'Keroro Gunsou', 'Mahou no Princess Minky Momo',
                 'Mahoraba: Heartful days', 'Mermaid Melody Pichi Pichi Pitch', 'Otogizoushi', 'Pokemon',
                 'Saishuu Heiki Kanojo', 'Bishoujo Senshi Sailor Moon', 'Bishoujo Senshi Sailor Moon S',
                 'Sensei no Ojikan: Doki Doki School Hours', 'Slayers', 'Slayers Next', 'Shin Tenchi Muyou!',
                 'Mousou Kagaku Series: Wandaba Style', 'Wind: A Breath of Heart (TV)', 'Yu☆Gi☆Oh!',
                 'Grappler Baki: Saidai Tournament-hen', 'Digimon Adventure', 'Yami no Matsuei',
                 'Koutetsu Tenshi Kurumi', 'Koutetsu Tenshi Kurumi 2', 'Major S2', 'Sakura Taisen', 'DNA²', 'The Big O',
                 'Bubblegum Crisis Tokyo 2040', 'Musekinin Kanchou Tylor', 'Saber Marionette J', 'Magikano',
                 'Kagihime Monogatari Eikyuu Alice Rinbukyoku', 'Battle Programmer Shirase', 'Kogepan',
                 'Sexy Commando Gaiden: Sugoiyo!! Masaru-san', 'Noein: Mou Hitori no Kimi e',
                 'Ayakashi: Japanese Classic Horror', 'Hanbun no Tsuki ga Noboru Sora', 'Ginga Nagareboshi Gin',
                 'Kage kara Mamoru!', 'Amaenaide yo!!', 'PopoloCrois', 'Mugen no Ryvius',
                 'Jinzou Ningen Kikaider The Animation', 'Legend of Duo', 'Futari wa Precure',
                 'Mahou no Stage Fancy Lala', 'Tenshi ni Narumon!', 'Kazemakase Tsukikage Ran', 'Otogi Juushi Akazukin',
                 'Popotan', 'Platonic Chain', 'PetoPeto-san', 'Onmyou Taisenki', 'Okusama wa Mahou Shoujo',
                 'Nurse Angel Ririka SOS', 'Juubee Ninpuuchou: Ryuuhougyoku-hen', 'Mermaid Forest',
                 'Night Walker: Mayonaka no Tantei', 'Shichinin no Nana', 'Mouse', 'Mamotte Shugogetten!', 'Major S1',
                 'Mahoutsukai Tai!', 'Legend of Basara', 'Koi Kaze', 'Juubee-chan: Lovely Gantai no Himitsu',
                 'Juubee-chan 2: Siberia Yagyuu no Gyakushuu', 'Iketeru Futari', 'Haunted Junction',
                 'Tsuki wa Higashi ni Hi wa Nishi ni: Operation Sanctuary', 'Hanaukyou Maid-tai: La Verite',
                 'Galaxy Angel Z', 'Galaxy Angel 3', 'Galaxy Angel 4', 'Touhai Densetsu Akagi: Yami ni Maiorita Tensai',
                 'Kashimashi: Girl Meets Girl', 'Koi Koi 7', 'Lamune', 'Lemon Angel Project', 'Sentimental Journey',
                 'Shadow Skill: Eigi', 'Otogi Story Tenshi no Shippo', 'Tenshi no Shippo Chu!',
                 'To Heart: Remember My Memories', 'Tokyo Mew Mew', 'Uta Kata', 'Kyuuketsuhime Miyu (TV)', 'Yawara!',
                 'Burn Up Scramble', 'Canvas 2: Niji-iro no Sketch', 'Tenchi Muyou!', 'Comic Party Revolution',
                 'Patapata Hikousen no Bouken', 'Mujin Wakusei Survive', 'Rec', 'Zoids Genesis',
                 'High School! Kimengumi', 'Yume de Aetara (TV)', 'Princess Tutu', 'Kingyo Chuuihou!',
                 'Hiatari Ryoukou!', 'MÄR', 'Bishoujo Senshi Sailor Moon R', 'Trouble Chocolate', 'Nanami-chan',
                 'Binchou-tan', 'Bomberman Jetters', 'Yuki no Joou', 'Zoids', 'Zoids Shinseiki/Zero',
                 'Ginyuu Mokushiroku Meine Liebe Wieder', 'Nanaka 6/17', 'Gasaraki', 'Miami Guns', 'Pugyuru',
                 'Shinigami no Ballad.', 'Ergo Proxy', 'Oniisama e...', 'Yomigaeru Sora: Rescue Wings',
                 'Kokoro Toshokan', 'NieA Under 7', 'Ghost in the Shell: Stand Alone Complex 2nd GIG',
                 'Android Ana Maico 2010', 'Chikyuu Shoujo Arjuna', 'Dragon Ball Z', 'Tactical Roar',
                 'Chicchana Yukitsukai Sugar', 'Ginsoukikou Ordian', 'Choujuushin Gravion', 'Sister Princess: Re Pure',
                 'Sister Princess', 'Narutaru: Mukuro Naru Hoshi Tama Taru Ko', 'Narue no Sekai', 'Colorful', 'Kiba',
                 'School Rumble Ni Gakki', 'Suzumiya Haruhi no Yuuutsu', 'Gakuen Heaven', 'Gokinjo Monogatari',
                 'Ouran Koukou Host Club', 'Soul Link', 'Strawberry Panic', 'Utawarerumono', 'Air Gear',
                 'Gunparade Orchestra', 'Digimon Savers', 'Makai Senki Disgaea', 'xxxHOLiC',
                 'Joshikousei: Girl&#039;s High', 'Kikou Senki Dragonar', 'Mahou Shoujo-tai Arusu', '.hack//Roots',
                 'Digimon Tamers', 'Street Fighter II V', 'Nana', 'Zegapain', 'Simoun',
                 'Aa! Megami-sama!: Sorezore no Tsubasa', 'Amaenaide yo!! Katsu!!', 'Megami Kouhosei', 'Black Lagoon',
                 'Yuusha-Ou GaoGaiGar', 'Princess Princess', 'Geneshaft', 'Himawari!', 'Ninku', 'Kakutou Bijin Wulong',
                 'Ike! Ina-chuu Takkyuubu', 'Ginga Densetsu Weed', 'Tokkou', 'Gintama', 'Ray The Animation',
                 'Transformers: Choujin Master Force', 'Transformers Headmasters', 'Transformers Victory',
                 'Transformers Superlink', 'Transformers Galaxy Force', 'Aura Battler Dunbine', 'Densetsu Kyojin Ideon',
                 'Higurashi no Naku Koro ni', 'Witchblade', 'Inukami!', 'Renkin San-kyuu Magical? Pokaan',
                 'Nishi no Yoki Majo: Astraea Testament', 'Yume Tsukai', 'The Third: Aoi Hitomi no Shoujo',
                 'Chibi Maruko-chan', 'Magical Nyan Nyan Taruto', 'Jyu Oh Sei', 'Daikuu Maryuu Gaiking',
                 'Saiunkoku Monogatari', 'HeatGuy J', 'Shin Chou Kyou Ryo: Condor Hero',
                 'Shin Chou Kyou Ryo: Condor Hero II', 'Virtua Fighter', 'Aria The Natural', 'Hit wo Nerae!',
                 'Yoshinaga-san&#039;chi no Gargoyle', 'Crayon Shin-chan', 'Hokuto no Ken',
                 'Kakutou Bijin Wulong: Rebirth', 'Tsubasa Chronicle 2nd Season', 'Yokoyama Mitsuteru Sangokushi',
                 'Astro Boy: Tetsuwan Atom', 'Glass no Kantai: La Legende du Vent de l&#039;Univers',
                 'Rikujou Bouei-tai Mao-chan', 'Shinshaku Sengoku Eiyuu Densetsu: Sanada Juu Yuushi The Animation',
                 'Kamisama Kazoku', 'Dual Parallel! Trouble Adventures', 'Bishoujo Senshi Sailor Moon: Sailor Stars',
                 'Blue Seed', 'Uchuu Kaizoku Captain Harlock', 'Star Ocean EX', 'Le Chevalier D&#039;Eon',
                 'Majutsushi Orphen', 'Majutsushi Orphen: Revenge', 'Honoo no Mirage', 'Kaikan Phrase',
                 'Generator Gawl', 'Kachou Ouji', 'Patalliro Saiyuuki!', 'Saint Beast: Seijuu Kourin-hen',
                 'Mizuiro Jidai', 'Elf wo Karu Mono-tachi', 'Elf wo Karu Mono-tachi II', 'The SoulTaker: Tamashii-gari',
                 'Bobobo-bo Bo-bobo', 'Ippatsu Kiki Musume', 'Oruchuban Ebichu', 'Nekojiru Gekijou Jirujiru Original',
                 'Touch', 'Kishin Houkou Demonbane (TV)', 'Chou Denji Robo Combattler V', 'Chou Denji Machine Voltes V',
                 'Love Get Chu', 'Hikari to Mizu no Daphne', 'Human Crossing', 'Kenran Butou Sai: The Mars Daybreak',
                 'Kimagure Orange☆Road', 'Macross', 'Oishinbo', 'Lime-iro Senkitan',
                 'Samurai Girl Real Bout High School', 'Shinkon Gattai Godannar!!',
                 'Shinkon Gattai Godannar!! 2nd Season', 'Senkaiden Houshin Engi',
                 'Mermaid Melody Pichi Pichi Pitch Pure', 'Beet the Vandel Buster Excellion',
                 'Figure 17: Tsubasa &amp; Hikaru', 'UFO Princess Valkyrie',
                 'UFO Princess Valkyrie 2: Juunigatsu no Yasoukyoku', 'Digimon Frontier', 'Tenchi Muyou! GXP',
                 'Betterman', 'Mushrambo', 'Medarot', 'Monkey Magic', 'Hachimitsu to Clover II', 'Kaze no Youjinbou',
                 'Choujuushin Gravion Zwei', 'I: Wish You Were Here', 'Final Fantasy: Unlimited',
                 'Maze☆Bakunetsu Jikuu (TV)', 'Neo Ranga', 'Mahou Senshi Louie', 'Samurai Gun', 'Slayers Try',
                 'Metal Fighter Miku', 'Gakuen Senki Muryou', 'Hyper Police', 'Lost Universe',
                 'Battle Athletess Daiundoukai (TV)', 'Momoiro Sisters', 'Eden&#039;s Bowy',
                 'Happy Seven: The TV Manga', 'Coyote Ragtime Show', 'Zero no Tsukaima',
                 'Masuda Kousuke Gekijou Gag Manga Biyori', 'Tsuyokiss', 'Nintama Rantarou', 'Gun-dou Musashi',
                 'NHK ni Youkoso!', 'Oban Star-Racers', 'Binbou Shimai Monogatari', 'Tonagura!', 'Chocotto Sister',
                 'Demashita! Powerpuff Girls Z', 'Bokura ga Ita', 'Aquarian Age: Sign for Evolution',
                 'Seihou Tenshi Angel Links', 'Innocent Venus', 'Saber Marionette J to X', 'SF Saiyuuki Starzinger',
                 'Bishoujo Senshi Sailor Moon SuperS', 'Night Head Genesis', 'Yuugo: Koushounin',
                 'Project BLUE Chikyuu SOS', 'Zone of the Enders: Dolores, I', 'Erementar Gerad',
                 'Fushigi no Umi no Nadia', 'Saint Seiya', 'Kyattou Ninden Teyandee', 'Yoroiden Samurai Troopers',
                 'Taiyou no Ko Esteban', 'Gakkou no Kaidan', 'Afro Samurai', 'Urusei Yatsura',
                 'Omishi Mahou Gekijou: Risky/Safety', 'Chikyuu Bouei Kigyou Dai-Guard', 'Digimon Adventure 02',
                 'DT Eightron', 'Idaten Jump', 'Hamelin no Violin Hiki', 'Aoki Densetsu Shoot!',
                 'Fushigi na Koala Blinky', 'Dororon Enma-kun', 'A.D. Police (TV)', 'Hokuto no Ken 2', 'Hi no Tori',
                 'Taiho Shichau zo (1996)', 'Kyoushoku Soukou Guyver (2005)', 'Watashi no Ashinaga Ojisan',
                 'Uchuu Koukyoushi Maetel: Ginga Tetsudou 999 Gaiden', 'Future GPX Cyber Formula', 'Macross 7',
                 'IGPX: Immortal Grand Prix', 'IGPX: Immortal Grand Prix (2005) 2nd Season', 'Lupin III',
                 'Lupin III: Part II', 'Lupin III: Part III', 'Alexander Senki', 'Mach GoGoGo', 'Hyakujuu-Ou GoLion',
                 'Brigadoon: Marin to Melan', 'Maison Ikkoku', 'Kemonozume', 'L/R: Licensed by Royal',
                 'Uchuu no Kishi Tekkaman', 'Uchuu no Kishi Tekkaman Blade', 'Hakaima Sadamitsu', 'Hakugei Densetsu',
                 'Monster Farm: Enbanseki no Himitsu', 'City Hunter', 'City Hunter 2', 'City Hunter 3',
                 'City Hunter &#039;91', 'D.Gray-man', 'Master Keaton', 'Akachan to Boku', 'Kodomo no Omocha (TV)',
                 'Ginga Tetsudou Monogatari', 'Ginga Tetsudou 999', 'Project ARMS', 'Project ARMS: The 2nd Chapter',
                 'Black Blood Brothers', 'Mahou Shoujo Pretty Sammy (1996)', 'Sci-fi Harry', 'Mamotte! Lollipop',
                 'Kirarin☆Revolution', 'Silent Mobius', 'Black Lagoon: The Second Barrage', 'Fuujin Monogatari',
                 'Kanon (2006)', 'Suki na Mono wa Suki Dakara Shou ga Nai!!', 'Ai Tenshi Densetsu Wedding Peach',
                 'Futari wa Precure: Splash☆Star', 'Death Note', 'Busou Renkin', 'Genshi Shounen Ryuu',
                 'Pumpkin Scissors', 'Souten no Ken', 'Brain Powerd', 'Yoake Mae yori Ruriiro na: Crescent Love',
                 'Negima!?', 'Obake no Q-tarou', 'Shin Taketori Monogatari: 1000-nen Joou', 'Attack No.1',
                 'Asatte no Houkou.', 'Tokimeki Memorial: Only Love', 'Shounen Onmyouji',
                 'Shijou Saikyou no Deshi Kenichi', 'Lovedol: Lovely Idol', 'Yamato Nadeshiko Shichihenge♥',
                 'Magic Knight Rayearth II', 'Pokemon Advanced Generation', 'Pokemon Diamond &amp; Pearl',
                 'Kaitou Saint Tail', 'Sumomomo Momomo: Chijou Saikyou no Yome', 'Otome wa Boku ni Koishiteru',
                 'Happiness!', 'Ghost Hunt', 'Jungle Taitei', 'Kishin Douji Zenki', 'Get Ride! AMDriver',
                 'Code Geass: Hangyaku no Lelouch', 'Koisuru Tenshi Angelique: Kokoro no Mezameru Toki',
                 'Kiniro no Corda: Primo Passo', 'Gift: Eternal Rainbow', '009-1', 'Tenpou Ibun: Ayakashi Ayashi',
                 'Mamoru-kun ni Megami no Shukufuku wo!', 'Bartender', 'Legendz: Yomigaeru Ryuuou Densetsu',
                 'Kujibiki♥Unbalance', 'Hataraki Man', 'Jigoku Shoujo Futakomori', 'Panyo Panyo Di Gi Charat',
                 'Eat-Man &#039;98', 'Galaxy Angel Rune', 'Red Garden', 'Soukou no Strain',
                 'Super Robot Taisen OG: Divine Wars', 'Katekyo Hitman Reborn!', 'Kekkaishi', 'Venus Versus Virus',
                 'Salaryman Kintarou', 'Captain Tsubasa: Road to 2002', 'Massugu ni Ikou.',
                 'Soreyuke! Uchuu Senkan Yamamoto Yohko (1999)', 'G-On Riders', 'Maou Dante', 'Devilman Lady',
                 'Peter Pan no Bouken', 'Sugar Sugar Rune', 'Uchuu Senkan Yamato', 'Uchuu Senkan Yamato 2',
                 'Uchuu Senkan Yamato III', 'Nerima Daikon Brothers', 'PostPet Momobin', 'Kurogane Communication',
                 'Cutey Honey', 'Haha wo Tazunete Sanzenri', 'Babel Nisei (2001)', 'Babel Nisei (1973)', 'Barom One',
                 'Bakuten Shoot Beyblade G Revolution', 'Bakuten Shoot Beyblade 2002', 'Bomberman B-Daman Bakugaiden',
                 'Bomberman B-Daman Bakugaiden V', 'Captain Tsubasa J', 'Transformers Micron Densetsu',
                 'Cosmo Warrior Zero', 'Cyborg 009: The Cyborg Soldier', 'Di Gi Charat Nyo', 'Dotto Koni-chan',
                 'Duel Masters', 'Nanatsu-iro★Drops', 'Bokurano', 'Kaze no Stigma', 'Reideen', 'iDOLM@STER Xenoglossia',
                 'Les Misérables: Shoujo Cosette', 'Nodame Cantabile', 'Romeo x Juliet', 'Tokyo Tribe 2', 'Eat-Man',
                 'Genma Taisen: Shinwa Zenya no Shou', 'Gun Frontier', 'Kinnikuman II Sei',
                 'Majuu Sensen: The Apocalypse', 'Rockman.EXE', 'Ryuusei Sentai Musumet', 'Shin Seiki Den Mars',
                 'Submarine Super 99', 'Hitohira', 'Nagasarete Airantou', 'Saint October', 'Devil May Cry',
                 'Shinkyoku Soukai Polyphonica', 'Super GALS! Kotobuki Ran', 'Naruto: Shippuuden',
                 'Uchuu Senshi Baldios', 'Muteki Kanban Musume', 'Shibawanko no Wa no Kokoro',
                 'Naikaku Kenryoku Hanzai Kyousei Torishimarikan Zaizen Joutarou', 'Super Milk-chan',
                 'Wagamama☆Fairy Mirumo de Pon!', 'Wild 7 Another Bouryaku Unga', 'Zoids Fuzors', 'Oh! Super Milk-chan',
                 'Ring ni Kakero 1: Nichibei Kessen-hen', 'Jikuu Tenshou Nazca',
                 'Dae Jang Geum: Jang Geum&#039;s Dream', 'Overman King Gainer', 'Master Mosquiton 99', 'Prism Ark',
                 'Kamichama Karin', 'Kyoushirou to Towa no Sora', 'Hanoka', 'Sonic X', 'Claymore', 'Shin Hakkenden',
                 'Deltora Quest', 'Seirei no Moribito', 'Ryuusei no Rockman', 'Shuffle! Memories', 'Dokkoida',
                 'Jagainu-kun', 'Zero no Tsukaima: Futatsuki no Kishi', 'Major S3', 'CLAMP Gakuen Tanteidan',
                 'Gaiking: Legend of Daiku-Maryu', 'Princess Nine: Kisaragi Joshikou Yakyuubu',
                 'Haou Taikei Ryuu Knight', 'Hidamari Sketch', 'Cutey Honey F', 'Gakuen Utopia Manabi Straight!',
                 'Tokyo Majin Gakuen Kenpucho: Tou', 'Silk Road Shounen Yuuto',
                 'Koisuru Tenshi Angelique: Kagayaki no Ashita', 'Getsumen To Heiki Mina',
                 'Gin&#039;iro no Olynsis: Tokito', 'Saru Getchu: On Air', 'Plawres Sanshirou', 'Kaze no Shoujo Emily',
                 'Sasami: Mahou Shoujo Club', 'Sasami: Mahou Shoujo Club 2', 'Kappa no Kaikata', 'Himesama Goyoujin',
                 'Master of Epic: The Animation Age', 'Fushigiboshi no☆Futagohime Gyu!', 'Lucky☆Star',
                 'Higurashi no Naku Koro ni Kai', 'YAT Anshin! Uchuu Ryokou', 'YAT Anshin! Uchuu Ryokou 2',
                 'Azuki-chan', 'Zettai Muteki Raijin-Oh', 'Masou Kishin Cybuster',
                 'Marginal Prince: Gekkeiju no Ouji-tachi', 'Saiunkoku Monogatari 2nd Season',
                 'Mahou Shoujo Lyrical Nanoha StrikerS', 'Futari wa Precure: Max Heart', 'Yes! Precure 5',
                 'Misute♡naide Daisy', 'Moonlight Mile 1st Season: Lift Off', 'Rocket Girls', 'Ashita no Nadja',
                 'Kikou Sennyo Rouran', 'Kimagure Robot', 'Ikkitousen: Dragon Destiny', 'Sore Ike! Anpanman',
                 'Chikyuu Bouei Kazoku', 'Sola', 'Meitantei Holmes', 'Glass no Kamen (2005)', 'Mutekiou Tri-Zenon',
                 'UFO Robo Grendizer', 'Wakusei Robo Danguard Ace', 'Himawari!!', 'Juusou Kikou Dancougar Nova',
                 'Tengen Toppa Gurren Lagann', 'Heroic Age', 'Hanada Shounen-shi', 'Taiho Shichau zo Special',
                 'Jigoku Sensei Nube', 'Taiho Shichau zo: Second Season', 'Yoshimune',
                 'Darker than Black: Kuro no Keiyakusha', 'Hayate no Gotoku!', 'El Cazador de la Bruja',
                 'Shining Tears X Wind', 'Wellber no Monogatari: Sisters of Wellber', 'Lovely★Complex',
                 'Eikoku Koi Monogatari Emma: Molders-hen', 'Cosmic Baton Girl Comet-san', 'Hime-chan no Ribbon',
                 'Mahou no Star Magical Emi', 'Mahou no Yousei Persia', 'Mahou no Angel Sweet Mint',
                 'Ai to Yuuki no Pig Girl Tonde Buurin', 'Cat&#039;s Eye', 'Mahou no Tenshi Creamy Mami',
                 'Kero Kero Chime', 'Kiko-chan Smile', 'Kindaichi Shounen no Jikenbo (TV)', 'NG Knight Ramune &amp; 40',
                 'VS Knight Lamune &amp; 40 Fire', 'Choujikuu Seiki Orguss', 'Seto no Hanayome', 'Touka Gettan',
                 'Kiss Dum: Engage Planet', 'Rockman.EXE Axess', 'Rockman.EXE Stream', 'Rockman.EXE Beast',
                 'Over Drive', 'Tenkuu Senki Shurato', 'Captain Tsubasa', 'Chouja Raideen', 'Yuusha Raideen',
                 'True Tears', 'Kaibutsu Oujo', 'Blue Dragon', 'Tanoshii Muumin Ikka', 'Nils no Fushigi na Tabi',
                 'Oh! Edo Rocket', 'Saint Beast: Kouin Jojishi Tenshi Tan',
                 'Kono Aozora ni Yakusoku wo: Youkoso Tsugumi Ryou e', 'Bakugan Battle Brawlers', 'Koutetsushin Jeeg',
                 'Terra e... (TV)', 'Ookiku Furikabutte', 'Skull Man', 'Koutetsu Sangokushi', 'Dennou Coil',
                 'Gegege no Kitarou (2007)', 'Doujin Work', 'Clannad', 'Muteki Choujin Zanbot 3',
                 'Waga Seishun no Arcadia: Mugen Kidou SSX', 'Karakuri Zoushi Ayatsuri Sakon', 'Black Jack (TV)',
                 'Black Jack 21', 'Kishin Taisen Gigantic Formula', 'Shigurui', 'Aishite Knight',
                 'Dr. Slump: Arale-chan', 'Maple Town Monogatari', 'Hikari no Densetsu', 'Alps no Shoujo Heidi',
                 'Mori no Tonto-tachi', 'Lady Lady!!', 'Honoo no Toukyuuji: Dodge Danpei',
                 'Dragon Quest: Dai no Daibouken', 'Hana no Ko Lunlun', 'Miyuki', 'Funny Pets',
                 'Ocha-ken: Chokotto Monogatari', 'Panda-Z: The Robonimation', 'Karasu Tengu Kabuto',
                 'Rakugo Tennyo Oyui', 'Seraphim Call', 'Mononoke', 'Baccano!', 'Devilman', 'Mazinger Z',
                 'Sentou Mecha Xabungle', 'Choujuu Kishin Dancougar', 'Taiyou no Kiba Dagram', 'Dr. Rin ni Kiitemite!',
                 'Tatakae! Chou Robot Seimeitai Transformers', 'Hare Tokidoki Buta (TV)', 'Jikuu Tantei Genshi-kun',
                 'Tezuka Osamu no Kyuuyaku Seisho Monogatari: In the Beginning', 'Red Baron',
                 'Transformers: Car Robots', 'D.I.C.E.', 'Fighting Foodons', 'Akihabara Dennou-gumi',
                 'Lime-iro Ryuukitan X', 'Akakichi no Eleven', 'Jibaku-kun', 'Uchuu Densetsu Ulysses 31',
                 'Anime Sanjuushi', 'Kenyuu Densetsu Yaiba', 'Tetsujin 28-gou (2004)', 'Sei Juushi Bismarck', 'Run=Dim',
                 'Pokemon Housoukyoku', 'Virus: Virus Buster Serge', 'Touma Kishinden Oni', 'Moetan', 'Rental Magica',
                 'Firestorm', 'Cybersix', 'Kagaku Ninja-tai Gatchaman', 'Hoshi no Kirby', 'SD Gundam Force',
                 'Ghost Sweeper GS Mikami', 'Ashita no Joe', 'Kodomo no Jikan (TV)', 'Zombie-Loan', 'Hello! Lady Lynn',
                 'Sazae-san', 'Gokudou-kun Manyuuki', 'Super Fishing Grander Musashi', 'Grander Musashi RV',
                 'Space Cobra', '3 Choume no Tama: Uchi no Tama Shirimasenka?', 'Doraemon (1979)', 'School Days',
                 'Gear Fighter Dendoh', 'Rumiko Takahashi Anthology', 'Kyouryuu Boukenki Jura Tripper',
                 'Onegai My Melody', 'Goshuushou-sama Ninomiya-kun', 'Chance Triangle Session', 'Papuwa',
                 'Nangoku Shounen Papuwa-kun', 'Genshiken 2', 'Sengoku Majin Goushougun',
                 'Masuda Kousuke Gekijou Gag Manga Biyori 2', 'Haja Kyosei G Dangaiou',
                 'Izumo: Takeki Tsurugi no Senki', 'Lady Georgie', 'Robin Hood no Daibouken',
                 'Kazoku Robinson Hyouryuuki: Fushigi na Shima no Flone', 'Huckleberry no Bouken',
                 'Alps Monogatari: Watashi no Annette', 'Shoukoujo Sara', 'Ai no Wakakusa Monogatari',
                 'Perrine Monogatari', 'Tetsuko no Tabi', 'Flanders no Inu', 'Ai Shoujo Pollyanna Story',
                 'Shoukoushi Cedie', 'Jungle Taitei (1989)', 'Trapp Ikka Monogatari',
                 'Wakakusa Monogatari: Nan to Jo-sensei', 'Romeo no Aoi Sora', 'Captain Future', 'Shion no Ou',
                 'Code-E', 'Jungle Taitei: Susume Leo!', 'Uchuujin Tanaka Tarou', 'Pinocchio yori Piccolino no Bouken',
                 'Kojika Monogatari', 'Jungle Book Shounen Mowgli', 'Ochame na Futago: Claire Gakuin Monogatari',
                 'Mitsubachi Maya no Bouken', 'Fushigi no Kuni no Alice', 'Minami no Niji no Lucy', 'Kashi no Ki Mokku',
                 'Don Chuck Monogatari', 'Araiguma Rascal', 'Tom Sawyer no Bouken',
                 'TaoTao Ehonkan Sekai Doubutsu Banashi', 'Anime 80-nichikan Sekai Isshuu', 'Mobile Suit Gundam 00',
                 'Soukou Kihei Votoms', 'D.C.II: Da Capo II', 'Shinreigari: Ghost Hound', 'Juusenki L-Gaim',
                 'Kenkou Zenrakei Suieibu Umishou', 'Mushi-Uta', 'Sky Girls', 'Sayonara Zetsubou Sensei',
                 'Wangan Midnight', 'Kakyuusei (1999)', 'Spoon Oba-san', 'Mirai Shounen Conan 2: Taiga Daibouken',
                 'Takarajima', 'Spider Riders: Oracle no Yuusha-tachi', 'Spider Riders: Yomigaeru Taiyou',
                 'Flanders no Inu, Boku no Patrasche', 'Tokyo Majin Gakuen Kenpucho: Tou Dai Ni Maku',
                 'Buzzer Beater 2nd Season', 'Tetsujin 28-gou', 'Gokuu no Daibouken', 'Akai Koudan Zillion',
                 'Hidamari no Ki', 'Uchuu Kaizoku Mito no Daibouken',
                 'Uchuu Kaizoku Mito no Daibouken: Futari no Joou-sama', 'Susie-chan to Marvy',
                 'Bakukyuu Renpatsu! Super Bedaman', 'Chousoku Spinner', 'Kaiketsu Jouki Tanteidan',
                 'Bakusou Kyoudai Let&#039;s &amp; Go', 'Bakusou Kyoudai Let&#039;s &amp; Go WGP',
                 'Majime ni Fumajime Kaiketsu Zorori']
blacklist = []
suggested_anime = "Select an anime below for a new recommendation!"


@app.route("/home/<name>", methods=["GET"])
def add_anime(name):
    if request.method == "GET":
        anime_name = name
        if anime_name not in anime_choices:
            output = f"'{anime_name}' is unknown"
            # return or something
        else:
            anime_choices.remove(anime_name)
            history.append(anime_names[anime_name])
            user_prevelence = cluster.find_similar_users(animes_watched=history)
            similar_anime_id = cluster.find_similar_animes(history, user_prevelence, blacklist)
            similar_anime_name = anime_id_to_names[str(similar_anime_id)]
            global suggested_anime
            suggested_anime = similar_anime_name
    return redirect(url_for('index'))


@app.route("/", methods = ["GET", "POST"])
@app.route("/home/", methods = ["GET", "POST"])
def index():
    global suggested_anime
    if request.method == "POST":
        if "remove-anime-button" in request.form:
            blacklist.append(suggested_anime)
            if suggested_anime in anime_choices:
                anime_choices.remove(suggested_anime)
            user_prevelence = cluster.find_similar_users(animes_watched=history)
            if user_prevelence:
                similar_anime_id = cluster.find_similar_animes(history, user_prevelence, blacklist)
                similar_anime_name = anime_id_to_names[str(similar_anime_id)]
                suggested_anime = similar_anime_name
        return render_template("index.html", suggested_name=suggested_anime, dropdown_choices = anime_choices)

    return render_template("index.html",
                       dropdown_choices=anime_choices,
                       suggested_name=suggested_anime)


# Borrowed from https://gist.github.com/itsnauman/b3d386e4cecf97d59c94
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get('filename', None)
        if filename:
            path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == "__main__":
    # app.run(host='localhost', debug=False, port=8000, threaded=True)
    app.run(debug=True)
