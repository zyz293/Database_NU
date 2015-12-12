drop function if exists enroll_check;

delimiter //
create function enroll_check (sid int(5), ccode char(9))
	returns boolean
	
begin
	if exists(select * from transcript where studid = sid and uoscode = ccode) 
		then return false;
	else return true;
	end if;
end;
//
delimiter ;