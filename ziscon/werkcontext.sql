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

