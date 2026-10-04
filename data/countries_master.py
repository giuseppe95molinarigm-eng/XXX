"""Master editorial data for all 195 country pages (American English).

Row fields:
  name, local, translit, capital, language, currency, register, subject, notes
- local/translit: name in its own language; translit only for non-Latin scripts (no diacritics).
  local == "" means the own-language name is English: the page shows the formal name (FORMAL).
- register: plain-language description for A Register of Colors. Colors in {braces}; the flag
  dots are the colors in order of first appearance (field and stripes first, then emblem).
- subject: the drawn landmark, used as the caption (one sentence).
Population comes from UN WPP 2024 (1 July 2025); area from data/base-mledoze.json unless AREA overrides.
"""

FORMAL = {
    "United States": "United States of America", "Australia": "Commonwealth of Australia",
    "United Kingdom": "United Kingdom of Great Britain and Northern Ireland", "Canada": "Canada",
    "Antigua and Barbuda": "Antigua and Barbuda", "Bahamas": "Commonwealth of The Bahamas",
    "Barbados": "Barbados", "Dominica": "Commonwealth of Dominica", "Grenada": "Grenada",
    "Jamaica": "Jamaica", "Saint Kitts and Nevis": "Federation of Saint Christopher and Nevis",
    "Saint Lucia": "Saint Lucia", "Saint Vincent and the Grenadines": "Saint Vincent and the Grenadines",
    "Trinidad and Tobago": "Republic of Trinidad and Tobago", "Guyana": "Co-operative Republic of Guyana",
    "Liberia": "Republic of Liberia", "Sierra Leone": "Republic of Sierra Leone", "Ghana": "Republic of Ghana",
    "Nigeria": "Federal Republic of Nigeria", "Gambia": "Republic of The Gambia", "Zambia": "Republic of Zambia",
    "South Sudan": "Republic of South Sudan", "Uganda": "Republic of Uganda", "Micronesia": "Federated States of Micronesia",
    "Solomon Islands": "Solomon Islands", "South Africa": "Republic of South Africa", "Zimbabwe": "Republic of Zimbabwe",
}

# Areas verified for the Phase 1 samples (see data/sample-data.csv); others from base data.
AREA = {"Italy": 302068, "Japan": 377975, "United States": 9833517, "Brazil": 8509380,
        "Egypt": 1001450, "Australia": 7688287}
POP_OVERRIDE = {"Holy See": "about 500"}   # UN WPP 2024: 501 (1 July 2025)

R = []
def c(name, local, translit, capital, language, currency, register, subject, notes=()):
    R.append(dict(name=name, local=local, translit=translit, capital=capital, language=language,
                  currency=currency, register=register, subject=subject, notes=list(notes)))

# ---------------------------------------------------------------- EUROPE
c("Albania", "Shqipëria", "", "Tirana", "Albanian", "Albanian lek (ALL)",
  "{Red}, with a {black} two-headed eagle in the middle, its wings spread.", "The old town of Berat")
c("Andorra", "Andorra", "", "Andorra la Vella", "Catalan", "Euro (EUR)",
  "Three upright stripes, left to right: {blue}, {yellow}, {red}; the middle one a little wider. On the yellow stripe, a shield in four parts: a bishop's hat and staff, two sets of red stripes on gold, and two red cows.",
  "The Romanesque church of Sant Joan de Caselles")
c("Austria", "Österreich", "", "Vienna", "German", "Euro (EUR)",
  "Three equal stripes, top to bottom: {red}, {white}, {red}.", "Schönbrunn Palace, Vienna")
c("Belarus", "Беларусь", "Belarus", "Minsk", "Belarusian, Russian", "Belarusian ruble (BYN)",
  "Two stripes, top to bottom: a wide {red} one and a narrower {green} one. Along the left edge runs an upright {white} strip with a red folk-embroidery pattern.",
  "Mir Castle")
c("Belgium", "België · Belgique", "", "Brussels", "Dutch, French, German", "Euro (EUR)",
  "Three upright stripes, left to right: {black}, {yellow}, {red}.", "The Grand-Place, Brussels")
c("Bosnia and Herzegovina", "Bosna i Hercegovina", "", "Sarajevo", "Bosnian, Croatian, Serbian", "Convertible mark (BAM)",
  "{Blue}, with a large {yellow} triangle hanging from the top edge, its straight side upright on the right. Down its slanting side runs a line of {white} stars, the first and last cut in half by the edges.",
  "The Old Bridge, Mostar")
c("Bulgaria", "България", "Balgariya", "Sofia", "Bulgarian", "Euro (EUR)",
  "Three equal stripes, top to bottom: {white}, {green}, {red}.", "Rila Monastery",
  ["Bulgaria adopted the euro on 1 January 2026."])
c("Croatia", "Hrvatska", "", "Zagreb", "Croatian", "Euro (EUR)",
  "Three equal stripes, top to bottom: {red}, {white}, {blue}. In the middle, a shield of red and white squares like a chessboard, under a crown of five small blue shields.",
  "The city walls of Dubrovnik")
c("Czechia", "Česko", "", "Prague", "Czech", "Czech koruna (CZK)",
  "Two stripes, {white} above {red}, with a {blue} triangle pointing in from the left edge to the middle.",
  "Charles Bridge and Prague Castle")
c("Denmark", "Danmark", "", "Copenhagen", "Danish", "Danish krone (DKK)",
  "{Red}, with a {white} cross whose upright bar sits closer to the left edge.", "Nyhavn, Copenhagen")
c("Estonia", "Eesti", "", "Tallinn", "Estonian", "Euro (EUR)",
  "Three equal stripes, top to bottom: {blue}, {black}, {white}.", "The old town of Tallinn")
c("Finland", "Suomi", "", "Helsinki", "Finnish, Swedish", "Euro (EUR)",
  "{White}, with a {blue} cross whose upright bar sits closer to the left edge.", "Helsinki Cathedral")
c("France", "France", "", "Paris", "French", "Euro (EUR)",
  "Three upright stripes, left to right: {blue}, {white}, {red}.", "The Eiffel Tower, Paris")
c("Germany", "Deutschland", "", "Berlin", "German", "Euro (EUR)",
  "Three equal stripes, top to bottom: {black}, {red}, {gold}.", "The Brandenburg Gate, Berlin")
c("Greece", "Ελλάδα", "Ellada", "Athens", "Greek", "Euro (EUR)",
  "Nine stripes, top to bottom, {blue} and {white} taking turns, starting and ending with blue. In the top left corner, a blue square with a white cross.",
  "The Parthenon, Athens")
c("Holy See", "Santa Sede", "", "Vatican City", "Italian, Latin", "Euro (EUR)",
  "A square flag. Two upright halves: {yellow} on the left, {white} on the right. On the white half, two crossed keys, one {gold} and one {silver}, tied with a {red} cord under the papal crown.",
  "St. Peter's Basilica",
  ["The Holy See governs Vatican City State; area and population are those of Vatican City."])
c("Hungary", "Magyarország", "", "Budapest", "Hungarian", "Hungarian forint (HUF)",
  "Three equal stripes, top to bottom: {red}, {white}, {green}.", "The Parliament, Budapest")
c("Iceland", "Ísland", "", "Reykjavik", "Icelandic", "Icelandic króna (ISK)",
  "{Blue}, with a {red} cross edged in {white}, its upright bar closer to the left edge.", "Skógafoss waterfall")
c("Ireland", "Éire", "", "Dublin", "Irish, English", "Euro (EUR)",
  "Three upright stripes, left to right: {green}, {white}, {orange}.", "The Cliffs of Moher")
c("Italy", "Italia", "", "Rome", "Italian", "Euro (EUR)",
  "Three upright stripes, left to right: {green}, {white}, {red}.", "The Colosseum, Rome",
  ["San Marino and Vatican City lie within Italy and are not part of its area."])
c("Latvia", "Latvija", "", "Riga", "Latvian", "Euro (EUR)",
  "Three stripes, top to bottom: {dark red}, a thin {white} one, dark red. The white stripe is half as tall as each red one.",
  "The old town of Riga")
c("Liechtenstein", "Liechtenstein", "", "Vaduz", "German", "Swiss franc (CHF)",
  "Two equal stripes, {blue} above {red}. Near the left of the blue stripe, a {gold} crown.", "Vaduz Castle")
c("Lithuania", "Lietuva", "", "Vilnius", "Lithuanian", "Euro (EUR)",
  "Three equal stripes, top to bottom: {yellow}, {green}, {red}.", "Trakai Island Castle")
c("Luxembourg", "Lëtzebuerg", "", "Luxembourg", "Luxembourgish, French, German", "Euro (EUR)",
  "Three equal stripes, top to bottom: {red}, {white}, {light blue}.", "Vianden Castle")
c("Malta", "Malta", "", "Valletta", "Maltese, English", "Euro (EUR)",
  "Two upright halves: {white} on the left, {red} on the right. In the top left corner, the George Cross in {grey} with a thin red edge.",
  "The Grand Harbour, Valletta")
c("Moldova", "Moldova", "", "Chișinău", "Romanian", "Moldovan leu (MDL)",
  "Three upright stripes, left to right: {blue}, {yellow}, {red}. On the yellow stripe, a {brown} eagle with a gold cross in its beak and a shield on its chest, red above blue, with the head of a wild ox.",
  "Orheiul Vechi cave monastery")
c("Monaco", "Monaco", "", "Monaco", "French", "Euro (EUR)",
  "Two equal stripes, {red} above {white}.", "The Prince's Palace and the harbor of Monaco")
c("Montenegro", "Crna Gora", "", "Podgorica", "Montenegrin", "Euro (EUR)",
  "{Red} with a {gold} border all around. In the middle, a gold two-headed eagle under a crown; on its chest, a small shield with a gold lion walking on {green} under a {blue} sky.",
  "Our Lady of the Rocks, Bay of Kotor")
c("Netherlands", "Nederland", "", "Amsterdam", "Dutch", "Euro (EUR)",
  "Three equal stripes, top to bottom: {red}, {white}, {blue}.", "The windmills of Kinderdijk",
  ["Amsterdam is the capital; the government sits in The Hague."])
c("North Macedonia", "Северна Македонија", "Severna Makedonija", "Skopje", "Macedonian, Albanian", "Macedonian denar (MKD)",
  "{Red}, with a {yellow} sun in the middle whose eight broad rays reach out to the edges and corners.",
  "The Church of St. John at Kaneo, Lake Ohrid")
c("Norway", "Norge", "", "Oslo", "Norwegian", "Norwegian krone (NOK)",
  "{Red}, with a {blue} cross edged in {white}, its upright bar closer to the left edge.", "Borgund Stave Church")
c("Poland", "Polska", "", "Warsaw", "Polish", "Polish złoty (PLN)",
  "Two equal stripes, {white} above {red}.", "The Cloth Hall, Kraków")
c("Portugal", "Portugal", "", "Lisbon", "Portuguese", "Euro (EUR)",
  "Two upright parts: {green} on the left, {red} on the right and wider. Where they meet, a {yellow} globe made of rings holding a shield: {white} with five small {blue} shields, inside a red border with seven yellow castles.",
  "Belém Tower, Lisbon")
c("Romania", "România", "", "Bucharest", "Romanian", "Romanian leu (RON)",
  "Three upright stripes, left to right: {blue}, {yellow}, {red}.", "Bran Castle")
c("Russia", "Россия", "Rossiya", "Moscow", "Russian", "Russian ruble (RUB)",
  "Three equal stripes, top to bottom: {white}, {blue}, {red}.", "St. Basil's Cathedral, Moscow",
  ["Crimea is shown as part of Ukraine, following United Nations practice."])
c("San Marino", "San Marino", "", "San Marino", "Italian", "Euro (EUR)",
  "Two equal stripes, {white} above {light blue}. In the middle, a shield with three towers on three {green} hills, in a wreath, under a {gold} crown, with the word LIBERTAS below.",
  "The Guaita tower on Monte Titano")
c("Serbia", "Србија", "Srbija", "Belgrade", "Serbian", "Serbian dinar (RSD)",
  "Three equal stripes, top to bottom: {red}, {blue}, {white}. Left of the middle, a white two-headed eagle on a red shield, under a {gold} crown.",
  "Belgrade Fortress",
  ["Kosovo is shown within Serbia, following United Nations practice; its status is disputed."])
c("Slovakia", "Slovensko", "", "Bratislava", "Slovak", "Euro (EUR)",
  "Three equal stripes, top to bottom: {white}, {blue}, {red}. Toward the left, a shield edged in white: a white double cross on three blue hills, on red.",
  "Bratislava Castle")
c("Slovenia", "Slovenija", "", "Ljubljana", "Slovene", "Euro (EUR)",
  "Three equal stripes, top to bottom: {white}, {blue}, {red}. In the top left, a shield edged in red: a white three-peaked mountain on blue, two wavy blue lines below it, and three {gold} stars above.",
  "Lake Bled and its island church")
c("Spain", "España", "", "Madrid", "Spanish", "Euro (EUR)",
  "Three stripes, top to bottom: {red}, {yellow}, red; the yellow one twice as tall as each red. Toward the left of the yellow stripe, the coat of arms between two pillars, each topped with a crown.",
  "The Alhambra, Granada")
c("Sweden", "Sverige", "", "Stockholm", "Swedish", "Swedish krona (SEK)",
  "{Blue}, with a {yellow} cross whose upright bar sits closer to the left edge.", "Gamla Stan, Stockholm")
c("Switzerland", "Schweiz · Suisse · Svizzera", "", "Bern", "German, French, Italian, Romansh", "Swiss franc (CHF)",
  "A square flag: {red}, with a {white} cross in the middle whose arms stop short of the edges.", "The Matterhorn")
c("Ukraine", "Україна", "Ukraina", "Kyiv", "Ukrainian", "Ukrainian hryvnia (UAH)",
  "Two equal stripes, {blue} above {yellow}.", "St. Sophia's Cathedral, Kyiv",
  ["Crimea is shown as part of Ukraine, following United Nations practice."])
c("United Kingdom", "", "", "London", "English", "Pound sterling (GBP)",
  "{Blue}, with a {white} diagonal cross from corner to corner and a thinner {red} diagonal cross on it, set slightly off center. Over both, a white upright cross with a red upright cross in its middle.",
  "The Elizabeth Tower (Big Ben), London")

# ---------------------------------------------------------------- AFRICA
c("Algeria", "الجزائر", "Al-Jazair", "Algiers", "Arabic, Tamazight", "Algerian dinar (DZD)",
  "Two upright halves: {green} on the left, {white} on the right. Across the middle, a {red} crescent and a red star.",
  "The Arch of Trajan, Timgad")
c("Angola", "Angola", "", "Luanda", "Portuguese", "Angolan kwanza (AOA)",
  "Two equal stripes, {red} above {black}. In the middle, a {yellow} half cogwheel crossed by a machete, with a yellow star.",
  "Kalandula Falls")
c("Benin", "Bénin", "", "Porto-Novo", "French", "West African CFA franc (XOF)",
  "An upright {green} stripe on the left; on the right, two stripes, {yellow} above {red}.", "The stilt village of Ganvie")
c("Botswana", "Botswana", "", "Gaborone", "English, Setswana", "Botswana pula (BWP)",
  "{Light blue}, with a {black} stripe across the middle edged in thin {white} stripes above and below.", "Elephants in the Okavango Delta")
c("Burkina Faso", "Burkina Faso", "", "Ouagadougou", "Mooré, French", "West African CFA franc (XOF)",
  "Two equal stripes, {red} above {green}, with a {yellow} star in the middle.", "The Grand Mosque of Bobo-Dioulasso")
c("Burundi", "Uburundi", "", "Gitega", "Kirundi, French", "Burundian franc (BIF)",
  "A {white} diagonal cross from corner to corner divides the flag: {red} at top and bottom, {green} at left and right. In the middle, a white circle with three red stars edged in green.",
  "Karera Falls")
c("Cabo Verde", "Cabo Verde", "", "Praia", "Portuguese", "Cape Verdean escudo (CVE)",
  "{Blue}, with thin stripes {white}, {red}, white just below the middle. Ten {yellow} stars form a ring centered on the stripes, toward the left.",
  "Pico do Fogo volcano")
c("Cameroon", "Cameroun · Cameroon", "", "Yaoundé", "French, English", "Central African CFA franc (XAF)",
  "Three upright stripes, left to right: {green}, {red}, {yellow}, with a yellow star in the middle of the red stripe.",
  "Mount Cameroon")
c("Central African Republic", "Centrafrique · Bêafrîka", "", "Bangui", "French, Sango", "Central African CFA franc (XAF)",
  "Four equal stripes, top to bottom: {blue}, {white}, {green}, {yellow}, crossed by an upright {red} stripe in the middle. A yellow star sits in the top left corner.",
  "Boali Falls")
c("Chad", "Tchad · تشاد", "Tshad", "N'Djamena", "French, Arabic", "Central African CFA franc (XAF)",
  "Three upright stripes, left to right: {blue}, {yellow}, {red}.", "The Aloba Arch, Ennedi Plateau")
c("Comoros", "Komori · Comores", "", "Moroni", "Comorian, Arabic, French", "Comorian franc (KMF)",
  "Four equal stripes, top to bottom: {yellow}, {white}, {red}, {blue}. From the left, a {green} triangle with a white crescent and four white stars.",
  "Mount Karthala")
c("Congo", "Congo", "", "Brazzaville", "French", "Central African CFA franc (XAF)",
  "Split by a diagonal from the bottom left to the top right: {green} in the top left, {red} in the bottom right, with a {yellow} band along the diagonal.",
  "The Congo River rapids at Brazzaville")
c("Côte d'Ivoire", "Côte d'Ivoire", "", "Yamoussoukro", "French", "West African CFA franc (XOF)",
  "Three upright stripes, left to right: {orange}, {white}, {green}.", "The historic town of Grand-Bassam",
  ["Yamoussoukro is the capital; most government offices are in Abidjan."])
c("Democratic Republic of the Congo", "RD Congo", "", "Kinshasa", "French", "Congolese franc (CDF)",
  "{Sky blue}, crossed from the bottom left to the top right by a {red} band edged in thin {yellow}. A yellow star sits in the top left corner.",
  "Nyiragongo volcano")
c("Djibouti", "Djibouti · جيبوتي", "Jibuti", "Djibouti", "French, Arabic", "Djiboutian franc (DJF)",
  "Two equal stripes, {light blue} above {green}. From the left, a {white} triangle with a {red} star.",
  "The limestone chimneys of Lake Abbe")
c("Egypt", "مصر", "Misr", "Cairo", "Arabic", "Egyptian pound (EGP)",
  "Three equal stripes, top to bottom: {red}, {white}, {black}. In the middle of the white stripe stands a {gold} eagle looking to your left. On its chest is a small shield with upright stripes, left to right: red, white, black. Its claws hold a gold ribbon with the country's name in Arabic.",
  "The Pyramids of Giza and the Great Sphinx",
  ["The Halaib Triangle, on the southern border, is administered by Egypt and claimed by Sudan."])
c("Equatorial Guinea", "Guinea Ecuatorial", "", "Malabo", "Spanish, French, Portuguese", "Central African CFA franc (XAF)",
  "Three equal stripes, top to bottom: {green}, {white}, {red}, with a {blue} triangle on the left. In the middle, a shield with a silk-cotton tree, six {yellow} stars above it and a motto below.",
  "Santa Isabel Cathedral, Malabo")
c("Eritrea", "ኤርትራ", "Ertra", "Asmara", "Tigrinya, Arabic", "Eritrean nakfa (ERN)",
  "A {red} triangle points from the left edge to the right edge, leaving {green} above and {blue} below. Inside the red, toward the left, a {yellow} olive branch in a ring of olive leaves.",
  "The Fiat Tagliero building, Asmara")
c("Eswatini", "eSwatini", "", "Mbabane, Lobamba", "Swazi, English", "Swazi lilangeni (SZL)",
  "Stripes top to bottom: {blue}, a thin {yellow}, a wide {red}, a thin yellow, blue. Across the red stripe lies a {black}-and-{white} shield, with two spears and a tasseled staff behind it.",
  "Sibebe Rock",
  ["Mbabane is the seat of government; Lobamba is the royal and legislative capital."])
c("Ethiopia", "ኢትዮጵያ", "Ityopya", "Addis Ababa", "Amharic", "Ethiopian birr (ETB)",
  "Three equal stripes, top to bottom: {green}, {yellow}, {red}. In the middle, a {blue} disc with a yellow star drawn in lines, and yellow rays between its points.",
  "The rock-hewn Church of St. George, Lalibela")
c("Gabon", "Gabon", "", "Libreville", "French", "Central African CFA franc (XAF)",
  "Three equal stripes, top to bottom: {green}, {yellow}, {blue}.", "The rainforest of Lopé National Park")
c("Gambia", "", "", "Banjul", "English", "Gambian dalasi (GMD)",
  "Stripes top to bottom: {red}, a thin {white}, {blue}, a thin white, {green}.", "Kunta Kinteh Island")
c("Ghana", "", "", "Accra", "English", "Ghanaian cedi (GHS)",
  "Three equal stripes, top to bottom: {red}, {yellow}, {green}, with a {black} star in the middle.", "Cape Coast Castle")
c("Guinea", "Guinée", "", "Conakry", "French", "Guinean franc (GNF)",
  "Three upright stripes, left to right: {red}, {yellow}, {green}.", "The Bridal Veil Falls, Kindia")
c("Guinea-Bissau", "Guiné-Bissau", "", "Bissau", "Portuguese", "West African CFA franc (XOF)",
  "An upright {red} stripe on the left with a {black} star; to the right, two stripes, {yellow} above {green}.", "The Bijagós Islands")
c("Kenya", "Kenya", "", "Nairobi", "Swahili, English", "Kenyan shilling (KES)",
  "Three stripes, top to bottom: {black}, {red}, {green}, separated by thin {white} stripes. In the middle, a red, black and white Maasai shield over two crossed white spears.",
  "Mount Kenya")
c("Lesotho", "Lesotho", "", "Maseru", "Sesotho, English", "Lesotho loti (LSL)",
  "Three stripes, top to bottom: {blue}, a wider {white}, {green}. In the middle of the white stripe, a {black} Basotho hat.",
  "Maletsunyane Falls")
c("Liberia", "", "", "Monrovia", "English", "Liberian dollar (LRD)",
  "Eleven stripes, top to bottom, {red} and {white} taking turns, starting and ending with red. In the top left corner, a {blue} square with one large white star.",
  "The rainforest of Sapo National Park")
c("Libya", "ليبيا", "Libya", "Tripoli", "Arabic", "Libyan dinar (LYD)",
  "Three stripes, top to bottom: {red}, a double-height {black}, {green}. In the middle of the black stripe, a {white} crescent and a white star.",
  "Leptis Magna")
c("Madagascar", "Madagasikara", "", "Antananarivo", "Malagasy, French", "Malagasy ariary (MGA)",
  "An upright {white} stripe on the left; on the right, two stripes, {red} above {green}.", "The Avenue of the Baobabs")
c("Malawi", "Malaŵi", "", "Lilongwe", "English, Chichewa", "Malawian kwacha (MWK)",
  "Three equal stripes, top to bottom: {black}, {red}, {green}. A red rising sun with 31 rays sits in the middle of the black stripe.",
  "Lake Malawi")
c("Mali", "Mali", "", "Bamako", "Bambara, French", "West African CFA franc (XOF)",
  "Three upright stripes, left to right: {green}, {yellow}, {red}.", "The Great Mosque of Djenné")
c("Mauritania", "موريتانيا", "Muritaniya", "Nouakchott", "Arabic", "Mauritanian ouguiya (MRU)",
  "{Green}, with a thin {red} stripe along the top and bottom edges. In the middle, a {yellow} crescent with a yellow star above it.",
  "The old mosque of Chinguetti")
c("Mauritius", "Maurice · Moris", "", "Port Louis", "English, French", "Mauritian rupee (MUR)",
  "Four equal stripes, top to bottom: {red}, {blue}, {yellow}, {green}.", "Le Morne Brabant")
c("Morocco", "المغرب", "Al-Maghrib", "Rabat", "Arabic, Tamazight", "Moroccan dirham (MAD)",
  "{Red}, with a {green} five-pointed star in the middle, drawn as an interlaced outline.", "The Koutoubia Mosque, Marrakesh",
  ["Western Sahara is shown separately, following United Nations practice; its status is disputed."])
c("Mozambique", "Moçambique", "", "Maputo", "Portuguese", "Mozambican metical (MZN)",
  "Three stripes, top to bottom: {green}, {black}, {yellow}, separated by thin {white} stripes. From the left, a {red} triangle with a yellow star, on which lie an open book, a rifle and a hoe.",
  "The fortress of São Sebastião, Island of Mozambique")
c("Namibia", "", "", "Windhoek", "English", "Namibian dollar (NAD)",
  "A {red} band edged in {white} runs from the bottom left corner to the top right corner, with {blue} above it and {green} below. In the blue corner, a {yellow} sun with twelve straight rays.",
  "The dunes of Sossusvlei")
c("Niger", "Niger", "", "Niamey", "Hausa, French", "West African CFA franc (XOF)",
  "Three equal stripes, top to bottom: {orange}, {white}, {green}, with an orange circle in the middle.", "The Grand Mosque of Agadez")
c("Nigeria", "", "", "Abuja", "English", "Nigerian naira (NGN)",
  "Three upright stripes, left to right: {green}, {white}, green.", "Zuma Rock")
c("Rwanda", "Rwanda", "", "Kigali", "Kinyarwanda, English, French", "Rwandan franc (RWF)",
  "Three stripes, top to bottom: a wide {blue} one, {yellow}, {green}. In the top right corner, a yellow sun with 24 rays.",
  "The Virunga volcanoes")
c("Sao Tome and Principe", "São Tomé e Príncipe", "", "São Tomé", "Portuguese", "São Tomé and Príncipe dobra (STN)",
  "Three stripes, top to bottom: {green}, a wider {yellow}, green, with a {red} triangle on the left. Two {black} stars sit on the yellow stripe.",
  "Pico Cão Grande")
c("Senegal", "Sénégal", "", "Dakar", "French", "West African CFA franc (XOF)",
  "Three upright stripes, left to right: {green}, {yellow}, {red}, with a green star in the middle.", "The House of Slaves, Gorée Island")
c("Seychelles", "Sesel", "", "Victoria", "Seychellois Creole, English, French", "Seychellois rupee (SCR)",
  "Five bands fanning out from the bottom left corner, left to right: {blue}, {yellow}, {red}, {white}, {green}.",
  "The granite boulders of Anse Source d'Argent")
c("Sierra Leone", "", "", "Freetown", "English", "Sierra Leonean leone (SLE)",
  "Three equal stripes, top to bottom: {green}, {white}, {blue}.", "Bunce Island")
c("Somalia", "Soomaaliya", "", "Mogadishu", "Somali, Arabic", "Somali shilling (SOS)",
  "{Light blue}, with a {white} five-pointed star in the middle.", "The rock paintings of Laas Geel",
  ["Somaliland is shown within Somalia, following United Nations practice."])
c("South Africa", "", "", "Pretoria, Cape Town, Bloemfontein", "12 official languages", "South African rand (ZAR)",
  "A {green} band shaped like a Y lying on its side: its two arms start at the left corners, meet in the middle and run on as one band to the right edge. The Y has thin {white} edges on its outer sides and a thin {gold} edge on the inside. Inside the Y, on the left, a {black} triangle. Above the Y, {red}; below it, {blue}.",
  "Table Mountain, Cape Town",
  ["Pretoria is the seat of government, Cape Town of parliament, Bloemfontein of the judiciary."])
c("South Sudan", "", "", "Juba", "English", "South Sudanese pound (SSP)",
  "Three stripes, top to bottom: {black}, {red}, {green}, separated by thin {white} stripes. From the left, a {blue} triangle with a {yellow} star.",
  "The White Nile at Juba")
c("Sudan", "السودان", "As-Sudan", "Khartoum", "Arabic, English", "Sudanese pound (SDG)",
  "Three equal stripes, top to bottom: {red}, {white}, {black}, with a {green} triangle on the left.", "The Pyramids of Meroë")
c("Tanzania", "Tanzania", "", "Dodoma", "Swahili, English", "Tanzanian shilling (TZS)",
  "A {black} band edged in thin {yellow} runs from the bottom left corner to the top right corner, with {green} above and {blue} below.",
  "Mount Kilimanjaro")
c("Togo", "Togo", "", "Lomé", "French", "West African CFA franc (XOF)",
  "Five stripes, top to bottom, {green} and {yellow} taking turns, starting and ending with green. In the top left corner, a {red} square with a {white} star.",
  "The earthen tower-houses of Koutammakou")
c("Tunisia", "تونس", "Tunis", "Tunis", "Arabic", "Tunisian dinar (TND)",
  "{Red}, with a {white} circle in the middle holding a red crescent and a red star.", "The Amphitheater of El Jem")
c("Uganda", "", "", "Kampala", "English, Swahili", "Ugandan shilling (UGX)",
  "Six equal stripes, top to bottom: {black}, {yellow}, {red}, black, yellow, red. In the middle, a {white} circle with a crowned crane facing left, in {grey}, white, gold and red.",
  "Murchison Falls")
c("Zambia", "", "", "Lusaka", "English", "Zambian kwacha (ZMW)",
  "{Green}. In the bottom right, three upright stripes, left to right: {red}, {black}, {orange}, with an orange eagle flying above them.",
  "Victoria Falls")
c("Zimbabwe", "", "", "Harare", "16 official languages", "Zimbabwe Gold (ZWG)",
  "Seven stripes, top to bottom: {green}, {yellow}, {red}, {black}, red, yellow, green. From the left, a {white} triangle edged in black, with a red star behind a yellow bird.",
  "Great Zimbabwe")

# ---------------------------------------------------------------- ASIA
c("Afghanistan", "افغانستان", "Afghanistan", "Kabul", "Pashto, Dari", "Afghan afghani (AFN)",
  "Three upright stripes, left to right: {black}, {red}, {green}. In the middle, a {white} emblem: a mosque with a pulpit, framed by wheat and topped by Arabic writing.",
  "The Minaret of Jam",
  ["This is the flag used at the United Nations. The authorities in control since 2021 use a different flag."])
c("Armenia", "Հայաստան", "Hayastan", "Yerevan", "Armenian", "Armenian dram (AMD)",
  "Three equal stripes, top to bottom: {red}, {blue}, {orange}.", "Khor Virap Monastery and Mount Ararat")
c("Azerbaijan", "Azərbaycan", "", "Baku", "Azerbaijani", "Azerbaijani manat (AZN)",
  "Three equal stripes, top to bottom: {light blue}, {red}, {green}, with a {white} crescent and an eight-pointed white star in the middle.",
  "The Maiden Tower, Baku")
c("Bahrain", "البحرين", "Al-Bahrain", "Manama", "Arabic", "Bahraini dinar (BHD)",
  "{White} on the left, {red} on the right, divided by a zigzag line with five white points.", "Qal'at al-Bahrain")
c("Bangladesh", "বাংলাদেশ", "Bangladesh", "Dhaka", "Bengali", "Bangladeshi taka (BDT)",
  "{Green}, with a {red} circle set slightly left of the middle.", "The Sixty Dome Mosque, Bagerhat")
c("Bhutan", "འབྲུག་ཡུལ", "Druk Yul", "Thimphu", "Dzongkha", "Bhutanese ngultrum (BTN)",
  "Split by a straight line from the bottom left corner to the top right corner: the top half {yellow}, the bottom half {orange}. Across the line lies a {white} dragon facing right, holding a jewel in each claw.",
  "Paro Taktsang (the Tiger's Nest)")
c("Brunei", "Brunei Darussalam", "", "Bandar Seri Begawan", "Malay", "Brunei dollar (BND)",
  "{Yellow}, crossed from top left to bottom right by two stripes, {white} above {black}. In the middle, the {red} national emblem: a crescent, a parasol, wings and two raised hands.",
  "The Sultan Omar Ali Saifuddien Mosque")
c("Cambodia", "កម្ពុជា", "Kampuchea", "Phnom Penh", "Khmer", "Cambodian riel (KHR)",
  "Three stripes, top to bottom: {blue}, a double-height {red}, blue. In the middle of the red stripe, a {white} outline of the temple of Angkor Wat with three towers.",
  "Angkor Wat")
c("China", "中国", "Zhongguo", "Beijing", "Mandarin Chinese", "Renminbi (CNY)",
  "{Red}. In the top left, one large {yellow} star with four small yellow stars in an arc to its right, each pointing toward the large one.",
  "The Great Wall",
  ["Taiwan is shown as part of China, following United Nations practice; figures exclude Taiwan, Hong Kong and Macao."])
c("Cyprus", "Κύπρος · Kıbrıs", "Kypros · Kibris", "Nicosia", "Greek, Turkish", "Euro (EUR)",
  "{White}, with a {copper orange} outline of the island in the middle and two crossed {green} olive branches below it.",
  "Petra tou Romiou (Aphrodite's Rock)",
  ["The whole island is shown, following United Nations practice; the north is not under government control."])
c("Georgia", "საქართველო", "Sakartvelo", "Tbilisi", "Georgian", "Georgian lari (GEL)",
  "{White}, with a large {red} cross and a small red cross with flared ends in each of the four corners.",
  "Gergeti Trinity Church and Mount Kazbek")
c("India", "भारत", "Bharat", "New Delhi", "Hindi, English", "Indian rupee (INR)",
  "Three equal stripes, top to bottom: {saffron}, {white}, {green}. In the middle, a {navy blue} wheel with 24 spokes.",
  "The Taj Mahal, Agra",
  ["Borders in Kashmir follow United Nations practice; the region is disputed."])
c("Indonesia", "Indonesia", "", "Jakarta", "Indonesian", "Indonesian rupiah (IDR)",
  "Two equal stripes, {red} above {white}.", "Borobudur")
c("Iran", "ایران", "Iran", "Tehran", "Persian", "Iranian rial (IRR)",
  "Three equal stripes, top to bottom: {green}, {white}, {red}. Along the inner edges of the green and red stripes runs a fringe of small white Arabic writing. In the middle, a red emblem of four curves and a sword.",
  "Persepolis")
c("Iraq", "العراق", "Al-Iraq", "Baghdad", "Arabic, Kurdish", "Iraqi dinar (IQD)",
  "Three equal stripes, top to bottom: {red}, {white}, {black}. Across the white stripe, the words Allahu Akbar in {green} Arabic writing.",
  "The Ziggurat of Ur")
c("Israel", "ישראל", "Yisrael", "Jerusalem*", "Hebrew", "Israeli new shekel (ILS)",
  "{White}, with two {blue} stripes near the top and bottom edges and a blue six-pointed star in the middle, drawn as two triangles.",
  "Masada",
  ["Israel designates Jerusalem as its capital; the United Nations does not recognize this, and most embassies are in Tel Aviv."])
c("Japan", "日本", "Nippon", "Tokyo", "Japanese", "Japanese yen (JPY)",
  "A {white} flag with one {red} circle in the exact middle.", "Mount Fuji and the Chureito Pagoda",
  ["The area includes the southern Kuril Islands, administered by Russia and claimed by Japan; they are not drawn on this map.",
   "Smaller remote islands are not shown at this scale."])
c("Jordan", "الأردن", "Al-Urdun", "Amman", "Arabic", "Jordanian dinar (JOD)",
  "Three equal stripes, top to bottom: {black}, {white}, {green}. From the left, a {red} triangle with a small white seven-pointed star.",
  "The Treasury, Petra")
c("Kazakhstan", "Қазақстан", "Qazaqstan", "Astana", "Kazakh, Russian", "Kazakhstani tenge (KZT)",
  "{Sky blue}. In the middle, a {gold} sun with 32 rays above a soaring gold eagle; along the left edge, an upright gold band of ornament.",
  "Charyn Canyon")
c("Kuwait", "الكويت", "Al-Kuwayt", "Kuwait City", "Arabic", "Kuwaiti dinar (KWD)",
  "Three equal stripes, top to bottom: {green}, {white}, {red}. On the left, a {black} shape with slanting sides.",
  "A dhow, the traditional sailing ship of the Gulf")
c("Kyrgyzstan", "Кыргызстан", "Kyrgyzstan", "Bishkek", "Kyrgyz, Russian", "Kyrgyzstani som (KGS)",
  "{Red}. In the middle, a {yellow} sun with 40 rays; inside it, the red crossed lines of a yurt roof.",
  "The Burana Tower")
c("Laos", "ລາວ", "Lao", "Vientiane", "Lao", "Lao kip (LAK)",
  "Three stripes, top to bottom: {red}, a double-height {blue}, red, with a {white} circle in the middle.", "Pha That Luang, Vientiane")
c("Lebanon", "لبنان", "Lubnan", "Beirut", "Arabic", "Lebanese pound (LBP)",
  "Three stripes, top to bottom: {red}, a double-height {white}, red, with a {green} cedar tree in the middle.", "The temples of Baalbek")
c("Malaysia", "Malaysia", "", "Kuala Lumpur", "Malay", "Malaysian ringgit (MYR)",
  "Fourteen stripes, top to bottom, {red} and {white} taking turns, starting with red. In the top left corner, a {blue} rectangle with a {yellow} crescent and a yellow fourteen-pointed star.",
  "Mount Kinabalu")
c("Maldives", "ދިވެހިރާއްޖެ", "Dhivehi Raajje", "Malé", "Dhivehi", "Maldivian rufiyaa (MVR)",
  "{Red}, with a {green} rectangle in the middle holding a {white} crescent.", "The Old Friday Mosque, Malé")
c("Mongolia", "Монгол Улс", "Mongol Uls", "Ulaanbaatar", "Mongolian", "Mongolian tögrög (MNT)",
  "Three upright stripes, left to right: {red}, {blue}, red. On the left red stripe, a {yellow} emblem of a flame, sun, moon, triangles, bars and a yin-yang.",
  "Erdene Zuu Monastery")
c("Myanmar", "မြန်မာ", "Myanma", "Naypyidaw", "Burmese", "Myanmar kyat (MMK)",
  "Three equal stripes, top to bottom: {yellow}, {green}, {red}, with a large {white} star in the middle.", "The Shwedagon Pagoda, Yangon")
c("Nepal", "नेपाल", "Nepal", "Kathmandu", "Nepali", "Nepalese rupee (NPR)",
  "Not a rectangle: two triangles stacked one on the other, the top one smaller, both pointing to your right. {Crimson} inside, with a {blue} border all the way around. In the top triangle, a {white} crescent moon lying on its back, with eight short rays rising from it; in the bottom triangle, a white sun with twelve points.",
  "Mount Everest (Sagarmatha)")
c("North Korea", "조선", "Choson", "Pyongyang", "Korean", "North Korean won (KPW)",
  "Stripes top to bottom: {blue}, a thin {white}, a wide {red}, a thin white, blue. Left of the middle, a white circle with a red five-pointed star.",
  "Mount Paektu")
c("Oman", "عُمان", "Uman", "Muscat", "Arabic", "Omani rial (OMR)",
  "Three stripes, top to bottom: {white}, {red}, {green}, with an upright red stripe along the left. In the top left corner, a white emblem of two crossed swords and a curved dagger.",
  "Nizwa Fort")
c("Pakistan", "پاکستان", "Pakistan", "Islamabad", "Urdu, English", "Pakistani rupee (PKR)",
  "{Green}, with an upright {white} stripe along the left. On the green, a white crescent and a white star.",
  "The Badshahi Mosque, Lahore",
  ["Borders in Kashmir follow United Nations practice; the region is disputed."])
c("Palestine", "فلسطين", "Filastin", "East Jerusalem*", "Arabic", "Israeli new shekel (ILS)",
  "Three equal stripes, top to bottom: {black}, {white}, {green}, with a {red} triangle on the left.",
  "The Church of the Nativity, Bethlehem",
  ["Palestine proclaims East Jerusalem as its capital; its administration sits in Ramallah.",
   "The State of Palestine comprises the West Bank, including East Jerusalem, and the Gaza Strip."])
c("Philippines", "Pilipinas", "", "Manila", "Filipino, English", "Philippine peso (PHP)",
  "Two equal stripes, {blue} above {red}. From the left, a {white} triangle with a {yellow} sun of eight rays in the middle and a yellow star in each corner.",
  "The Banaue Rice Terraces")
c("Qatar", "قطر", "Qatar", "Doha", "Arabic", "Qatari riyal (QAR)",
  "{Maroon}, with a {white} band along the left edge, joined by a zigzag line with nine points.", "Al Zubarah Fort")
c("Saudi Arabia", "السعودية", "As-Saudiyah", "Riyadh", "Arabic", "Saudi riyal (SAR)",
  "{Green}. Across the upper middle runs a line of {white} Arabic writing, the declaration of faith; beneath it lies a white sword pointing to your left.",
  "The rock tombs of Hegra, AlUla")
c("Singapore", "Singapura", "", "Singapore", "English, Malay, Mandarin, Tamil", "Singapore dollar (SGD)",
  "Two equal stripes, {red} above {white}. In the top left, a white crescent with five white stars in a ring.", "The Merlion and Marina Bay")
c("South Korea", "대한민국", "Daehan Minguk", "Seoul", "Korean", "South Korean won (KRW)",
  "{White}. In the middle, a circle split by an S-shaped line: {red} above, {blue} below. In the four corners, {black} sets of three bars, some broken in the middle.",
  "Gyeongbokgung Palace, Seoul")
c("Sri Lanka", "ශ්‍රී ලංකා", "Sri Lanka", "Sri Jayawardenepura Kotte", "Sinhala, Tamil", "Sri Lankan rupee (LKR)",
  "A {gold} border runs around the flag and also splits it into two parts. On the left, two upright stripes: {green}, then {orange}. On the right, a large {maroon} panel with a gold lion facing left, a sword raised in its front paw, and a gold leaf in each corner.",
  "Sigiriya Rock",
  ["Colombo is the commercial capital."])
c("Syria", "سوريا", "Suriya", "Damascus", "Arabic", "Syrian pound (SYP)",
  "Three equal stripes, top to bottom: {green}, {white}, {black}, with three {red} stars across the white stripe.",
  "The Krak des Chevaliers",
  ["This flag was adopted in 2025."])
c("Tajikistan", "Тоҷикистон", "Tojikiston", "Dushanbe", "Tajik", "Tajikistani somoni (TJS)",
  "Three stripes, top to bottom: {red}, a wider {white}, {green}. In the middle, a {gold} crown under an arc of seven gold stars.",
  "The Hisor Fortress")
c("Thailand", "ประเทศไทย", "Prathet Thai", "Bangkok", "Thai", "Thai baht (THB)",
  "Five stripes, top to bottom: {red}, {white}, a double-height {blue}, white, red.", "Wat Arun, Bangkok")
c("Timor-Leste", "Timor-Leste", "", "Dili", "Tetum, Portuguese", "US dollar (USD)",
  "{Red}, with a {yellow} triangle from the left and, on top of it, a smaller {black} triangle holding a {white} star.",
  "Mount Ramelau")
c("Türkiye", "Türkiye", "", "Ankara", "Turkish", "Turkish lira (TRY)",
  "{Red}, with a {white} crescent and a white star left of the middle, the crescent opening toward the star.", "Hagia Sophia, Istanbul")
c("Turkmenistan", "Türkmenistan", "", "Ashgabat", "Turkmen", "Turkmen manat (TMT)",
  "{Green}. Near the left, an upright {red} stripe holding five carpet patterns one above another, in red, {orange}, {white}, {black} and {gold}, above two crossed olive branches. Beside it, a white crescent and five white stars.",
  "The Darvaza gas crater")
c("United Arab Emirates", "الإمارات", "Al-Imarat", "Abu Dhabi", "Arabic", "UAE dirham (AED)",
  "An upright {red} stripe on the left; on the right, three equal stripes: {green}, {white}, {black}.",
  "The wind towers of Al Fahidi, Dubai")
c("Uzbekistan", "Oʻzbekiston", "", "Tashkent", "Uzbek", "Uzbekistani som (UZS)",
  "Three equal stripes, top to bottom: {blue}, {white}, {green}, separated by thin {red} stripes. In the top left, a white crescent and twelve white stars.",
  "The Registan, Samarkand")
c("Vietnam", "Việt Nam", "", "Hanoi", "Vietnamese", "Vietnamese dong (VND)",
  "{Red}, with a large {yellow} five-pointed star in the middle.", "Ha Long Bay")
c("Yemen", "اليمن", "Al-Yaman", "Sana'a", "Arabic", "Yemeni rial (YER)",
  "Three equal stripes, top to bottom: {red}, {white}, {black}.", "The mud-brick towers of Shibam")

# ---------------------------------------------------------------- NORTH AMERICA & THE CARIBBEAN
c("Antigua and Barbuda", "", "", "Saint John's", "English", "East Caribbean dollar (XCD)",
  "{Red}, with a large V shape pointing down: inside it, stripes top to bottom {black}, {blue}, {white}, with a {yellow} rising sun on the black stripe.",
  "Nelson's Dockyard, English Harbour")
c("Bahamas", "", "", "Nassau", "English", "Bahamian dollar (BSD)",
  "Three equal stripes, top to bottom: {aquamarine}, {gold}, aquamarine, with a {black} triangle on the left.", "The Queen's Staircase, Nassau")
c("Barbados", "", "", "Bridgetown", "English", "Barbadian dollar (BBD)",
  "Three upright stripes, left to right: {blue}, {gold}, blue. On the gold stripe, the head of a {black} trident.", "The rocks of Bathsheba")
c("Belize", "Belize", "", "Belmopan", "English", "Belize dollar (BZD)",
  "{Royal blue}, with a narrow {red} stripe along the top and the bottom. In the middle, a {white} circle ringed by 50 {green} leaves holding the coat of arms: two men beside a shield with tools and a sailing ship, under a mahogany tree, above the motto SUB UMBRA FLOREO.",
  "Xunantunich")
c("Canada", "", "", "Ottawa", "English, French", "Canadian dollar (CAD)",
  "Three upright stripes, left to right: {red}, a double-width {white} square, red, with a red eleven-pointed maple leaf in the middle.",
  "Parliament Hill, Ottawa")
c("Costa Rica", "Costa Rica", "", "San José", "Spanish", "Costa Rican colón (CRC)",
  "Five stripes, top to bottom: {blue}, {white}, a double-height {red}, white, blue. Toward the left of the red stripe, a white oval with the coat of arms: volcanoes between two seas, ships and stars.",
  "Arenal Volcano")
c("Cuba", "Cuba", "", "Havana", "Spanish", "Cuban peso (CUP)",
  "Five stripes, top to bottom, {blue} and {white} taking turns, starting and ending with blue. From the left, a {red} triangle with a white star.",
  "El Capitolio, Havana")
c("Dominica", "", "", "Roseau", "English", "East Caribbean dollar (XCD)",
  "{Green}, crossed by a cross of three thin stripes: {yellow}, {black}, {white}. In the middle, a {red} circle with a Sisserou parrot in {purple} and green, ringed by ten green stars.",
  "Trafalgar Falls")
c("Dominican Republic", "República Dominicana", "", "Santo Domingo", "Spanish", "Dominican peso (DOP)",
  "A {white} cross divides the flag into four: {blue} top left and bottom right, {red} top right and bottom left. In the middle, a small coat of arms with a Bible and a cross between laurel and palm branches.",
  "The Cathedral of Santa María la Menor, Santo Domingo")
c("El Salvador", "El Salvador", "", "San Salvador", "Spanish", "US dollar (USD)",
  "Three equal stripes, top to bottom: {blue}, {white}, blue. In the middle, the coat of arms: a {gold}-edged triangle with five volcanoes, a cap of liberty and a rainbow, ringed by the country's name.",
  "Santa Ana Volcano")
c("Grenada", "", "", "St. George's", "English", "East Caribbean dollar (XCD)",
  "A {red} border with three {yellow} stars along the top and three along the bottom. Inside, yellow and {green} triangles meet in the middle, where a red circle holds a yellow star. On the left green triangle, a small nutmeg.",
  "The Carenage, St. George's")
c("Guatemala", "Guatemala", "", "Guatemala City", "Spanish", "Guatemalan quetzal (GTQ)",
  "Three upright stripes, left to right: {sky blue}, {white}, sky blue. In the middle, a {green} and red quetzal bird on a scroll, over crossed rifles and swords inside a laurel wreath.",
  "Temple I, Tikal")
c("Haiti", "Ayiti · Haïti", "", "Port-au-Prince", "Haitian Creole, French", "Haitian gourde (HTG)",
  "Two equal stripes, {blue} above {red}. In the middle, a {white} panel with a palm tree, cannons, flags and the motto L'UNION FAIT LA FORCE.",
  "The Citadelle Laferrière")
c("Honduras", "Honduras", "", "Tegucigalpa", "Spanish", "Honduran lempira (HNL)",
  "Three equal stripes, top to bottom: {turquoise}, {white}, turquoise, with five turquoise stars in an X on the white stripe.",
  "The Maya ruins of Copán")
c("Jamaica", "", "", "Kingston", "English", "Jamaican dollar (JMD)",
  "A {gold} diagonal cross from corner to corner, with {green} triangles at top and bottom and {black} triangles at left and right.",
  "Dunn's River Falls")
c("Mexico", "México", "", "Mexico City", "Spanish", "Mexican peso (MXN)",
  "Three upright stripes, left to right: {green}, {white}, {red}. In the middle, a {brown} eagle on a cactus eating a snake, above a wreath of oak and laurel.",
  "El Castillo, Chichén Itzá")
c("Nicaragua", "Nicaragua", "", "Managua", "Spanish", "Nicaraguan córdoba (NIO)",
  "Three equal stripes, top to bottom: {blue}, {white}, blue. In the middle, a triangle with five volcanoes, a cap of liberty and a rainbow, ringed by the country's name in {gold}.",
  "León Cathedral")
c("Panama", "Panamá", "", "Panama City", "Spanish", "Balboa (PAB), US dollar (USD)",
  "Four rectangles: top left {white} with a {blue} star, top right {red}, bottom left blue, bottom right white with a red star.",
  "The Miraflores Locks, Panama Canal")
c("Saint Kitts and Nevis", "", "", "Basseterre", "English", "East Caribbean dollar (XCD)",
  "A {black} band edged in {yellow} runs from the bottom left corner to the top right corner, with two {white} stars on it. {Green} above, {red} below.",
  "Brimstone Hill Fortress")
c("Saint Lucia", "", "", "Castries", "English", "East Caribbean dollar (XCD)",
  "{Light blue}. In the middle, a {black} triangle edged in {white}, with a {gold} triangle at its base in front.", "The Pitons")
c("Saint Vincent and the Grenadines", "", "", "Kingstown", "English", "East Caribbean dollar (XCD)",
  "Three upright stripes, left to right: {blue}, a double-width {yellow}, {green}. In the middle, three green diamonds in a V shape.",
  "La Soufrière volcano")
c("Trinidad and Tobago", "", "", "Port of Spain", "English", "Trinidad and Tobago dollar (TTD)",
  "{Red}, crossed from top left to bottom right by a {black} band edged in {white}.", "The jetty at Pigeon Point, Tobago")
c("United States", "", "", "Washington, D.C.", "English", "US dollar (USD)",
  "Thirteen stripes, top to bottom, starting and ending with red: seven {red} and six {white}, taking turns. In the top left corner, a {blue} rectangle as tall as the top seven stripes, holding 50 small white stars in nine rows of six and five, taking turns.",
  "The Statue of Liberty, New York Harbor. The bald eagle is the national bird",
  ["Alaska and Hawaii are shown at different scales.",
   "The area includes inland and coastal waters, not overseas territories."])

# ---------------------------------------------------------------- SOUTH AMERICA
c("Argentina", "Argentina", "", "Buenos Aires", "Spanish", "Argentine peso (ARS)",
  "Three equal stripes, top to bottom: {light blue}, {white}, light blue, with a {gold} sun with a face in the middle.",
  "The Perito Moreno Glacier")
c("Bolivia", "Bolivia", "", "Sucre, La Paz", "Spanish and 36 Indigenous languages", "Bolivian boliviano (BOB)",
  "Three equal stripes, top to bottom: {red}, {yellow}, {green}. In the middle, the coat of arms: an oval with the mountain of Potosí, an alpaca and the sun, framed by flags, with a condor on top.", "The Gate of the Sun, Tiwanaku",
  ["Sucre is the constitutional capital; La Paz is the seat of government."])
c("Brazil", "Brasil", "", "Brasília", "Portuguese", "Brazilian real (BRL)",
  "{Green}, with a large {yellow} diamond. Inside the diamond, a {blue} circle crossed by a curved {white} band, higher on the left than on the right, with the words ORDEM E PROGRESSO in green. Twenty-seven small white stars: one above the band, all the others below it.",
  "Sugarloaf Mountain, Rio de Janeiro. The rufous-bellied thrush is the national bird",
  ["Offshore islands, including Fernando de Noronha, are too small to show at this scale."])
c("Chile", "Chile", "", "Santiago", "Spanish", "Chilean peso (CLP)",
  "Two equal stripes, {white} above {red}. In the top left, a {blue} square with a white star.", "The moai of Rapa Nui (Easter Island)")
c("Colombia", "Colombia", "", "Bogotá", "Spanish", "Colombian peso (COP)",
  "Three stripes, top to bottom: a double-height {yellow}, {blue}, {red}.", "Las Lajas Sanctuary")
c("Ecuador", "Ecuador", "", "Quito", "Spanish", "US dollar (USD)",
  "Three stripes, top to bottom: a double-height {yellow}, {blue}, {red}. In the middle, the coat of arms: a condor above an oval showing a snow-capped volcano, a river with a steamship and the sun, framed by flags.",
  "Cotopaxi volcano")
c("Guyana", "", "", "Georgetown", "English", "Guyanese dollar (GYD)",
  "{Green}. From the left, a {gold} arrowhead edged in {white} reaches the right edge, with a {red} triangle edged in {black} inside it.",
  "Kaieteur Falls")
c("Paraguay", "Paraguay · Paraguái", "", "Asunción", "Spanish, Guarani", "Paraguayan guaraní (PYG)",
  "Three equal stripes, top to bottom: {red}, {white}, {blue}. In the middle, a round emblem with a {yellow} star in a wreath; the back of the flag carries a different emblem, a lion.",
  "The Jesuit mission of La Santísima Trinidad")
c("Peru", "Perú", "", "Lima", "Spanish, Quechua", "Peruvian sol (PEN)",
  "Three upright stripes, left to right: {red}, {white}, red. In the middle, the coat of arms: a shield with a vicuña, a cinchona tree and a horn of plenty spilling coins, in a {green} wreath.", "Machu Picchu")
c("Suriname", "Suriname", "", "Paramaribo", "Dutch", "Surinamese dollar (SRD)",
  "Five stripes, top to bottom: {green}, a thin {white}, a wide {red}, a thin white, green, with a {yellow} star in the middle.",
  "The Cathedral of Saints Peter and Paul, Paramaribo")
c("Uruguay", "Uruguay", "", "Montevideo", "Spanish", "Uruguayan peso (UYU)",
  "Nine stripes, top to bottom, {white} and {blue} taking turns, starting and ending with white. In the top left, a white square with a {gold} sun with a face.",
  "The lighthouse of Colonia del Sacramento")
c("Venezuela", "Venezuela", "", "Caracas", "Spanish", "Venezuelan bolívar (VES)",
  "Three equal stripes, top to bottom: {yellow}, {blue}, {red}, with an arc of eight {white} stars on the blue stripe.",
  "Angel Falls")

# ---------------------------------------------------------------- OCEANIA
c("Australia", "", "", "Canberra", "English", "Australian dollar (AUD)",
  "{Blue}. In the top left corner, the Union Flag in blue, {white} and {red} (see United Kingdom). Below it, a large white seven-pointed star; on the right, the five white stars of the Southern Cross.",
  "Sydney Opera House",
  ["The area covers the mainland, Tasmania and nearby islands, not the external territories."])
c("Fiji", "Viti", "", "Suva", "English, Fijian", "Fijian dollar (FJD)",
  "{Light blue}, with the Union Flag in the top left. On the right, a shield: a {red} cross on {white}, a {gold} lion at the top, and sugar cane, a coconut palm, bananas and a dove in its quarters.",
  "A drua, the traditional double-hulled canoe")
c("Kiribati", "Kiribati", "", "South Tarawa", "English, Gilbertese", "Australian dollar (AUD)",
  "The top half {red}, with a {yellow} frigatebird flying over a yellow rising sun. The bottom half has wavy stripes, {blue} and {white} taking turns.",
  "A frigatebird over Tarawa Atoll")
c("Marshall Islands", "Majel", "", "Majuro", "Marshallese, English", "US dollar (USD)",
  "{Blue}. Two widening stripes, {orange} above {white}, run from the bottom left corner to the top right corner. In the top left, a white star with 24 points.",
  "An outrigger canoe off Majuro Atoll")
c("Micronesia", "", "", "Palikir", "English", "US dollar (USD)",
  "{Light blue}, with four {white} stars in a diamond in the middle.", "The ruins of Nan Madol")
c("Nauru", "Naoero", "", "Yaren*", "Nauruan, English", "Australian dollar (AUD)",
  "{Blue}, with a thin {yellow} stripe across the middle and a {white} twelve-pointed star below it on the left.",
  "The coral pinnacles of Nauru's coast",
  ["Nauru has no official capital; government offices are in Yaren."])
c("New Zealand", "Aotearoa", "", "Wellington", "English, Māori", "New Zealand dollar (NZD)",
  "{Blue}, with the Union Flag in the top left. On the right, four {red} stars edged in {white}: the Southern Cross.",
  "Mitre Peak, Milford Sound")
c("Palau", "Belau", "", "Ngerulmud", "Palauan, English", "US dollar (USD)",
  "{Light blue}, with a {yellow} full moon set slightly left of the middle.", "The Rock Islands")
c("Papua New Guinea", "Papua Niugini", "", "Port Moresby", "Tok Pisin, English, Hiri Motu", "Papua New Guinean kina (PGK)",
  "Split from top left to bottom right: {red} above, {black} below. On the red, a {yellow} bird of paradise; on the black, the five {white} stars of the Southern Cross.",
  "A haus tambaran, the spirit house of the Sepik")
c("Samoa", "Sāmoa", "", "Apia", "Samoan, English", "Samoan tala (WST)",
  "{Red}, with a {blue} rectangle in the top left holding the five {white} stars of the Southern Cross.", "To Sua Ocean Trench")
c("Solomon Islands", "", "", "Honiara", "English", "Solomon Islands dollar (SBD)",
  "A thin {yellow} stripe runs from the bottom left corner to the top right corner. {Blue} above, with five {white} stars; {green} below.",
  "A carved war canoe")
c("Tonga", "Tonga", "", "Nuku'alofa", "Tongan, English", "Tongan paʻanga (TOP)",
  "{Red}, with a {white} rectangle in the top left holding a red cross.", "The Haʻamonga ʻa Maui trilithon")
c("Tuvalu", "Tuvalu", "", "Funafuti", "Tuvaluan, English", "Australian dollar (AUD)",
  "{Light blue}, with the Union Flag in the top left and nine {yellow} stars on the right, set out as the islands lie on a map.",
  "Funafuti Atoll")
c("Vanuatu", "Vanuatu", "", "Port Vila", "Bislama, English, French", "Vanuatu vatu (VUV)",
  "A {black} triangle on the left, edged by a {yellow} Y lying on its side that runs on as a thin band to the right edge. {Red} above, {green} below. In the black triangle, a yellow boar's tusk around two crossed fern leaves.",
  "Mount Yasur volcano")

COUNTRIES = {r["name"]: r for r in R}
