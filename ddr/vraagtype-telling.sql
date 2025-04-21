SELECT vr.[CONTROLID], count(*) as Count
FROM           [HIX_Acc].[dbo].[VRLIJST_VROPSLG] vo
    inner JOIN [HIX_Acc].[dbo].[vrlijst_vragen] vr on (vo.[REALVRID] = vr.[VRAAGID])
    inner JOIN [HIX_Acc].[dbo].[VRLIJST_CONTROLS] vc ON (vr.[CONTROLID] = vc.[CONTROLID])
GROUP BY vr.[CONTROLID]
ORDER BY vr.[controlid] ASC