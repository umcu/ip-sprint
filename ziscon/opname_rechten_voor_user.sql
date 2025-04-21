SELECT
GU.[USERCODE]
,GL.[GROEPCODE]
,WC.[ID]
,WC.[SettingId]
,WC.[SegmentClassId]
,WCS.[SEGMENTID]
,CL.[LOCATIONID]
,CL.[description]
FROM        [dbo].[ZISCON_GROEPUSR] GU
       JOIN [dbo].[ZISCON_GROEPLNK] GL
             ON GU.[GRPUSRCODE] = GL.[LINKCODE]
       JOIN [dbo].[ZISCON_GROEPEN] G
             ON GL.[GROEPCODE] = G.[CODE]
       JOIN [dbo].[CONFIG_WORKCONTEXT] WC
             ON G.[CODE] = WC.[OwnerId]
       JOIN [dbo].[CONFIG_WCSEGMENTS] WCS
             ON WC.[ID] = WCS.[CONFIGUREDWORKCONTEXTID]
       JOIN [dbo].[CSZISLIB_LOCATION] CL
             ON WCS.[SEGMENTID] = CL.[LOCATIONID]
       WHERE  GU.[USERCODE] = 'MEGGINK2'
          and WC.[SegmentClassId] = 'CSZISLIB_LOCATION'
          and WC.[SettingId] = 'OND_RECHTEN'
          order by locationID
