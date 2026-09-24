import json
def b(es, en): return {"es": es, "en": en}

MENU = [
 {"id":"especial","kind":"featured","short":b("Especial del mes","Monthly special"),
  "eyebrow":b("Especial del mes · Agosto","Monthly special · August"),
  "title":"Tokyo Style", "sub":b("Nuestra nueva era de pizza","A new era of pizza"),
  "traits":[b("Masa madre","Sourdough"),b("Doble fermentación 72 h","72-hour double fermentation"),b("Recién horneada","Fresh out of the oven"),b("Fluffy & ligera","Fluffy & light"),b("Jugosa & sabrosa","Juicy & flavorful")],
  "note":b("Disponibilidad limitada. Las imágenes son ilustrativas.","Limited availability. Photos are illustrative."),
  "items":[
   {"n":b("Salchicha italiana & pesto","Italian sausage & pesto"),"d":b("Pesto, burrata, salchicha italiana","Basil pesto, italian sausage, burrata cheese"),"p":195,"img":"tk_salchicha","cut":True},
   {"n":b("Cherry & pistache","Cherry & pistachio"),"d":b("Pomodoro de cherrys, queso mozzarella, pesto de pistache","Cherry tomato pomodoro, mozzarella cheese, pistachio pesto"),"p":175,"img":"tk_cherry","cut":True},
   {"n":b("Tartufata","Tartufata"),"d":b("Tartufata, queso, miel, aceite de trufa, crema de trufa","Truffle sauce, mozzarella cheese, olive oil, truffle cream, honey"),"p":165,"img":"tk_tartufata","cut":True},
   {"n":b("Pepperoni","Pepperoni"),"d":b("Pomodoro, queso mozzarella, mucho pepperoni","Pomodoro, mozzarella cheese, lots of pepperoni"),"p":155,"img":"tk_pepperoni","cut":True},
  ]},

 {"id":"rebanadas","kind":"list","title":b("Rebanadas de pizza","Pizza slices"),"short":b("Rebanadas","Slices"),
  "styles":[b("Estilo NY · delgada","NY style · thin"),b("Estilo Detroit · gruesa, de charola","Detroit style · thick, pan-baked")],"note":b("Elige tu estilo. Mismo precio.","Choose your style. Same price."),
  "items":[
   {"n":b("Margarita","Margherita"),"d":b("Tomates italianos, mozzarella, albahaca","Italian tomatoes, mozzarella cheese, basil"),"p":110},
   {"n":"Pepperoni","d":b("Tomates italianos, mozzarella, pepperoni","Italian tomatoes, mozzarella cheese, pepperoni"),"p":115},
   {"n":b("Cebolla caramelizada & pistache","Caramelized onion & pistachio"),"d":b("Queso mozzarella, cebolla caramelizada, pistache","Mozzarella cheese, caramelized onions, pistachio"),"p":115,"nuevo":True},
   {"n":b("Jamón ahumado","Smoked ham"),"d":b("Mozzarella, jamón ahumado, pesto de pistache y burrata","Mozzarella cheese, smoked ham, pistachio pesto, burrata cheese"),"p":130,"img":"sl_jamon","cut":True},
   {"n":"Bacon lovers","d":b("Pomodoro, mozzarella, mermelada de tocino, burrata derretida, pancetta","Italian tomatoes, mozzarella, bacon jam, melted burrata, pancetta"),"p":130,"nuevo":True},
   {"n":b("Hawaiana","Hawaiian"),"d":b("Tomates italianos, mozzarella, pancetta, piña","Italian tomatoes, mozzarella, pancetta, pineapple"),"p":135},
   {"n":b("Trufa & hongos","Truffle & mushrooms"),"d":b("Mozzarella, crema de trufa, setas & hongos","Mixed mushrooms, mozzarella cheese, truffle cream"),"p":135},
   {"n":b("Trufa & pancetta","Truffle & pancetta"),"d":b("Mozzarella, crema de trufa, pancetta ahumada","Mozzarella, truffle cream, smoked pancetta"),"p":145},
   {"n":b("Arúgula & burrata","Arugula & burrata"),"d":b("Arúgula, burrata, jamón ahumado, mozzarella, pomodoro","Arugula, burrata cheese & smoked ham, on top of a margherita slice"),"p":145,"nuevo":True},
   {"n":"PPP","d":b("Tomates italianos, mozzarella, pepperoni, burrata, miel spicy","Italian tomatoes, mozzarella cheese, pepperoni, burrata cheese, hot honey"),"p":150},
   {"n":"Meat loooovers","d":b("Pomodoro, mozzarella, pepperoni, salchicha italiana, pancetta, albóndigas, pomodoro extra","Italian tomatoes, mozzarella, pepperoni, italian sausage, meatballs, pancetta, extra tomato sauce"),"p":165},
  ],
  "pills":{"title":b("Toppings & dips · pasa tu pizza al siguiente nivel","Toppings & dips · take your pizza to the next level"),"p":30,"opts":[
   {"n":b("Arúgula","Arugula"),"g":"20 g"},{"n":b("Aceite de trufa","Truffle oil"),"g":"10 g"},{"n":b("Hongos al ajillo","Garlic mushrooms"),"g":"70 g"},{"n":b("Mermelada de tocino","Bacon jam"),"g":"30 g"},{"n":b("Pesto de pistache","Pistachio pesto"),"g":"20 g"},{"n":b("Miel habanero","Habanero honey"),"g":"20 g"},{"n":b("Crema de burrata","Burrata cream"),"g":"90 g"}]}},

 {"id":"completas","kind":"list","title":b("Pizzas completas","Whole pizzas"),"short":b("Pizzas completas","Whole pizzas"),"sub":b("Detroit o NY · 8 rebanadas · para 4–6 personas","Detroit or NY · 8 slices · serves 4–6"),
  "items":[
   {"n":b("Margarita","Margherita"),"p":570},
   {"n":"Pepperoni","p":620},
   {"n":b("Hawaiana","Hawaiian"),"p":650},
   {"n":b("Trufa y hongos","Truffle & mushrooms"),"p":650},
   {"n":b("Jamón, pesto y burrata","Ham, pesto & burrata"),"d":b("Mozzarella, jamón ahumado, pesto de pistache, burrata, albahaca","Mozzarella, smoked ham, pistachio pesto, burrata, basil"),"p":690,"img":"pz_jamon","cut":True},
  ]},

 {"id":"focaccias","kind":"list","title":b("Focaccias de masa madre","Sourdough focaccias"),"short":b("Focaccias","Focaccias"),
  "note":b("Elige tu focaccia: fresca (crema de burrata) ó horneada (mozzarella & cheddar).","Choose your focaccia: fresh (burrata cream) or baked (mozzarella & cheddar)."),
  "items":[
   {"num":1,"n":b("Meatballs & pomodoro","Meatballs & pomodoro"),"d":b("Focaccia de masa madre, meatballs, mucha salsa pomodoro","Sourdough focaccia, meatballs, pomodoro sauce"),"p":250,"img":"f1"},
   {"num":2,"n":b("Jamón ahumado & aguacate","Smoked ham & avocado"),"d":b("Focaccia de masa madre, jamón ahumado, aguacate, aceite de trufa","Sourdough focaccia, smoked ham, avocado, truffle oil"),"p":180,"img":"f2"},
   {"num":3,"n":b("Jamón ahumado & pesto","Smoked ham & pesto"),"d":b("Focaccia de masa madre, jamón ahumado, pesto","Sourdough focaccia, smoked ham, basil pesto"),"p":180,"img":"f3"},
   {"num":4,"n":b("Pancetta, jamón ahumado, cebolla & miel","Pancetta, smoked ham, onion & honey"),"d":b("Focaccia de masa madre, pancetta, jamón ahumado, miel picante, cebolla caramelizada","Sourdough focaccia, italian pancetta, smoked ham, hot honey, caramelized onions"),"p":250},
   {"num":5,"n":b("Veggie mix & pesto rojo","Veggie mix & red pesto"),"d":b("Focaccia de masa madre, aguacate, pesto de tomate deshidratado, arúgula, reducción de balsámico","Sourdough focaccia, avocado, red pesto, arugula, balsamic glaze"),"p":180,"img":"f5","land":True},
   {"num":6,"n":b("Jamón ahumado, trufa & miel","Smoked ham, truffle & honey"),"d":b("Focaccia de masa madre, jamón ahumado, tartufata italiana, miel picante","Sourdough focaccia, smoked ham, italian truffle, hot honey"),"p":180,"img":"f6"},
  ],
  "pills":{"title":b("Extras","Extras"),"p":30,"opts":[{"n":b("Aguacate","Avocado")},{"n":b("Hot honey","Hot honey")},{"n":b("Arúgula","Arugula")}]}},

 {"id":"entradas","kind":"list","title":b("Para empezar","To start"),"short":b("Para empezar","Starters"),
  "items":[
   {"n":b("Tomates cherry & burrata al horno","Baked cherry tomatoes & burrata"),"d":b("Tomates cherry rostizados, burrata fresca, albahaca, aceite de oliva","Roasted cherry tomatoes, fresh burrata, basil, olive oil"),"p":90,"nuevo":True,"img":"tomates"},
   {"n":b("Meatballs","Meatballs"),"d":b("Carne molida 100% angus, parmesano, aceite de oliva. Elige tu salsa: pesto, spicy vodka o trufa","100% angus beef, parmesan, olive oil. Choose your sauce: pesto, spicy vodka or truffle"),"p":160},
  ]},

 {"id":"ensaladas","kind":"list","title":b("Ensaladas","Salads"),"price":130,
  "items":[
   {"n":b("Burrata y trufa","Burrata & truffle"),"d":b("Arúgula baby, pistache, reducción de balsámico, aceite de trufa, burrata, láminas de parmesano","Baby arugula, pistachio, balsamic glaze, truffle oil, burrata, parmesan shavings"),"nuevo":True},
   {"n":b("Arúgula & jamón ahumado","Arugula & smoked ham"),"d":b("Arúgula baby, pesto rojo, reducción de balsámico, jamón ahumado, nueces de la India tostadas","Baby arugula, red pesto, balsamic glaze, smoked ham, toasted cashews"),"nuevo":True},
  ]},

 {"id":"pastas","kind":"pasta","title":b("Pastas","Pastas"),"price":200,"sub":b("Arma la tuya en 3 pasos","Build yours in 3 steps"),
  "recLabel":b("Recomendamos","We recommend"),
  "steps":[
   {"title":b("Elige la forma","Choose the shape"),"opts":[{"n":"Gnocchi"},{"n":"Rigatoni"},{"n":"Ravioli"}]},
   {"title":b("Elige la salsa","Choose the sauce"),"opts":[
     {"n":"Pesto","rec":b("burrata y pancetta","burrata & pancetta"),"plus":90},
     {"n":"Spicy vodka","rec":b("albóndigas","meatballs"),"plus":55},
     {"n":b("Trufa","Truffle"),"rec":b("hongos y pancetta","mushrooms & pancetta"),"plus":70}]},
   {"title":b("Elige los toppings","Choose your toppings"),"opts":[],
    "groups":[
     {"n":b("Toppings premium","Premium toppings"),"p":55,"opts":[{"n":b("Salchicha","Sausage"),"g":"40 g"},{"n":b("Albóndigas","Meatballs"),"g":"25 g"},{"n":"Pancetta","g":"40 g"},{"n":b("Crema de burrata","Burrata cream"),"g":"90 g"}]},
     {"n":b("Toppings","Toppings"),"p":30,"opts":[{"n":b("Hongos al ajillo","Garlic mushrooms"),"g":"70 g"},{"n":b("Aceite de trufa","Truffle oil"),"g":"10 g"}]}]}],
  "extra":[{"n":b("Lasagna con burrata","Burrata lasagna"),"d":b("Lasagna con burrata, pesto rojo y ragú de 8 horas","Lasagna with burrata, red pesto and 8-hour ragù"),"p":250,"nuevo":True,"img":"lasagna","land":True}]},

 {"id":"postres","kind":"cards","title":b("Postres","Desserts"),"price":120,
  "items":[
   {"n":b("Panacotta & mango","Panna cotta & mango"),"d":b("Nata premium, coulis de mango natural de Colima","Premium cream, natural Colima mango coulis"),"nuevo":True,"img":"panacotta"},
   {"n":b("Tiramisú de pistache","Pistachio tiramisu"),"d":b("Mascarpone y pistache, soletillas con espresso & amaretto, pistache triturado","Pistachio mascarpone, espresso & amaretto-soaked ladyfingers, crushed pistachio")},
   {"n":b("Panacotta & aceite de oliva","Panna cotta & olive oil"),"d":b("Nata premium, aceite de oliva extra virgen D.O.P. italiano y una pizca de sal rosa del Himalaya","Premium cream, Italian D.O.P. extra virgin olive oil and a pinch of Himalayan pink salt"),"nuevo":True},
  ]},

 {"id":"bebidas","kind":"drinks","title":b("Bebidas","Drinks"),"glass":b(" copa"," glass"),"bottle":b(" botella"," bottle"),
  "groups":[
   {"n":b("Spritzs & sangría","Spritzes & sangria"),"items":[
     {"n":"Aperol spritz","p":150},{"n":"Campari spritz","p":150},{"n":"Hugo spritz","p":180},{"n":"Toronja spritz","d":b("Toronja, prosecco y soda","Grapefruit, prosecco and soda"),"p":175,"nuevo":True},{"n":b("Sangría tinta","Red sangria"),"p":175}]},
   {"n":b("Bebidas suaves","Soft drinks"),"items":[
     {"n":b("Cerveza","Beer"),"d":"Heineken, Indio","p":70},
     {"n":b("Limonadas","Lemonades"),"d":b("Limón, jamaica, mango","Lime, hibiscus, mango"),"p":75},
     {"n":b("Sodas","Sodas"),"d":"Coca-Cola, Fanta, Sprite","p":65},
     {"n":"Félix","d":b("Manzana, guayaba","Apple, guava"),"p":65},
     {"n":b("Agua Ciel","Ciel water"),"p":60},{"n":"Topo Chico","p":70}]},
   {"n":b("Cerveza artesanal mexicana","Mexican craft beer"),"items":[
     {"n":"Colimita","d":"Lager","p":110},{"n":"Piedra Lisa","d":"Session IPA","p":115},{"n":"Principia Espectra","d":"IPA","p":140}]},
   {"n":b("Cocteles","Cocktails"),"items":[
     {"n":b("Margarita de la casa","House margarita"),"p":99},{"n":b("Cocteles clásicos","Classic cocktails"),"p":180}]},
   {"n":b("Vino mexicano · blancos","Mexican wine · whites"),"wine":True,"items":[
     {"n":"Puerto Nuevo · Sauvignon blanc","d":"Valle de Guadalupe, Baja California","p":99,"p2":450},
     {"n":"L.A. Cetto Verano · Sauvignon blanc","d":"Valle de Guadalupe, Baja California","p":175,"p2":660}]},
   {"n":b("Vino mexicano · tintos","Mexican wine · reds"),"wine":True,"items":[
     {"n":"Puerto Nuevo · Cabernet malbec","d":"Valle de Guadalupe, Baja California","p":99,"p2":450},
     {"n":"L.A. Cetto Invierno · Petit verdot","d":"Valle de Guadalupe, Baja California","p":175,"p2":660},
     {"n":"Megacero","d":"Encinillas, Chihuahua","p":1490}]},
  ]},
]

imgs = json.load(open('imgs.json'))
logo = imgs.pop('logo')
html = open('menu_template.html').read()
html = html.replace('__LOGOW__', imgs.pop('logo_w')).replace('__LOGO__', logo).replace('__IMGS__', json.dumps(imgs)).replace('__MENU__', json.dumps(MENU, ensure_ascii=False))
open('../../build/papaya-slice-menu.html','w').write(html)
print(len(html)//1024, 'KB')
