SELECT g.code, g.searchcode,
       wc.SettingId, wc.SettingSubId, wc.SegmentClassId, wc.[ContextType], wc.[Inverted],
       wcs.SegmentId,
       iv.INSTTYPE, iv.speccode, iv.[VALUE]
FROM           [HIX_Acc].[dbo].[ZISCON_GROEPEN] G
    INNER JOIN [HIX_Acc].[dbo].[CONFIG_WORKCONTEXT] WC ON G.[CODE] = WC.[OwnerId]
    INNER JOIN [HIX_Acc].[dbo].[CONFIG_WCSEGMENTS] WCS ON WC.[ID] = WCS.[CONFIGUREDWORKCONTEXTID]
    INNER JOIN [HIX_Acc].[dbo].[CONFIG_INSTVARS] IV on ((iv.[owner] = wc.OwnerId) and (iv.naam = wc.SettingId))
WHERE wcs.Disabled = 'false' and g.searchcode like 'ZH%'

SELECT wc.ownerid, wc.OwnerType, iv.OWNER,
       wc.SettingId, wc.SettingSubId, wc.SegmentClassId, wc.[ContextType], wc.[Inverted],
       wcs.SegmentId, wcs.Disabled,
       iv.INSTTYPE, iv.speccode, iv.[VALUE]
FROM           [HIX_Acc].[dbo].[CONFIG_WORKCONTEXT] WC
    INNER JOIN [HIX_Acc].[dbo].[CONFIG_WCSEGMENTS] WCS ON WC.[ID] = WCS.[CONFIGUREDWORKCONTEXTID]
    INNER JOIN [HIX_Acc].[dbo].[CONFIG_INSTVARS] IV on iv.naam = wc.SettingId
WHERE wcs.Disabled = 'false' and wc.ownertype = 'G'
      and wc.[SettingId] = 'AG_US_BEK' and wc.OwnerId = 'ZH0125'

-- config_instflag:
--   naam, speccode, actief, vlaggen

-- config_wcsegments (koppeltabel):
--   configuredworkcontextid <-> config_workcontext.id, segmentid, disabled (boolean)

-- config_workcontext:
--   id=PK, ownerid <-> username/group code, ownertype, settingid, settingsubid, segmentsclassid, contexttype, inverted (boolean)
--   ownertype: G (27135) of U (4912)
--   settingid: alias voor setting
--   subsettingid: alias voor subsetting, soms tabelnaam, soms leeg
--   segmentclassid: module of tabel, bijvoorbeeld agenda_agenda of vrlcat
--   segmentid: agenda-id, vrlcat-id enzovoorts

-- config_instvars
--   naam, owner, insttype, speccode (onduidelijk), value, etd_status (vaak lege kolom)
--       insttype telling
--       C           5671
--       D            351
--       G           6383
--       L          70606
--       U         904805

-- config_insthelp: lege tabel, negeren
-- config_trsetval: lege tabel, negeren
-- config_insthist: mutaties in configuraties, lijkt niet relevant nu
-- config_instinfo: toelichting bij sommige configuraties (beperkt aantal records)
