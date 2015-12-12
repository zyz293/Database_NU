drop function if exists withdrawalter;

delimiter //
create trigger withdrawalter 
before update on uosoffering
for each row
begin
	if new.enrollment * 2 < new.maxenrollment
		then insert into student values ('0','0','0','0');
	end if;
end;
//
delimiter ;