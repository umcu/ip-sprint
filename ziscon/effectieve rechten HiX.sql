--Effectieve rechten op gebruiker. Deze bestaan uit de rechten op alle groepen die de gebruiker effectief heeft, en de rechten die op de gebruiker zelf staan.
--De gebruiker waarvoor we de rechten willen weten:
DECLARE @gebr nvarchar(8) = 'SEHA'; --SEHA is een inloggroep, een bijzonder type gebruiker. Is in dit geval een mooie testcase

--bepalen van de effectieve groepen, met behulp van recursie,
--hier zit dubbeling in omdat hoger gelegen groepen in de boom via meerdere wegen georven kunnen worden,
--er zijn namelijk vaak meerdere groepen gekoppeld aan een gebruiker
with groepen (GROEPCODE, LINKCODE, Level)
as (
	--de groepen die aan de gebruiker gekoppeld zijn
	SELECT [GROEPCODE], [LINKCODE], 0 as Level
	FROM [HiX_Rapportage].[dbo].[ZISCON_GROEPLNK]
	where LINKCODE = @gebr
	--Haal voor alle gevonden groepen op aan welke groepen deze gekoppeld zijn, recursie totdat de hoofgroep gevonden is (deze is nergens aan gekoppeld)
	UNION ALL
	select e.[GROEPCODE], e.[LINKCODE], d.LEVEL + 1
	from [HiX_Rapportage].[dbo].[ZISCON_GROEPLNK] as e
	inner join groepen as d
		on '@G'+d.[GROEPCODE] = e.[LINKCODE] 
)
--Haal vervrolgens voor alle gevonden groepen de instellingen en rechten op uit de CONFIG_INSTVARTS tabel
SELECT recht.*
FROM [HiX_Rapportage].[dbo].[CONFIG_INSTVARS] as recht
inner join (
	SELECT DISTINCT '@G'+GROEPCODE as owner
	FROM groepen
	--Er kunnen ook rechten aan de gebruiker gekoppeld zijn
	UNION
	SELECT @gebr as owner
) eff_groepen
on recht.owner = eff_groepen.owner
order by NAAM
GO

/*******************************************************************
Om de output te interpreteren zijn de volgende dingen belangrijk:
- CONFIG_INSTVARS bevat instellingen, rechten en werkcontexten.
- Daarnaast bevat CONFIG_INSTVARS ook gebruikers voorkeuren: historie, laatste vulling van invoervelden, breedte van schermen, etc.
- Werkcontexten zijn te herkennen aan INSTTYPE "C", hiervoor geldt:
	- De value van een werkcontext is als volgt opgebouwd:
		- Er kunnen 1 of meerdere contexten ingesteld zijn
		- …Èn context bestaat uit: X,{GUID},[T|F],<Een of meerdere ID's>
		- De X staat voor de Soort werkcontext (0=inzien, 1=printen, etc.)
		- Het GUID is binnen HiX te vertalen naar een LOGIC (dit kan een tabel zijn). Hiervoor is de expressie DDAliasOfGuid() te gebruiken.
		- Na de GUID komt een T of een F. Dit is het "Alles behalve" vinkje in HiX. Wanneer dit aanstaat zijn de hierop volgende ID's juist uitgesloten
		- De ID's geven aan wat er binnen de Logic (GUID) toegestaan is, danwel uitgesloten (alles behalve)
	- Wanneer de naam "__CSSTD__CSSTD__" is, dan is het een standaard werkcontext (werkt op alle rechten die gevoelig zijn voor deze context)
	- Wanneer de naam anders is, dan is het een rechtgebonden context, deze is slechts op ÈÈn recht van toepassing
- Wanneer het instellingstype niet C is, dan kan het een recht, een instelling Ûf een voorkeur zijn. Hier heb ik geen lijn in ontdekt.
- Het lijkt er op dat er rechten voorkomen in CONFIG_INSTVARS die niet meer bestaan in HiX
********************************************************************/