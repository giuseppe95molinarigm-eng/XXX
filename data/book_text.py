"""Running text written for the book (American English). Front-matter text from the Phase 1
Blueprint lives in build/book.py with the revisions approved in the text-revision document."""

CONTINENT = {
 "Europe": dict(
  deck="The Old World, Close Together",
  invitation="Every border here is a short train ride from the next story.",
  essay="""Nowhere else are so many countries packed so tightly together. In Europe a single day's journey can cross three languages, two alphabets and a dozen centuries, from a Roman road to a glass railway station built last year. It is a continent of old stones and short distances: cathedral towns, harbor cities, alpine passes, islands in a warm sea and forests that run to the Arctic. Its borders have moved more often than almost anywhere on earth, and many of the flags in this section are younger than the buildings drawn beside them. Travel here rewards slowness. Take the regional train rather than the plane, stay a second night, eat what the town is proud of, and learn three words of each language before you arrive. The forty-four countries that follow run from the smallest state in the world to the largest; fill them in any order you like."""),
 "Africa": dict(
  deck="The Cradle of Humankind",
  invitation="Begin with the river, the desert or the sea: each one leads on.",
  essay="""Africa is where the human story begins, and it is larger than most maps let it look: the United States, China, India and most of Europe would fit inside it at once. Its fifty-four countries hold the longest river on earth, the largest hot desert, the highest free-standing mountain and some of the oldest cities still lived in. Here are the pyramids and the great mosques of mud, the stone towers of Great Zimbabwe and the rock churches of Lalibela, coastlines of coral and coastlines of fog. It is also the continent of more than two thousand languages, and of markets, music and hospitality that most travelers remember longest. Distances are real and journeys take time, so plan generously and leave room for the day that goes differently than intended. Those days, more often than not, are the ones that end up written on these pages."""),
 "Asia": dict(
  deck="The Largest Continent",
  invitation="From the highest mountains to the busiest cities, the road is long and generous.",
  essay="""Asia holds more than half of the people on earth and the highest ground on the planet, and the forty-eight countries in this section reach from the Mediterranean shore to the Pacific. It is a continent of scale: rice terraces cut into whole mountainsides, walls that cross deserts, cities that never quite go to sleep, and quiet monasteries at the end of a long climb. The oldest written stories began here, and so did many of the world's great faiths, scripts and cuisines. Travel in Asia often means learning a new way of doing ordinary things: greeting, eating, bargaining, waiting. Accept the invitation. Eat at the stall with the longest line, take the overnight train, and keep a note of the dishes you cannot pronounce. You will want their names later, when you try to describe them to someone at home."""),
 "North America & the Caribbean": dict(
  deck="Mountains, Islands and Open Roads",
  invitation="Some journeys here are measured in miles, others in islands.",
  essay="""This section runs from the Arctic islands of Canada to the warm islands of the Caribbean, by way of deserts, prairies, volcanoes and rainforest. Its twenty-three countries include two of the largest on earth and some of the smallest, nations of a few dozen square miles where a single road loops the whole coast. Here are ancient Maya cities rising from the forest, colonial squares painted every color, national parks the size of small countries and a canal that joins two oceans. It is a region of long road trips and short ferry rides, of steel drums and fiddles, of food carried across the sea by everyone who ever arrived. Cross a border by land at least once, and take the slow boat when there is one. The Caribbean also holds many territories that are not independent countries; the note at the end of this section explains them."""),
 "South America": dict(
  deck="The Continent of Superlatives",
  invitation="Follow the Andes south, the Amazon east, and the coast wherever it goes.",
  essay="""South America is a continent of extremes: the longest mountain range above the sea, the largest rainforest, the driest desert, the highest waterfall and one of the greatest rivers on earth. Its twelve countries share a long history and two great languages, Spanish and Portuguese, alongside dozens of Indigenous ones that are still spoken every day. Here are Inca stonework that fits without mortar, cities built at the altitude of a mountain summit, glaciers that break into lakes, and beaches that never seem to end. Distances are vast, and the bus rides are part of the story. Take an overnight one at least once, wake up somewhere higher, colder or greener than where you fell asleep, and write down the first thing you see. South America has a way of staying with people long after the last stamp in the passport."""),
 "Oceania": dict(
  deck="The Ocean Continent",
  invitation="Here the sea is not the edge of the map. It is the map.",
  essay="""Oceania is made mostly of water. Its fourteen countries are scattered across the largest ocean on earth, from the vast dry heart of Australia to coral atolls that rise only a few feet above the waves. The first people to settle these islands crossed thousands of miles of open sea in canoes, steering by the stars, the swell and the flight of birds, and their descendants still keep those skills alive. Here are reefs you can see from space, volcanoes still smoking, fjords cut deep into green mountains and islands where the nearest neighbor is a day's sailing away. Time moves differently in the Pacific. Let it. Arrive without too many plans, accept the invitation to sit and talk, and watch the light change over the lagoon in the evening. It will be one of the pages you remember best."""),
}

BUCKET = {
 "Europe": [
  ("Climb to the top of the Eiffel Tower", "France"), ("Watch the sun set over the caldera of Santorini", "Greece"),
  ("Walk the city walls of Dubrovnik", "Croatia"), ("Cross Charles Bridge in Prague at dawn", "Czechia"),
  ("See the Northern Lights above the Arctic Circle", "Norway, Sweden, Finland or Iceland"),
  ("Take a gondola through the canals of Venice", "Italy"), ("Hike a stretch of the Alps between two huts", "Switzerland or Austria"),
  ("Hear a fado singer in Lisbon", "Portugal"), ("Cycle past the windmills of Kinderdijk", "Netherlands"),
  ("Visit the Alhambra in Granada", "Spain"), ("Bathe in a thermal bath in Budapest", "Hungary"),
  ("Ride the Trans-Siberian Railway for at least one night", "Russia"),
  ("Walk the Royal Mile to Edinburgh Castle", "United Kingdom"),
  ("Stand on the Cliffs of Moher in the wind", "Ireland"), ("Row across Lake Bled to its island church", "Slovenia")],
 "Africa": [
  ("Stand before the Pyramids of Giza", "Egypt"), ("Watch the Great Migration cross the Mara", "Kenya or Tanzania"),
  ("Feel the spray of Victoria Falls", "Zambia or Zimbabwe"), ("Climb a dune at sunrise in Sossusvlei", "Namibia"),
  ("Track mountain gorillas in the Virunga volcanoes", "Rwanda or Uganda"),
  ("Get lost in the medina of Marrakesh", "Morocco"), ("Take the cable car up Table Mountain", "South Africa"),
  ("Walk among the baobabs at sunset", "Madagascar"), ("Visit the rock-hewn churches of Lalibela", "Ethiopia"),
  ("Reach the summit of Kilimanjaro", "Tanzania"), ("Glide through the Okavango Delta in a mokoro canoe", "Botswana"),
  ("See the Great Mosque of Djenné", "Mali"), ("Explore the Roman ruins of Leptis Magna or El Jem", "Libya or Tunisia"),
  ("Snorkel the coral reefs of Zanzibar", "Tanzania"), ("Spend a night under the stars in the Sahara", "Algeria, Morocco or Tunisia")],
 "Asia": [
  ("Walk a section of the Great Wall", "China"), ("See the Taj Mahal at sunrise", "India"),
  ("Watch the sun rise over Angkor Wat", "Cambodia"), ("See the cherry blossoms in Kyoto", "Japan"),
  ("Cruise among the islands of Ha Long Bay", "Vietnam"), ("Enter Petra through the Siq", "Jordan"),
  ("Fly over Cappadocia in a hot-air balloon", "Türkiye"), ("Trek toward Everest Base Camp", "Nepal"),
  ("Climb to the Tiger's Nest monastery", "Bhutan"), ("Walk the Registan in Samarkand", "Uzbekistan"),
  ("Visit Borobudur at first light", "Indonesia"), ("Stay a night in a traditional ryokan", "Japan"),
  ("Climb Sigiriya Rock", "Sri Lanka"), ("Eat your way through a night market", "Thailand or Malaysia"),
  ("Sleep in a ger on the Mongolian steppe", "Mongolia")],
 "North America & the Caribbean": [
  ("Stand at the rim of the Grand Canyon", "United States"), ("See the Statue of Liberty from the water", "United States"),
  ("Watch the Northern Lights in the Yukon", "Canada"), ("Paddle a canoe on Moraine Lake", "Canada"),
  ("Climb the pyramids of Teotihuacan", "Mexico"), ("Watch the light at Chichén Itzá on the equinox", "Mexico"),
  ("Swim in a cenote", "Mexico"), ("Ride in a classic car through Old Havana", "Cuba"),
  ("Watch a ship pass through the Panama Canal", "Panama"), ("Hike to the top of a volcano", "Guatemala, Costa Rica or El Salvador"),
  ("Dive the Great Blue Hole", "Belize"), ("See the Pitons from the sea", "Saint Lucia"),
  ("Join Carnival in Port of Spain", "Trinidad and Tobago"), ("Visit Tikal at dawn", "Guatemala"),
  ("Drive a stretch of the Pacific Coast Highway", "United States")],
 "South America": [
  ("Walk the Inca Trail to Machu Picchu", "Peru"), ("Stand on the salt flats of Uyuni", "Bolivia"),
  ("Hear the roar of Iguazú Falls", "Argentina or Brazil"), ("See Angel Falls, the highest waterfall on earth", "Venezuela"),
  ("Watch the Perito Moreno Glacier calve", "Argentina"), ("Hike the towers of Torres del Paine", "Chile"),
  ("Meet the wildlife of the Galápagos", "Ecuador"), ("Spend a night in the Amazon rainforest", "Brazil, Peru or Colombia"),
  ("Take the cable car up Sugarloaf Mountain", "Brazil"), ("Dance a tango in Buenos Aires", "Argentina"),
  ("Stand among the moai of Rapa Nui", "Chile"), ("Walk the colorful walled city of Cartagena", "Colombia"),
  ("Cross Lake Titicaca to its islands", "Peru or Bolivia"), ("Stargaze in the Atacama Desert", "Chile"),
  ("See Kaieteur Falls from the edge", "Guyana")],
 "Oceania": [
  ("Snorkel the Great Barrier Reef", "Australia"), ("Watch the sun set over Uluru", "Australia"),
  ("See a performance at the Sydney Opera House", "Australia"), ("Cruise Milford Sound", "New Zealand"),
  ("Walk the Tongariro Alpine Crossing", "New Zealand"), ("Swim in the To Sua Ocean Trench", "Samoa"),
  ("Kayak through the Rock Islands", "Palau"), ("Stand at the rim of Mount Yasur", "Vanuatu"),
  ("Join a kava ceremony in a village", "Fiji"), ("Explore the ruins of Nan Madol", "Micronesia"),
  ("Dive a Second World War wreck", "Solomon Islands or Papua New Guinea"), ("Watch whales off the coast", "Tonga"),
  ("Visit a village in the Highlands", "Papua New Guinea"), ("Sleep on an atoll where the road ends at the sea", "Kiribati, Tuvalu or Marshall Islands"),
  ("Sail between islands on an inter-island ferry", "Fiji, Samoa or Tonga")],
}

CARIBBEAN_NOTE = """Not every island in the Caribbean is a country. Alongside the thirteen independent states in this section, the region holds more than a dozen territories that belong to, or are freely associated with, countries elsewhere. Puerto Rico and the U.S. Virgin Islands are territories of the United States. Anguilla, Bermuda, the British Virgin Islands, the Cayman Islands, Montserrat and the Turks and Caicos Islands are British Overseas Territories. Aruba, Curaçao and Sint Maarten are countries within the Kingdom of the Netherlands, and Bonaire, Sint Eustatius and Saba are special municipalities of the Netherlands. Guadeloupe and Martinique are overseas regions of France, and Saint Martin and Saint Barthélemy are French overseas collectivities. Many of them have their own flags, and all of them are well worth the journey. Because they are not independent countries, they do not have pages of their own in this book; record them here, or on the notes pages at the end of this section."""

COLOR_NOTE = """This book is printed on cream uncoated paper, chosen because it takes color the way a good sketchbook does: softly, and in layers.

Colored pencils are the right tool. Work lightly at first and build the color up in several passes; the paper will hold far more pigment than you expect. Watercolor pencils work too, if you use them almost dry.

Avoid markers, felt-tip pens and heavy ink. They soak through uncoated paper and will mark the country on the other side of the page.

Before you color a flag, color its little circles first. They give you the colors in the order they appear, and they become your key. If you are unsure which part takes which color, A Register of Colors at the back of the book explains every flag in words.

Use the notes pages at the back of the book to test a new pencil or a new shade before you commit to a page.

And remember: there is no wrong way to do this. A flag colored on a train, with the only blue you had, is still the right flag."""

PROFILE_FIELDS = ["Name", "Home country", "Home town", "Languages I speak", "Languages I have attempted",
                  "The first journey I remember", "The place that started it all", "What I travel for",
                  "My favorite way to travel", "Countries visited before this book", "The one place I most want to see"]

BEST_THINGS = ["The best meal", "The worst bed", "The kindest stranger", "The hardest border", "The longest wait",
               "The most beautiful view", "The best journey by train, boat or road", "The strangest thing I ate",
               "The place I would return to first", "The place I will never return to"]

TOP_FIVE = ["Beaches", "Sunsets", "Restaurants", "Cities", "Hikes and walks", "Museums",
            "Markets", "Train, boat and road journeys", "Places to swim", "Festivals and celebrations",
            "Views from the top", "Places I slept"]

LEDGER = ["Countries visited, of 195", "Continents visited, of 6", "Journeys taken", "Nights away from home",
          "Borders crossed by land", "Flights taken", "The longest flight", "The longest single journey",
          "The highest point I stood on", "The lowest point I stood on", "The farthest from home",
          "Time zones crossed in one trip", "Islands visited", "Seas and oceans swum in",
          "Languages heard", "Currencies spent", "Times I got lost", "Passports filled"]
