delimiter //
CREATE TRIGGER DROPALERT 
before UPDATE ON uosoffering 
for each row
begin
if new.Enrollment<new.MaxEnrollment*0.5 then
	if exists
    (select * from uosoffering u
    where new.enrollment < u.Enrollment and u.UoSCode=new.UoSCode and u.year=new.year and u.semester=new.Semester)
    
    #new.Enrollment<new.MaxEnrollment*0.5 and new.enrollment < (select enrollment from uosoffering u1 where u1.UoSCode = new.UoSCode and u1.year=new.year and u1.Semester = new.Semester)
	then insert into student values('-1','-1','-1','-1');
	end if;
end if;
end; 
//
delimiter ;

