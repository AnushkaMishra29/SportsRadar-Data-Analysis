select c.name,cr.rank,cr.points
from competitors c
join competitors_ranking cr 
on c.competitor_id=cr.competitor_id;

select c.name, cr.rank
from competitors c 
join competitors_ranking cr 
on c.competitor_id=cr.competitor_id
order by cr.rank
limit 5;

select c.name
from competitors c
join competitors_ranking cr 
on c.competitor_id=cr.competitor_id
where cr.movement=0;

select c.country, sum(cr.points) as total_points
from competitors c 
join competitors_ranking cr 
on c.competitor_id=cr.competitor_id
where c.country='Croatia';

select c.country, count(*) as competitor_count
from competitors c
group by c.country;

select c.name, cr.points
from competitors c 
join competitors_ranking cr 
on c.competitor_id=cr.competitor_id
order by cr.points desc
LIMIT 5;


