drop procedure if exists enroll_try;

delimiter //
create procedure enroll_try(
in ccode char(9),
in current_quarter char(2),
in current_year int(4),
in next_quarter char(2),
in next_year int(4) ,
in sid int(5))

if exists(select * from uosoffering where uoscode = ccode and semester = current_quarter 
	and year = current_year and enrollment < maxenrollment and check_pre(sid, ccode) and enroll_check(sid, ccode))
	then 
		insert into transcript values(sid, ccode, current_quarter, current_year, null);
		update uosoffering set enrollment = enrollment + 1 where uoscode = ccode 
		and semester = current_quarter and year = current_year;
elseif exists(select * from uosoffering where uoscode = ccode and semester = next_quarter 
	and year = next_year and enrollment < maxenrollment and check_pre(sid, ccode) and enroll_check(sid, ccode))
	then 
		insert into transcript values(sid, ccode, next_quarter, next_year, null);
		update uosoffering set enrollment = enrollment + 1 where uoscode = ccode 
		and semester = next_quarter and year = next_year;
elseif exists(select * from transcript where studid = sid and uoscode = ccode)
	then select uoscode from transcript where studid = sid and uoscode = ccode;
else
	select prerequoscode from requires where uoscode = ccode and uoscode not in
	(select uoscode from transcript where studid = sid and grade <> 'F' and grade is not null);
end if;
//
delimiter ;