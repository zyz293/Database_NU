delimiter //

create procedure withdraw_try(
in sid int(11),
in course_num char(8))


if exists(select * from transcript)
then
update uosoffering set Enrollment = Enrollment-1 where  uosoffering.UoSCode=course_num and (uosoffering.Semester, uosoffering.Year) in (select
Semester, Year from transcript where StudId=sid and UoSCode=course_num);


#in ( 
#select Semester from transcript where StudId=sid and UoSCode=course_num) and uosoffering.Year in(
#select Year from transcript where StudId=sid and UoSCode=course_num);

delete from transcript  where UoScode = course_num and grade is NULL and StudId = sid;


end if;
//
delimiter ; 