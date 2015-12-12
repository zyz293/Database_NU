delimiter //
create function check_pre(sid int(11), course_num char(8))
	returns boolean
	
begin
	declare n1 integer;
    declare n2 integer;
	set n1 = (select count(*) from requires r where course_num = r.UoSCode and now()>=r.EnforcedSince and (r.UoSCode in (select t.UoSCode from transcript t where t.StudId = sid and t.grade <> 'F' and t.grade <>'None' and t.grade is not NULL)));
	
	set n2 = (select count(*) from requires r where course_num = r.UoSCode and now()>=r.EnforcedSince);
	
	if (n1 = n2)  or not exists(select * from requires r1 where r1.UoSCode = course_num) then return True; else return False; end if;
end; //

delimiter ;