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

Voor type U is de inhoud van `VALUE` divers. Regelmatig zien we hierin XLM-strings, 
net als bij type C (zie onder). Hierin vinden we onder andere 
gebruikersvoorkeuren zoals historie, laatste vulling van invoervelden, breedte van schermen, enzovoorts.
Er zijn ook records met `owner=@Gxxxx`, dus instellingen/rechten voor groepen.

Voor type L onderscheiden we in de waarde van `VALUE` enkele eenvoudige patronen:
LT (70594 records), LTTTTTT (8, in module Taak), CT (4, in module Faktuur).
LT wordt gebruikt in samengestelde rechten, maar ook in enkelvoudige rechten,
bijvoorbeeld in de modules Behandeling en VPK.

Voor type C onderscheiden we in de waarde van `VALUE` meerdere patronen.
De eenvoudige patronen zijn: Lx, Cx, Cxxxxxx, Lxxxxxx, Nd,
waarbij x een van de waardes uit onderstaande tabel is en d=1 of 2.

| code | kleurcode   |                                                                                      |
|------|-------------|--------------------------------------------------------------------------------------|
| T    | groen       | ja                                                                                   |
| F    | rood        | nee, tenzij via overerving                                                           |
| M    | geel        | nee, tenzij met rechtgebonden werkcontext; met zwart kader: werkcontext is ingesteld |
| S    | blauw       | nee, tenzij met standaard werkcontext; met zwart kader: werkcontext is ingesteld     |
| D    | donkergrijs | nooit                                                                                |

Uitzonderlijke patronen zijn `Cx` gevolgd door een identifier van 10 posities, 
en `C` direct gevolgd door een identifier.

Daarnaast zijn er twee complexe patronen, die we aanduiden als `C{}` en `C xml`. 
Het patroon `C xml` beschrijft waardes die een XML-string bevatten.
Dit zullen we in de toekomst documenteren.

Het patroon `C{}` beschrijft waardes die werkcontexten met GUID's bevatten. Deze zullen
we hieronder uitgebreid beschrijven.

1. Er kunnen 1 of meerdere contexten ingesteld zijn.
2. Eén context bestaat uit: X,{GUID},[T|F],<een of meer identifiers>
3. De X staat voor het soort recht (0=inzien, 1=printen, 3=toevoegen, 4=wijzigen, 5=verwijderen, 6=alles)
4. De GUID kun je vertalen naar een logic-naam (meestal tabelnaam); op te zoeken met de expressiefunctie 
   expressie DDAliasOfGuid(), bijvoorbeeld in HiX Overzichtsgenerator.
   Dataplatform bevat een vertaaltabel chipsoft_logic_table_guids voor dit doel. 
5. Na de GUID komt een T of een F. Dit is vinkje 'alles behalve' in HiX.
   Wanneer dit aanstaat zijn de hierop volgende ID's juist uitgesloten.
6. De ID's geven aan wat er binnen de Logic (GUID) toegestaan is, danwel uitgesloten (alles behalve)
7. Wanneer de naam "__CSSTD__CSSTD__" is, dan is het een standaard werkcontext
   (werkt op alle rechten die gevoelig zijn voor deze context).
8. Wanneer de naam anders is, dan is het een rechtgebonden context;
   deze context is slechts op één recht van toepassing.

Voorbeeld:

```
C
"1,{0D1A4B8F-CAC9-4589-933B-A8BC3175AFCB},F,""""""UCRI      """"""",
"0,{0D1A4B8F-CAC9-4589-933B-A8BC3175AFCB},T,""""""GEV       """",""""MMW       """",""""IMMDNR    """",SEKSUOLOGI,""""KLGAFG    """",""""KPP       """",""""VSRL      """",""""SCTCOO    """""""
```
