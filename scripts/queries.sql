select * from entity_type;

select * from entity_type_definition;

select * from node;

select * from relation;


-- Joined definitions
select et.type, etd.version, count(distinct n.eid)
from entity_type et join entity_type_definition etd on et.eid = etd.entity_type_eid
	left join node n on etd.eid = n.definition_eid
group by 1, 2;


select
	et.type, 
	etd.properties,
	etd.relationships,
	n.properties
from entity_type et join entity_type_definition etd on et.eid = etd.entity_type_eid
					join node n on etd.eid = n.definition_eid;
					