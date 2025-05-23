# ZISCON

ZISCON is de module van HiX waarin instellingen en rechten zijn geconfigureerd.
In de database vinden we voor deze module twee groepen tabellen:
`ziscon_xxx` en `config_xxx`.

## Ziscon-tabellen
De groep tabellen `ziscon_xxx` is een erg grote groep. We verdelen deze in een kleine groep 
met tabellen die relevant zijn voor het modelleren van rechten en een grote groep overige tabellen.

### Ziscon: relevante tabellen

Voor het deel van bepalen van rechten van gebruikers, rollen en groepen zijn op dit moment
de volgende tabellen als relevant bestempeld:

- `ziscon_groepen` (groepen)
- `ziscon_groepusr` (rollen, inloggroepen)
- `ziscon_groeplnk` (relaties tussen groepen en onderling, en tussen gebruikers en groepen)
- `ziscon_user` (gebruikers)

### Ziscon: overige tabellen

Dit zijn er te veel om op te noemen.

## Config-tabellen

De groep tabellen `config_xxx` is overzichtelijk. We beschrijven ze hieronder 
afzonderlijk.

### Config: overige tabellen

`config_insthelp`: dit is een lege tabel, die we derhalve kunnen negeren.

`config_trsetval`: idem

`config_insthist`: deze tabel bevat mutaties in configuraties, en lijkt niet relevant voor
het modelleren van rechten.

`config_instinfo`: deze tabel bevat toelichtingen bij sommige configuraties en bevat
slechts een beperkt aantal records.

`config_instflag`: kolommen `naam`, `speccode`, `actief`, `vlaggen`.
De functie van deze tabel - en dus ook de relevantie voor het modelleren van rechten - is nog niet duidelijk.

### config_workcontext

`config_wcsegments`: kolommen `configuredworkcontextid` (identifier), `SegmentId`(identifier),
`Disabled` (boolean). Deze tabel bevat de segmenten van een werkcontext. 

config_workcontext: kolommen `id` (identifier, primary key), `ownerid` (gebruikersnaam of groepcode),
`ownertype`, `settingid` (string), `settingsubid` (string), `segmentclassid` (string, meestal naam
van tabel of logic in HiX), `contexttype` (getal), `inverted` (boolean).

- `ownertype`: G (27135 records) of U (4912 records)
- `settingid`: alias voor setting
- `subsettingid`: alias voor subsetting, soms tabelnaam, soms leeg
- `segmentclassid`: naam van module of tabel (logic), bijvoorbeeld agenda_agenda of vrlcat
- `segmentid`: identifier voor record in tabel, bijvoorbeeld subagenda of vragenlijst-categorie

Deze tabellen kun je het beste joinen op

`config_wcsegments.configuredworkcontextid = config_workcontext.id`

### config_instvars

`config_instvars`: kolommen `naam` (naam van configuratie of recht), `owner` (eigenaar van
configuratie/recht), `insttype` (type configuratie), `speccode`
(naam  van recht wanneer naam=’ond_rechten’, samengestelde rechten),
`value` (de feitelijke instelling), `etd_status` (vaak lege kolom)

| insttype |  aantal | toelichting    | owner    |
|----------|--------:|----------------|----------|
| C        |    5671 | context        |          |
| D        |     351 | default        | chipsoft |
| G        |    6383 | global setting | chipsoft |
| L        |   70606 | local setting  |          |
| U        |  904805 | user setting   |          |

De relevante informatie zit in de kolom `VALUE`. Het is praktisch om aan het 
einde van `VALUE` bepaalde tekens te 'strip-pen', bijvoorbeeld (in hex-notatie)
'00', '01' en 'a9'.

Voor types G en D zullen we de inhoud van `VALUE` niet
beschrijven, omdat deze instellingen niet relevant zijn voor het modelleren van rechten.

Voor type U is de inhoud van `VALUE` divers. Regelmatig zien we hierin XML-strings, 
net als bij type C (zie onder). Hierin vinden we onder andere 
gebruikersvoorkeuren zoals historie, laatste vulling van invoervelden, breedte van schermen, enzovoorts.
Er zijn ook records met `owner=@Gxxxx`, dus instellingen/rechten voor groepen.

Voor type L onderscheiden we in de waarde van `VALUE` enkele eenvoudige patronen:
Lx1 (70594 records), Lx6 (8, in module Taak), Cx1 (4, in module Faktuur).
Lx1 bevat dat de waarde van `VALUE` bestaat uit 'L' gevolgd door 1 lettercode, uit onderstaande tabel.
Lx6 bevat dat de waarde van `VALUE` bestaat uit 'L' gevolgd door 6 lettercode, eveneens uit onderstaande tabel.
Cx1 bevat dat de waarde van `VALUE` bestaat uit 'C' gevolgd door 1 lettercode, uit onderstaande tabel.

Lx1 wordt gebruikt in samengestelde rechten, maar ook in enkelvoudige rechten,
bijvoorbeeld in de modules Behandeling en VPK.


| code | kleurcode   |                                                                                      |
|------|-------------|--------------------------------------------------------------------------------------|
| T    | groen       | ja                                                                                   |
| F    | rood        | nee, tenzij via overerving                                                           |
| M    | geel        | nee, tenzij met rechtgebonden werkcontext; met zwart kader: werkcontext is ingesteld |
| S    | blauw       | nee, tenzij met standaard werkcontext; met zwart kader: werkcontext is ingesteld     |
| D    | donkergrijs | nooit                                                                                |

Voor type C heeft de waarde van `VALUE` altijd hetzelfde patroon, dat we aanduiden als `C{}`
Dit patroon is een aanduiding voor werkcontexten die GUID's bevatten. De inhoud van `VALUE` is
in dit geval als volgt opgebouwd.

1. `VALUE` bestaat uit 1 of meer contexten.
2. Een context bestaat uit: X,{GUID},[T|F],<één of meer identifiers>.
3. De X staat voor het soort recht (0=inzien, 1=printen, 3=toevoegen, 4=wijzigen, 5=verwijderen, 6=alles).
4. De GUID kun je vertalen naar een logic-naam (meestal tabelnaam); op te zoeken met de expressiefunctie 
   expressie DDAliasOfGuid(), bijvoorbeeld in HiX Overzichtsgenerator.
   Het Dataplatform bevat een vertaaltabel `chipsoft_logic_table_guids` voor dit doel.
   Deze bevat de inhoud van de logic `dd_logics`. Deze vertaaltabel moet regelmatig worden ververst.
5. Na de GUID komt een T of een F. Dit is vinkje 'alles behalve' in HiX.
   Wanneer dit aanstaat zijn de hierop volgende ID's juist uitgesloten.
6. De identifiers geven aan wat er binnen de logic toegestaan is, dan wel uitgesloten is (alles behalve).
   Bijvoorbeeld: identifiers van vragenlijst-categorieën of codes van (sub)agenda's.
7. Wanneer het attribuut `naam` van het record de waarde `__CSSTD__CSSTD__`is,
   dan is het een standaard werkcontext
   (werkt op alle rechten die gevoelig zijn voor deze context).
8. Wanneer `naam` een andere waarde heeft, dan is het een rechtgebonden context;
   deze context is slechts op één recht van toepassing, namelijk het recht met deze naam.

Voorbeeld:

```
C
"1,{0D1A4B8F-CAC9-4589-933B-A8BC3175AFCB},F,""""""UCRI      """"""",
"0,{0D1A4B8F-CAC9-4589-933B-A8BC3175AFCB},T,""""""GEV       """",""""MMW       """",""""IMMDNR    """",SEKSUOLOGI,""""KLGAFG    """",""""KPP       """",""""VSRL      """",""""SCTCOO    """""""
```
