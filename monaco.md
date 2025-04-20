---
sidebar_label: 'Monaco'
sidebar_position: 20
description: informatie over het bronsysteem Monaco
---
# Monaco

<table>
<thead>
<tr><th>Algemene informatie</th><th></th></tr>
</thead>
<tbody>
<tr>
<td>Naam bronsysteem</td>
<td>Monaco</td>
</tr>
<tr>
<td>Omschrijving bronsysteem</td>
<td>
Informatiesysteem voor roosteren van onregelmatige diensten, onder andere verpleegkundigen
</td>
</tr>
<tr>
<td>Status bronsysteem</td>
<td>actueel</td>
</tr>
<tr>
<td>Datum toegevoegd</td>
<td>
onbekend
</td>
</tr>
<tr>
<td>Datum akkoord</td>
<td>
todo
</td>
</tr>
</tbody> 
</table> 

<table>
<thead>
<tr><th>Contactpersonen</th><th></th></tr>
</thead>
<tbody>
<tr>
<td>Data-verantwoordelijke</td>
<td>
Amanda Jipat, Directie P&amp;O, teamleider functioneel beheer
</td>
</tr>
<tr>
<td>Data-steward</td>
<td>
Patrick Burm, DIT/Bedrijfsvoeringapplicaties
</td>
</tr>
<tr>
<td>Technisch contactpersoon</td>
<td>
Patrick Burm, DIT/Bedrijfsvoeringapplicaties
</td>
</tr>
</tbody> 
</table> 

<table>
<thead>
<tr><th>Beveiliging van de gegevens</th><th></th></tr>
</thead>
<tbody>
<tr>
<td>Incidentprocedure</td>
<td>
incidentmelding via ServiceNow, ter attentie van Bedrijfsvoeringapplicaties
</td>
</tr>
<tr>
<td>Kwaliteitscriteria</td>
<td>
nog te bespreken met data-steward en belangrijkste gebruikers van de data.
</td>
</tr>
<tr>
<td>Terugmeldingsplicht</td>
<td>
incidentmelding via ServiceNow, ter attentie van Bedrijfsvoeringapplicaties
</td>
</tr>
</tbody> 
</table> 

<table>
<thead>
<tr><th>Gebruik</th><th></th></tr>
</thead>
<tbody>
<tr>
<td>Doorleveren toegestaan</td>
<td>Ja</td>
</tr>
<tr>
<td>Toelichting doorleveren</td>
<td>
todo: vermoedelijk alleen met toestemming van data-verantwoordelijke, en alleen na uitleg data-steward
over gebruik en interpretatie van data.
</td>
</tr>
</tbody> 
</table> 

<table>
<thead>
<tr><th>Documentatie</th><th></th></tr>
</thead>
<tbody>
<tr>
<td>Structuur van brontabellen</td>
<td>
todo
</td>
</tr>
<tr>
<td>Systeemdocumentatie</td>
<td>todo</td>
</tr>
</tbody> 
</table> 

<table>
<thead>
<tr><th>Wijze van levering</th><th></th></tr>
</thead>
<tbody>
<tr>
<td>Dataplatform load-laag</td>
<td>prestaging</td>
</tr>
<tr>
<td>Type bron</td>
<td>Pervasive</td>
</tr>
<tr>
<td>Locatie bron</td>
<td>DPOMONA1502 / VPXDB-EDWDATA02</td>
</tr>
<tr>
<td>Post-deploy script</td>
<td>/STG/deployment/post_deploy_monaco.sql</td>
</tr>
<tr>
<td>Aanlevering techniek</td>
<td>via linked server</td>
</tr>
<tr>
<td>Verversingsmethode</td>
<td>CDC Full, full compare</td>
</tr>
<tr>
<td>Verversingsfrequentie</td>
<td>dagelijks, roosterdata 3x per etmaal, overige data 1x per etmaal</td>
</tr>
</tbody> 
</table> 

<table>
<thead>
<tr><th>Datatransformatie</th><th></th></tr>
</thead>
<tbody>
<tr>
<td>Datamodellen</td>
<td>
In welke datamodellen in de DWH-laag is de data beschikbaar? Voor zover bekend: geen.
</td>
</tr>
</tbody> 
</table> 

<table>
<thead>
<tr><th>Versiebeheer</th><th></th></tr>
</thead>
<tbody>
<tr>
<td>Laatste review-datum</td>
<td>Datum dat deze data leveringsovereenkomst voor het laatst geactualiseerd is</td>
</tr>
</tbody> 
</table>