Chiriac Cristian-Alexandru
331CC
Tema 1 ISC


Task 1 - crypto-attack

După citirea script-ului oferit și instalarea gmpy2, am început prin a trimite
date aleatoare serverului; liniile de cod afișate de python la apariția unei
excepții m-au ajutat să înțeleg formatul datelor acceptate de server:
 - se criptează un mesaj în maniera din encrypt0r.py folosind cheia publică
   convenabil prezentă în message.txt, alături de flag-ul criptat
 - rezultatul se pune într-un dicționar cu cheia "flag"
 - dicționarul este trecut în format JSON și codat în base64

După ce am implementat acești pași, am încercat să criptez un mesaj propriu și
am descoperit că serverul nu face altceva decât să decripteze un mesaj și să
afișeze un mesaj de succes dacă s-a trimis flag-ul, altfel afișează mesajul
original, decriptat. Astfel, este necesară modificarea flag-ului criptat într-o
manieră pe care serverul să n-o poată considera flag-ul valid și care să poată
fi reversibilă. Cu ajutorul modular arithmetic[1] am folosit cheia publică
pentru a cripta numărul 2, am înmulțit rezultatul (în formatul gmpy2) cu
flag-ul din fișier (despachetat din base64, json, base64 și formatul binar al
gmpy2) și am trimis flag-ul "salted" (reîmpachetat în formatul binar al gmpy2,
base64, json și base64) către server; rezultatul primit a trebuit reconvertit
în integer, împărțit la 2 și retransformat în string, obținând astfel
flag-ul decriptat.


Task 2 - linux-acl

După analizarea tuturor căilor din variabila PATH, am continuat să explorez
binarul robot-sudo. Prin folosirea strings am descoperit fișierul acestuia de
configurare, /usr/lib/tar/gay/r0b0t3rs.conf, din care am descoperit binarul ce
va afișa flag-ul, /etc/.extra/hidden/th3CEO.

Negăsind probleme evidente de configurare a permisiunilor, mi-am directat
atenția asupra robot-sudo, pe care am vrut să îl copiez pe local; întrucât scp
returna eroarea "the input device is not a TTY", am recurs la a folosi xxd
pentru a afișa în terminal conținutul binarului robot-sudo.
Am copiat output-ul din terminal și am folosit pe local xxd cu opțiunea -r pe
acest output pentru a reobține binarul, ca apoi să îl pot analiza în ghidra[2].

Descoperirea utilizării eronate a strncmp (folosind lungimea comenzilor din
fișierul de configurare ca parametru de lungime maximă a strncmp) m-a făcut să
realizez că, dacă creez un folder cu aceeași cale ca a fișierului vacuum-control,
doar extinsă, înseamnă că pot, folosind căi relative, să execut orice
binar/script din sistem sub userul wallybot.

Am creat folderul /usr/local/bin/vacuum-controller (cu 3 caractere mai lung),
apoi am folosit calea /usr/local/bin/vacuum-controller/../robot-sudo ca
argument pentru robot-sudo ca să îl re-execut, de data aceasta ca utilizatorul
wallybot, ce are dreptul de a executa th3CEO. Apoi am analizat th3CEO în ghidra,
unde am extras parola așteptată de acesta și am folosit-o pentru a obține flag-ul.


Task 3 - binary-exploit

Primul lucru pe care l-am făcut după descărcarea arhivei a fost să utilizez
checksec[3] pentru a verifica ce mecanisme de protecție are binarul oferit. În
mod nesurprinzător, acesta a raportat No canary found și No PIE, deci un buffer
overflow/rop programming sunt metodele pe care mă așteptam să le folosesc în
rezolvare.

Folosind ghidra, am descoperit funcția vulnerabilă la buffer overflow - loop,
respectiv ținta noastră - funcția win. Găsirea offset-ului până la adresa de
retur a funcției loop (84 de octeți, deci 21 de int-uri ce trebuiesc citite de
la tastatură) a fost trivială, precum și obținerea adresei lui win (No PIE).

Ultimul pas este scrierea pe stivă a argumentului lui win, astfel încât acesta
să fie egal cu lucky_number (variabilă globală cu o valoare aleatoare, deci nu
se află pe stivă, nu o puteam suprascrie folosind buffer overflow).

Soluția pe care am găsit-o s-a bazat pe faptul că, pe unul din cazurile posibile
din loop, valoarea lui lucky_number se actualizează, iar instrucțiunea cu care
aceasta se scrie în memorie folosește ca intermediar registrul eax, căruia, prin
rop programming, îi pot da în mod trivial o valoare cunoscută. Am folosit chiar
return-ul cu valoarea 0 din loop cu acest scop, apoi am sărit direct la
instrucțiunea de scriere a lucky_number, ca, la final, să apelez win cu
argumentul 0 (valoarea lui lucky_number setată artificial de mine).

Bucata din payload ce abuzează bufferul are structura următoare:

      21 * "0\n" + addr_write_lucky_number + '\n' + 39 * "65535\n" +
      + addr_win + filler_win_ret_addr + win_param1,

unde cei 39 * 4 = 156 de octeți sunt filler pentru a fi popped de pe stivă de
către codul cuprins între addr_write_lucky_number și următorul ret, win_param1
este 0 pentru a fi egal cu noua valoare a lucky_number, addr_write_lucky_number
este 0x0804952d, iar addr_win este 0x08049236.

Payload-ul se bazează pe presupunerea că, în partea de joc de noroc, programul
va obține un rezultat ce ulterior va oferi opțiunea de a continua jocul, altfel
nu se va returna valoarea corectă 0 (hardcodată în payload ca parametru al win).
În consecință, programul rămâne un joc de noroc, întrucât este posibil să fie
necesare mai multe încercări de rulare pentru a obține rezultatul dorit.


Bibliografie:
 - [1] https://en.wikipedia.org/wiki/Modular_arithmetic
 - [2] https://github.com/NationalSecurityAgency/ghidra
 - [3] https://github.com/slimm609/checksec.sh
