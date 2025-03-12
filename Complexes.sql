select ven.venue_name as Venue, comp.complex_name as Complex
from venues ven 
join complexes comp on ven.complex_id=comp.complex_id;

select comp.complex_name as complex, count(ven.venue_name) as venues
from complexes comp 
join venues ven on comp.complex_id=ven.complex_id
group by (comp.complex_name);

select v.venue_id,v.venue_name,v.city_name,v.country_name,v.country_code,v.timezone,c.complex_name
from venues v join complexes c on v.complex_id=c.complex_id
 where country_name='China';
 
 select venue_name, timezone 
 from venues
 order by venue_name;
 
 select distinct(c.complex_name) as Complex_with_multiple_venues
 from complexes c 
 join venues v on c.complex_id=v.complex_id
 where c.complex_id in (
    select complex_id 
    from venues 
    group by complex_id 
    having count(*) > 1
)
order by c.complex_name;

select venue_name, country_name
from venues 
order by venue_name,country_name;

select v.venue_name, c.complex_name
from complexes c 
join venues v 
where c.complex_name='Nacional'

