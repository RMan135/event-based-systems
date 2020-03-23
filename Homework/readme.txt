Echipa: Razvan Baisan, Cabac Dorina

Generatorul de publicatii si subscriptii se poate configura din fisierul
de configurare config.json

Campurile posibile apar sub cheia "keys" din fisierul de configurare.

Fiecare camp trebuie sa aiba un tip ("type") si reguli pentru generarea
valorii ("rules") si a regulilor subscriptiilor ("subscription_rules").

La regulile de generare a valorii putem avea o cheie "possible_values" care
va dicta toate valorile posibile pentru campul respectiv. Daca nu avem o
astfel de cheie trebuie sa fie prezente alte reguli pentru generare (de ex.
valoarea minima si maxima la tipul double sau data de inceput si sfarsit a
unei perioade de timp pentru tipul date)

La regulile de generare a subscriptiei putem avea procentul minim de aparitii
a campului respectiv si daca dorim, procentele minime de aparitie pentru 
diferiti operatori.

Mai avem in fisierul de configurare cheile "publication_generation" si 
"subscription_generation" care momentan tin doar numarul dorit de publicatii,
respectiv subscriptii.

Tot in fisierul de configurare avem cheia "types" care contine informatii despre
tipurile de date (momentan doar operatorii disponibili).