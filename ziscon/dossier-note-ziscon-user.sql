SELECT TOP (1000)
    DN.[USERID]
   ,ZU.[FUNKTIE]
   ,DN.[DATUM]
   ,DN.[TIJD]
   ,DN.[OPENBAAR]
   ,DN.[NOTE]
   ,DN.[SPECIALID]
   ,DN.[NOTE_TYPE]
   ,DN.[CREATOR]
  FROM      [HIX_Acc].[dbo].[DOSSIER_NOTE] DN
       JOIN [hix_acc].[dbo].[ZISCON_USER] ZU
       ON DN.[USERID] = ZU.[NAAM]
  WHERE DN.[SPECIALID] IN ('PSY', 'GGZ') AND ZU.[DISABLED] = 0
  ORDER BY dn.datum DESC