drop function if exists check_pre;

delimiter //
create function check_pre (sid int(5), ccode char(9))
	returns boolean
begin
	declare n2 char(9);
	set n2 = (select PrereqUoSCode from requires r where r.uoscode = ccode and now() >= r.enforcedsince);
	if (exists(select * from transcript where studid = sid and uoscode = n2 and (grade <> 'F' or grade is not null)) or not exists(select * from requires r1 where r1.UoSCode = ccode))
		then return true;
	else return false;
	end if;
end;
//
delimiter ;