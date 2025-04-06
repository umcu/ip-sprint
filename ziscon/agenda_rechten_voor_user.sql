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
 
SELECT *
FROM           [HIX_Acc].[dbo].[ZISCON_GROEPEN] G
    inner JOIN [HIX_Acc].[dbo].[CONFIG_WORKCONTEXT] WC ON G.[CODE] = WC.[OwnerId]
    INNER JOIN [HIX_Acc].[dbo].[CONFIG_WCSEGMENTS] WCS ON WC.[ID] = WCS.[CONFIGUREDWORKCONTEXTID]
WHERE wc.[SettingId] like 'OND%'

-- settingid                 settingsubid               segmentclassid segmentid
-- AG*                       ''                         agenda_agenda  agendacode
-- OND_RECHTEN               functionaliteit in module  nadere aanduiding binnen functionaliteit, bijvoorbeeld vrlcat
 --

SELECT *
FROM           [HIX_Acc].[dbo].[ZISCON_GROEPEN] G
    inner JOIN [HIX_Acc].[dbo].[CONFIG_WORKCONTEXT] WC ON G.[CODE] = WC.[OwnerId]
    INNER JOIN [HIX_Acc].[dbo].[CONFIG_WCSEGMENTS] WCS ON WC.[ID] = WCS.[CONFIGUREDWORKCONTEXTID]
    INNER JOIN [HIX_Acc].[dbo].[AGENDA_AGENDA] A ON WCS.[SEGMENTID] = A.[AGENDA]
    WHERE wc.[SettingId] = 'AG_US_BEK'
