SELECT GU.[USERCODE], GU.[GRPUSRCODE], GL.[GROEPCODE], G.[OMSCHR], A.[NAAM], A.[OMSCHR], A.[AGENDA]
FROM           [HIX_Acc].[dbo].[ZISCON_GROEPUSR] GU
    inner JOIN [HIX_Acc].[dbo].[ZISCON_GROEPLNK] GL ON ((GU.[GRPUSRCODE] = GL.[LINKCODE]) OR (GU.[USERCODE] = GL.[LINKCODE]))
    inner JOIN [HIX_Acc].[dbo].[ZISCON_GROEPEN]  G  ON GL.[GROEPCODE] = G.[CODE]
    inner JOIN [HIX_Acc].[dbo].[CONFIG_WORKCONTEXT] WC ON G.[CODE] = WC.[OwnerId]
    inner JOIN [HIX_Acc].[dbo].[CONFIG_WCSEGMENTS] WCS ON WC.[ID] = WCS.[CONFIGUREDWORKCONTEXTID]
    inner JOIN [HIX_Acc].[dbo].[AGENDA_AGENDA] A ON WCS.[SEGMENTID] = A.[AGENDA]
WHERE  GU.[USERCODE] = 'LVOS13' and wc.[SettingId] = 'AG_US_BEK'

SELECT GU.[USERCODE], GU.[GRPUSRCODE], GL.[GROEPCODE], G.[OMSCHR]
FROM           [HIX_Acc].[dbo].[ZISCON_GROEPUSR] GU
    inner JOIN [HIX_Acc].[dbo].[ZISCON_GROEPLNK] GL ON ((GU.[GRPUSRCODE] = GL.[LINKCODE]) OR (GU.[USERCODE] = GL.[LINKCODE]))
    inner JOIN [HIX_Acc].[dbo].[ZISCON_GROEPEN]  G  ON GL.[GROEPCODE] = G.[CODE]
WHERE  GU.[USERCODE] = 'LVOS13'

-- USERCODE	GRPUSRCODE	GROEPCODE   OMSCHR
-- LVOS13	ZH001407	ZH1178      Arts in opleiding Interne Geneeskunde (UMC)
-- LVOS13	ZH001407	ZH0003      Aanvullend - Mag inloggen met testgebruikers UMC Utrecht
--
-- Inspectie in HiX: lvos13 is lid van slechts 1 groep, g.code = gl.groepcode = ZH1178. Komt overeen met query-resultaat.
-- Als je van deze groep de agenda-rechten opzoekt, krijg je slechts deze: ZH0021, ZH0022, ZH0023, ZH0025, ZH0026, ZH0027, ZH0028, ZH0086
-- dit is alleen B&O!!!
-- in welke werkcontext-segmenten komt (bijv) ZH0096 (endocrinologie) voor?
-- daarvoor moet je weten wat de parent-groepen, grandparent-groepen, ... van ZH1178 zijn. 
-- dat vind je in ziscon_groeplnk: alle records met linkcode = '@GZH1178' 

SELECT *
FROM           [HIX_Acc].[dbo].[ZISCON_GROEPEN] G
    inner JOIN [HIX_Acc].[dbo].[CONFIG_WORKCONTEXT] WC ON G.[CODE] = WC.[OwnerId]
    INNER JOIN [HIX_Acc].[dbo].[CONFIG_WCSEGMENTS] WCS ON WC.[ID] = WCS.[CONFIGUREDWORKCONTEXTID]

SELECT *
FROM           [HIX_Acc].[dbo].[ZISCON_GROEPEN] G
    inner JOIN [HIX_Acc].[dbo].[CONFIG_WORKCONTEXT] WC ON G.[CODE] = WC.[OwnerId]
    INNER JOIN [HIX_Acc].[dbo].[CONFIG_WCSEGMENTS] WCS ON WC.[ID] = WCS.[CONFIGUREDWORKCONTEXTID]
    INNER JOIN [HIX_Acc].[dbo].[AGENDA_AGENDA] A ON WCS.[SEGMENTID] = A.[AGENDA]
    WHERE wc.[SettingId] = 'AG_US_BEK'


-- exporteren voor data-inspectie met Python
-- SELECT * FROM [HIX_Acc].[dbo].[ZISCON_GROEPEN]
-- SELECT * FROM [HIX_Acc].[dbo].[ZISCON_GROEPUSR]
-- SELECT * FROM [HIX_Acc].[dbo].[ZISCON_GROEPLNK]
