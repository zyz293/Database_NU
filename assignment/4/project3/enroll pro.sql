delimiter //
create procedure enroll_try(
in course_num char(8),
in current_year int(11),
in current_quarter char(2),
in sid int(11),
in next_year int(11),
in next_quarter char(2))



# course is not full
if exists(select * from uosoffering u1
where (u1.year = next_year and u1.Semester = next_quarter) and u1.UoSCode = course_num and u1.Enrollment < u1.MaxEnrollment)
and check_pre(sid, course_num)
then #qualified to add this course
    
	insert into transcript values(sid, course_num, next_quarter, next_year, NULL);
    update uosoffering set Enrollment = Enrollment+1 where uosoffering.UoSCode=course_num and uosoffering.year = next_year and uosoffering.Semester = next_quarter;

elseif exists(select * from uosoffering u1
where (u1.year = current_year and u1.Semester = current_quarter) and u1.UoSCode = course_num and u1.Enrollment < u1.MaxEnrollment)
and check_pre(sid, course_num)
then #qualified to add this course
    
	insert into transcript values(sid, course_num, current_quarter, current_year, NULL);
    update uosoffering set Enrollment = Enrollment+1 where uosoffering.UoSCode=course_num and uosoffering.year = current_year and uosoffering.Semester = current_quarter;

else
	select r.PrereqUoSCode from requires r where r.UoSCode=course_num and r.UoSCode not in(select t.UoSCode from transcript t where t.StudId = sid and t.grade <> 'F' and t.grade <> 'None' and t.grade is not NULL);
end if; //

delimiter ;



#(u1.year = current_year and u1.Semester = current_quarter) or 




