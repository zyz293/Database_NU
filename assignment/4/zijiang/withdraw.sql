drop function if exists withdraw;

delimiter //
create procedure withdraw (
in sid int(5), 
in ccode char(9),
in quarter char(2),
in nowyear int(4))

if exists(select * from transcript where studid = sid and uoscode = ccode and grade is null)
	then 
		select * from transcript where studid = sid and uoscode = ccode and grade is null;
		delete from transcript where studid = sid and uoscode = ccode and grade is null;
		update uosoffering set enrollment = enrollment - 1 where uoscode = ccode and semester = quarter and year = nowyear;
end if;
//
delimiter ;