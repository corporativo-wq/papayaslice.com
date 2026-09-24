import json
def b(es,en): return {"es":es,"en":en}
MENU_URL="https://claude.ai/artifact/DoMWeTromrd56uR4MHRPeL"
WATI="https://wa.me/529841798683?text=Hola%20Papaya%20Slice%2C%20quiero%20reservar"
D={
 "menuUrl":MENU_URL,
 "mq1":[b("Todo lo que necesitas es una rebanada","All you need is a slice"),b("Masa madre · 72 h","Sourdough · 72 h"),"NY · Detroit · Tokyo",b("Playa del Carmen · Cancún","Playa del Carmen · Cancún")],
 "mq2":[b("Reserva por WhatsApp","Reserve on WhatsApp"),b("Pide por Rappi o Uber Eats","Order on Rappi or Uber Eats"),b("Pizzas completas para 4–6","Whole pizzas for 4–6")],
 "dishes":[
  {"img":"sl_jamon","anchor":"rebanadas","kind":b("Rebanada NY","NY slice"),"n":b("Jamón ahumado","Smoked ham"),"d":b("Mozzarella, jamón ahumado, pesto de pistache y burrata","Mozzarella, smoked ham, pistachio pesto, burrata"),"p":130},
  {"img":"tk_cherry","anchor":"especial","kind":b("Especial del mes · Tokyo Style","Monthly special · Tokyo Style"),"n":b("Cherry & pistache","Cherry & pistachio"),"d":b("Pomodoro de cherrys, mozzarella, pesto de pistache","Cherry tomato pomodoro, mozzarella, pistachio pesto"),"p":175},
  {"img":"tk_pepperoni","anchor":"especial","kind":b("Tokyo Style","Tokyo Style"),"n":"Pepperoni","d":b("Pomodoro, mozzarella, mucho pepperoni","Pomodoro, mozzarella, lots of pepperoni"),"p":155},
  {"img":"f2","cover":True,"anchor":"focaccias","kind":b("Focaccia de masa madre","Sourdough focaccia"),"n":b("Jamón ahumado & aguacate","Smoked ham & avocado"),"d":b("Jamón ahumado, aguacate, aceite de trufa","Smoked ham, avocado, truffle oil"),"p":180},
  {"img":"pz_jamon","anchor":"completas","kind":b("Pizza completa · 8 rebanadas","Whole pizza · 8 slices"),"n":b("Jamón, pesto y burrata","Ham, pesto & burrata"),"d":b("Para 4–6 personas","Serves 4–6"),"p":690},
  {"img":"panacotta","cover":True,"anchor":"postres","kind":b("Postre","Dessert"),"n":b("Panacotta & mango","Panna cotta & mango"),"d":b("Nata premium, coulis de mango de Colima","Premium cream, Colima mango coulis"),"p":120},
 ],
 "branches":{
  "38":{"page":"playa-del-carmen","name":"Av. 38","city":"Playa del Carmen","label":b("Playa del Carmen · Av. 38","Playa del Carmen · Av. 38"),
        "addr":b("Calle 38 entre 5a Av. y Calle Flamingos, Locales Miranda #4, Centro, Playa del Carmen","Calle 38 between 5th Ave. and Calle Flamingos, Locales Miranda #4, Centro, Playa del Carmen"),"tel":"+52 984 803 5648",
        "maps":"https://www.google.com/maps/search/?api=1&query=Papaya%20Slice%20Playa%20del%20Carmen&query_place_id=ChIJNSS3HGtDTo8RPtVX0R9kA34","wa":WATI,
        "rappi":"https://www.rappi.com.mx/restaurantes/1930135819-papaya-slice-mx","uber":"https://www.ubereats.com/mx/store/papaya-slice-mx-riviera-maya/WmePdADXWy-KCQKVOP7y5Q",
        "hours":{"default":["13:00","24:00"]},"rating":"4.7","reviews":"1,002","todo":None},
  "nader":{"page":"cancun","name":"Náder","city":"Cancún","label":b("Cancún · Av. Náder","Cancún · Av. Náder"),
        "addr":b("Av. Carlos Náder 44, Centro, Cancún","Av. Carlos Náder 44, Centro, Cancún"),"tel":"+52 998 174 6115",
        "maps":"https://www.google.com/maps/search/?api=1&query=Papaya%20Slice%20Nader%20Cancun&query_place_id=ChIJP8gEC1ktTI8RI6subVZflxw","wa":WATI,
        "rappi":"https://www.rappi.com.mx/restaurantes/1930378884-papaya-slice-mx","uber":None,
        "hours":{"default":["14:00","22:00"],"1":None,"4":["14:00","23:00"],"5":["14:00","23:00"],"6":["14:00","23:00"]},"rating":"4.8","reviews":"262","todo":None},
 },
 "quotes":[
  {"t":b("La mejor rebanada de Playa. La orilla cruje y adentro es puro aire.","Best slice in Playa. The crust crackles and inside it's pure air."),"a":"Reseña de ejemplo"},
  {"t":b("Pedimos la Tokyo Style de pistache y no volvimos a hablar hasta terminarla.","We ordered the pistachio Tokyo Style and didn't speak again until it was gone."),"a":"Reseña de ejemplo"},
  {"t":b("Focaccia de masa madre con jamón y aguacate. Fin del debate.","Sourdough focaccia with ham and avocado. End of discussion."),"a":"Reseña de ejemplo"},
  {"t":b("Por rebanada puedes probar de todo. Fuimos cinco y pedimos ocho distintas.","By the slice you can try everything. Five of us ordered eight different ones."),"a":"Reseña de ejemplo"},
 ],
}
# --- build ---
imgs=json.load(open('imgs.json')); imgs.pop('aperol2',None)
h=open('landing_template.html').read()
h=h.replace('__LOGO__',imgs.pop('logo')).replace('__GIRL__',imgs.pop('girl')).replace('__LOGOW__',imgs.pop('logo_w')).replace('__LOGOCREAM__',imgs.pop('logo_cream')).replace('__PIZZA__',imgs['hero_png']).replace('__TORONJA__',imgs.pop('toronja')).replace('__APEROL1__',imgs.pop('aperol1')).replace('__HUGO__',imgs.pop('hugo'))
h=h.replace('__WATI__',WATI).replace('__MENU__',MENU_URL)
h=h.replace('__IMGS__',json.dumps(imgs)).replace('__DATA__',json.dumps(D,ensure_ascii=False))
open('../../build/papaya-slice-landing.html','w').write(h)
print(len(h)//1024,'KB')
