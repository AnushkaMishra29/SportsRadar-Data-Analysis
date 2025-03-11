select comp.competition_name as competitions,cat.category_name as category 
from competitions comp 
join categories cat on comp.category_id=cat.category_id;

select cat.category_name as category, count(comp.competition_name) as competition_count 
from competitions comp 
join categories cat on comp.category_id=cat.category_id 
group by cat.category_name;

select competition_name, type 
from competitions 
where competitions.type='doubles';

select comp.competition_name, cat.category_name 
from competitions comp join categories cat on comp.category_id=cat.category_id
where cat.category_name='ITF Men';

select comp.competition_name as parent_competitions, comp1.competition_name as sub_competitions, comp1.gender,comp1.type
from competitions comp 
join competitions comp1 on comp1.parent_id=comp.competition_id
order by comp.competition_name;

select cat.category_name as category, comp.type as competition_type, count(comp.competition_id) as competition_count
from competitions comp
join categories cat ON comp.category_id = cat.category_id
group by cat.category_name, comp.type;

select * from competitions where parent_id IS NULL
